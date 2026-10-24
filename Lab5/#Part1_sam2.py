#Part1_sam2

import pygame
import sys
import random

pygame.init()

# ===================== إعداد النافذة و الألوان =====================
WIDTH, HEIGHT = 300, 380      # 300x300 للوحة + شريط تحت للنص
CELL_SIZE = 100
ROWS, COLS = 3, 3

WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GRAY   = (200, 200, 200)
LINE_COLOR = (0, 150, 200)
X_COLOR    = (255, 80, 80)
O_COLOR    = (80, 160, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - X and O")

FONT       = pygame.font.Font(None, 32)
SMALL_FONT = pygame.font.Font(None, 22)

clock = pygame.time.Clock()

# ===================== حالة اللعبة =====================
# board: 0 = فاضي، 1 = X، -1 = O
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
current_player = 1         # 1 = X (البشر)، -1 = O (بشر أو AI)
game_over = False
winner = None              # 1 أو -1 أو 0 للتعادل

# mode:
# "HvH"    → Human vs Human
# "AI_E"   → Human vs Easy AI
# "AI_M"   → Human vs Medium AI
# "AI_H"   → Human vs Hard AI (Minimax)
mode = None


# ===================== دوال مساعدة =====================
def reset_game():
    """إعادة تعيين اللوحة و المتغيرات."""
    global board, current_player, game_over, winner
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    current_player = 1
    game_over = False
    winner = None


def draw_grid():
    """رسم الشبكة (3x3)."""
    screen.fill(WHITE)
    # خطوط عمودية
    for c in range(1, COLS):
        x = c * CELL_SIZE
        pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, 300), 3)
    # خطوط أفقية
    for r in range(1, ROWS):
        y = r * CELL_SIZE
        pygame.draw.line(screen, LINE_COLOR, (0, y), (300, y), 3)


def draw_marks():
    """رسم X و O في الخلايا."""
    for r in range(ROWS):
        for c in range(COLS):
            val = board[r][c]
            cx = c * CELL_SIZE + CELL_SIZE // 2
            cy = r * CELL_SIZE + CELL_SIZE // 2

            if val == 1:  # X
                offset = 30
                pygame.draw.line(screen, X_COLOR,
                                 (cx - offset, cy - offset),
                                 (cx + offset, cy + offset), 3)
                pygame.draw.line(screen, X_COLOR,
                                 (cx - offset, cy + offset),
                                 (cx + offset, cy - offset), 3)
            elif val == -1:  # O
                pygame.draw.circle(screen, O_COLOR, (cx, cy), 30, 3)


def check_winner_state(b):
    """
    تفحص حالة اللوحة:
    ترجع  1  لو فاز X
    ترجع -1 لو فاز O
    ترجع  0  لو تعادل
    ترجع None لو لسه ما انتهت.
    """
    # صفوف
    for r in range(ROWS):
        s = sum(b[r])
        if s == 3:
            return 1
        if s == -3:
            return -1

    # أعمدة
    for c in range(COLS):
        s = b[0][c] + b[1][c] + b[2][c]
        if s == 3:
            return 1
        if s == -3:
            return -1

    # قطريات
    d1 = b[0][0] + b[1][1] + b[2][2]
    d2 = b[0][2] + b[1][1] + b[2][0]
    if d1 == 3 or d2 == 3:
        return 1
    if d1 == -3 or d2 == -3:
        return -1

    # تعادل؟
    if all(b[r][c] != 0 for r in range(ROWS) for c in range(COLS)):
        return 0

    return None


def update_winner():
    """تحديث قيمة winner و game_over حسب حالة اللوحة."""
    global winner, game_over
    result = check_winner_state(board)
    if result is not None:
        winner = result
        game_over = True


