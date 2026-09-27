import os
import tkinter as tk
from tkinter import *
def __init__(self, name, age):
    self.name = name
    self.age = age
    self.tk = tk.Tk()
    self.tk.atributes('-fullscreen', True)
    self.width = self.tk.winfo_screenwidth()
    self.height = self.tk.winfo_screenheight()
    
if __name__ == "__main__":
    game = Game()
    game.tk.mainloop()
    print(self.width, self.height)