# chess board is laid out in rows called ranks and columns called files
# the board is 8 ranks and 8 files
#
# Forsyth-Edwards Notation (FEN) is a standard notation for describing
# a particular board position of a chess game.

import pygame
import settings

FEN_NEW_GAME = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

# enumerate all the types of chess pieces


class PieceType:
    NONE = None
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6

# enumerate all the colors of chess pieces


class PieceColor:
    NONE = None
    WHITE = 8
    BLACK = 16

# define a class to represent a chess piece


class Piece:
    def __init__(self, fen_character):
        if fen_character == "P":
            self.type = PieceType.PAWN
            self.color = PieceColor.WHITE
        elif fen_character == "p":
            self.type = PieceType.PAWN
            self.color = PieceColor.BLACK
        elif fen_character == "R":
            self.type = PieceType.ROOK
            self.color = PieceColor.WHITE
        elif fen_character == "r":
            self.type = PieceType.ROOK
            self.color = PieceColor.BLACK
        elif fen_character == "N":
            self.type = PieceType.KNIGHT
            self.color = PieceColor.WHITE
        elif fen_character == "n":
            self.type = PieceType.KNIGHT
            self.color = PieceColor.BLACK
        elif fen_character == "B":
            self.type = PieceType.BISHOP
            self.color = PieceColor.WHITE
        elif fen_character == "b":
            self.type = PieceType.BISHOP
            self.color = PieceColor.BLACK
        elif fen_character == "Q":
            self.type = PieceType.QUEEN
            self.color = PieceColor.WHITE
        elif fen_character == "q":
            self.type = PieceType.QUEEN
            self.color = PieceColor.BLACK
        elif fen_character == "K":
            self.type = PieceType.KING
            self.color = PieceColor.WHITE
        elif fen_character == "k":
            self.type = PieceType.KING
            self.color = PieceColor.BLACK
        else:
            self.type = PieceType.NONE
            self.color = PieceColor.NONE

    def fen_char(self):

        my_char = "?"
        if self.type == PieceType.PAWN:
            my_char = "P"
        elif self.type == PieceType.ROOK:
            my_char = "R"
        elif self.type == PieceType.KNIGHT:
            my_char = "N"
        elif self.type == PieceType.BISHOP:
            my_char = "B"
        elif self.type == PieceType.QUEEN:
            my_char = "Q"
        elif self.type == PieceType.KING:
            my_char = "K"

        if self.color == PieceColor.BLACK:
            my_char = my_char.lower()

        return my_char

    def __str__(self):
        return self.fen_char()

# define a class to represent a chess board