def draw_status_text():
    """عرض نص الحالة تحت اللوحة (الدور / النتيجة / التعليمات)."""
    bar_rect = pygame.Rect(0, 300, WIDTH, 80)
    pygame.draw.rect(screen, (245, 245, 245), bar_rect)
    pygame.draw.rect(screen, GRAY, bar_rect, 1)

    # السطر الأساسي
    if not game_over:
        if current_player == 1:
            main_text = "Turn: Player X"
        else:
            if mode == "HvH":
                main_text = "Turn: Player O"
            else:
                main_text = "Turn: AI (O)"
    else:
        if winner == 1:
            main_text = "Player X wins!"
        elif winner == -1:
            main_text = "Player O wins!" if mode == "HvH" else "AI wins!"
        else:
            main_text = "Draw!"

    text = FONT.render(main_text, True, BLACK)
    screen.blit(text, text.get_rect(center=(WIDTH // 2, 320)))

    # السطر الثاني: التعليمات و وضع اللعب
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

    hint = SMALL_FONT.render("R: Restart   ESC: Quit", True, (80, 80, 80))
    mode_text = SMALL_FONT.render(mode_txt, True, (50, 50, 50))

    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 350)))
    screen.blit(mode_text, mode_text.get_rect(center=(WIDTH // 2, 370)))


def get_empty_cells():
    """ترجع قائمة بالخلايا الفارغة (r, c)."""
    return [(r, c) for r in range(ROWS) for c in range(COLS) if board[r][c] == 0]


# ===================== الذكاء الاصطناعي =====================
# -------- Easy AI: حركات عشوائية --------
def ai_easy():
    moves = get_empty_cells()
    if not moves:
        return None
    return random.choice(moves)


# -------- Medium AI: يحاول يفوز أو يمنع الفوز --------
def ai_medium(ai_player=-1, human_player=1):
    moves = get_empty_cells()

    # 1) إذا فيه حركة تخلي AI يفوز → العبها
    for r, c in moves:
        board[r][c] = ai_player
        if check_winner_state(board) == ai_player:
            board[r][c] = 0
            return (r, c)
        board[r][c] = 0

    # 2) إذا اللاعب يقدر يفوز في الحركة الجاية → امنعه
    for r, c in moves:
        board[r][c] = human_player
        if check_winner_state(board) == human_player:
            board[r][c] = 0
            return (r, c)
        board[r][c] = 0

    # 3) غير كذا → حركة عشوائية صحيحة
    return ai_easy()


# -------- Hard AI: Minimax (لا يُهزَم) --------
def minimax(b, is_max_turn, ai_player, human_player):
    """
    خوارزمية Minimax:
    ترجع (score, move)
    score: 1  إذا مصلحة الـ AI
           -1 إذا مصلحة اللاعب
           0  تعادل
    """
    result = check_winner_state(b)
    if result is not None:
        if result == ai_player:
            return (1, None)
        elif result == human_player:
            return (-1, None)
        else:
            return (0, None)

    if is_max_turn:
        best_score = -999
        best_move = None
        for r in range(ROWS):
            for c in range(COLS):
                if b[r][c] == 0:
                    b[r][c] = ai_player
                    score, _ = minimax(b, False, ai_player, human_player)
                    b[r][c] = 0
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        return best_score, best_move
    else:
        best_score = 999
        best_move = None
        for r in range(ROWS):
            for c in range(COLS):
                if b[r][c] == 0:
                    b[r][c] = human_player
                    score, _ = minimax(b, True, ai_player, human_player)
                    b[r][c] = 0
                    if score < best_score:
                        best_score = score
                        best_move = (r, c)
        return best_score, best_move


def ai_hard(ai_player=-1, human_player=1):
    _, move = minimax(board, True, ai_player, human_player)
    return move


# ===================== شاشة اختيار الوضع (Menu) =====================
def menu_screen():
    """
    شاشة البداية:
    1 = Human vs Human
    2 = Human vs Easy AI
    3 = Human vs Medium AI
    4 = Human vs Hard AI
    """
    global mode
    choosing = True
    while choosing:
        screen.fill(WHITE)

        title = FONT.render("Tic Tac Toe - Menu", True, BLACK)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 60)))

        t1 = SMALL_FONT.render("1 - Human vs Human", True, BLACK)
        t2 = SMALL_FONT.render("2 - Human vs Easy AI", True, BLACK)
        t3 = SMALL_FONT.render("3 - Human vs Medium AI", True, BLACK)
        t4 = SMALL_FONT.render("4 - Human vs Hard AI", True, BLACK)
        screen.blit(t1, (40, 120))
        screen.blit(t2, (40, 150))
        screen.blit(t3, (40, 180))
        screen.blit(t4, (40, 210))

        hint = SMALL_FONT.render("Choose mode (1-4)  |  ESC to Quit", True, (80, 80, 80))
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


# ===================== الحلقة الرئيسية =====================
def main():
    global current_player, game_over

    # شاشة اختيار الوضع أولاً
    menu_screen()
    reset_game()

    running = True
    while running:
        clock.tick(60)

        # دور الـ AI إذا الوضع ليس HvH
        if not game_over and mode in ("AI_E", "AI_M", "AI_H") and current_player == -1:
            pygame.time.delay(200)
            if mode == "AI_E":
                move = ai_easy()
            elif mode == "AI_M":
                move = ai_medium()
            else:  # AI_H
                move = ai_hard()
            if move:
                r, c = move
                board[r][c] = -1
                update_winner()
                if not game_over:
                    current_player = 1

        # معالجة الأحداث
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    # رجوع للمنيو ثم إعادة اللعبة
                    menu_screen()
                    reset_game()

            # ضغط بالماوس → حركة اللاعب
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                if y < 300:  # داخل الشبكة
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    if board[row][col] == 0:
                        # إذا الوضع Human vs Human → كل مرّة لاعب مختلف
                        # إذا AI → X هو الإنسان (current_player لازم يكون 1)
                        if mode == "HvH" or current_player == 1:
                            board[row][col] = current_player
                            update_winner()
                            if not game_over:
                                # تبديل الدور
                                current_player *= -1

        # الرسم
        draw_grid()
        draw_marks()
        draw_status_text()
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
