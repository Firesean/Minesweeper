import tkinter as tk
from tkinter import messagebox

class Interface:
    LINE_WIDTH = 3
    LOST_TEXT = "YOU LOSE"
    TIMER = 1000
    U_FLAG = u"\u2691"
    U_BOMB = u"\u2699"
    WON_TEXT = "YOU WIN"
    menu = None
    new_game_menu = None
    bombs_menu = None
    board_size_menu = None
    colors = ["black", "blue", "green", "red", "purple", "maroon", "turquoise", "black", "gray"]

    def __init__(self, root, window_size, game, icon_path):
        self.root = root
        self.window_size = window_size
        self.game = game
        self.spacer = lambda : int(self.window_size / self.game.board_size)
        self.canvas = tk.Canvas(self.root, width=self.window_size, height=self.window_size)
        self.icon_path = icon_path
        self.font_style = f"TimesNewRoman {0} bold".format(self.spacer())

        # Main
        self.set_up_interface()
        self.root.mainloop()
# Interface Setup


    def default_window(self):
        self.root.bind("<Button-1>", lambda event: self.reveal_cell(event))
        self.root.bind("<Button-3>", lambda event: self.check_cell(event))
        self.root.geometry("{0}x{0}".format(self.window_size+self.spacer())) # Window Size
        self.root.title("{}".format(type(self.game).__name__)) # Window Title
        self.root.iconbitmap("{}".format(self.icon_path)) # Icon Picture
        self.root.resizable(width=False, height=False) # Cannot be resize

    def set_up_interface(self):
        self.default_window()
        self.create_menu()
        self.update_interface()

    def set_bombs(self, bombs):
        self.game.set_total_bombs(bombs)

    def set_board_size(self, board_size):
        self.game.set_board_size(board_size)

    def create_menu(self):
        self.menu = tk.Menu(self.root, tearoff=0)
        self.new_game_menu = tk.Menu(self.root, tearoff=0)
        self.bombs_menu = tk.Menu(self.root, tearoff=0)
        self.board_size_menu = tk.Menu(self.root, tearoff=0)
        # Set Up Menu Items
        for amount in range(10,31,5): # Start from 10 not including 31 we go by 5's # Issue Prints 30 for all and Bombs doesnt work
            self.bombs_menu.add_command(label="Bombs : {}".format(amount), command=lambda x=amount: self.set_bombs(x))
            self.board_size_menu.add_command(label="Board Size : {}".format(amount), command=lambda x = amount: self.set_board_size(x))
        # Place Menu Items
        self.menu.add_command(label="New Game", command=self.new_game)
        self.menu.add_cascade(label="Select Bombs", menu=self.bombs_menu)
        self.menu.add_cascade(label="Set Board Size", menu=self.board_size_menu)
        self.menu.add_command(label="Exit", command=self.root.quit)
        self.root.config(menu=self.menu)

    def draw_lines(self):
        for lines_over in range(0, len(self.game.board)):
            line_pos = lines_over * self.spacer()
            self.canvas.create_line(line_pos, 0, line_pos, self.window_size, width=self.LINE_WIDTH) # Vertical V ^
            self.canvas.create_line(0, line_pos, self.window_size, line_pos, width=self.LINE_WIDTH) # Horizontal
        self.canvas.create_rectangle(2, 2, self.window_size, self.window_size, width=self.LINE_WIDTH)

    def draw_board(self):
        for row in self.game.board:
            for cell in row:
                if cell.is_flagged():
                    _text = self.U_FLAG
                    clr = "black"
                elif not cell.is_revealed():
                    continue
                elif cell.is_bomb():
                    _text = self.U_BOMB
                    clr = "black"
                else:
                    _text = cell.bombs_around
                    clr = self.colors[_text]
                self.canvas.create_text(cell.x_pos * self.spacer() + (self.spacer()/2),
                                        cell.y_pos * self.spacer() + (self.spacer()/2),
                                        text=_text, font=self.font_style, fill=clr)
# Update Information
    def update_interface(self):
        self.canvas.destroy()
        self.canvas = tk.Canvas(self.root, width=self.window_size, height=self.window_size)
        self.canvas.place(relx=.5, rely=.52, anchor=tk.CENTER)
        smiley = tk.Button(self.root, text=u"\u263A", font=self.font_style,
                           height=0, width=0, bg="yellow", command=lambda : self.new_game())
        smiley.place(relx=.48, y=0)
        self.draw_lines()
        self.draw_board()
        self.check_game()

    def check_game(self):
        if self.game.get_game_lost():
            self.display_big_text(self.LOST_TEXT, "red")
        elif self.game.get_game_won():
            self.display_big_text(self.WON_TEXT, "green")

    def reveal_cell(self, event=None):
        if event:
            x, y = event.x, event.y
            offset = self.spacer() / 2
            if x < offset or y < offset: # Makes sure you are on the board interface
                return
        row = int(event.x / self.spacer())
        col = int(event.y / self.spacer())
        self.game.reveal_cell(row, col)
        self.update_interface()

    def check_cell(self, event=None):
        if event:
            x, y = event.x, event.y
            offset = self.spacer() / 2
            if x < offset or y < offset: # Makes sure you are on the board interface
                return
        row = int(event.x / self.spacer())
        col = int(event.y / self.spacer())
        self.game.flag_cell(row, col)
        self.update_interface()
# Resets
    def new_game(self): # New Game
        self.game.start_game()
        self.update_interface()

    def display_big_text(self, text, color): # Display Text
        pos = self.window_size/2
        self.canvas.create_text(pos, pos, text=text, fill=color, font="TimeNewsRoman {} bold".format(self.spacer()))
        messagebox.showinfo(type(self.game).__name__, text)
        self.new_game()