class Board:
    def __init__(self, fen_string: str = FEN_NEW_GAME):
        self.board = [[None for x in range(8)] for y in range(8)]
        self.turn = PieceColor.WHITE
        self.fen_decode(fen_string)

    def __str__(self):
        return "Board: " + str(self.board)

    def wipe_board(self):
        # initialize the board with the starting positions
        for y in range(8):
            for x in range(8):
                self.board[y][x] = None

    def reset_board(self):
        self.fen_decode(FEN_NEW_GAME)

    def move(self, start: str, end: str):
        print("Moving piece from " + start + " to " + end)
        start_file = ord(start[0]) - 97
        start_rank = 8 - int(start[1])
        end_file = ord(end[0]) - 97
        end_rank = 8 - int(end[1])

        self.board[end_rank][end_file] = self.board[start_rank][start_file]
        self.board[start_rank][start_file] = None

        if self.turn == PieceColor.WHITE:
            self.turn = PieceColor.BLACK
        else:
            self.turn = PieceColor.WHITE

    def fen_encode(self):
        board_string = ""
        empty_counter = 0

        for rank in range(8):
            for file in range(8):
                if self.board[rank][file] is None:
                    empty_counter += 1
                else:
                    if empty_counter > 0:
                        board_string += str(empty_counter)
                        empty_counter = 0
                    board_string += str(self.board[rank][file])

            if empty_counter > 0:
                board_string += str(empty_counter)

            board_string += "/"
            empty_counter = 0

        board_string = board_string.rstrip("/")

        if self.turn == PieceColor.WHITE:
            board_string += " w"
        else:
            board_string += " b"

        return board_string

    def fen_decode(self, board_state: str):
        print("Loading board state: " + board_state)
        self.wipe_board()
        rank = 7
        file = 0

        fen_chunks = board_state.split(" ")

        if len(fen_chunks) > 0:
            for char in fen_chunks[0]:
                if char == "/":
                    rank -= 1
                    file = 0
                elif char.isdigit():
                    file += int(char)
                else:
                    self.board[7 - rank][file] = Piece(char)
                    file += 1

        if len(fen_chunks) > 1:
            if fen_chunks[1] == "w":
                self.turn = PieceColor.WHITE
            else:
                self.turn = PieceColor.BLACK

        print("Board state loaded: " + self.fen_encode())

    def enumerate_moves(self, start: str):
        print("Enumerating moves from " + start)
        moves = []
        start_file = ord(start[0]) - 97
        start_rank = 8 - int(start[1])

        piece = self.board[start_rank][start_file]

        if piece is None:
            return None

        if piece.type == PieceType.PAWN:
            if piece.color == PieceColor.WHITE:
                if start_rank == 6:
                    # check for first turn move
                    if self.board[start_rank - 1][start_file] is None:
                        moves.append(start + chr(start_file + 97) +
                                     str(8 - (start_rank - 1)))
                    if self.board[start_rank - 2][start_file] is None:
                        moves.append(start + chr(start_file + 97) +
                                     str(8 - (start_rank - 2)))
                else:
                    # subsequent moves
                    if self.board[start_rank - 1][start_file] is None:
                        moves.append(start + chr(start_file + 97) +
                                     str(8 - (start_rank - 1)))
                # check for captures
                if start_rank > 0:
                    if start_file > 0:
                        if self.board[start_rank - 1][start_file - 1] is not None:
                            if self.board[start_rank - 1][start_file - 1].color == PieceColor.BLACK:
                                moves.append(start + chr(start_file + 96) +
                                             str(8 - (start_rank - 1)))
                    if start_file < 7:
                        if self.board[start_rank - 1][start_file + 1] is not None:
                            if self.board[start_rank - 1][start_file + 1].color == PieceColor.BLACK:
                                moves.append(start + chr(start_file + 98) +
                                             str(8 - (start_rank - 1)))

            else:
                if start_rank == 1:
                    # check for first turn move
                    if self.board[start_rank + 1][start_file] is None:
                        moves.append(start + chr(start_file + 97) +
                                     str(8 - (start_rank + 1)))
                    if self.board[start_rank + 2][start_file] is None:
                        moves.append(start + chr(start_file + 97) +
                                     str(8 - (start_rank + 2)))
                else:
                    # subsequent moves
                    if self.board[start_rank + 1][start_file] is None:
                        moves.append(start + chr(start_file + 97) +
                                     str(8 - (start_rank + 1)))
                # check for captures
                if start_rank < 7:
                    if start_file > 0:
                        if self.board[start_rank + 1][start_file - 1] is not None:
                            if self.board[start_rank + 1][start_file - 1].color == PieceColor.WHITE:
                                moves.append(start + chr(start_file + 96) +
                                             str(8 - (start_rank + 1)))
                    if start_file < 7:
                        if self.board[start_rank + 1][start_file + 1] is not None:
                            if self.board[start_rank + 1][start_file + 1].color == PieceColor.WHITE:
                                moves.append(start + chr(start_file + 98) +
                                             str(8 - (start_rank + 1)))

        elif piece.type == PieceType.ROOK:
            cur_rank = start_rank
            cur_file = start_file

            while cur_rank < 7:
                cur_rank += 1
                if self.board[cur_rank][cur_file] is None:
                    moves.append(start + chr(cur_file + 97) +
                                 str(8 - cur_rank))
                else:
                    if self.board[cur_rank][cur_file].color != piece.color:
                        moves.append(start + chr(cur_file + 97) +
                                     str(8 - cur_rank))
                    break

            cur_rank = start_rank
            cur_file = start_file

            while cur_rank > 0:
                cur_rank -= 1
                if self.board[cur_rank][cur_file] is None:
                    moves.append(start + chr(cur_file + 97) +
                                 str(8 - cur_rank))
                else:
                    if self.board[cur_rank][cur_file].color != piece.color:
                        moves.append(start + chr(cur_file + 97) +
                                     str(8 - cur_rank))
                    break

            cur_rank = start_rank
            cur_file = start_file

            while cur_file < 7:
                cur_file += 1
                if self.board[cur_rank][cur_file] is None:
                    moves.append(start + chr(cur_file + 97) +
                                 str(8 - cur_rank))
                else:
                    if self.board[cur_rank][cur_file].color != piece.color:
                        moves.append(start + chr(cur_file + 97) +
                                     str(8 - cur_rank))
                    break

            cur_rank = start_rank
            cur_file = start_file

            while cur_file > 0:
                cur_file -= 1
                if self.board[cur_rank][cur_file] is None:
                    moves.append(start + chr(cur_file + 97) +
                                 str(8 - cur_rank))
                else:
                    if self.board[cur_rank][cur_file].color != piece.color:
                        moves.append(start + chr(cur_file + 97) +
                                     str(8 - cur_rank))
                    break

        elif piece.type == PieceType.KNIGHT:
            pass
        elif piece.type == PieceType.BISHOP:
            # check for captures in each diagonal
            cur_rank = start_rank
            cur_file = start_file

            while cur_rank < 7 and cur_file < 7:
                cur_rank += 1
                cur_file += 1
                if self.board[cur_rank][cur_file] is None:
                    moves.append(start + chr(cur_file + 97) +
                                 str(8 - cur_rank))
                else:
                    if self.board[cur_rank][cur_file].color != piece.color:
                        moves.append(start + chr(cur_file + 97) +
                                     str(8 - cur_rank))
                    break

            cur_rank = start_rank
            cur_file = start_file

            while cur_rank < 7 and cur_file > 0:
                cur_rank += 1
                cur_file -= 1
                if self.board[cur_rank][cur_file] is None:
                    moves.append(start + chr(cur_file + 97) +
                                 str(8 - cur_rank))
                else:
                    if self.board[cur_rank][cur_file].color != piece.color:
                        moves.append(start + chr(cur_file + 97) +
                                     str(8 - cur_rank))
                    break

            cur_rank = start_rank
            cur_file = start_file

            while cur_rank > 0 and cur_file < 7:
                cur_rank -= 1
                cur_file += 1
                if self.board[cur_rank][cur_file] is None:
                    moves.append(start + chr(cur_file + 97) +
                                 str(8 - cur_rank))
                else:
                    if self.board[cur_rank][cur_file].color != piece.color:
                        moves.append(start + chr(cur_file + 97) +
                                     str(8 - cur_rank))
                    break

            cur_rank = start_rank
            cur_file = start_file

            while cur_rank > 0 and cur_file > 0:
                cur_rank -= 1
                cur_file -= 1
                if self.board[cur_rank][cur_file] is None:
                    moves.append(start + chr(cur_file + 97) +
                                 str(8 - cur_rank))
                else:
                    if self.board[cur_rank][cur_file].color != piece.color:
                        moves.append(start + chr(cur_file + 97) +
                                     str(8 - cur_rank))
                    break

        elif piece.type == PieceType.QUEEN:
            # check the queen horizontal and vertical moves
            cur_rank = start_rank
            cur_file = start_file

            while cur_rank < 7:
                cur_rank += 1
                if self.board[cur_rank][cur_file] is None:
                    moves.append(start + chr(cur_file + 97) +
                                 str(8 - cur_rank))
                else:
                    if self.board[cur_rank][cur_file].color != piece.color:
                        moves.append(start + chr(cur_file + 97) +
                                     str(8 - cur_rank))
                    break

            cur_rank = start_rank
            cur_file = start_file

            while cur_rank > 0:
                cur_rank -= 1
                if self.board[cur_rank][cur_file] is None:
                    moves.append(start + chr(cur_file + 97) +
                                 str(8 - cur_rank))
                else:
                    if self.board[cur_rank][cur_file].color != piece.color:
                        moves.append(start + chr(cur_file + 97) +
                                     str(8 - cur_rank))
                    break

            cur_rank = start_rank
            cur_file = start_file

            while cur_file < 7:
                cur_file += 1
                if self.board[cur_rank][cur_file] is None:
                    moves.append(start + chr(cur_file + 97) +
                                 str(8 - cur_rank))
                else:
                    if self.board[cur_rank][cur_file].color != piece.color:
                        moves.append(start + chr(cur_file + 97) +
                                     str(8 - cur_rank))
                    break

            cur_rank = start_rank
            cur_file = start_file

            while cur_file > 0:
                cur_file -= 1
                if self.board[cur_rank][cur_file] is None:
                    moves.append(start + chr(cur_file + 97) +
                                 str(8 - cur_rank))
                else:
                    if self.board[cur_rank][cur_file].color != piece.color:
                        moves.append(start + chr(cur_file + 97) +
                                     str(8 - cur_rank))
                    break

            # check the queen diagonal moves
            cur_rank = start_rank
            cur_file = start_file

            while cur_rank < 7 and cur_file < 7:
                cur_rank += 1
                cur_file += 1
                if self.board[cur_rank][cur_file] is None:
                    moves.append(start + chr(cur_file + 97) +
                                 str(8 - cur_rank))
                else:
                    if self.board[cur_rank][cur_file].color != piece.color:
                        moves.append(start + chr(cur_file + 97) +
                                     str(8 - cur_rank))
                    break

            cur_rank = start_rank
            cur_file = start_file

            while cur_rank < 7 and cur_file > 0:
                cur_rank += 1
                cur_file -= 1
                if self.board[cur_rank][cur_file] is None:
                    moves.append(start + chr(cur_file + 97) +
                                 str(8 - cur_rank))
                else:
                    if self.board[cur_rank][cur_file].color != piece.color:
                        moves.append(start + chr(cur_file + 97) +
                                     str(8 - cur_rank))
                    break

            cur_rank = start_rank
            cur_file = start_file

            while cur_rank > 0 and cur_file < 7:
                cur_rank -= 1
                cur_file += 1
                if self.board[cur_rank][cur_file] is None:
                    moves.append(start + chr(cur_file + 97) +
                                 str(8 - cur_rank))
                else:
                    if self.board[cur_rank][cur_file].color != piece.color:
                        moves.append(start + chr(cur_file + 97) +
                                     str(8 - cur_rank))
                    break

            cur_rank = start_rank
            cur_file = start_file

            while cur_rank > 0 and cur_file > 0:
                cur_rank -= 1
                cur_file -= 1
                if self.board[cur_rank][cur_file] is None:
                    moves.append(start + chr(cur_file + 97) +
                                 str(8 - cur_rank))
                else:
                    if self.board[cur_rank][cur_file].color != piece.color:
                        moves.append(start + chr(cur_file + 97) +
                                     str(8 - cur_rank))
                    break
        elif piece.type == PieceType.KING:
            pass

        print("Moves: " + str(moves))

        if len(moves) > 0:
            return moves
        else:
            return None


