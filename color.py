from random import randint
from PIL import Image, ImageDraw

SCREEN_SIZE = (1920, 1080)
CANVAS_SIZE = (SCREEN_SIZE[0]*2, SCREEN_SIZE[1]*2)


def rand_rgb():
    return (randint(0,255), randint(0,255), randint(0,255))

def rand_bool():
    return randint(0,1)

def rand_point(first_point = None):
    point = [0,0]
    i = rand_bool()
    point[i] = randint(0,CANVAS_SIZE[i])
    point[1-i] = 0 if rand_bool() else CANVAS_SIZE[1-i]
    return point

def rand_line():
    point1 = rand_point()
    point2 = rand_point()
    while point1[0] == point2[0] or point1[1] == point2[1]: 
        print(f"Redo: {point1}, {point2}")
        point1 = rand_point()
    print(f"Results: {point1}, {point2}")
    return (point1[0], point1[1], point2[0], point2[1])

img = Image.new('RGB', CANVAS_SIZE, (0,0,0))
draw = ImageDraw.Draw(img)
for i in range(randint(1,100)):
    draw.line(rand_line(), rand_rgb(), width=randint(4,20))

img.thumbnail(SCREEN_SIZE, Image.ANTIALIAS)
img.show()
