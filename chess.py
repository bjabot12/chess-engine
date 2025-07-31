import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1020, 1020
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE

# Colors
WHITE = (255, 255, 221)
BLACK = (134, 166, 102)
SELECTED_COLOR = (200, 0, 0)


# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

button_rect = pygame.Rect(1100, 100, 150, 50)

# Load chess piece images
pieces = {
    'r': pygame.image.load('images/bR.png'),
    'b': pygame.image.load('images/bB.png'),
    'n': pygame.image.load('images/bN.png'),
    'q': pygame.image.load('images/bQ.png'),
    'k': pygame.image.load('images/bK.png'),
    'p': pygame.image.load('images/bp.png'),
    'R': pygame.image.load('images/wR.png'),
    'N': pygame.image.load('images/wN.png'),
    'B': pygame.image.load('images/wB.png'),
    'Q': pygame.image.load('images/wQ.png'),
    'K': pygame.image.load('images/wK.png'),
    'P': pygame.image.load('images/wp.png'),
}

class Piece:
    def __init__(self, notation, value=0):
        self.notation = notation
        self.value = value



def move(row, col, selected_square, board):
    board[row][col] = board[selected_square[0]][selected_square[1]]
    board[selected_square[0]][selected_square[1]] = ' '
    return board


class GameState:
    def __init__(self):
        board = [
            "rnbqkbnr",
            "pppppppp",
            "        ",
            "        ",
            "        ",
            "        ",
            "PPPPPPPP",
            "RNBQKBNR"
        ]
        self.chess_board = [list(row) for row in board]
        self.white_to_play = True

    def getBoard(self):
        return self.chess_board
    
    def change_turn(self):
        self.white_to_play = not self.white_to_play
    
    def reset_board(self):
        board = [
                    "rnbqkbnr",
                    "pppppppp",
                    "        ",
                    "        ",
                    "        ",
                    "        ",
                    "PPPPPPPP",
                    "RNBQKBNR"
                ]
        self.chess_board = [list(row) for row in board]
        self.white_to_play = True

               

def is_valid_move(piece, board, start_pos, end_pos):
    # print("hei " + piece.lower())
    if piece.lower() == "p":
        return is_valid_pawn_move(board, start_pos, end_pos)
    elif piece.lower() == "b":
        return is_valid_bishop_move(board, start_pos, end_pos)
    elif piece.lower() == "r":
        return is_valid_rook_move(board, start_pos, end_pos)
    elif piece.lower() == "n":
        return is_valid_knight_move(board, start_pos, end_pos)
    elif piece.lower() == "q":
        return is_valid_queen_move(board, start_pos, end_pos)
    elif piece.lower() == "k":
        return is_valid_king_move(board, start_pos, end_pos)
    

