import pygame
import random
import math


pygame.init()

#audio
pygame.mixer.music.load("HW3-Task1-sound.mp3")
pygame.mixer.music.play(-1)

FONT = pygame.font.Font(None, 25)
BIG_FONT = pygame.font.Font(None, 35)

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 720
BOARD_SIZE = 720
PANEL_WIDTH = WINDOW_WIDTH - BOARD_SIZE

# colors
LIGHT_SQUARE = (238, 238, 210)
DARK_SQUARE  = (118, 150,  86)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
Orange = (255, 165, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
RED = (200, 0, 0)
QUEEN_COLOR = (40, 40, 40)

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("N Queens Local Search Visualizer")


# N Queens Core Logic

def compute_h(board):
    """Number of attacking pairs of queens"""
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j]:
                conflicts += 1
            if abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts


def random_board(n):
    """Random board: one queen per column random row"""
    board = []
    for i in range(n):
        row = random.randrange(n)
        board.append(row)
    return board


def generate_all_neighbors(board):
    """Generate all neighbors by moving one queen in one column"""
    neighbors = []
    n = len(board)
    for col in range(n):
        old_row = board[col]
        for new_row in range(n):
            if new_row == old_row:
                continue
            new_board = board[:]
            new_board[col] = new_row
            h_neighbor = compute_h(new_board)
            neighbors.append((new_board, col, old_row, new_row, h_neighbor))
    return neighbors


def classify_move(h_old, h_new):
    if h_new < h_old:
        return "improved"
    elif h_new == h_old:
        return "sideways"
    else:
        return "worse"


# Step functions for the 5 algorithms

def step_simple_hc(board, algo_state):
    """Simple Hill Climbing: first strictly better neighbor"""
    h_current = compute_h(board)
    if h_current == 0:
        return board, None, None, True, algo_state

    for new_board, col, old_row, new_row, h_neighbor in generate_all_neighbors(board):
        if h_neighbor < h_current:
            move_type = classify_move(h_current, h_neighbor)
            finished = (h_neighbor == 0)
            return new_board, (col, old_row, new_row), move_type, finished, algo_state

    # no improving neighbor: local minimum
    return board, None, None, True, algo_state


def step_steepest_hc(board, algo_state):
    """Steepest Ascent HC: evaluate all neighbors move to the one with lowest h"""
    h_current = compute_h(board)
    if h_current == 0:
        return board, None, None, True, algo_state

    best_board = None
    best_move = None
    best_h = h_current

    for new_board, col, old_row, new_row, h_neighbor in generate_all_neighbors(board):
        if h_neighbor < best_h:
            best_h = h_neighbor
            best_board = new_board
            best_move = (col, old_row, new_row)

    if best_board is not None and best_h < h_current:
        move_type = classify_move(h_current, best_h)
        finished = (best_h == 0)
        return best_board, best_move, move_type, finished, algo_state

    # no better neighbor: stuck
    return board, None, None, True, algo_state


def step_stochastic_hc(board, algo_state):
    """Stochastic HC: randomly pick one move from among improving neighbors"""
    h_current = compute_h(board)
    if h_current == 0:
        return board, None, None, True, algo_state

    improving = []
    for new_board, col, old_row, new_row, h_neighbor in generate_all_neighbors(board):
        if h_neighbor < h_current:
            improving.append((new_board, col, old_row, new_row, h_neighbor))

    if not improving:
        # no improving neighbors: local minimum
        return board, None, None, True, algo_state

    new_board, col, old_row, new_row, h_neighbor = random.choice(improving)
    move_type = classify_move(h_current, h_neighbor)
    finished = (h_neighbor == 0)
    move = (col, old_row, new_row)
    return new_board, move, move_type, finished, algo_state


def step_random_restart_hc(board, algo_state):
    """Random Restart Hill Climbing based on steepest ascent HC"""
    n = len(board)
    if "restart_count" not in algo_state:
        algo_state["restart_count"] = 0
        algo_state["max_restarts"] = 50

    h_current = compute_h(board)
    if h_current == 0:
        return board, None, None, True, algo_state

    best_board = None
    best_move = None
    best_h = h_current

    for new_board, col, old_row, new_row, h_neighbor in generate_all_neighbors(board):
        if h_neighbor < best_h:
            best_h = h_neighbor
            best_board = new_board
            best_move = (col, old_row, new_row)

    if best_board is not None and best_h < h_current:
        move_type = classify_move(h_current, best_h)
        finished = (best_h == 0)
        return best_board, best_move, move_type, finished, algo_state

    # no better neighbor: restart
    algo_state["restart_count"] += 1
    if algo_state["restart_count"] > algo_state["max_restarts"]:
        return board, None, None, True, algo_state

    new_board = random_board(n)
    # restart is not a move on the board so don’t highlight a square
    return new_board, None, None, False, algo_state


