import sys

import pygame
import requests
import io
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_WHITE = (240, 234, 210)
GREEN = (88, 129, 87)
BLUE = (0, 0, 255)
YELLOW = (233, 196, 106)
ORANGE = (244, 162, 97)

# define constants for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}

# card images
response_1 = requests.get("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")
im_bytes = io.BytesIO(response_1.content)
card_images = pygame.image.load(im_bytes)

# card back images
response_2 = requests.get("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")
im_bytes = io.BytesIO(response_2.content)
card_back = pygame.image.load(im_bytes)

CARD_SIZE = (72, 96)

pygame.init()

screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 40)


class Card:

    def __init__(self, rank, suit, is_open):
        self.rank = rank
        self.suit = suit
        self.is_open = is_open

    def draw(self, pos):

        if not self.is_open:

            card_rect = (0, 0, CARD_SIZE[0], CARD_SIZE[1])
            screen.blit(card_back, pos, card_rect)

        else:
            card_rect = (
                CARD_SIZE[0] * RANKS.index(self.rank),
                CARD_SIZE[1] * SUITS.index(self.suit),
                CARD_SIZE[0],
                CARD_SIZE[1]
            )

            screen.blit(card_images, pos, card_rect)

    def __str__(self):
        return f"Card: {self.suit}{self.rank}"


class Hand:

    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0

        for card in self.cards:
            if card.is_open:
                if card.rank == "A" and value + 11 <= 21:
                    value += 11
                else:
                    value += VALUES[card.rank]

        return value

    def draw(self, pos):
        x, y = pos
        jump = 0
        if len(self.cards) > 0:
            for card in self.cards:
                card.draw((x + jump, y))
                jump += CARD_SIZE[0] + 10


class Deck:

    def __init__(self):
        self.deck = [Card(rank, suit, True) for rank in RANKS for suit in SUITS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self, is_open):
        card = self.deck.pop()
        card.is_open = is_open
        return card


class Button:
    def __init__(self, pos, text, action):
        self.top_rect = pygame.Rect(pos, (100, 50))
        self.top_color = YELLOW

        self.elevation = 6
        self.dynamic_elevation = self.elevation

        self.bottom_rect = pygame.Rect(pos, (100, self.elevation))
        self.bottom_color = BLACK

        self.text = text
        self.text_surf = font.render(self.text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

        self.x = pos[0]
        self.y = pos[1]
        self.func = action

        self.orig_y = self.y

        self.pressed = False

    def draw(self):
        self.top_rect.y = self.orig_y - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)

        screen.blit(self.text_surf, self.text_rect)

    def check(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = ORANGE
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    self.func()
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = YELLOW


class Main:

    def __init__(self):
        self.player = Hand()
        self.dealer = Hand()
        self.deck = Deck()
        self.message = 'Welcome.'
        self.in_play = False
        self.score = 0
        self.started = False
        self.buttons = []

    def deal(self):

        self.in_play = True
        self.player = Hand()
        self.dealer = Hand()
        self.deck = Deck()

        self.started = True

        # deal player
        for _ in range(2):
            self.player.add_card(self.deck.deal(True))

        # deal dealer
        self.dealer.add_card(self.deck.deal(True))
        self.dealer.add_card(self.deck.deal(False))

        # check delt cards
        if self.player.get_value() < 21:
            self.message = "Hit or Stand?"
        else:
            self.in_play = False
            self.score += 1
            self.message = "Black Jack!!!"

    def hit(self):
        if self.in_play:
            self.player.add_card(self.deck.deal(True))

            if self.player.get_value() < 21:
                self.message = "Hit or Stand?"

            elif self.player.get_value() == 21:
                self.message = 'Dealer is busted.'
                self.score += 1
                self.in_play = False
            else:
                self.message = 'Player is busted.'
                self.score -= 1
                self.in_play = False
        else:
            self.message = "Press Deal"

    def stand(self):

        if self.in_play:
            self.in_play = False

            # open dealer cards
            for card in self.dealer.cards:
                card.is_open = True

            # deal cards
            while self.dealer.get_value() < 17:
                self.dealer.add_card(self.deck.deal(True))

            dealer_value = self.dealer.get_value()

            if dealer_value > 21:
                self.message = 'Dealer is busted.'
                self.score += 1
                return

            #  calculate winner

            if self.dealer.get_value() <= self.player.get_value():
                self.message = 'Dealer is busted.'
                self.score += 1

            else:
                self.message = 'Player is busted.'
                self.score -= 1
        else:
            self.message = "Press Deal"

    def draw_elements(self):

        # draw cards
        self.player.draw((100, 400))
        self.dealer.draw((100, 100))

        # draw message
        message_surf = font.render(self.message, True, YELLOW)
        message_rect = message_surf.get_rect(topleft=(30, 300))
        screen.blit(message_surf, message_rect)

        if self.started:
            # draw score
            score_surf = font.render(f'Score: {self.score}', True, YELLOW)
            score_rect = score_surf.get_rect(topleft=(350, 30))
            screen.blit(score_surf, score_rect)

            # draw player hand value
            p_value_surf = font.render(f'{self.player.get_value()}', True, DARK_WHITE)
            p_val_rect = p_value_surf.get_rect(topleft=(50, 450))
            screen.blit(p_value_surf, p_val_rect)

            # draw dealer hand value
            d_value_surf = font.render(f'{self.dealer.get_value()}', True, DARK_WHITE)
            d_val_rect = d_value_surf.get_rect(topleft=(50, 150))
            screen.blit(d_value_surf, d_val_rect)

            # draw buttons
            for button in self.buttons:
                button.check()
                button.draw()


def game_start():
    main = Main()

    # create buttons
    button_names = ['DEAL', 'HIT', 'STAND']
    funcs = [main.deal, main.hit, main.stand]

    shift = 0
    for name, func in zip(button_names, funcs):
        btn = Button((50 + shift, 520), name, func)
        shift += 120
        main.buttons.append(btn)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main.deal()

        screen.fill(GREEN)
        main.draw_elements()
        if not main.started:
            main.started = True
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    game_start()
