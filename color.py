#Background generator
#Brightness based on: https://www.nbdtech.com/Blog/archive/2008/04/27/Calculating-the-Perceived-Brightness-of-a-Color.aspx

from random import randint
from PIL import Image, ImageDraw
import math

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

def coords_diamond(center_coords):
    x = center_coords[0]
    y = center_coords[1]
    z = randint(1,3)
    return [(x+z, y), (x, y+z), (x-z, y), (x, y-z)]

def coords_circle(center_coords):
    x = center_coords[0]
    y = center_coords[1]
    z = randint(1,3)
    return [(x-z, y-z), (x+z, y+z)]

class Backgroundifier():
    
    def __init__(self):
        self.CANVAS_SIZE = SCREEN_SIZE

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

    def draw_lines(self):
        # gen larger and sample down with antialiasing
        self.CANVAS_SIZE = (SCREEN_SIZE[0]*2, SCREEN_SIZE[1]*2)
        img = Image.new('RGB', self.CANVAS_SIZE, BLACK)
        draw = ImageDraw.Draw(img)
        for i in range(randint(1,25)):
            draw.line(self.rand_line(), rand_rgb(True), width=4)
        img.resize(SCREEN_SIZE, Image.ANTIALIAS)
        return img

    def draw_stars(self):
        self.CANVAS_SIZE = SCREEN_SIZE
        img = Image.new('RGB', self.CANVAS_SIZE, BLACK)
        draw = ImageDraw.Draw(img)
        for i in range(randint(1000,5000)): 
            draw.point(self.rand_point(), rand_rgb(True))
        for i in range(randint(10,30)): 
            if randint(0,1):
                draw.polygon(coords_diamond(self.rand_point()), rand_rgb(True))
            else:
                draw.ellipse(coords_circle(self.rand_point()), rand_rgb(True))
        img.resize(SCREEN_SIZE, Image.ANTIALIAS)
        return img

    def draw(self):
        background_type = randint(0,1)
        img = None
        if background_type == 0:
            img = self.draw_lines()
        elif background_type == 1:
            img = self.draw_stars()
        elif background_type > 1:
            print('nope')
        img.show()

if __name__ == '__main__':
    background = Backgroundifier()
    background.draw()
