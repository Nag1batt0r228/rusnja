from tkinter import *
import time 
import random 
import os
import traceback

class Main:

    def __init__(self):
        self.tk = Tk()
        self.tk.title("Proba")
        self.tk.resizable(0,0)
        self.tk.wm_attributes('-topmost', 1)
        self.canvas_height = self.tk.winfo_screenheight()
        self.canvas_width = self.tk.winfo_screenwidth()
        self.canvas = Canvas(width=self.canvas_width, height=self.canvas_height, bg ="white",highlightthickness=0)
        self.canvas.pack()
        self.sprites =[]
        self.running = True
        
    def mainloop(self):
        while 1:
            for sprite in self.sprites:
                sprite.move()
            self.tk.update_idletasks()
            self.tk.update()


class Coords:
    def __init__(self, x1 =0, x2=0, y1=0,y2=0):
        self.x1=x1
        self.x2=x2
        self.y1=y1
        self.y2=y2
def gorizont(co1, co2):

    if co1.x1 >co2.x2 and co1.x1 <co2.x2:
        return True
    elif co1.x2 >co2.x1 and co1.x2 <co2.x2:
        return True
    elif co2.x1 >co1.x1 and co2.x1 <co1.x2:
        return True
    elif co2.x2 >co1.x2 and co2.x2 <co1.x2:
        return True
    else:
           return False
def vertikall(co1, co2):
    if co1.y1 >co2.y1 and co2.y2>co1.y1:
        return True

    elif co1.y1>co2.y1 and co1.y2 <co2.y2:
        return True
    elif co2.y1>co1.y1 and co2.y1 <co1.y2:
        return True
    elif co2.y2>co1.y2 and co2.y2 <co1.y1:
        return True
    else:
        return False                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

def collid_left(co1,co2):                        #зіткнення зліва
    if vertikall(co1,co2):
        if co1.x1 <=co2.x2 and co1.x2 >=co2.x1:
             return True
        return False
def collid_right(co1,co2):
    if vertikall(co1, co2):
        if co1.x2 >= co2.x1 and co1.x2 <=co2.x2:
            return True
        return False 
def collid_top(co1,co2):
    if gorizont(co1,co2):
        if co1.y1 >=co2.y2 and co1.y2 >= co2.y1:
            return True 
        return False 
def collid_baton(y,co1,co2):
    if gorizont(co1,co2):
        y_n =co1.y2 + y
        if y_n >= co2.y1 and y_n <= co2.y2 :
            return True 
        return False 

class Sprite:
    def __init__(self, game):
        self.game = game
        self.endgame = False 
        self.coordinates= None
    def move(self):
        pass
    def coorde(self):
        return self.coordinates
    
class platformSprite(Sprite):           #####
    def __init__(self, game, photo, width, height,x, y):
        Sprite.__init__(self,game)
        self.photo =photo
        self.image = game.canvas.create_image(x,y, image = self.photo,anchor ='nw')
        self.coordinates = Coords(x,y,width +x, height +y)


class ManSprite(Sprite):
    def __init__(self, game):
        Sprite.__init__(self,game)
        self.image_left = [
            PhotoImage(file = "sickman_lf.gif"),
            PhotoImage(file = "sickman_lf2.gif"),
            PhotoImage(file = "sickman_lf2.gif")
        ]
        self.image_right = [
            PhotoImage(file = "sickman_rt.gif"),
            PhotoImage(file = "sickman_rt2.gif"),
            PhotoImage(file = "sickman_rt3.gif")
        ]
        self.image =self.game.create_image =(200,500, self.image = self.image_left, anchor ='w')

        self.x = -2
        self.y = 0
        self.current_image =0
        self.current_image_add = 1
        self.last_time = time.time()
        self.coordinates =Coords()
        self.last_dir = 'lf'



game =Main()
game.tk.mainloop()