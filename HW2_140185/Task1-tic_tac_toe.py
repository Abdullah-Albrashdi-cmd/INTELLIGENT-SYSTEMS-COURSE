#Part1-Task1-Tec Tac Toe-140185

import pygame
import random
import time

pygame.init()

#audio
pygame.mixer.music.load("Task1_sound.mp3")
pygame.mixer.music.play(-1)

WIDTH, HEIGHT = 500, 550
ROWS, COLS = 3,3
CELL_SIZE = 100

BOARD_SIZE = CELL_SIZE * COLS
BOARD_X = (WIDTH - BOARD_SIZE) // 2

#Color Settingfs
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GRAY = (200, 200, 200)
LINE_COLOR = (0, 150, 200)
X_COLOR = (255, 80, 80)
O_COLOR = (80, 160, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - X and O")

clock = pygame.time.Clock()

#Font Settings
T_Font = pygame.font.Font(None, 50)
FONT = pygame.font.Font(None, 35)
SMALL_FONT = pygame.font.Font(None, 25)




#---------------------------------------------------------------------------------------------------------------------------------------#
def create_board():
    return {i: '' for i in range(1, 10)}

def isSpaceFree(board, position):
    return (board[position] == '')

def checkforwin(board):
    winning_position = [
        (1,2,3),(4,5,6),(7,8,9),
        (1,4,7),(2,5,8),(3,6,9),
        (1,5,9),(3,5,7)
    ]
    for pos in winning_position:
        if (board[pos[0]] == board[pos[1]] == board[pos[2]] and board[pos[0]] != ''):
            return board[pos[0]]   #'X' or 'O'
    return None

def checkfordraw(board):
    return all(board[pos] != '' for pos in board.keys())


def minimax(board, isMaximizer):
    winner = checkforwin(board)
    if winner == 'X':
        return 1
    elif winner == 'O':
        return -1
    elif checkfordraw(board):
        return 0
    
    if isMaximizer:
        bestScore = -float('Inf')
        for pos in board.keys():
            if isSpaceFree(board, pos):
                board[pos] = 'X'
                score = minimax(board, False)
                board[pos] = ''
                bestScore = max(score, bestScore)
    else:
        bestScore = float('Inf')
        for pos in board.keys():
            if isSpaceFree(board, pos):
                board[pos] = 'O'
                score = minimax(board, True)
                board[pos] = ''
                bestScore = min(score, bestScore)
    return bestScore

#This function now the position then draw it 
def pos_to_row_col(pos):
    idx = pos - 1
    row = idx // 3
    col = idx % 3
    return row, col

#This function modify the board
def row_col_to_pos(row, col):
    return row * 3 + col + 1

#Ai easy
def ai_easy(board):
    moves = [pos for pos in board.keys() if isSpaceFree(board, pos)]
    if not moves:
        return None
    return random.choice(moves)

#Ai medium
def ai_medium(board):
    moves = [pos for pos in board.keys() if isSpaceFree(board, pos)]
    for pos in moves:
        board[pos] = 'X'
        if checkforwin(board) == 'X':
            board[pos] = ''
            return pos
        board[pos] = ''

    for pos in moves:
        board[pos] = 'O'
        if checkforwin(board) == 'O':
            board[pos] = ''
            return pos
        board[pos] = ''

    return ai_easy(board)

#Ai hard
def ai_hard(board):
    move = None
    bestScore = -float('Inf')
    for pos in board.keys():
        if isSpaceFree(board, pos):
            board[pos] = 'X'
            score = minimax(board, False)
            board[pos] = ''
            if score > bestScore:
                bestScore = score
                move = pos
    return move


def draw_grid():
    screen.fill(BLACK)
 
    for c in range(1, COLS):
        x = BOARD_X + c * CELL_SIZE
        pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, CELL_SIZE * ROWS), 3)

    for r in range(1, ROWS):
        y = r * CELL_SIZE
        pygame.draw.line(
            screen, LINE_COLOR,
            (BOARD_X, y),
            (BOARD_X + BOARD_SIZE, y),
            3
        )


def draw_marks(board):
    for pos, mark in board.items():
        if mark == '':
            continue
        row, col = pos_to_row_col(pos)
        cx = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
        cy = row * CELL_SIZE + CELL_SIZE // 2

        if mark == 'X':
            offset = 30
            pygame.draw.line(screen, X_COLOR, (cx - offset, cy - offset), (cx + offset, cy + offset), 3)
            pygame.draw.line(screen, X_COLOR, (cx - offset, cy + offset), (cx + offset, cy - offset), 3)
        else: # ='O'
            pygame.draw.circle(screen, O_COLOR, (cx, cy), 30, 3)



