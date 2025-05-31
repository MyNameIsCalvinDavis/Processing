import time
from datetime import datetime

_NAMES = [x+y for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for y in "1234567890"]

OUTW = 15
OUTH = 10
CELL_SIZE = 40
N = 3
NORTH = (0,-1)
EAST = (1,0)
SOUTH = (0,1)
WEST = (-1,0)


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
    s_time = datetime.now()
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
    print(datetime.now() - s_time)
    extractTileAdjacencies()
    print(datetime.now() - s_time)
    #print(ALL_TILES[0].isCompatible(ALL_TILES[9], "SOUTH"))
    #print(ALL_TILES[30].dir_adj)

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
    
def extractTileAdjacencies():
    # For every tile, for all 4 directions, identify what tiles I am adjacent to
    for orig_tile in ALL_TILES:
        # Not checking neighbors, checking ALL tiles in the dataset
        for s in ["NORTH", "EAST", "SOUTH", "WEST"]:
            for other_tile in ALL_TILES:
                if orig_tile.isCompatible(other_tile, s):
                    orig_tile.dir_adj[s].append(other_tile)
            
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
        self.data = None
        self.name = None
        self.img_x = x
        self.img_y = y
        self.dir_adj = {
            "NORTH":[],
            "SOUTH":[],
            "EAST":[],
            "WEST":[]
        }
        
        self.pimg = img
        self.n = n
        
    def XYtoPImagePixelsIndex(self, x,y):
        return (x % self.pimg.width) + (y % self.pimg.height) * self.pimg.width
        
    def isCompatible(self, other, d):
        # DEFAULT j,i = [X X .] [X X .]
        
        # Sacrificing space for readability - the condensed version of this
        # Would be less understandable
        if d == "EAST": # Rows: all // Cols: [1:] == [:n-1]
            for i in range(self.n):
                for j in range(self.n-1):
                    #print("Compare", j+1, i, "----", j,i)
                    if self.getColorFromData(j+1, i) != other.getColorFromData(j, i):
                        return False
            return True
        if d == "WEST": # Rows: all // Cols: [:n-1] == [1:]
            for i in range(self.n):
                for j in range(self.n-1):
                    #print("Compare", j, i, "----", j,i)
                    if self.getColorFromData(j, i) != other.getColorFromData(j+1, i):
                        return False
            return True
        
        if d == "NORTH": # Rows: [:n-1] == [1:] // Cols: all
            for i in range(self.n-1):
                for j in range(self.n):
                    #print("Compare", j, i, "----", j,i+1)
                    if self.getColorFromData(j, i) != other.getColorFromData(j, i+1):
                        return False
            return True
        
        if d == "SOUTH":
            # This [1:] cols line up with other [:n-1] cols? [. X X] [X X .]
            for i in range(self.n-1):
                for j in range(self.n):
                    #print("Compare", j, i+1, "----", j,i)
                    if self.getColorFromData(j, i+1) != other.getColorFromData(j, i):
                        return False
            return True
            
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


