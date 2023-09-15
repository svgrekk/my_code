import pygame
import sys
from pygame.math import Vector2
import random


class Fruit:

    def __init__(self):
        self.x = None
        self.y = None
        self.pos = None
        self.change_pos()
        self.fruit_rect = pygame.Rect((0, img_size[0] * 3), (img_size[0], img_size[1]))

    def draw_fruit(self):
        screen.blit(snake_img, self.pos, self.fruit_rect)

    def change_pos(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x * cell_size, self.y * cell_size)


class Snake:
    def __init__(self):
        self.body = [Vector2(6, 10), Vector2(7, 10), Vector2(8, 10)]
        self.direction = Vector2(-1, 0)
        self.new_block = False

    def reset(self):
        self.body = [Vector2(6, 10), Vector2(7, 10), Vector2(8, 10)]
        self.direction = Vector2(-1, 0)
        self.new_block = False

    def get_head_rect(self):

        head_to_body = self.body[0] - self.body[1]
        head_rect = None

        if head_to_body.x == 1:
            head_rect = (4 * img_size[0], 0, img_size[0], img_size[1])
        elif head_to_body.x == -1:
            head_rect = (3 * img_size[0], 1 * img_size[1], img_size[0], img_size[1])
        elif head_to_body.y == 1:
            head_rect = (4 * img_size[0], 1 * img_size[1], img_size[0], img_size[1])
        elif head_to_body.y == -1:
            head_rect = (3 * img_size[0], 0, img_size[0], img_size[1])

        return head_rect

    def get_tail_rect(self):
        tail_to_body = self.body[-1] - self.body[-2]
        tail_rect = None
        if tail_to_body.x == 1:
            tail_rect = (3 * img_size[0], 3 * img_size[1], img_size[0], img_size[1])

        elif tail_to_body.x == -1:
            tail_rect = (4 * img_size[0], 2 * img_size[1], img_size[0], img_size[1])

        elif tail_to_body.y == 1:
            tail_rect = (3 * img_size[0], 2 * img_size[1], img_size[0], img_size[1])

        elif tail_to_body.y == -1:
            tail_rect = (4 * img_size[0], 3 * img_size[1], img_size[0], img_size[1])

        return tail_rect

    def draw_snake(self):
        body_rect = None
        for index, block in enumerate(self.body):

            if index == 0:
                head_rect = self.get_head_rect()
                screen.blit(snake_img, (block.x * cell_size, block.y * cell_size), head_rect)

            elif index == len(self.body) - 1:
                tail_rect = self.get_tail_rect()
                screen.blit(snake_img, (block.x * cell_size, block.y * cell_size), tail_rect)

            else:
                next_block = block - self.body[index + 1]
                prev_block = block - self.body[index - 1]
                # moving up or down
                if prev_block.y == next_block.y:
                    body_rect = (1 * img_size[0], 0, img_size[0], img_size[1])
                # moving left or right
                elif prev_block.x == next_block.x:
                    body_rect = (2 * img_size[0], 1 * img_size[1], img_size[0], img_size[1])

                # turn up moving right or left moving down
                elif prev_block.y == 1 and next_block.x == 1 or next_block.y == 1 and prev_block.x == 1:
                    body_rect = (2 * img_size[0], 2 * img_size[1], img_size[0], img_size[1])

                # turn down moving right or left moving up
                elif prev_block.y == -1 and next_block.x == 1 or next_block.y == -1 and prev_block.x == 1:
                    body_rect = (2 * img_size[0], 0 * img_size[1], img_size[0], img_size[1])

                # turn up moving left or right moving down
                elif prev_block.y == 1 and next_block.x == -1 or next_block.y == 1 and prev_block.x == -1:
                    body_rect = (0 * img_size[0], 1 * img_size[1], img_size[0], img_size[1])

                # turn down moving left or right moving up
                elif prev_block.y == -1 and next_block.x == -1 or next_block.y == -1 and prev_block.x == -1:
                    body_rect = (0 * img_size[0], 0 * img_size[1], img_size[0], img_size[1])

                body_rect = pygame.Rect(body_rect)
                screen.blit(snake_img, (block.x * cell_size, block.y * cell_size), body_rect)

    def move_snake(self):
        if not self.new_block:
            snake_tail = self.body[:-1]
            self.body = [self.body[0] + self.direction] + snake_tail
        else:
            snake_tail = self.body[:]
            self.body = [self.body[0] + self.direction] + snake_tail
            self.new_block = False

    def add_block(self):
        self.new_block = True


class Main:
    def __init__(self):
        self.fruit = Fruit()
        self.snake = Snake()
        self.score = 0

    def key_handler(self, key):
        if key == pygame.K_UP and \
                self.snake.body[0] + Vector2(0, -1) != self.snake.body[1]:
            self.snake.direction = Vector2(0, -1)

        elif key == pygame.K_LEFT and \
                self.snake.body[0] + Vector2(-1, 0) != self.snake.body[1]:
            self.snake.direction = Vector2(-1, 0)

        elif key == pygame.K_RIGHT and \
                self.snake.body[0] + Vector2(1, 0) != self.snake.body[1]:
            self.snake.direction = Vector2(1, 0)

        elif key == pygame.K_DOWN and \
                self.snake.body[0] + Vector2(0, 1) != self.snake.body[1]:
            self.snake.direction = Vector2(0, 1)

    def check_collision(self):
        if self.snake.body[0] * cell_size == self.fruit.pos:
            self.fruit.change_pos()
            self.snake.add_block()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.change_pos()

    def game_over(self):
        self.snake.reset()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))

        score_rect = score_surface.get_rect(center=(screen.get_rect().centerx, 45))

        apple_surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        apple_surf.blit(snake_img, (0, 0), self.fruit.fruit_rect)
        apple_rect = apple_surf.get_rect(midright=(score_rect.left - 10, score_rect.centery))
        apple_rect = apple_surf.get_rect(midright=(score_rect.left - 10, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left - 3, apple_rect.top - 3,
                              apple_rect.width + score_rect.width + 20,
                              apple_rect.height + 8)

        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)
        screen.blit(score_surface, score_rect)
        screen.blit(apple_surf, apple_rect)

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()


pygame.init()

GREEN = (175, 215, 70)
DARK_GREEN = (126, 166, 114)
cell_size = 64
cell_number = 15

screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
pygame.display.set_caption('SNAKE')
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 60)

snake_img = pygame.image.load('SNAKE/IMG/snake-graphics.png').convert_alpha()
img_size = (64, 64)

main = Main()
screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update, 200)

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == screen_update:
            main.update()

        elif event.type == pygame.KEYDOWN:
            main.key_handler(event.key)

    screen.fill(GREEN)
    main.draw_elements()
    pygame.display.update()
    clock.tick(60)
