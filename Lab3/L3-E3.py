import pygame
class GameBoard:
    def __init__(self, rows, cols, cell_size, x_offset=50, y_offset=50):
        self.rows= rows
        self.cols = cols
        self.cell_size = cell_size
        self.x_offset = x_offset
        self.y_offset = y_offset

        self.board = [[0 for col in range(self.cols)] for _ in range(self.rows)]
        self.colors = {
            "bg" : (240, 250, 240),
            "g" : (100,100,100),
            "p1" : (255,0,0),
            "p2" : (0,0,255)
        }

        self.current_player =1

    def get_cell_from_pos(self, pos):
        x,y = pos
        col = (x-self.x_offset) // self.cell_size
        row = (y-self.y_offset) // self.cell_size

        if 0<=row< self.rows and 0<=col<self.cols:
            return row,col
        return None
    
    def handle_click(self, pos):
        cell = self.get_cell_form_pos(pos)
        if cell:
            row, col =cell
            if self.board[row][col]==0:
                self.board[row][col] = self.current_player
                self.current_player = 3 - self.current_player

    def draw(self, screen):
        width = self.cols * self.cell_size
        heght = self.rows * self.cell_size

        pygame.draw.rect(screen, self.colors["bg"], self.x_offset, self.y_offset, width, heght)

        # draw the grid lines
        for row in range(self.rows+1):
            y = row * self.cell_size + self.y_offset
            pygame.draw.line(screen, self.colors["g"], (self.x_offset, y),(self.x_offset + width, y))

        for col in range(self.cols+1):
            x = col * self.cell_size + self.x_offset
            pygame.draw.line(screen, self.colors["g"], (x, self.y_offset ),(self.y_offset + width, x))