def draw_board():
    # draw the board
    for rank in range(8):
        for file in range(8):
            # generate the tile name
            tile_name = chr(file + 97) + str(8 - rank)

            if (file + rank) % 2 == 0:
                color = settings.WHITE
            else:
                color = settings.BLACK

            if tile_name == mouse['tile'] and mouse['dragging'] is None:
                if board.board[rank][file] is not None:
                    if board.board[rank][file].color == board.turn:
                        color = (40, 255, 40)
                        if mouse['clicked']:
                            mouse['moves'] = board.enumerate_moves(tile_name)
                            if mouse['moves'] is not None:
                                mouse['dragging'] = tile_name

                    else:
                        color = (255, 40, 40)

            if mouse['moves'] is not None:
                search = mouse['dragging'] + tile_name
                if search in mouse['moves']:
                    color = (255, 255, 180)

            if mouse['dragging'] is not None:

                if mouse['dragging'] == tile_name:
                    color = (255, 255, 40)

                elif mouse['tile'] == tile_name:
                    color = (40, 40, 255)
                    if mouse['clicked']:
                        board.move(mouse['dragging'], tile_name)
                        mouse['dragging'] = None
                        mouse['moves'] = None

            pygame.draw.rect(screen, color, [
                             file * settings.SQUARE_SIZE, rank * settings.SQUARE_SIZE, settings.SQUARE_SIZE, settings.SQUARE_SIZE])

            # render the tile name to the screen
            text = font.render(tile_name, True, settings.FONT_COLOR_WHITE)
            screen.blit(text, (file * settings.SQUARE_SIZE +
                        10, rank * settings.SQUARE_SIZE + 10))

            if board.board[rank][file] is not None:

                piece = board.board[rank][file].fen_char()
                sprite = piece_sprites[piece]

                centered_file = file * settings.SQUARE_SIZE + \
                    (settings.SQUARE_SIZE / 2) - \
                    (sprite.get_width() / 2)

                centered_rank = rank * settings.SQUARE_SIZE + \
                    (settings.SQUARE_SIZE / 2) - \
                    (sprite.get_height() / 2)

                screen.blit(sprite, [centered_file, centered_rank])

    # draw the fen string
    fen_string = board.fen_encode()
    text = font.render(fen_string, True, settings.FONT_COLOR_WHITE)
    screen.blit(text, (8, 8 * settings.SQUARE_SIZE + 8))


