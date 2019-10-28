class Cell:

    def __init__(self, x , y):
        self.a_bomb = False
        self.bombs_around = 0
        self.revealed = False
        self.flagged = False
        self.x_pos = x
        self.y_pos = y

    def is_flagged(self):
        return self.flagged

    def set_flagged(self):
        if not self.revealed and not self.is_flagged():
            self.flagged = True
        else:
            self.flagged = False

    def is_bomb(self):  # Returns if bomb
        return self.a_bomb

    def get_bombs_around(self): # Returns bombs around cell
        return self.bombs_around

    def set_bomb(self): # Sets Bomb
        self.a_bomb = True

    def add_bomb_around(self):
        self.bombs_around += 1

    def set_revealed(self):  # Sets revealed
        self.flagged = False
        self.revealed = True

    def is_revealed(self): # Returns is revealed
        return self.revealed
