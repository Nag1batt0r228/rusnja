from tkinter import *
import os
import traceback
import random 
import time 

class Game:
 def __init__(self):
    self.tk = Tk()
    self.tk.title("Человечек спешит к выходу")
    self.tk.resizable(0, 0)
    self.tk.wm_attributes("-topmost", 1)
    self.canvas = Canvas(self.tk, width=1600, height=900,highlightthickness=0)
    self.canvas.pack()
    self.tk.update()
    self.canvas_height = 900
    self.canvas_width = 1600
    self.bg = PhotoImage(file="donbas1.gif")
    w = self.bg.width()
    h = self.bg.height()
    self.canvas.create_image(image=self.bg, anchor='nw')
    self.sprites = []
    self.running = True
def mainloop(self):
    while 1:
        if self.running == True:
            for sprite in self.sprites:
                sprite.move()
        self.tk.update_idletasks()
        self.tk.update()
        time.sleep(0.01)
class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    def within_x(co1, co2):
            if (co1.x1 > co2.x1 and co1.x1 < co2.x2) \
                or (co1.x2 > co2.x1 and co1.x2 < co2.x2) \
                or (co2.x1 > co1.x1 and co2.x1 < co1.x2) \
                or (co2        .x2 > co1.x1 and co2.x2 < co1.x2):
                    return True
            else:
                    return False
    def within_y(co1, co2):
        if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
            or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
            or (co2.y1 > co1.y1 and co2.y1 < co1.y2) \
            or (co2.y2 > co1.y1 and co2.y2 < co1.y2):
                    return True
        else:
                    return False
    def collided_left(co1, co2):
        if within_y(co1, co2):
            if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:
                return True
            return True
    def collided_right(co1, co2):
        if within_y(co1, co2):
            if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
                return True
            return False
    def collided_top(co1, co2):
        if within_x(co1, co2):
            if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
                return True
            return False
    def collided_bottom(y, co1, co2):
        if within_x(co1, co2):
            y_calc = co1.y2 + y
            if y_calc >= co2.y1 and y_calc <= co2.y2:
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
    
class PlatformSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, \
        image=self.photo_image, anchor='nw')
        self.coordinates = Coords(x, y, x + width, y + height)
