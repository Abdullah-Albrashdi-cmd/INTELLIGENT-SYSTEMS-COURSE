#Part1-Task2-Connect Four-140185

import pygame
import time
import math
import random

pygame.init()

#audio
pygame.mixer.music.load("Task2_sound.mp3")
pygame.mixer.music.play(-1)

#Settings
ROWS = 6
COLS = 7
SQUARE_SIZE = 75
RADIUS = int(SQUARE_SIZE / 2 - 6)

BOARD_WIDTH = COLS * SQUARE_SIZE
BOARD_HEIGHT = ROWS * SQUARE_SIZE
WIN_SCORE  = math.inf
LOSS_SCORE = -math.inf

HEADER_HEIGHT = 160
STATUS_HEIGHT = 80
WIDTH = BOARD_WIDTH + 80
HEIGHT = HEADER_HEIGHT + BOARD_HEIGHT + STATUS_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
TITLE_FONT = pygame.font.Font(None, 45)
FONT = pygame.font.Font(None, 30)
SMALL_FONT = pygame.font.Font(None, 25)

#Colors
BLUE = (46, 90, 170)
BG_COLOR = (0, 0, 0)
BOARD_BG = (25, 32, 60)
RED = (255, 99, 132) # Human
YELLOW = (255, 214, 102) # AI
WHITE = (240, 240, 240)
GRAY = (180, 180, 190)

# ----------------------------------------------------------------------------------------------#

def create_board():
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(0)
        board.append(row)
    return board


def copy_board(board):
    return [row[:] for row in board]


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r
    return None


def is_valid_location(board, col):
    return board[ROWS - 1][col] == 0


def winning_move(board, piece):
    #Horizontal check
    for c in range(COLS - 3):
        for r in range(ROWS):
            if (board[r][c] == piece and
                board[r][c+1] == piece and
                board[r][c+2] == piece and
                board[r][c+3] == piece):
                return True

    #Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if (board[r][c] == piece and
                board[r+1][c] == piece and
                board[r+2][c] == piece and
                board[r+3][c] == piece):
                return True

    #Positive diagonal check
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if (board[r][c] == piece and
                board[r+1][c+1] == piece and
                board[r+2][c+2] == piece and
                board[r+3][c+3] == piece):
                return True

    #Negative diagonal check
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if (board[r][c] == piece and
                board[r-1][c+1] == piece and
                board[r-2][c+2] == piece and
                board[r-3][c+3] == piece):
                return True

    return False


def get_valid_locations(board):
    valid_locations = []
    for c in range(COLS):
        if is_valid_location(board, c):
            valid_locations.append(c)
    return valid_locations


def evaluate_window(window, piece):
    score = 0
    opp_piece = 1 if piece == 2 else 2

    if window.count(piece) == 4:
        score += 120
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 7
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 3

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 8

    return score