def is_valid_bishop_move(board, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    # Check if the start and end positions are on the same diagonal
    if abs(start_row - end_row) != abs(start_col - end_col):
        return False

    # Check if the bishop's path is clear (no pieces in between)
    row_dir = 1 if end_row > start_row else -1
    col_dir = 1 if end_col > start_col else -1
    check_row, check_col = start_row + row_dir, start_col + col_dir
    while check_row != end_row and check_col != end_col:
        if board[check_row][check_col] != ' ':
            return False
        check_row += row_dir
        check_col += col_dir

    if board[end_row][end_col] == ' ' or board[end_row][end_col].islower() != board[start_row][start_col].islower():
            return True
    return False

def is_valid_rook_move(board, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    # Check if the start and end positions are in the same row or column
    if start_row != end_row and start_col != end_col:
        return False

    # Check if the rook's path is clear (no pieces in between)
    if start_row == end_row:
        # Moving horizontally
        step = 1 if end_col > start_col else -1
        for col in range(start_col + step, end_col, step):
            if board[start_row][col] != ' ':
                return False
    else:
        # Moving vertically
        step = 1 if end_row > start_row else -1
        for row in range(start_row + step, end_row, step):
            if board[row][start_col] != ' ':
                return False


    if board[end_row][end_col] == ' ' or board[end_row][end_col].islower() != board[start_row][start_col].islower():
            return True
    return False


def is_valid_knight_move(board, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    # Check if the move is in an L-shape pattern (2 squares in one direction, 1 square perpendicular)
    row_move = abs(start_row - end_row)
    col_move = abs(start_col - end_col)

    if (row_move == 2 and col_move == 1) or (row_move == 1 and col_move == 2):
        # Check if the end position is within the board bounds
        if end_row < 0 or end_row > 7 or end_col < 0 or end_col > 7:
            return False

        # Check if the end position is empty or has an opponent's piece
        if board[end_row][end_col] == ' ' or board[end_row][end_col].islower() != board[start_row][start_col].islower():
            print("HHHEEER!!!")
            print(start_pos, end_pos)
            print(board[end_row][end_col])
            return True

    return False


def is_valid_pawn_move(board, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    # Check if the end position is within the board's bounds
    if end_row < 0 or end_row > 7 or end_col < 0 or end_col > 7:
        return False

    # # Check if the end position is empty
    # if board[end_row][end_col] != ' ':
    #     return False

    # White pawn moves
    if board[start_row][start_col] == 'P':
        if start_col == end_col and end_row == start_row - 1 and board[end_row][end_col] == ' ':
            return True
        elif start_row == 6 and start_col == end_col and end_row == start_row - 2 and board[start_row - 1][start_col] == ' ':
            return True
        elif abs(start_col - end_col) == 1 and end_row == start_row - 1 and board[end_row][end_col].islower():
            return True

    # Black pawn moves
    elif board[start_row][start_col] == 'p':
        if start_col == end_col and end_row == start_row + 1 and board[end_row][end_col] == ' ':
            return True
        elif start_row == 1 and start_col == end_col and end_row == start_row + 2 and board[start_row + 1][start_col] == ' ':
            return True
        
        elif abs(start_col - end_col) == 1 and end_row == start_row + 1 and board[end_row][end_col].isupper():
            return True

    return False

def is_valid_queen_move(board, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    # Check if it's a valid rook move (vertical or horizontal)
    if start_row == end_row or start_col == end_col:
        return is_valid_rook_move(board, start_pos, end_pos)

    # Check if it's a valid bishop move (diagonal)
    row_move = abs(start_row - end_row)
    col_move = abs(start_col - end_col)
    if row_move == col_move:
        return is_valid_bishop_move(board, start_pos, end_pos)

    return False

def is_valid_king_move(board, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    # Check if the move is within one square in any direction
    row_move = abs(start_row - end_row)
    col_move = abs(start_col - end_col)

    if row_move <= 1 and col_move <= 1:
        # Check if the end position is within the board bounds
        if end_row < 0 or end_row > 7 or end_col < 0 or end_col > 7:
            return False

        # Check if the end position is either empty or has an opponent's piece
        if board[end_row][end_col] == ' ' or board[end_row][end_col].islower() != board[start_row][start_col].islower():
            return True

    return False


def is_king_in_check(board, king_pos, king_color):
    king_row, king_col = king_pos
    
    # Check for opponent's pieces threatening the king
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != ' ' and piece.islower() != king_color:
                if piece.lower() == 'p':
                    target_positions = [(row-1, col-1), (row-1, col+1)] if piece.islower() else [(row+1, col-1), (row+1, col+1)]
                    for target_row, target_col in target_positions:
                        if target_row == king_row and target_col == king_col:
                            print("check")
                            return True
                elif piece.lower() == 'n':
                    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
                    for dr, dc in knight_moves:
                        if row + dr == king_row and col + dc == king_col:
                            print("check")
                            return True
                else:
                    if is_valid_move(board, (row, col), king_pos):
                        print("check")
                        return True

    return False

# Functions
def draw_board(chess_board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = chess_board[row][col]
            if piece != ' ':
                screen.blit(pieces[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))
    

def get_square(mouse_pos):
    row = mouse_pos[1] // SQUARE_SIZE
    col = mouse_pos[0] // SQUARE_SIZE
    return row, col

def draw_button(text):
    color = (50, 90, 140)
    pygame.draw.rect(screen, color, button_rect)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

def main():

    clock = pygame.time.Clock()
    selected_square = None

    gs = GameState()
    chess_board = gs.getBoard()

    print(chess_board[0][0])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, col = get_square(mouse_pos)
                hovered = button_rect.collidepoint(mouse_pos)
                print(chess_board[row][col])
                if selected_square is None:
                    # Checks to see who's turn it is
                    if gs.white_to_play is True and chess_board[row][col].isupper():
                        selected_square = (row, col)
                    elif gs.white_to_play is False and chess_board[row][col].islower():
                        selected_square = (row, col)
                    else:
                        continue
                else:
                    if is_valid_move(chess_board[selected_square[0]][selected_square[1]], chess_board, selected_square, (row,col)):
                        chess_board = move(row, col, selected_square, chess_board)
                        selected_square = None
                        gs.change_turn()
                    else:
                        selected_square = None
        screen.fill((255, 255, 255))
        draw_board(chess_board)
        if selected_square:
            s = pygame.Surface((SQUARE_SIZE,SQUARE_SIZE))  # the size of your rect
            s.set_alpha(80)                # alpha level
            s.fill((SELECTED_COLOR))           # this fills the entire surface
            screen.blit(s, (selected_square[1] * SQUARE_SIZE, selected_square[0] * SQUARE_SIZE))
        
        pygame.draw.rect(screen, (70, 130, 180), button_rect)
        pygame.display.flip()
        clock.tick(60)


def find_valid_moves():
    gs = GameState()
    chess_board = gs.getBoard()
    clock = pygame.time.Clock()
    i = 0
    
    cs1 = chess_board

    for start_row, row in enumerate(cs1):
        for start_col, col in enumerate(row):
            print(str(col))
            if col != " " and col != "P" and col != "p":

                for end_row in range(8):
                    for end_col in range(8):
                        if is_valid_move(col, chess_board, (start_row, start_col), (end_row, end_col)):
                            chess_board = move(end_row, end_col, (start_row, start_col), chess_board)
                            print("valid move")
                            
                            # Handle events
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                            
                            # Draw and update display
                            screen.fill((255, 255, 255))
                            draw_board(chess_board)
                            pygame.display.flip()
                            pygame.time.wait(1000)
                            
                            # Control frame rate
                            clock.tick(5)  # Limit to 5 frames per second
                            
                            i += 1
                            gs.reset_board()
                            chess_board = gs.getBoard()
    print(f"Total valid moves found: {i}")
                    


def test_valid_moves():
        gs = GameState()
        chess_board = gs.getBoard()
        for row in chess_board:
            for piece in row:
                print(piece)

if __name__ == "__main__":
    # test_valid_moves()
    # main()
    find_valid_moves()
