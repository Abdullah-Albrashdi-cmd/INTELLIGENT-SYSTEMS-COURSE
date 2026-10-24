import pygame
import sys
import random

pygame.init()

# ---------------- إعداد النافذة و الألوان (ثوابت فقط) ----------------
WIDTH, HEIGHT = 400, 500
CELL_SIZE = 100
ROWS, COLS = 3, 3

BOARD_SIZE = CELL_SIZE * COLS           # 300
BOARD_X = (WIDTH - BOARD_SIZE) // 2     # 50 → البورد في النص أفقيًا

WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GRAY   = (200, 200, 200)
LINE_COLOR = (0, 150, 200)
X_COLOR    = (255, 80, 80)
O_COLOR    = (80, 160, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - Part 1 (No Global)")

FONT       = pygame.font.Font(None, 32)
SMALL_FONT = pygame.font.Font(None, 22)

clock = pygame.time.Clock()


# ---------------- دوال منطق اللعبة (مبنية على كودك) ----------------

def create_board():
    """إنشاء لوحة كقاموس من 1 إلى 9 مثل كودك."""
    return {i: '' for i in range(1, 10)}

def is_space_free(board, position):
    """فحص هل الخانة فاضية أم لا."""
    return board[position] == ''

def check_for_win(board):
    """فحص الفوز (نفس winning_position في كودك)."""
    winning_position = [
        (1,2,3),(4,5,6),(7,8,9),
        (1,4,7),(2,5,8),(3,6,9),
        (1,5,9),(3,5,7)
    ]
    for pos in winning_position:
        if (board[pos[0]] == board[pos[1]] == board[pos[2]]
            and board[pos[0]] != ''):
            return board[pos[0]]   # 'X' أو 'O'
    return None

def check_for_draw(board):
    """فحص التعادل: كل الخانات ليست فارغة."""
    return all(board[pos] != '' for pos in board.keys())

# تحويل بين position (1-9) و (row, col)
def pos_to_row_col(pos):
    idx = pos - 1
    row = idx // 3
    col = idx % 3
    return row, col

def row_col_to_pos(row, col):
    return row * 3 + col + 1

# -------- Minimax (Hard AI logic) --------
def minimax(board, is_maximizer):
    """خوارزمية Minimax: ترجع قيمة تقييم اللوحة للـ X."""
    winner = check_for_win(board)
    if winner == 'X':
        return 1
    elif winner == 'O':
        return -1
    elif check_for_draw(board):
        return 0

    if is_maximizer:
        best_score = -float('inf')
        for pos in board.keys():
            if is_space_free(board, pos):
                board[pos] = 'X'
                score = minimax(board, False)
                board[pos] = ''
                best_score = max(score, best_score)
    else:
        best_score = float('inf')
        for pos in board.keys():
            if is_space_free(board, pos):
                board[pos] = 'O'
                score = minimax(board, True)
                board[pos] = ''
                best_score = min(score, best_score)
    return best_score

def ai_hard_move(board):
    """
    Hard AI: تختار أفضل حركة للـ X باستخدام Minimax.
    (هذه كانت best_move، الآن اسمها واضح على أنها Hard AI)
    """
    move = None
    best_score = -float('inf')
    for pos in board.keys():
        if is_space_free(board, pos):
            board[pos] = 'X'
            score = minimax(board, False)
            board[pos] = ''
            if score > best_score:
                best_score = score
                move = pos
    return move


# -------- Easy AI: اختيار عشوائي من الخانات الفارغة --------
def ai_easy_move(board):
    free_positions = [pos for pos in board.keys() if is_space_free(board, pos)]
    if not free_positions:
        return None
    return random.choice(free_positions)

# -------- Medium AI: يحاول يفوز أو يمنع اللاعب --------
def ai_medium_move(board):
    free_positions = [pos for pos in board.keys() if is_space_free(board, pos)]

    # 1) لو X يقدر يفوز الآن
    for pos in free_positions:
        board[pos] = 'X'
        if check_for_win(board) == 'X':
            board[pos] = ''
            return pos
        board[pos] = ''

    # 2) لو O يقدر يفوز بالحركة الجاية → نمنعه
    for pos in free_positions:
        board[pos] = 'O'
        if check_for_win(board) == 'O':
            board[pos] = ''
            return pos
        board[pos] = ''

    # 3) غير ذلك → عشوائي
    return ai_easy_move(board)


# ---------------- الرسم ----------------

def draw_grid():
    screen.fill(WHITE)
    # خطوط عمودية
    for c in range(1, COLS):
        x = BOARD_X + c * CELL_SIZE
        pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, CELL_SIZE * ROWS), 3)
    # خطوط أفقية
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
            pygame.draw.line(screen, X_COLOR,
                             (cx - offset, cy - offset),
                             (cx + offset, cy + offset), 3)
            pygame.draw.line(screen, X_COLOR,
                             (cx - offset, cy + offset),
                             (cx + offset, cy - offset), 3)
        else:  # 'O'
            pygame.draw.circle(screen, O_COLOR, (cx, cy), 30, 3)

