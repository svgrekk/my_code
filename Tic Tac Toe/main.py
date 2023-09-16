import pygame
import sys


class Player:
    def __init__(self, num):
        self.sign = num

    def get_sign(self):
        return self.sign

    def __str__(self):
        return str(self.sign)


class Game:
    def __init__(self):
        self.active = None
        self.tile_height = None
        self.tile_width = None
        self.turn = None
        self.players = None
        self.board = None
        self.start_game()

    def start_game(self):
        self.board = [[0] * 3 for _ in range(3)]
        self.players = [Player(1), Player(2)]
        self.turn = 0
        self.tile_width = 100
        self.tile_height = 100
        self.active = True

    def draw_board(self):
        for i in range(3):
            for j in range(3):
                rect = pygame.Rect(i * self.tile_height, j * self.tile_width,
                                   self.tile_height, self.tile_width)
                pygame.draw.rect(screen, 'grey', rect, 5)

                if self.board[i][j] == 1:
                    y, x = rect.topleft
                    y1, x1 = rect.bottomright
                    pygame.draw.line(screen, (255, 255, 255), (x, y), (x1, y1), 15)
                    y, x = rect.topright
                    y1, x1 = rect.bottomleft
                    pygame.draw.line(screen, (255, 255, 255), (x, y), (x1, y1), 15)

                elif self.board[i][j] == 2:
                    y, x = rect.center
                    pygame.draw.circle(screen, (255, 255, 255), (x, y), 45, 10)

    def check_rows(self):
        for i in range(len(self.board)):
            if self.board[i] == [1, 1, 1] or self.board[i] == [2, 2, 2]:
                self.active = False
                pygame.draw.line(screen, 'red',
                                 (0 * self.tile_width, i * self.tile_height + self.tile_height / 2),
                                 (3 * self.tile_width, i * self.tile_height + self.tile_height / 2),
                                 10)

    def check_cols(self):

        for i in range(len(self.board)):
            column = [self.board[j][i] for j in range(len(self.board[i]))]

            if column == [1, 1, 1] or column == [2, 2, 2]:
                self.active = False
                pygame.draw.line(screen, 'red',
                                 (i * self.tile_width + self.tile_width / 2, 0 * self.tile_height),
                                 (i * self.tile_width + self.tile_width / 2, 3 * self.tile_height),
                                 10)

    def draw_diag(self, start, end):
        pygame.draw.line(screen, 'red', start, end, 10)

    def check_diags(self):

        diagonal = [self.board[i][i] for i in range(len(self.board))]
        diagonal_2 = [self.board[i][j] for i, j in
                      zip(range(len(self.board)),
                          range(len(self.board) - 1, -1, -1))]

        if diagonal == [1, 1, 1] or diagonal == [2, 2, 2]:
            self.active = False
            start = (0 * self.tile_width, 0 * self.tile_height)
            end = (3 * self.tile_width, 3 * self.tile_height)
            self.draw_diag(start, end)
            return

        elif diagonal_2 == [1, 1, 1] or diagonal_2 == [2, 2, 2]:
            self.active = False
            start = (0 * self.tile_width, 3 * self.tile_height)
            end = (3 * self.tile_width, 0 * self.tile_height)
            self.draw_diag(start, end)

    def check_win(self):
        self.check_rows()
        self.check_cols()
        self.check_diags()

    def move(self, position):
        if self.active:
            j, i = position
            i = int(i / self.tile_height)
            j = int(j / self.tile_width)
            sign = self.players[self.turn % 2].get_sign()

            if self.board[i][j] == 0:
                self.board[i][j] = sign
                self.turn += 1


pygame.init()

FPS = 60

screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption('Tic Tac Toe')
clock = pygame.time.Clock()

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            game.move(pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.start_game()

    screen.fill((0, 0, 0))
    game.draw_board()
    game.check_win()

    clock.tick(FPS)
    pygame.display.flip()
