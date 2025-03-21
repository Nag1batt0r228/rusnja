from tkinter import *
import os
import traceback
import random 
import time 

class Game:
    
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Smert' rusni")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes('-topmost', 1)
        self.canvas_height = 900#self.tk.winfo_screenheight()
        self.canvas_width = 1600#self.tk.winfo_screenmmwidth()
        self.canvas = Canvas(self.tk, width=self.canvas_width, height=self.canvas_height, bd=0, highlightthickness=0)
        self.canvas.pack()
        self.bg = PhotoImage(file = "donbas1.gif")
        #original_bg = Image.open("C:\\Users\\Zenyk\\Desktop\\rusnja\\donbas1.gif")
       # resized_bg=original_bg.resize((self.canvas_height,self.canvas_width),Image.Resampling.LANCZOS)
        #self.bg = ImageTk.PhotoImage(resized_bg)
        self.canvas.create_image(0, 0, image=self.bg, anchor='nw')
        self.sprites = []
        self.running = True

    def mainloop(self):
        while 1:
            if self.running == True:
                for sprite in self.sprites:
                    sprite.move()
                    #if isinstance(sprite,ManSprite):
                   #     coords = self.canvas.coords(self.image)
                    #    print("Man coords in mainloop: ",coords) 
                     #   if not coords:
                      #      print("Error: Man is lost")
                self.tk.update_idletasks()
                self.tk.update()
                time.sleep(0.01)
class Coords:
    
    def __init__(self,x1 =0,y1=0,x2=0,y2=0):
        self.x1 = x1
        self.x2=x2
        self.y1=y1
        self.y2=y2
def within_x(co1,co2):   #зіткнення горизонтально
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
        
def within_y(co1,co2):  #зіткнення вертикально
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
    if within_y(co1,co2):
         if co1.x1 <=co2.x2 and co1.x2 >=co2.x1:
             return True
         return False
     
def collid_right(co1,co2):                       #зіткнення справа
    if within_y(co1,co2):
        if co1.x2 >=co2.x1 and co1.x2<=co2.x2:
            return True 
        return False
    
def collid_top(co1,co2):                         #зіткнення зверху
    if within_x(co1,co2):
        if co1.y1 <=co2.y2 and co1.y1 >=co2.y1:
            return True
        return False
    
def collid_bottom(y,co1,co2):                      #зіткнення знизу
    if within_x(co1,co2):
             y_calc = co1.y2 + y
             if y_calc  >=co2.y1 and y_calc <=co2.y2 :
                return True
             return False
         
class Sprite:
    def __init__(self, game):
        self.game = game
        self.endgame = False 
        self.coordinates = None
    def move(self):
            pass
    def coords(self):
            return self.coordinates

class platformSprite(Sprite):
    def __init__(self, game, photo_image,width,height,x,y):
        Sprite.__init__(self,game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x,y, \
            image = self.photo_image, anchor = 'nw')
        self.coordinates = Coords(x,y,width +x,height+y)
         