def draw_status_text(mode, current_player, game_over, winner):
    bar_rect = pygame.Rect(0, 300, WIDTH, HEIGHT - 300)
    pygame.draw.rect(screen, (245, 245, 245), bar_rect)
    pygame.draw.rect(screen, GRAY, bar_rect, 1)

    # الرسالة الرئيسية
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

    text = FONT.render(main_text, True, BLACK)
    screen.blit(text, text.get_rect(center=(WIDTH // 2, 320)))

    # وضع اللعب
    if mode == "HvH":
        mode_txt = "Mode: Human vs Human"
    elif mode == "AI_E":
        mode_txt = "Mode: Human vs Easy AI (Random)"
    elif mode == "AI_M":
        mode_txt = "Mode: Human vs Medium AI"
    elif mode == "AI_H":
        mode_txt = "Mode: Human vs Hard AI (Minimax)"
    else:
        mode_txt = ""

    hint = SMALL_FONT.render("R: Restart  |  ESC: Quit", True, (80, 80, 80))
    mode_text = SMALL_FONT.render(mode_txt, True, (50, 50, 50))

    screen.blit(hint,      hint.get_rect(center=(WIDTH // 2, 350)))
    screen.blit(mode_text, mode_text.get_rect(center=(WIDTH // 2, 380)))


# ---------------- شاشة الـ Menu ----------------

def menu_screen():
    mode = None
    choosing = True
    while choosing:
        screen.fill(WHITE)

        title = FONT.render("Tic Tac Toe - Part 1", True, BLACK)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 60)))

        t1 = SMALL_FONT.render("1 - Human vs Human",             True, BLACK)
        t2 = SMALL_FONT.render("2 - Human vs Easy AI (Random)",  True, BLACK)
        t3 = SMALL_FONT.render("3 - Human vs Medium AI",         True, BLACK)
        t4 = SMALL_FONT.render("4 - Human vs Hard AI (Minimax)", True, BLACK)
        screen.blit(t1, (40, 120))
        screen.blit(t2, (40, 150))
        screen.blit(t3, (40, 180))
        screen.blit(t4, (40, 210))

        hint = SMALL_FONT.render("Choose mode (1-4)  |  ESC to Quit",
                                 True, (80, 80, 80))
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 260)))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_1:
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


# ---------------- الحلقة الرئيسية ----------------

def main():
    mode = menu_screen()
    board = create_board()
    current_player = 'X'   # في أوضاع AI: X = AI, O = Human
    game_over = False
    winner = None

    running = True
    while running:
        clock.tick(60)

        # ----- دور الـ AI في أوضاع AI -----
        if (not game_over) and (mode in ("AI_E", "AI_M", "AI_H")) and current_player == 'X':
            pygame.time.delay(200)
            if mode == "AI_E":
                pos = ai_easy_move(board)
            elif mode == "AI_M":
                pos = ai_medium_move(board)
            else:  # AI_H
                pos = ai_hard_move(board)

            if pos is not None and is_space_free(board, pos):
                board[pos] = 'X'
                w = check_for_win(board)
                if w is not None:
                    winner = w
                    game_over = True
                elif check_for_draw(board):
                    winner = None
                    game_over = True
                else:
                    current_player = 'O'

        # ----- الأحداث -----
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
                # داخل البورد فقط
                if 0 <= y < CELL_SIZE * ROWS and BOARD_X <= x < BOARD_X + BOARD_SIZE:
                    col = (x - BOARD_X) // CELL_SIZE
                    row = y // CELL_SIZE
                    pos = row_col_to_pos(row, col)

                    if is_space_free(board, pos):
                        if mode == "HvH":
                            # X و O بشريين
                            board[pos] = current_player
                            w = check_for_win(board)
                            if w is not None:
                                winner = w
                                game_over = True
                            elif check_for_draw(board):
                                winner = None
                                game_over = True
                            else:
                                current_player = 'O' if current_player == 'X' else 'X'
                        else:
                            # أوضاع AI: اللاعب هو O فقط
                            if current_player == 'O':
                                board[pos] = 'O'
                                w = check_for_win(board)
                                if w is not None:
                                    winner = w
                                    game_over = True
                                elif check_for_draw(board):
                                    winner = None
                                    game_over = True
                                else:
                                    current_player = 'X'

        # ----- الرسم -----
        draw_grid()
        draw_marks(board)
        draw_status_text(mode, current_player, game_over, winner)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