class StickFigureSprite(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.images_left = [
            PhotoImage(file="sickman_lf.gif"),
            PhotoImage(file="sickman_lft2.gif"),
            PhotoImage(file="sickman_lft3.gif")
            ]
        self.images_right = [
            PhotoImage(file="sickman_rt.gif"),
            PhotoImage(file="sickman_rt2.gif"),
            PhotoImage(file="sickman_rt3.gif")   # Placeholder for image
        ]
        
        # Initialize character's position and state
        self.image = game.canvas.create_image(200, 470, image=self.images_left[0], anchor='nw')
        self.x = -2
        self.y = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()  # Ensure you define this class
        self.game = game  # Reference to the game instance
        
        # Bind key events
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)

    def turn_left(self, evt):
        # If the character is on the ground (y == 0), move left
        if self.y == 0:
            self.x = -2

    def turn_right(self, evt):
        # If the character is on the ground (y == 0), move right
        if self.y == 0:
            self.x = 2

    def jump(self, evt):
        # Start jumping if the character is on the ground
        if self.y == 0:
            self.y = -4
            self.jump_count = 0

    def animate(self):
        # Animate character's movement
        if self.x != 0 and self.y == 0:
            if time.time() - self.last_time > 0.1:  # Delay for animation frame
                self.last_time = time.time()
                self.current_image += self.current_image_add
                
                # Reverse the animation direction when the frame reaches the end
                if self.current_image >= 2:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1

                # Change the character's image based on movement direction
                if self.x < 0:
                    # Moving left
                    if self.y != 0:
                        self.game.canvas.itemconfig(self.image, image=self.images_left[2])  # Jump animation
                    else:
                        self.game.canvas.itemconfig(self.image, image=self.images_left[self.current_image])
                elif self.x > 0:
                    # Moving right
                    if self.y != 0:
                        self.game.canvas.itemconfig(self.image, image=self.images_right[2])  # Jump animation
                    else:
                        self.game.canvas.itemconfig(self.image, image=self.images_right[self.current_image])

    def coords(self):            
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + 27  # Assuming 27px width of the character
        self.coordinates.y2 = xy[1] + 30  # Assuming 30px height of the character
        return self.coordinates

    def move(self):
        # Animate and move the character based on its velocity and position
        self.animate()

        # Handle gravity and jumping logic
        if self.y < 0:
            self.jump_count += 1
            if self.jump_count > 20:
                self.y = 4  # Change direction after reaching jump limit

        if self.y > 0:
            self.jump_count -= 1

        # Get the current coordinates of the character
        co = self.coords()

        # Define collision boundaries
        left = True
        right = True
        top = True
        bottom = True
        falling = True

        # Handle collision with the bottom of the canvas
        if self.y > 0 and co.y2 >= self.game.canvas_height:
            self.y = 0
            bottom = False

        # Handle collision with the top of the canvas
        elif self.y < 0 and co.y1 <= 0:
            self.y = 0
            top = False

        # Handle collision with the right edge of the canvas
        if self.x > 0 and co.x2 >= self.game.canvas_width:
            self.x = 0
            right = False

        # Handle collision with the left edge of the canvas
        elif self.x < 0 and co.x1 <= 0:
            self.x = 0
            left = False

        # Handle collision with other sprites
        for sprite in self.game.sprites:
            if sprite == self:
                continue  # Skip self-check

            sprite_co = sprite.coords()

            # Collision detection with the top side
            if top and self.y < 0 and collided_top(co, sprite_co):
                self.y = -self.y  # Reverse the y-axis velocity
                top = False

            # Collision detection with the bottom side
            if bottom and self.y > 0 and collided_bottom(self.y, co, sprite_co):
                self.y = sprite_co.y1 - co.y2  # Prevent overlap, stop falling
                if self.y < 0:
                    self.y = 0
                bottom = False
                top = False

            # Handle falling logic (the character is falling if no other collisions detected)
            if bottom and falling and self.y == 0 and co.y2 < self.game.canvas_height and collided_bottom(1, co, sprite_co):
                falling = False
                if left and self.x < 0 and collided_left(co, sprite_co):
                    self.x = 0
                    left = False
                    if sprite.endgame:
                        self.game.running = False
                    if right and self.x > 0 and collided_right(co, sprite_co):
                            self.x = 0
                            right = False
                            if sprite.endgame:
                                self.game.running = False
                if falling and bottom and self.y == 0 and co.y2 < self.game.canvas_height:
                    self.y = 4
                self.game.canvas.move(self.image, self.x, self.y)
class DoorSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y,image=self.photo_image, anchor='nw')
        self.coordinates = Coords(x, y, x + (width / 2), y + height)
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
         850,20,1500,850)
     flat11 = platformSprite(g,PhotoImage(file = "flat3.gif"),\
         66,10, 430,490)
     flat12 = platformSprite(g,PhotoImage(file = "flat.gif"),\
         100,10,530,460)
     flat13 = platformSprite(g,PhotoImage(file = "flat2.gif"),\
         66,10,170,370)
     flat14 = platformSprite(g,PhotoImage(file = "flat2.gif"),\
         66,10,320,310)
     flat15 = platformSprite(g,PhotoImage(file = "flat.gif"),\
         100,10,450,270)
     flat16 = platformSprite(g,PhotoImage(file = "flat2.gif"),\
         100,10,600,250)
     flat17 = platformSprite(g,PhotoImage(file = "flat.gif"),\
         100,10,720,200)
     flat18 = platformSprite(g,PhotoImage(file = "flat3.gif"),\
         100,10,870,200)
     flat19 = platformSprite(g,PhotoImage(file = "flat.gif"),\
         100,10,950,200)
     flat20 = platformSprite(g,PhotoImage(file = "flat3.gif"),\
         100,10,1070,200)
     flat21 = platformSprite(g,PhotoImage(file = "flat3.gif"),\
         100,10,1200,200)
     flatboss = platformSprite(g,PhotoImage(file ="bossflat.gif"),\
         300,10,700,450)
     flatboss1 = platformSprite(g,PhotoImage(file ="bossflat.gif"),\
         300,10,1400,200)
     
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
     
     door = DoorSprite(g,PhotoImage(file = "bunkerdoor_open.gif"),40,30,1550,850)
     g.sprites.append(door)
     sf = ManSprite(g)
     g.sprites.append(sf)
     g.mainloop()
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()