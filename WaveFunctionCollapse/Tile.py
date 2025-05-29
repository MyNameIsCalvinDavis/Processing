import time

_NAMES = [x+y for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for y in "1234567890"]

OUTW = 15
OUTH = 10
CELL_SIZE = 40
N = 3
IMG = None
IMG_WIDTH = None
IMG_HEIGHT = None

STATE_GRID = []
ALL_TILES = []

def setup():
    global IMG
    global IMG_WIDTH
    global IMG_HEIGHT
    size(OUTW*CELL_SIZE,OUTH*CELL_SIZE)
    imgs = {
        1:("Flower", 10,10),
        2:("Pattern2", 3,3),
        3:("Pattern3", 3,3),
        4:("Pattern4", 3,3),
        5:("Pattern5", 5,5),
        6:("Pattern6", 4,4),
        7:("FlowersBig", 46,46),
        8:("BeachLand2", 20,10),
        9:("BeachLand3", 10,5),
        10:("BeachLand4", 4,7),
        11:("BlueDots", 15,15),
        12:("BlueDots2", 15,15),
        13:("City", 9,9)
    }
    choice = 13

    WIDTH = imgs[choice][1]
    HEIGHT = imgs[choice][2]
    IMG = load_image("patterns/{}.png".format(imgs[choice][0]))
    IMG.load_pixels()
    IMG_WIDTH = IMG.width
    IMG_HEIGHT = IMG.height
    extractAllTiles()

def draw():
    background(100)
    for tile in ALL_TILES:
        drawTile(tile=tile)
    
    for row in range(OUTH):
        for col in range(OUTW):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            stroke(100)
            no_fill()
            rect(x, y, CELL_SIZE, CELL_SIZE)

def extractAllTiles():
    for y in range(IMG_HEIGHT):
        for x in range(IMG_WIDTH):
            T = Tile(x,y, IMG)
            T.extractColorData()
            ALL_TILES.append(T)

def drawTile(x=None,y=None,tile=None):
    if not x or not y:
        x = tile.img_x
        y = tile.img_y
    anchor_x = x * CELL_SIZE
    anchor_y = y * CELL_SIZE
    mini_cell_size = CELL_SIZE / N
    for x in range(N):
        for y in range(N):
            col = tile.getColorFromData(x, y)
            fill(col)
            stroke(240)
            rect(anchor_y + (y * mini_cell_size),
                 anchor_x + (x * mini_cell_size), mini_cell_size, mini_cell_size)
            
class Tile:
    """
    A Tile represents a sliced-out chunk from an image. A Cell's domain contains multiple Tiles
    """
    def __init__(self, x,y, img, n=3):
        """
        x,y: x,y location on img
        img: PImage object
        """
        self.data = []
        self.name = None
        self.img_x = x
        self.img_y = y
        
        self.pimg = img
        self.n = n
        
    def XYtoPImagePixelsIndex(self, x,y):
        return (x % self.pimg.width) + (y % self.pimg.height) * self.pimg.width
        
    def extractColorData(self):
        # Produce nxn section of self.img.pixels 
        # (('#FFFFFFFF', '#FFFFFFFF', '#FFFFFFFF'),
        #  ('#FFFFFFFF', '#000000FF', '#000000FF'),
        #  ('#FFFFFFFF', '#000000FF', '#ED1C24FF'))
        self.data = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                pix_index = self.XYtoPImagePixelsIndex(j + self.img_x,i + self.img_y)
                row.append(hex_color(self.pimg.pixels[pix_index]))
            self.data.append(tuple(row))
        self.data = tuple(self.data)
    
    def getColorFromData(self, x,y):
        # Given self.data, return the x,y within
        return self.data[y][x]