class ManSprite(Sprite):
    def __init__(self, game):
    
        Sprite.__init__(self,game)
        self.image_left = [
            PhotoImage(file = "sickman_lf.gif"),
            PhotoImage(file = "sickman_lft2.gif"),
            PhotoImage(file = "sickman_lft3.gif")
        ]
        self.image_right = [
            PhotoImage(file = "sickman_rt.gif"),
            PhotoImage(file = "sickman_rt2.gif"),
            PhotoImage(file = "sickman_rt3.gif")
        ]
        '''
        try:
            self.image_staylf = (PhotoImage(file = "stay_lf.gif"))
            self.image_stayrt = (PhotoImage(file = "stay.gif"))
        except Exception as e:
            print("Error loading image:", e)
            '''
       # self.image_stayrt = PhotoImage(file = "stay.gif")
        x_spawn = 150
        y_spawn=400
        self.coordinates = Coords(x_spawn,y_spawn, x_spawn +27, y_spawn + 30)
        if x_spawn <0:
            x_spawn = 0
        elif x_spawn >self.game.canvas_width:
            x_spawn = self.game.canvas_width - 27
        if y_spawn <0:
            y_spawn = 0
        elif y_spawn >self.game.canvas_height:
            y_spawn = self.game.canvas_height - 30
        #self.image = game.canvas.create_image(x_spawn,y_spawn,\
          #  image = self.image_staylf,anchor ='nw')
        self.image = game.canvas.create_image(x_spawn,y_spawn,\
              image = self.image_left[0], anchor = 'nw')
        self.game.canvas.tag_raise(self.image)
        print ("Man created with image ID: ", self.image)
        print("Man initial coordinates: ", game.canvas.coords(self.image))
        self.x = 0
        self.y = 0
        self.current_image = 0
        self.current_image_add =1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()
        #self.last_direct = 'Left'
        
        
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)                #клавіші
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)
    def turn_left(self,evt):
        if self.y ==0:
            self.x = -2 
            #self.last_direct = 'Left'
            
    def turn_right(self,evt):
        if self.y ==0:
            self.x = 2
            #self.last_direct ='Right'
    def jump(self,evt):
        if self.y ==0:
            self.y= -4
            self.jump_count=0
    def animated(self):            #REMEMBER!     #movement animation
        if self.x !=0 and self.y ==0:
            if time.time() - self.last_time >0.1:
                self.last_time = time.time()
                self.current_image +=self.current_image_add
                if self.current_image >=2:
                     self.current_image_add = -1
                if self.current_image<=0:
                     self.current_image_add = 1
            if self.x <0:
                if self.y != 0:
                    self.game.canvas.itemconfig(self.image, \
                        image = self.image_left[2])
                else:
                    self.game.canvas.itemconfig(self.image,\
                        image = self.image_left[
                            self.current_image
                            ])
            elif self.x >0:
                if self.y !=0:
                    self.game.canvas.itemconfig(self.image,\
                        image = self.image_right[2])
                else:
                    self.game.canvas.itemconfig(self.image,\
                        image = self.image_right[
                            self.current_image
                        ]) 
        '''elif self.x==0 and self.y==0:
            if self.last_direct == 'Left':
                self.game.canvas.itemconfig(self.image,image =self.image_staylf)
            elif self.last_direct == 'Right':
                self.game.canvas.itemconfig(self.image,image = self.image_stayrt)
           '''         
    def coords(self):                                  #зберігання коорд х та у
            xy = self.game.canvas.coords(self.image)
            self.coordinates.x1 = xy[0]
            self.coordinates.y1 = xy[1]
            self.coordinates.x2 = xy[0] + 27
            self.coordinates.y2 = xy[1] + 30
            return self.coordinates 
    def move(self):  # JUMP
        self.animated()
        print("ManSprite move called, current coordinates:", self.game.canvas.coords(self.image))
        co = self.coords()  
        

        if self.y < 0:
            self.jump_count += 1
            if self.jump_count > 20:
                self.y = 0  # Перестаємо підніматися
            elif self.y > 0:
                self.jump_count -= 1
    
            left = True
            right = True
            top = True
            bottom = True
            falling = True
    
            if self.y > 0 and co.y2 >= self.game.canvas_height:
                self.y = 0
                bottom = False
                falling = False  # Фікс зависання у повітрі
            elif self.y == 0 and co.y2 <=self.game.canvas_height:
                falling = True
    
            if self.x > 0 and co.x2 >= self.game.canvas_width:
                self.x = 0
                right = False
            elif self.x < 0 and co.x1 <= 0:
                self.x = 0
                left = False  # Було `left = 0`, а треба `False`
    
            for sprite in self.game.sprites:
                if sprite == self:
                    continue
    
                sprite_co = sprite.coords()
        
                if top and self.y < 0 and collid_top(co, sprite_co):
                    self.y = -self.y
                    top = False
        
                if bottom and self.y > 0 and collid_bottom(self.y, co, sprite_co):
                    self.y = sprite_co.y1 - co.y2
                    if self.y < 0:
                        self.y = 0
                    bottom = False
                    top = False
        
                if bottom and falling and self.y == 0 and co.y2 < self.game.canvas_height and collid_bottom(1, co, sprite_co):
                    falling = False  # Виправляє зависання у повітрі
        
                if left and self.x < 0 and collid_left(co, sprite_co):
                    self.x = 0
                    left = False
                    if hasattr(sprite, "endgame") and sprite.endgame:
                        self.game.running = False
        
                if right and self.x > 0 and collid_right(co, sprite_co):
                    self.x = 0
                    right = False
                    if hasattr(sprite, "endgame") and sprite.endgame:
                        self.game.running = False
        
            if falling and self.y == 0 and co.y2 < self.game.canvas_height:
                self.y = 4  # Персонаж починає падати тільки якщо не на платформі
        
            self.game.canvas.move(self.image, self.x, self.y)
        
            print(f"Typ sprite.endgame: {type(sprite.endgame)}, of {sprite.endgame}")

    
