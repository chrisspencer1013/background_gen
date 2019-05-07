from random import randint
from PIL import Image, ImageDraw

SCREEN_SIZE = (1920, 1080)
CANVAS_SIZE = (SCREEN_SIZE[0]*2, SCREEN_SIZE[1]*2) # gen larger and sample down with antialiasing

def rand_rgb():
    color =  [randint(0,255), randint(0,255), randint(0,255)]
    if color[0] < 44 and color[1] < 44 and color[2] < 44: #TODO: rework this
        print("Color too dark")
        choice = randint(0,2)
        color[choice] = color[choice] - 75
    return tuple(color)

def rand_point(first_point = None):
    point = [0,0]
    i = randint(0,1)
    point[i] = randint(0,CANVAS_SIZE[i])
    point[1-i] = 0 if randint(0,1) else CANVAS_SIZE[1-i]
    if first_point:
        if first_point[0] == point[0]:
            point[0] = 0 if first_point[0] > 0 else CANVAS_SIZE[0]
        if first_point[1] == point[1]:
            point[1] = 0 if first_point[1] > 0 else CANVAS_SIZE[0]
    return point

def rand_line():
    point1 = rand_point()
    point2 = rand_point(point1)
    print(f"Line coords: {point1}, {point2}")
    return (point1[0], point1[1], point2[0], point2[1])

img = Image.new('RGB', CANVAS_SIZE, (0,0,0))
draw = ImageDraw.Draw(img)
for i in range(randint(1,25)):
    draw.line(rand_line(), rand_rgb(), width=4)

img.resize(SCREEN_SIZE, Image.ANTIALIAS)
img.show()
