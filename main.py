import pygame
import settings


# enumerate all the types of chess pieces


class PieceType:
    PAWN = 0
    ROOK = 1
    KNIGHT = 2
    BISHOP = 3
    QUEEN = 4
    KING = 5

# enumerate all the colors of chess pieces


class PieceColor:
    WHITE = 0
    BLACK = 1

# define a class to represent a chess piece


class Piece:
    def __init__(self, piece_type, piece_color):
        self.type = piece_type
        self.color = piece_color

    def __str__(self):
        return "Type: " + str(self.type) + " Color: " + str(self.color)

# define a class to represent a chess board


class Board:
    def __init__(self):
        self.board = [[None for x in range(8)] for y in range(8)]

    def __str__(self):
        return "Board: " + str(self.board)

    def init_board(self):
        # initialize the board with the starting positions
        for i in range(8):
            self.board[1][i] = Piece(PieceType.PAWN, PieceColor.WHITE)
            self.board[6][i] = Piece(PieceType.PAWN, PieceColor.BLACK)

        self.board[0][0] = Piece(PieceType.ROOK, PieceColor.WHITE)
        self.board[0][7] = Piece(PieceType.ROOK, PieceColor.WHITE)
        self.board[7][0] = Piece(PieceType.ROOK, PieceColor.BLACK)
        self.board[7][7] = Piece(PieceType.ROOK, PieceColor.BLACK)

        self.board[0][1] = Piece(PieceType.KNIGHT, PieceColor.WHITE)
        self.board[0][6] = Piece(PieceType.KNIGHT, PieceColor.WHITE)
        self.board[7][1] = Piece(PieceType.KNIGHT, PieceColor.BLACK)
        self.board[7][6] = Piece(PieceType.KNIGHT, PieceColor.BLACK)

        self.board[0][2] = Piece(PieceType.BISHOP, PieceColor.WHITE)
        self.board[0][5] = Piece(PieceType.BISHOP, PieceColor.WHITE)
        self.board[7][2] = Piece(PieceType.BISHOP, PieceColor.BLACK)
        self.board[7][5] = Piece(PieceType.BISHOP, PieceColor.BLACK)

        self.board[0][3] = Piece(PieceType.QUEEN, PieceColor.WHITE)
        self.board[7][3] = Piece(PieceType.QUEEN, PieceColor.BLACK)

        self.board[0][4] = Piece(PieceType.KING, PieceColor.WHITE)
        self.board[7][4] = Piece(PieceType.KING, PieceColor.BLACK)


def draw_board():
    # draw the board
    for y in range(8):
        for x in range(8):
            if (x + y) % 2 == 0:
                color = settings.WHITE
            else:
                color = settings.BLACK
            pygame.draw.rect(screen, color, [
                             x * settings.SQUARE_SIZE, y * settings.SQUARE_SIZE, settings.SQUARE_SIZE, settings.SQUARE_SIZE])


def handle_events():
    global done

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True


def draw_screen():
    screen.fill('black')
    # draw the screen
    draw_board()

    pygame.display.flip()


def main():

    while not done:
        handle_events()
        draw_screen()
        clock.tick(settings.fps)


if __name__ == "__main__":
    board = Board()
    clock = pygame.time.Clock()
    done = False
    pygame.init()
    font = pygame.font.SysFont(None, settings.FONT_SIZE_NORMAL)
    screen = pygame.display.set_mode((settings.width, settings.height))
    pygame.display.set_caption("bad-chess")

    main()
