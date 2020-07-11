import Minesweeper as Game
import Interface
import tkinter as tk

fire_icon = r"FireIcon32x32.ico"
game = Game.Minesweeper()
root = tk.Tk()
display = Interface.Interface(root, 750, game, fire_icon)