def step_simulated_annealing(board, algo_state):
    """One step of Simulated Annealing"""
    if "T" not in algo_state:
        algo_state["T"] = 10.0
        algo_state["T_min"] = 0.01
        algo_state["alpha"] = 0.99

    T = algo_state["T"]
    h_current = compute_h(board)

    if h_current == 0 or T < algo_state["T_min"]:
        return board, None, None, True, algo_state

    n = len(board)
    col = random.randrange(n)
    old_row = board[col]
    possible_rows = [r for r in range(n) if r != old_row]
    new_row = random.choice(possible_rows)

    new_board = board[:]
    new_board[col] = new_row
    h_new = compute_h(new_board)

    delta = h_current - h_new
    accept = False
    if delta > 0:
        accept = True
    else:
        probability = math.exp(delta / T)
        if random.random() < probability:
            accept = True

    move = None
    move_type = None
    if accept:
        move_type = classify_move(h_current, h_new)
        move = (col, old_row, new_row)
        board = new_board

    algo_state["T"] = T * algo_state["alpha"]
    finished = (compute_h(board) == 0 or algo_state["T"] < algo_state["T_min"])
    return board, move, move_type, finished, algo_state




class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, surface, active=False):
        if active:
            color = Orange

        else:
            color = (200, 200, 200)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        if self.text:
            text_surf = FONT.render(self.text, True, BLACK)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Dropdown:
    def __init__(self, x, y, w, h, options, start_index=0, label="N"):
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options
        self.selected_index = start_index
        self.open = False
        self.label = label

        self.arrow_w = 28

    @property
    def value(self):
        return self.options[self.selected_index]

    def draw(self, surface):
        # main box
        pygame.draw.rect(surface, (210, 180, 140), self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        text_str = f"{self.label} = {self.value}"
        text_surf = FONT.render(text_str, True, BLACK)
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 8, self.rect.centery))
        surface.blit(text_surf, text_rect)

        arrow_rect = pygame.Rect(
            self.rect.right - self.arrow_w,
            self.rect.y,
            self.arrow_w,
            self.rect.height
        )

        pygame.draw.line(surface, BLACK, (arrow_rect.x, arrow_rect.y),
                         (arrow_rect.x, arrow_rect.bottom), 2)

        up_rect = pygame.Rect(arrow_rect.x, arrow_rect.y, arrow_rect.width, arrow_rect.height // 2)
        down_rect = pygame.Rect(arrow_rect.x, arrow_rect.y + arrow_rect.height // 2,
                                arrow_rect.width, arrow_rect.height - arrow_rect.height // 2)

        up_cx = up_rect.centerx
        up_cy = up_rect.centery
        pygame.draw.polygon(surface, BLACK, [
            (up_cx, up_cy - 6),
            (up_cx - 6, up_cy + 3),
            (up_cx + 6, up_cy + 3)
        ])

        down_cx = down_rect.centerx
        down_cy = down_rect.centery
        pygame.draw.polygon(surface, BLACK, [
            (down_cx - 6, down_cy - 3),
            (down_cx + 6, down_cy - 3),
            (down_cx, down_cy + 6)
        ])

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            arrow_rect = pygame.Rect(
                self.rect.right - self.arrow_w,
                self.rect.y,
                self.arrow_w,
                self.rect.height
            )

            up_rect = pygame.Rect(arrow_rect.x, arrow_rect.y, arrow_rect.width, arrow_rect.height // 2)
            down_rect = pygame.Rect(arrow_rect.x, arrow_rect.y + arrow_rect.height // 2,
                                    arrow_rect.width, arrow_rect.height - arrow_rect.height // 2)

            if up_rect.collidepoint(pos):
                if self.selected_index > 0:
                    self.selected_index -= 1
                    return self.value
                return None

            if down_rect.collidepoint(pos):
                if self.selected_index < len(self.options) - 1:
                    self.selected_index += 1
                    return self.value
                return None

        return None



def draw_board(surface, board, last_move, last_move_type):
    n = len(board)
    cell_size = BOARD_SIZE // n

    # squares
    for row in range(n):
        for col in range(n):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            if (row + col) % 2 == 0:
                color = LIGHT_SQUARE
            else:
                color = DARK_SQUARE
            pygame.draw.rect(surface, color, rect)

    # highlight last move
    if last_move is not None and last_move_type is not None:
        col, old_row, new_row = last_move
        if last_move_type == "improved":
            highlight_color = GREEN
        elif last_move_type == "sideways":
            highlight_color = YELLOW
        else:
            highlight_color = RED

        old_rect = pygame.Rect(col * cell_size, old_row * cell_size, cell_size, cell_size)
        new_rect = pygame.Rect(col * cell_size, new_row * cell_size, cell_size, cell_size)
        pygame.draw.rect(surface, highlight_color, old_rect, 4)
        pygame.draw.rect(surface, highlight_color, new_rect, 4)

    # queens
    for col in range(len(board)):
        row = board[col]
        cx = col * cell_size + cell_size // 2
        cy = row * cell_size + cell_size // 2
        radius = int(cell_size * 0.3)
        pygame.draw.circle(surface, QUEEN_COLOR, (cx, cy), radius)


def draw_info_panel(surface, board, algo_name, h_value, algo_state, last_move_type, finished):
    x = BOARD_SIZE
    surface.fill(WHITE, (x, 0, PANEL_WIDTH, WINDOW_HEIGHT))

    title = BIG_FONT.render("Local Search N Queens", True, BLACK)
    surface.blit(title, (x + 20, 10))

    # info block
    y = 60
    surface.blit(FONT.render(f"Current h = {h_value}", True, BLACK), (x + 20, y))
    y += 25

    if algo_name == "sa":
        T = algo_state.get("T", 0.0)
        surface.blit(FONT.render(f"Temperature T = {T:.3f}", True, BLACK), (x + 20, y))
    else:
        surface.blit(FONT.render("Temperature T = -", True, BLACK), (x + 20, y))
    y += 25

    if algo_name == "restart":
        rc = algo_state.get("restart_count", 0)
        surface.blit(FONT.render(f"Restarts = {rc}", True, BLACK), (x + 20, y))
    else:
        surface.blit(FONT.render("Restarts = -", True, BLACK), (x + 20, y))
    y += 25

    if last_move_type is not None:
        mv_text = last_move_type 

    else:
        mv_text = "None"

    surface.blit(FONT.render(f"Last move type: {mv_text}", True, BLACK), (x + 20, y))
    y += 25

    if finished:
        status = "Finished" 
    else:
        status = "Ready"
    surface.blit(FONT.render(f"Status: {status}", True, BLACK), (x + 20, y))


def main():
    clock = pygame.time.Clock()

    # N dropdown
    N_options = [4, 6, 8, 10]
    dropdown_N = Dropdown(BOARD_SIZE + 20, 230, 150, 30, N_options, start_index=1)
    N = dropdown_N.value
    board = [0] * N
    initial_board = board[:]

    current_algo = "simple"
    algo_state = {}
    finished = False
    last_move = None
    last_move_type = None
    auto_run = False

    x = BOARD_SIZE + 20
    btn_width = PANEL_WIDTH - 40
    btn_height = 35
    gap = 10

    # Under dropdown
    y_controls = 280
    btn_randomize   = Button(x, y_controls,                          btn_width, btn_height, "Randomize")
    btn_start_pause = Button(x, y_controls + (btn_height + gap),     btn_width, btn_height, "Start")
    btn_step        = Button(x, y_controls + 2 * (btn_height + gap), btn_width, btn_height, "Step")
    btn_reset       = Button(x, y_controls + 3 * (btn_height + gap), btn_width, btn_height, "Reset")

    # Algorithm section
    y_algo_label = y_controls + 4 * (btn_height + gap) + 20
    algo_label_pos = (x + 20, y_algo_label)

    y_algo_buttons = y_algo_label + 25
    algo_specs = [
        ("simple",    "Simple Hill Climbing"),
        ("steepest",  "Steepest-Ascent HC"),
        ("stochastic","Stochastic HC"),
        ("restart",   "Random-Restart HC"),
        ("sa",        "Simulated Annealing"),
    ]

    algo_buttons = []
    for i in range(len(algo_specs)):
        key = algo_specs[i][0]
        label = algo_specs[i][1]
        btn_y = y_algo_buttons + i * (btn_height + gap)
        btn = Button(x, btn_y, btn_width, btn_height, label)
        algo_buttons.append((key, btn))


    def reset_algo_state():
        nonlocal algo_state, finished, last_move, last_move_type
        algo_state = {}
        finished = False
        last_move = None
        last_move_type = None

    def capture_initial_board():
        nonlocal initial_board
        initial_board = board[:]

    def change_N(new_N):
        nonlocal N, board, auto_run
        N = new_N
        board = [0] * N
        auto_run = False
        reset_algo_state()
        capture_initial_board()

    def randomize_board():
        nonlocal board, auto_run
        board = random_board(len(board))
        auto_run = False
        reset_algo_state()
        capture_initial_board()

    def reset_board():
        nonlocal board, auto_run
        board = initial_board[:]
        auto_run = False
        reset_algo_state()

    def step_once():
        nonlocal board, algo_state, finished, last_move, last_move_type, current_algo
        if finished:
            return
        if current_algo == "simple":
            board2, move, move_type, done, new_state = step_simple_hc(board, algo_state)
        elif current_algo == "steepest":
            board2, move, move_type, done, new_state = step_steepest_hc(board, algo_state)
        elif current_algo == "stochastic":
            board2, move, move_type, done, new_state = step_stochastic_hc(board, algo_state)
        elif current_algo == "restart":
            board2, move, move_type, done, new_state = step_random_restart_hc(board, algo_state)
        else:
            board2, move, move_type, done, new_state = step_simulated_annealing(board, algo_state)
        board = board2
        algo_state = new_state
        finished = done
        last_move = move
        last_move_type = move_type

    def toggle_auto_run():
        nonlocal auto_run
        if not auto_run:
            reset_algo_state()
            capture_initial_board()
            auto_run = True
        else:
            auto_run = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            selected_N = dropdown_N.handle_event(event)
            if selected_N is not None:
                change_N(selected_N)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos

                dd_height = dropdown_N.rect.height * (1 + (len(N_options) if dropdown_N.open else 0))
                dd_rect = pygame.Rect(dropdown_N.rect.x, dropdown_N.rect.y,
                                      dropdown_N.rect.width, dd_height)
                if dd_rect.collidepoint(pos):
                    continue

                # manual placement on board
                if pos[0] < BOARD_SIZE and pos[1] < BOARD_SIZE:
                    n = len(board)
                    cell_size = BOARD_SIZE // n
                    col = pos[0] // cell_size
                    row = pos[1] // cell_size
                    if 0 <= col < n and 0 <= row < n:
                        board[col] = row
                        auto_run = False
                        reset_algo_state()
                        capture_initial_board()
                else:
                    if btn_randomize.is_clicked(pos):
                        randomize_board()
                    elif btn_start_pause.is_clicked(pos):
                        toggle_auto_run()
                    elif btn_step.is_clicked(pos):
                        auto_run = False
                        step_once()
                    elif btn_reset.is_clicked(pos):
                        reset_board()
                    else:
                        for key, btn in algo_buttons:
                            if btn.is_clicked(pos):
                                current_algo = key
                                auto_run = False
                                reset_algo_state()
                                break

        if auto_run:
            if not finished:
                step_once()
            else:
                auto_run = False

        # drawing
        SCREEN.fill(WHITE)
        h_value = compute_h(board)

        draw_board(SCREEN, board, last_move, last_move_type)
        draw_info_panel(SCREEN, board, current_algo, h_value, algo_state, last_move_type, finished)

        # Board size label
        panel_x = BOARD_SIZE
        SCREEN.blit(FONT.render("Board size (N):", True, BLACK), (panel_x + 20, 205))

        # Control buttons
        btn_start_pause.text = "Pause" if auto_run and not finished else "Start"
        btn_randomize.draw(SCREEN)
        btn_start_pause.draw(SCREEN)
        btn_step.draw(SCREEN)
        btn_reset.draw(SCREEN)

        # Algorithm label and buttons
        SCREEN.blit(FONT.render("Algorithm:", True, BLACK), algo_label_pos)
        for key, btn in algo_buttons:
            btn.draw(SCREEN, active=(key == current_algo))

        dropdown_N.draw(SCREEN)

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


main()