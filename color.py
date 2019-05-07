#Background generator
#Brightness based on: https://www.nbdtech.com/Blog/archive/2008/04/27/Calculating-the-Perceived-Brightness-of-a-Color.aspx

from random import randint
from PIL import Image, ImageDraw
import math
#TODO: logging... shouldve started with it lul

SCREEN_SIZE = (1920, 1080)
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)

def rand_rgb(bright=None): 
    if bright == None:
        return (randint(0,255), randint(0,255), randint(0,255))
    elif bright:
        color =  [randint(0,255), randint(0,255), randint(0,255)]
        while math.sqrt(.241*color[0]**2 + .691*color[1]**2 + .068*color[2]**2) < 130: 
            color[randint(0,2)] += 20
        return tuple(color)
    else:
        color =  [randint(0,255), randint(0,255), randint(0,255)]
        while math.sqrt(.241*color[0]**2 + .691*color[1]**2 + .068*color[2]**2) > 130: 
            color[randint(0,2)] -= 20
        return tuple(color)


def coords_diamond(center, z = None):
    x = center[0]
    y = center[1]
    z = randint(1,3) if not z else z
    return [(x+z, y), (x, y+z), (x-z, y), (x, y-z)]

def coords_circle(center, z = None):
    x = center[0]
    y = center[1]
    z = randint(1,3) if not z else z
    return [(x-z, y-z), (x+z, y+z)]

class Backgroundifier():
    
    def __init__(self):
        self.CANVAS_SIZE = SCREEN_SIZE
        self.img = None
        self.draw = None

    def rand_point(self, boarder = False, first_point = None): 
        if boarder:
            point = [0,0]
            i = randint(0,1)
            point[i] = randint(0, self.CANVAS_SIZE[i])
            point[1-i] = 0 if randint(0,1) else self.CANVAS_SIZE[1-i]
            if first_point:
                if first_point[0] == point[0]:
                    point[0] = 0 if first_point[0] > 0 else self.CANVAS_SIZE[0]
                if first_point[1] == point[1]:
                    point[1] = 0 if first_point[1] > 0 else self.CANVAS_SIZE[0]
            return point
        else:
            return (randint(0,self.CANVAS_SIZE[0]), randint(0,self.CANVAS_SIZE[1]))

    def rand_line(self):
        point1 = self.rand_point(boarder=True)
        point2 = self.rand_point(boarder=True, first_point=point1)
        #print(f"Line coords: {point1}, {point2}")
        return (point1[0], point1[1], point2[0], point2[1])

    def background_lines(self):
        # gen larger and sample down with antialiasing
        self.CANVAS_SIZE = (SCREEN_SIZE[0]*2, SCREEN_SIZE[1]*2)
        self.img = Image.new('RGB', self.CANVAS_SIZE, BLACK)
        self.draw = ImageDraw.Draw(self.img)
        for i in range(randint(1,25)):
            self.draw.line(self.rand_line(), rand_rgb(True), width=4)
        self.img.resize(SCREEN_SIZE, Image.ANTIALIAS)

    def background_stars(self):
        self.CANVAS_SIZE = SCREEN_SIZE
        self.img = Image.new('RGB', self.CANVAS_SIZE, BLACK)
        self.draw = ImageDraw.Draw(self.img)
        for i in range(randint(1000,5000)): 
            self.draw.point(self.rand_point(), rand_rgb(True))
        for i in range(randint(10,30)): 
            if randint(0,1):
                self.draw.polygon(coords_diamond(center=self.rand_point()), rand_rgb(True))
            else:
                self.draw.ellipse(coords_circle(center=self.rand_point()), rand_rgb(True))
        self.img.resize(SCREEN_SIZE, Image.ANTIALIAS)
    
    def generate_shape(self):
        shape = randint(0,3)
        if shape == 0: #TODO: dicitonary function mapping? #small circle
            self.draw.ellipse(coords_circle(center=self.rand_point(), z=randint(40,300)), rand_rgb(True))
        elif shape == 1: #large circle
            self.draw.ellipse(coords_circle(center=self.rand_point(), z=randint(400,1000)), rand_rgb(True))
        elif shape == 2: #square (yes, this uses coords_circle, i know i should make it generic TODO)
            self.draw.rectangle(coords_circle(center=self.rand_point(), z=randint(40,300)), rand_rgb(True))
        #todo
        

    def background_shapes(self):
        self.CANVAS_SIZE = (SCREEN_SIZE[0]*2, SCREEN_SIZE[1]*2)
        self.img = Image.new('RGB', self.CANVAS_SIZE, BLACK)
        self.draw = ImageDraw.Draw(self.img)
        for i in range(randint(2,5)):
            self.generate_shape()
            
    def create_background(self):
        background_type = 2 #randint(0,1)
        if background_type == 0:
            self.background_lines()
        elif background_type == 1:
            self.background_stars()
        elif background_type == 2:
            self.background_shapes()
        else:
            print('oof')
        self.img.show()

if __name__ == '__main__':
    b = Backgroundifier()
    b.create_background()