class DoorSprite(Sprite):
    def __init__(self, game,photo_image,x,y,width,heigth):
        Sprite.__init__(self,game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x,y,image = self.photo_image,anchor ='nw')
        self.coordinates = Coords(x,y,x+(width/2),y +heigth)
        self.endgame = True

    
        
        
    
try:
     g = Game()                                                  #platforms
     flat1 = platformSprite(g,PhotoImage(file = "flat.gif"),\
         100,10,0,850) 
     flat2 = platformSprite(g,PhotoImage(file = "flat.gif"),\
         100,10,150,810)
     flat3 = platformSprite(g,PhotoImage(file = "flat.gif"),\
         100,10,300,770)
     flat4 = platformSprite(g,PhotoImage(file = "flat.gif"),\
         100,10,300,530)
     flat5 = platformSprite(g,PhotoImage(file = "flat2.gif"),\
         66,10,175,720)
     flat6 = platformSprite(g,PhotoImage(file = "flat2.gif"),\
         66,10,50,670)
     flat7 = platformSprite(g,PhotoImage(file = "flat2.gif"),\
         66,10,170,490)
     flat8 = platformSprite(g,PhotoImage(file = "flat2.gif"),\
         66,10,34,430)
     flat9 = platformSprite(g,PhotoImage(file = "flat3.gif"),\
         32,10,170,620)
     flat10 = platformSprite(g,PhotoImage(file = "flat3.gif"),\
         32,10,230,570)
     flat0 = platformSprite(g,PhotoImage(file = "flat0.gif"),\
         800,20,0,850)
     flat01 = platformSprite(g,PhotoImage(file ="flat0.gif"),\
         800,20,1500,850)
     flat11 = platformSprite(g,PhotoImage(file = "flat3.gif"),\
         32,10, 430,490)
     flat12 = platformSprite(g,PhotoImage(file = "flat.gif"),\
         100,10,530,460)
     flat13 = platformSprite(g,PhotoImage(file = "flat2.gif"),\
         66,10,170,370)
     flat14 = platformSprite(g,PhotoImage(file = "flat2.gif"),\
         66,10,320,310)
     flat15 = platformSprite(g,PhotoImage(file = "flat.gif"),\
         100,10,450,270)
     flat16 = platformSprite(g,PhotoImage(file = "flat2.gif"),\
         66,10,600,250)
     flat17 = platformSprite(g,PhotoImage(file = "flat.gif"),\
         100,10,720,200)
     flat18 = platformSprite(g,PhotoImage(file = "flat3.gif"),\
         32,10,870,200)
     flat19 = platformSprite(g,PhotoImage(file = "flat.gif"),\
         100,10,950,200)
     flat20 = platformSprite(g,PhotoImage(file = "flat3.gif"),\
         32,10,1070,200)
     flat21 = platformSprite(g,PhotoImage(file = "flat3.gif"),\
         32,10,1200,200)
     flatboss = platformSprite(g,PhotoImage(file ="bossflat.gif"),\
         300,10,700,450)
     flatboss1 = platformSprite(g,PhotoImage(file ="bossflat.gif"),\
         300,10,1400,200)
     
    # flattest = platformSprite(g,PhotoImage(file = "flat0.gif"),\
     #    0,850,20,850)
     g.sprites.append(flat1)
     g.sprites.append(flat2)
     g.sprites.append(flat3)
     g.sprites.append(flat4)
     g.sprites.append(flat5)
     g.sprites.append(flat6)
     g.sprites.append(flat7)
     g.sprites.append(flat8)
     g.sprites.append(flat9)
     g.sprites.append(flat10)
     g.sprites.append(flat0)
     g.sprites.append(flat01)
     g.sprites.append(flat11)
     g.sprites.append(flat12)
     g.sprites.append(flat13)
     g.sprites.append(flat14)
     g.sprites.append(flat15)
     g.sprites.append(flat16)
     g.sprites.append(flat17)
     g.sprites.append(flat18)
     g.sprites.append(flat19)
     g.sprites.append(flat20)
     g.sprites.append(flat21)
     g.sprites.append(flatboss)
     g.sprites.append(flatboss1)
     #g.sprites.append(flattest)
     door = DoorSprite(g,PhotoImage(file = "bunkerdoor_open.gif"),40,30,1550,850)
     g.sprites.append(door)
     sf = ManSprite(g)
     g.sprites.append(sf)
     g.mainloop()
     
     
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()