from random import *
from Cell import *

class Minesweeper:

    def __init__(self, size=10, bombs=8):
        # Values
        self.board = []
        self.board_size = size
        self.bombs = bombs
        self.game_lost = False
        self.game_won = False
        # Main
        self.start_game()
# Game Information / Resets
    def start_game(self): # New Game
        self.game_won = False
        self.game_lost = False
        self.new_board()
        self.place_bombs()
        self.set_bombs_around()

    def get_game_won(self):
        return self.game_won

    def get_game_lost(self):
        return self.game_lost

    def new_board(self):  # Resets Board / New Board
        self.board = []
        for x in range(0, self.board_size):
            self.board.append([])
            for y in range(0, self.board_size):
                self.board[x].append(Cell(x, y))

    def is_loser(self): # Checks for bomb revealed
        for row in self.board:
            for cell in row:
                if cell.is_revealed() and cell.is_bomb():
                    self.game_lost = True
                    return True
        return False

    def is_winner(self):  # Checks board for all revealed except bombs
        for row in self.board:
            for cell in row:
                if not cell.is_bomb() and not cell.is_revealed():  # If not Bomb and not revealed yet
                    return False
        self.game_won = True
        return True

    def reveal_all_cells(self): # Reveal all and display
        for row in self.board:
            for cell in row:
                cell.set_revealed()

    def set_board_size(self, length):
        self.board_size = length

# Bombs Related

    def set_total_bombs(self, bombs_total):
        self.bombs = bombs_total

    def set_bombs_around(self):  # Determines bombs around cells
        for row in range(0, len(self.board)): # Row
            for col in range(0, len(self.board)): # Col
                if self.board[row][col].is_bomb():
                    self.add_around_bomb(row, col)

    def add_around_bomb(self, row, col): # Cells around get one more bomb around
        for x in range(-1,2):
            for y in range(-1, 2):
                cell = self.get_cell(row+x, col+y)
                if cell:
                    cell.add_bomb_around()

    def place_bombs(self):  # Randomly sets bombs
        for i in range(self.bombs):
            while True:
                index_x, index_y = randint(0, len(self.board)-1), randint(0, len(self.board)-1)
                if not self.board[index_x][index_y].is_bomb():
                    self.board[index_x][index_y].set_bomb()
                    break
# Cells Related
    def different_cell(self, cell_1, cell_2): # Determines separate cells
        if isinstance(cell_2, Cell) and (cell_1.x_pos, cell_1.y_pos) != (cell_2.x_pos, cell_2.y_pos):
            return True
        return False

    def on_board(self, x , y): # On the board
        if len(self.board) > x > -1 and len(self.board) > y > -1:
            return True
        return False

    def reveal_cell(self, row, col):  # Sets it revealed
        if not self.on_board(row, col):
            return
        self.board[row][col].set_revealed()
        if self.board[row][col].get_bombs_around() == 0:
            for x in range(-1,2):
                for y in range(-1,2):
                    if self.on_board(row+x, col+y):
                        if not self.board[row+x][col+y].is_revealed():
                            if self.different_cell(self.get_cell(row, col), self.get_cell(row + x, col + y)):
                                self.reveal_cell(row + x, col + y)
        if self.is_loser() or self.is_winner():
            self.reveal_all_cells()

    def flag_cell(self, row, col): # Sets cell flag
        if not self.on_board(row, col):
            return
        self.board[row][col].set_flagged()

    def get_cell(self, x, y):  # Returns the cell class
        if self.on_board(x,y):
            return self.board[x][y]