def score_position(board, piece):
    score = 0

    #Center column preference
    center_col = COLS // 2
    center_array = [board[r][center_col] for r in range(ROWS)]
    score += center_array.count(piece) * 4

    #Horizontal windows
    for r in range(ROWS):
        row_array = [board[r][c] for c in range(COLS)]
        for c in range(COLS - 3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    #Vertical windows
    for c in range(COLS):
        col_array = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    #Positive diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    #Negative diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


#MINIMAX (no pruning)
def minimax(board, depth, isMaximizer, ai_piece):
    valid_locations = get_valid_locations(board)
    opp_piece = 1 if ai_piece == 2 else 2

    # Terminal cases
    if winning_move(board, ai_piece):
        return WIN_SCORE
    elif winning_move(board, opp_piece):
        return LOSS_SCORE
    elif depth == 0 or len(valid_locations) == 0:
        return score_position(board, ai_piece)

    if isMaximizer:
        bestScore = -math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = copy_board(board)
            drop_piece(temp_board, row, col, ai_piece)

            score = minimax(temp_board, depth - 1, False, ai_piece)
            bestScore = max(bestScore, score)

        return bestScore

    else:
        bestScore = math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = copy_board(board)
            drop_piece(temp_board, row, col, opp_piece)

            score = minimax(temp_board, depth - 1, True, ai_piece)
            bestScore = min(bestScore, score)

        return bestScore


#MINIMAX with Alpha Beta
def minimax_ab(board, depth, alpha, beta, isMaximizer, ai_piece):
    valid_locations = get_valid_locations(board)
    opp_piece = 1 if ai_piece == 2 else 2

    #Terminal cases
    if winning_move(board, ai_piece):
        return WIN_SCORE
    elif winning_move(board, opp_piece):
        return LOSS_SCORE
    elif depth == 0 or len(valid_locations) == 0:
        return score_position(board, ai_piece)

    if isMaximizer:
        value = -math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = copy_board(board)
            drop_piece(temp_board, row, col, ai_piece)

            score = minimax_ab(temp_board, depth - 1, alpha, beta, False, ai_piece)
            value = max(value, score)
            alpha = max(alpha, value)
            if alpha >= beta:
                break #prune
        return value

    else:
        value = math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = copy_board(board)
            drop_piece(temp_board, row, col, opp_piece)

            score = minimax_ab(temp_board, depth - 1, alpha, beta, True, ai_piece)
            value = min(value, score)
            beta = min(beta, value)
            if alpha >= beta:
                break #prune
        return value


#Move selection
def bestMove(board, depth, ai_piece, algorithm):
    valid_locations = get_valid_locations(board)
    if not valid_locations:
        return None #no legal moves

    bestScore = -math.inf
    best_col = random.choice(valid_locations)

    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = copy_board(board)
        drop_piece(temp_board, row, col, ai_piece)

        if algorithm == "alphabeta":
            score = minimax_ab(temp_board, depth - 1, -math.inf, math.inf, False, ai_piece)
        else:
            score = minimax(temp_board, depth - 1, False, ai_piece)

        if score > bestScore:
            bestScore = score
            best_col = col

    return best_col


def difficulty_label(depth):
    if depth <= 2:
        return "Easy"
    elif depth <= 4:
        return "Medium"
    else:
        return "Hard"


def draw_header(algorithm, depth, turn, game_over, winner_piece):
    pygame.draw.rect(screen, BG_COLOR, (0, 0, WIDTH, HEADER_HEIGHT))

    #Title
    title = TITLE_FONT.render("Connect Four Game", True, WHITE)
    x = 30
    h = TITLE_FONT.get_height()
    y = HEADER_HEIGHT // 2 - h // 2
    screen.blit(title, (x, y))

    #Algorithm and difficulty info
    algo_text = "Alpha-Beta" if algorithm == "alphabeta" else "Minimax"
    info = SMALL_FONT.render(f"AI: {algo_text} | Depth: {depth} ({difficulty_label(depth)})",True, GRAY)
    screen.blit(info, (30, 20))

    #Status
    if game_over:
        if winner_piece == 1:
            msg, color = "You Win!", RED
        elif winner_piece == 2:
            msg, color = "AI Wins!", YELLOW
        else:
            msg, color = "Draw!", WHITE
    else:
        if turn == 0:
            msg, color = "Your Turn", RED
        else:
            msg, color = "AI Turn...", YELLOW

    status = FONT.render(msg, True, color)
    status_x = WIDTH - 200
    status_h = FONT.get_height()
    status_y = HEADER_HEIGHT // 2 - status_h // 2
    screen.blit(status, (status_x, status_y))


def draw_board(board):
    board_rect = pygame.Rect((WIDTH - BOARD_WIDTH) // 2 - 10,HEADER_HEIGHT - 10,BOARD_WIDTH + 20,BOARD_HEIGHT + 20)
    pygame.draw.rect(screen, BOARD_BG, board_rect, border_radius=20)

    offset_x = (WIDTH - BOARD_WIDTH) // 2
    offset_y = HEADER_HEIGHT

    for c in range(COLS):
        for r in range(ROWS):
            rect = pygame.Rect(
                offset_x + c * SQUARE_SIZE,
                offset_y + (ROWS - 1 - r) * SQUARE_SIZE,
                SQUARE_SIZE, SQUARE_SIZE
            )
            pygame.draw.rect(screen, BLUE, rect, border_radius=18)
            pygame.draw.circle(
                screen, BG_COLOR,
                (rect.x + SQUARE_SIZE // 2, rect.y + SQUARE_SIZE // 2),
                RADIUS
            )

    for c in range(COLS):
        for r in range(ROWS):
            piece = board[r][c]
            if piece == 0:
                continue
            col_x = offset_x + c * SQUARE_SIZE + SQUARE_SIZE // 2
            row_y = offset_y + (ROWS - 1 - r) * SQUARE_SIZE + SQUARE_SIZE // 2
            color = RED if piece == 1 else YELLOW
            pygame.draw.circle(screen, color, (col_x, row_y), RADIUS)

    pygame.display.update()


def menu_screen():
    algorithm = "alphabeta"
    depth = 4

    #Select Algorithm
    choosing_algo = True
    while choosing_algo:
        screen.fill(BG_COLOR)

        title = TITLE_FONT.render("Connect Four Game", True, WHITE)
        sub = SMALL_FONT.render("Step 1: Choose algorithm", True, GRAY)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 80)))
        screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 120)))

        t1 = FONT.render("M - Minimax", True, WHITE)
        t2 = FONT.render("A - Alpha-Beta", True, WHITE)
        t3 = SMALL_FONT.render("Press ENTER to confirm selection", True, GRAY)

        screen.blit(t1, (80, 200))
        screen.blit(t2, (80, 240))
        screen.blit(t3, (80, 300))

        info = SMALL_FONT.render(f"Selected Algorithm: {'Alpha-Beta' if algorithm == 'alphabeta' else 'Minimax'}",True, WHITE)
        screen.blit(info, (80, 360))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    algorithm = "minimax"
                elif event.key == pygame.K_a:
                    algorithm = "alphabeta"
                elif event.key == pygame.K_RETURN:
                    choosing_algo = False

    #Choose difficulty
    choosing_diff = True
    while choosing_diff:
        screen.fill(BG_COLOR)

        title = TITLE_FONT.render("Connect Four - Setup", True, WHITE)
        sub = SMALL_FONT.render("Step 2: Choose difficulty", True, GRAY)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 80)))
        screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 120)))

        t3 = FONT.render("1 - Easy", True, GRAY)
        t4 = FONT.render("2 - Medium", True, GRAY)
        t5 = FONT.render("3 - Hard", True, GRAY)
        t6 = SMALL_FONT.render("Press ENTER to start game", True, WHITE)

        screen.blit(t3, (80, 200))
        screen.blit(t4, (80, 240))
        screen.blit(t5, (80, 280))
        screen.blit(t6, (80, 340))

        info = SMALL_FONT.render(f"Selected Difficulty:  {difficulty_label(depth)}",True, WHITE)
        screen.blit(info, (80, 400))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    depth = 2
                elif event.key == pygame.K_2:
                    depth = 4
                elif event.key == pygame.K_3:
                    depth = 6
                elif event.key == pygame.K_RETURN:
                    choosing_diff = False

    return algorithm, depth


