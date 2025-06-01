import time
from datetime import datetime
import operator
import random


_NAMES = [x+y for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for y in "1234567890"]

OUTW = 40
OUTH = 40
CELL_SIZE = 10
N = 3
NORTH = (0,-1)
EAST = (1,0)
SOUTH = (0,1)
WEST = (-1,0)
DIRS = { NORTH:"NORTH", SOUTH:"SOUTH", EAST:"EAST", WEST:"WEST" }
OPPOSITE_DIRS = { "NORTH":"SOUTH", "SOUTH":"NORTH", "EAST":"WEST", "WEST":"EAST" }


IMG = None
IMG_WIDTH = None
IMG_HEIGHT = None

STATE_GRID = []
ALL_TILES = []

def drawCellOutlines():
    for row in range(OUTH):
        for col in range(OUTW):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            stroke(100)
            no_fill()
            rect(x, y, CELL_SIZE, CELL_SIZE)

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
        13:("City", 9,9),
        14:("some_design", 30,30),
        15:("CityScape", 10,10),
        16:("CircleSquare", 10,10),
        17:("FlowerSmall", 10,10),
        18:("FlowerSmallRoots", 10,15)
    }
    choice = 17

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
    initStateGrid()
    #print(ALL_TILES[0].isCompatible(ALL_TILES[9], "SOUTH"))
    #print(ALL_TILES[30].dir_adj)

def draw():
    background(240)
    #for tile in ALL_TILES:
    #    drawTile(tile=tile)
    #for cell in sum(STATE_GRID, []):
    #    cell.collapse()
    #    drawCell_center(cell=cell)
    #drawCellOutlines()
    drawStateGrid()
    
    # Pick next cell based on entropy
    next_cell = pickLowestEntropyCell()
    #print("### Pick next cell:", next_cell.x, next_cell.y)

    
    # Collapse that cell into a single domain
    next_cell.collapse()
    #drawCell_center(cell=next_cell)
    
    #print("Update")
    # With the collapsed domain, propagate to adjacent tiles
    updateAdjacentCellDomains(next_cell)
    #print("Update over")
    
    # Go through STATE_GRID and collapse/draw all 1-domain tiles
    one_d_list = sum(STATE_GRID, [])
    for x in one_d_list:
        if len(x.domain) == 1:
            drawCell_center(cell=x)
    # Repeat

def updateAdjacentCellDomains(cell):
    
    stack = [cell]
    while stack:
        #print("== Current stack:", [(x.x, x.y) for x in stack])
        mycell = stack.pop(0)
        #print("Popped", mycell.x, mycell.y)
        #print("====== New stack:", [(x.x, x.y) for x in stack])

        nbs = getNeighborCells(mycell) # ( (nb_cell, dirToNb_cell), ... )
        
        #print("Main cell:", mycell.x,mycell.y, len(mycell.domain))
        #print([x for x in nbs])
        for nb, d in nbs: # d is maincell -> nb direction
            #print("-- Check:", nb.x,nb.y, len(nb.domain))
            if len(nb.domain) == 1: continue
            if (nb.x,nb.y) == (mycell.x,mycell.y): raise
            
            # What tiles can I be next to?
            
            # What tiles can the neighbor be next to?
            # "Next to" meaning, direction from them to me (NSEW)
            #other_valid_d_tiles = nb.dir_adj[OPPOSITE_DIR[d]]
            
            # Find the overlap of their valid next-to tiles, to my domain
            valid_tiles_for_neighbor = []
            for tile_n in nb.domain:
                for tile_o in mycell.domain:
                    # Compare all of our tiles
                    # Can your tile be next to my tile?
                    # If yes, your tile is allowed, move on to the next of your tiles to compare
                    
                    if tile_n in tile_o.dir_adj[d]:
                        valid_tiles_for_neighbor.append(tile_n)
                        break
                else:
                    # tile_n is not in any of mycell's allowed adjacent tiles
                    # print("Removing", tile_n, "from neighbor tile")
                    pass
                    
            
            # Set the neighbor domain to the filtered list
            # Not going to remove bad tiles, just set nb domain to good tiles
            # print("Num valid tiles for neighbor:", len(valid_tiles_for_neighbor))
            old_domain = len(nb.domain)
            nb.domain = valid_tiles_for_neighbor
            new_domain = len(nb.domain)
            if old_domain != new_domain:
                #print("Adding", nb.x,nb.y, "to stack")
                stack.append(nb)
            
            