def draw_status_text(mode, current_player, game_over, winner):
    barRect = pygame.Rect(0, 300, WIDTH, HEIGHT - 300)
    pygame.draw.rect(screen, BLACK, barRect)
    pygame.draw.rect(screen, BLACK, barRect, 1)

    if not game_over:
        if mode == "HvH":
            main_text = f"Turn: Player {current_player}"
        else:
            if current_player == 'X':
                main_text = "Turn: AI (X)"
            else:
                main_text = "Turn: Player (O)"
    else:
        if winner == 'X':
            main_text = "AI (X) Wins!" if mode != "HvH" else "Player X Wins!"
        elif winner == 'O':
            main_text = "Player O Wins!"
        else:
            main_text = "Draw!"

    text = FONT.render(main_text, True, WHITE)
    screen.blit(text, text.get_rect(center=(WIDTH // 2, 400)))

    if mode == "HvH":
        mode_txt = "Mode: Human vs Human"
    elif mode == "AI_E":
        mode_txt = "Mode: Human vs Easy AI"
    elif mode == "AI_M":
        mode_txt = "Mode: Human vs Medium AI"
    elif mode == "AI_H":
        mode_txt = "Mode: Human vs Hard AI"
    else:
        mode_txt = ""

    hint = SMALL_FONT.render("Press 'R' to Restart  |  'ESC' to Quit", True, WHITE)
    mode_text = SMALL_FONT.render(mode_txt, True, WHITE)

    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 440)))
    screen.blit(mode_text, mode_text.get_rect(center=(WIDTH // 2, 480)))



def menu_screen():
    mode = None
    choosing = True
    while choosing:
        screen.fill(BLACK)

        title = T_Font.render("Tic Tac Toe - X and O", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 60)))

        t1 = FONT.render("1 - Human vs Human", True, WHITE)
        t2 = FONT.render("2 - Human vs Easy AI",  True, WHITE)
        t3 = FONT.render("3 - Human vs Medium AI", True, WHITE)
        t4 = FONT.render("4 - Human vs Hard AI", True, WHITE)
        screen.blit(t1, (110, 150))
        screen.blit(t2, (110, 200))
        screen.blit(t3, (110, 250))
        screen.blit(t4, (110, 300))

        hint = SMALL_FONT.render("Choose mode (1-4)  | Press ESC to Quit",True, GRAY)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 400)))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #K_ESCAPE = "esc key"
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_1: #K_1 = "1"
                    mode = "HvH"
                    choosing = False
                elif event.key == pygame.K_2:
                    mode = "AI_E"
                    choosing = False
                elif event.key == pygame.K_3:
                    mode = "AI_M"
                    choosing = False
                elif event.key == pygame.K_4:
                    mode = "AI_H"
                    choosing = False

    return mode

def main():
    mode = menu_screen()
    board = create_board()
    current_player = 'X'
    game_over = False
    winner = None

    running = True
    while running:

        if (not game_over) and (mode in ("AI_E", "AI_M", "AI_H")) and current_player == 'X':
            time.sleep(0.5)
            if mode == "AI_E":
                pos = ai_easy(board)
            elif mode == "AI_M":
                pos = ai_medium(board)
            else:
                pos = ai_hard(board)

            if pos is not None and isSpaceFree(board, pos):
                board[pos] = 'X'
                w = checkforwin(board)
                if w is not None:
                    winner = w
                    game_over = True
                elif checkfordraw(board):
                    winner = None
                    game_over = True
                else:
                    current_player = 'O'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    mode = menu_screen()
                    board = create_board()
                    current_player = 'X'
                    game_over = False
                    winner = None
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                if 0 <= y < CELL_SIZE * ROWS and BOARD_X <= x < BOARD_X + BOARD_SIZE:
                    col = (x - BOARD_X) // CELL_SIZE
                    row = y // CELL_SIZE
                    pos = row_col_to_pos(row, col)

                    if isSpaceFree(board, pos):
                        if mode == "HvH":
                            board[pos] = current_player
                            w = checkforwin(board)
                            if w is not None:
                                winner = w
                                game_over = True
                            elif checkfordraw(board):
                                winner = None
                                game_over = True
                            else:
                                current_player = 'O' if current_player == 'X' else 'X'
                        else:
                            if current_player == 'O':
                                board[pos] = 'O'
                                w = checkforwin(board)
                                if w is not None:
                                    winner = w
                                    game_over = True
                                elif checkforwin(board):
                                    winner = None
                                    game_over = True
                                else:
                                    current_player = 'X'

        draw_grid()
        draw_marks(board)
        draw_status_text(mode, current_player, game_over, winner)
        pygame.display.update()

 
#Call main to run the program
main()