#gravity-based visual disc drop animation
def animate_drop(board, col, final_row, piece):
    offset_x = (WIDTH - BOARD_WIDTH) // 2
    offset_y = HEADER_HEIGHT
    color = RED if piece == 1 else YELLOW

    for temp_row in range(ROWS - 1, final_row - 1, -1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        draw_board(board)
        draw_footer()

        x = offset_x + col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = offset_y + (ROWS - 1 - temp_row) * SQUARE_SIZE + SQUARE_SIZE // 2
        pygame.draw.circle(screen, color, (x, y), RADIUS)
        pygame.display.update()
        time.sleep(0.05)


def draw_footer():
    pygame.draw.rect(screen, BG_COLOR, (0, HEIGHT - STATUS_HEIGHT, WIDTH, STATUS_HEIGHT))
    text = SMALL_FONT.render("ESC: Quit  |  After a match Press 'R' to play again", True, GRAY)
    screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT - STATUS_HEIGHT // 2)))

# ----------------------------------------------------------------------------------------------#

# main function
def main():
    board = create_board()
    algorithm, depth = menu_screen()

    game_over = False
    turn = 0  #0 = Human, 1 = AI
    winner_piece = 0

    offset_x = (WIDTH - BOARD_WIDTH) // 2

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()

            #Player move
            if event.type == pygame.MOUSEMOTION and not game_over:
                draw_header(algorithm, depth, turn, game_over, winner_piece)
                draw_board(board)
                draw_footer()

                posx = event.pos[0]
                pygame.draw.rect(screen, BG_COLOR, (0, HEADER_HEIGHT - 60, WIDTH, 60))
                if offset_x <= posx <= offset_x + BOARD_WIDTH:
                    pygame.draw.circle(screen, RED, (posx, HEADER_HEIGHT - 20), RADIUS)
                pygame.display.update()

            if (event.type == pygame.MOUSEBUTTONDOWN and not game_over and turn == 0):
                posx = event.pos[0]
                col = (posx - offset_x) // SQUARE_SIZE
                if 0 <= col < COLS and is_valid_location(board, col):
                    row = get_next_open_row(board, col)

                    #gravity animation for player
                    animate_drop(board, col, row, 1)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        game_over = True
                        winner_piece = 1

                    turn = 1
                    draw_header(algorithm, depth, turn, game_over, winner_piece)
                    draw_board(board)
                    draw_footer()
                    pygame.display.update()

        #AI move
        if turn == 1 and not game_over:
            time.sleep(0.5)

            ai_piece = 2
            col = bestMove(board, depth, ai_piece, algorithm)

            if col is None or not is_valid_location(board, col):
                game_over = True
                winner_piece = 0
            else:
                row = get_next_open_row(board, col)

                # gravity animation for AI
                animate_drop(board, col, row, ai_piece)
                drop_piece(board, row, col, ai_piece)

                if winning_move(board, ai_piece):
                    game_over = True
                    winner_piece = ai_piece

            turn = 0
            draw_header(algorithm, depth, turn, game_over, winner_piece)
            draw_board(board)
            draw_footer()
            pygame.display.update()

        if game_over:
            msg = SMALL_FONT.render("Press R to play again or ESC to quit", True, WHITE)
            pygame.draw.rect(screen, BG_COLOR, (0, HEIGHT - STATUS_HEIGHT, WIDTH, STATUS_HEIGHT))
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT - STATUS_HEIGHT // 2)))
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            algorithm, depth = menu_screen()
                            board = create_board()
                            game_over = False
                            winner_piece = 0
                            turn = 0

                            draw_header(algorithm, depth, turn, game_over, winner_piece)
                            draw_board(board)
                            draw_footer()
                            pygame.display.update()

                            waiting = False
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()

#Call main to run the program
main()