def handle_events():
    global done, mouse
    mouse['clicked'] = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse['clicked'] = True


def draw_screen():
    screen.fill('black')
    # draw the screen
    draw_board()

    pygame.display.flip()


def get_mouse_tile():
    x, y = pygame.mouse.get_pos()
    if x < 800 and y < 800:
        # get the tile name
        file = int(x / settings.SQUARE_SIZE)
        rank = int(y / settings.SQUARE_SIZE)
        tile_name = chr(file + 97) + str(8 - rank)

        return tile_name
    else:
        return None


def handle_input():
    mouse['tile'] = get_mouse_tile()


def main():

    while not done:
        handle_events()
        handle_input()
        draw_screen()
        clock.tick(settings.FPS)


if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption("bad-chess")
    font = pygame.font.SysFont(None, settings.FONT_SIZE_NORMAL)
    clock = pygame.time.Clock()

    piece_sprites = {
        'B': pygame.image.load("sprites/white-bishop.png").convert_alpha(),
        'K': pygame.image.load("sprites/white-king.png").convert_alpha(),
        'N': pygame.image.load("sprites/white-knight.png").convert_alpha(),
        'P': pygame.image.load("sprites/white-pawn.png").convert_alpha(),
        'Q': pygame.image.load("sprites/white-queen.png").convert_alpha(),
        'R': pygame.image.load("sprites/white-rook.png").convert_alpha(),
        'b': pygame.image.load("sprites/black-bishop.png").convert_alpha(),
        'k': pygame.image.load("sprites/black-king.png").convert_alpha(),
        'n': pygame.image.load("sprites/black-knight.png").convert_alpha(),
        'p': pygame.image.load("sprites/black-pawn.png").convert_alpha(),
        'q': pygame.image.load("sprites/black-queen.png").convert_alpha(),
        'r': pygame.image.load("sprites/black-rook.png").convert_alpha(),
    }

    mouse = {
        "tile": None,
        "clicked": None,
        "dragging": None,
        "moves": None
    }

    board = Board()
    board.move('e2', 'e4')
    print(board.fen_encode())
    board.move('e7', 'e5')
    print(board.fen_encode())

    # print(board.fen_encode())

    # board.fen_decode("r1b1k1nr/p2p1pNp/n2B4/1p1NP2P/6P1/3P1Q2/P1P1K3/q5b1 w")
    # board.fen_decode("8/8/8/4p1K1/2k1P3/8/8/8 b")
    # board.fen_decode("4k2r/6r1/8/8/8/8/3R4/R3K3 w")
    # board.fen_decode(
    #     "qQqQqQqQ/QqQqQqQq/qQqQqQqQ/QqQqQqQq/qQqQqQqQ/QqQqQqQq/qQqQqQqQ/QqQqQqQq w")

    done = False

    main()
