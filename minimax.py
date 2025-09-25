# Importing necessary libraries
import numpy as np
import pygame
import sys
import math

# Colors - RGB values for various colors used in the game
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Dimensions - Constants for the board size and window dimensions
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

# Initialize pygame
pygame.init()

# Fonts - Fonts for displaying text
font = pygame.font.SysFont("monospace", 50)
score_font = pygame.font.SysFont("monospace", 35)

# Constants - Game-related constants
PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def winning_move(board, piece):
    # Check horizontal locations for a win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # Check vertical locations for a win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Check positively sloped diagonals for a win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Check negatively sloped diagonals for a win
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    ai_score = 0
    player_score = 0

    # Horizontal Scoring
    for row in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[row, :])]
        for col in range(COLUMN_COUNT - 3):
            window = row_array[col:col + 4]
            ai_score += evaluate_window(window, AI_PIECE)
            player_score += evaluate_window(window, PLAYER_PIECE)

    # Vertical Scoring
    for col in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, col])]
        for row in range(ROW_COUNT - 3):
            window = col_array[row:row + 4]
            ai_score += evaluate_window(window, AI_PIECE)
            player_score += evaluate_window(window, PLAYER_PIECE)

    # Positive Diagonal Scoring
    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT - 3):
            window = [board[row + i][col + i] for i in range(4)]
            ai_score += evaluate_window(window, AI_PIECE)
            player_score += evaluate_window(window, PLAYER_PIECE)

    # Negative Diagonal Scoring
    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT - 3):
            window = [board[row + 3 - i][col + i] for i in range(4)]
            ai_score += evaluate_window(window, AI_PIECE)
            player_score += evaluate_window(window, PLAYER_PIECE)

    return ai_score if piece == AI_PIECE else player_score


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def is_terminal_node(board):
    return (
            winning_move(board, PLAYER_PIECE)
            or winning_move(board, AI_PIECE)
            or len(get_valid_locations(board)) == 0
    )


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = np.random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


board = create_board()
game_over = False
turn = np.random.randint(PLAYER, AI)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Connect Four with Scores")


def draw_board(board, player_score, ai_score):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen,
                BLUE,
                (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE),
            )
            pygame.draw.circle(
                screen,
                BLACK,
                (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2),
                ),
                RADIUS,
            )

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(
                    screen,
                    RED,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        height - int(r * SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        height - int(r * SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )

    # Draw scores
    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
    player_label = score_font.render(f"Player: {player_score}", 1, RED)
    ai_label = score_font.render(f"AI: {ai_score}", 1, YELLOW)
    screen.blit(player_label, (40, 10))
    screen.blit(ai_label, (width - 200, 10))

    pygame.display.update()


# Initialize scores
player_score = 0
ai_score = 0

draw_board(board, player_score, ai_score)


def winning_move_in_one_step(board, piece):
    valid_locations = get_valid_locations(board)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        if winning_move(temp_board, piece):
            return col
    return None


def minimax(board, depth, alpha, beta, maximizingPlayer):
    # ------------------------ your code ------------------------
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000000000000)
            else:
                return (None, 0)
        else: 
            return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -math.inf
        best_col = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = math.inf
        best_col = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value


def display_end_screen(player_score, ai_score, winner_message):
    end_screen = pygame.display.set_mode((500, 300))
    pygame.display.set_caption("Game Over")

    end_screen.fill(WHITE)
    title_font = pygame.font.SysFont("monospace", 50)
    score_font = pygame.font.SysFont("monospace", 35)

    winner_label = title_font.render(winner_message, 1, RED)
    player_score_label = score_font.render(f"Player Score: {player_score}", 1, BLACK)
    ai_score_label = score_font.render(f"AI Score: {ai_score}", 1, BLACK)

    end_screen.blit(winner_label, (100, 50))
    end_screen.blit(player_score_label, (100, 150))
    end_screen.blit(ai_score_label, (100, 200))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            draw_board(board, player_score, ai_score)
            pos_x = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (pos_x, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # Player Turn
            if turn == PLAYER:
                pos_x = event.pos[0]
                col = int(math.floor(pos_x / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = font.render("You win!", 1, RED)
                        screen.blit(label, (40, 10))
                        player_score += 1
                        game_over = True

                    turn = AI
                    draw_board(board, player_score, ai_score)

    # AI Turn
    if turn == AI and not game_over:
        col, _ = minimax(board, 4, -math.inf, math.inf, True)
        # col = minimax()
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = font.render("AI wins!", 1, YELLOW)
                screen.blit(label, (40, 10))
                ai_score += 1
                game_over = True

            turn = PLAYER
            draw_board(board, player_score, ai_score)

    if game_over:
        pygame.time.wait(3000)

        if winning_move(board, PLAYER_PIECE):
            display_end_screen(player_score, ai_score, "Player Wins!")
        elif winning_move(board, AI_PIECE):
            display_end_screen(player_score, ai_score, "AI Wins!")
        else:
            display_end_screen(player_score, ai_score, "It's a Draw!")

        pygame.time.wait(3000)