def drawStateGrid():
    for cell in sum(STATE_GRID, []):
        drawCell_center(cell=cell)

class Cell:
    def __init__(self, x,y):
        
        # A cell starts with every tile in its domain
        # Domain is a list because we're not doing weighted probabilities,
        # We're just filling the list with unique tiles that may have the same overlap data
        self.domain = [tile for tile in ALL_TILES] # So glad Python is a reference-based language
        self.entropy = self.getEntropy()
        
        self.x = x
        self.y = y
        
    def getEntropy(self):
        return len(self.domain)
    
    def collapse(self):
        # Choose a tile at random from the domain
        if len(self.domain) == 1: return
        self.domain = [random.choice(self.domain)]
        self.entropy = self.getEntropy()
    
def getNeighborCells(cell):
    x = cell.x
    y = cell.y
    
    nbs = []
    for d in (NORTH, EAST, SOUTH, WEST):
        if ((x + d[0]) < 0 or \
            (x + d[0]) >= OUTW or \
            (y + d[1]) < 0 or \
            (y + d[1]) >= OUTH):
            continue
        nb_c = getCell(x+d[0], y+d[1])
        nbs.append((nb_c, DIRS[d]))
    return nbs
    

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

def getCell(x,y):
    return STATE_GRID[y][x]

def pickLowestEntropyCell():
    sorted_x = sorted(
        sum(STATE_GRID, []),
        key=operator.attrgetter('entropy')
        )
    #print([float(x.se) for x in sorted_x])
    # Return the lowest non-zero entropy
    options = []
    for x in sorted_x:
        if (len(x.domain) > 1) and (x.entropy >= sorted_x[0].entropy):
            options.append(x)
    
    return options[0]

def initStateGrid():
    global STATE_GRID
    STATE_GRID = [
            [Cell(x,y) for x in range(OUTW)] for y in range(OUTH)
        ]

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
            colr = tile.getColorFromData(x, y)
            fill(colr)
            #stroke(240)
            rect(anchor_y + (y * mini_cell_size),
                 anchor_x + (x * mini_cell_size), mini_cell_size, mini_cell_size)

def drawCell_whole(x=None,y=None,cell=None):
    # Draw a cell's single-item domain, which is just a tile
    if not x or not y:
        x = cell.x
        y = cell.y
    anchor_x = x * CELL_SIZE
    anchor_y = y * CELL_SIZE
    mini_cell_size = CELL_SIZE / N
    for x in range(N):
        for y in range(N):
            if len(cell.domain) != 1:
                colr = ("#FFAAFFFF") # Some random color
            else:
                colr = cell.domain[0].getColorFromData(x, y)
            fill(colr)
            stroke(240)
            rect(anchor_x + (x * mini_cell_size),
                 anchor_y + (y * mini_cell_size), mini_cell_size, mini_cell_size)

def drawCell_center(x=None,y=None,cell=None):
    # Draw a cell's single-item domain, which is just a tile
    if not x or not y:
        x = cell.x
        y = cell.y
    #print("DC-C", x,y)
    anchor_x = x * CELL_SIZE
    anchor_y = y * CELL_SIZE
    
    if len(cell.domain) != 1:
        colr = ("#FFAAFFFF") # Some random color
    else:
        colr = cell.domain[0].getColorFromData(N//2,N//2)
        
    fill(colr)
    #stroke(240)
    rect(anchor_x,
         anchor_y, CELL_SIZE, CELL_SIZE)
            
