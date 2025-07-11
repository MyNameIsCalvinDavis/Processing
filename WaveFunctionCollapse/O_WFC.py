import time
from datetime import datetime
import operator
from copy import deepcopy
import random


_NAMES = [x+y for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for y in "1234567890"]

OUTW = 200
OUTH = 100
CELL_SIZE = 5
N = 5
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
STATE_LOG = []
ALL_TILES = []
ALL_TILES_HASH = {}

def drawCellOutlines():
    for row in range(OUTH):
        for col in range(OUTW):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            stroke(0)
            no_fill()
            rect(x, y, CELL_SIZE, CELL_SIZE)

def setup():

    global IMG
    global IMG_WIDTH
    global IMG_HEIGHT
    global s_time
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
        15:("CityScape", 15,10),
        16:("CircleSquare", 10,10),
        17:("FlowerSmall", 10,10),
        18:("FlowerSmallRoots", 10,15),
        19:("Water", 16,16),
        20:("Skyline", 39,28),
        21:("Skyline2", 32,31),
        22:("Dungeon", 17,15),
        23:("Nested", 14,14),
        24:("Platformer", 72,32),
        25:("3Bricks", 32,32),
        26:("Disk", 30,30),
        27:("Cat", 18,16),
        28:("Platformer", 72,32),
        29:("Lake", 20,19),
        30:("Knot", 17,17),
        31:("BrownFox", 62,12),
        32:("LilGuy", 18,16),
        33:("Shadow", 40,40),
        34:("SmallCircle",30,30),
        35:("Flowers",15,24)
    }
    choice = 27

    WIDTH = imgs[choice][1]
    HEIGHT = imgs[choice][2]
    IMG = load_image("patterns/{}.png".format(imgs[choice][0]))
    IMG.load_pixels()
    IMG_WIDTH = IMG.width
    IMG_HEIGHT = IMG.height
    print("Extract tiles before", datetime.now() - s_time)
    extractAllTiles()
    random.shuffle(ALL_TILES)
    print("Extract tiles after", datetime.now() - s_time)
    print("Extract adjacencies before", datetime.now() - s_time)
    extractTileAdjacencies()
    print("Extract adjacencies before", datetime.now() - s_time)
    print(datetime.now() - s_time)
    
    # How many unique tiles
    s = set()
    for tile in ALL_TILES:
        s.add(tile.getHash())
    print(len(ALL_TILES), len(s))
    
    initStateGrid()
    #print(ALL_TILES[0].isCompatible(ALL_TILES[9], "SOUTH"))
    #print(ALL_TILES[30].dir_adj)

def backupStateGridDomains():
    global STATE_LOG
    domains = []
    for cell in sum(STATE_GRID, []):
        domains.append(cell.domain.copy())
    STATE_LOG.append(domains)
    #if len(STATE_LOG) > 10000: STATE_LOG = STATE_LOG[100:]
    
def restoreStateGridDomains(jump=1):
    for i in range(jump):
        STATE_LOG.pop()
    restore = STATE_LOG[-1]
    for cell,d in zip(sum(STATE_GRID, []), restore):
        cell.domain = d.copy()
        cell.getEntropy()
        cell.collapsed = False
        cell.checked = False

def resetCells(x,y,radius=4):
    cells = []
    for row in range(x-radius, x+radius+1):
        for col in range(y-radius, y+radius+1):
            c = getCell(row,col)
            if c: cells.append(c)
    
    # Just the __init__ of Cell
    for c in cells:
        c.domain = [tile for tile in ALL_TILES] # So glad Python is a reference-based language
        c.entropy = c.getEntropy()
        c.checked = False
        c.collapsed = False
        c.outline = (True, (255,0,0))
    
    # Update cell adjacency of the perimeter of the square
    edge_cells = []
    # Top
    edge_cells += [getCell(x,y-radius-1) for x in range(x-radius-1, x+radius+2)]
    # Bottom
    edge_cells += [getCell(x,y+radius+1) for x in range(x-radius-1, x+radius+2)]
    # Left
    edge_cells += [getCell(x-radius-1,y) for y in range(y-radius-1, y+radius+2)]
    # Right
    edge_cells += [getCell(x+radius+1,y) for y in range(y-radius-1, y+radius+2)]
    for c in edge_cells:
        if not c: continue
        c.outline = (True, (0,0,255))
        #if updateAdjacentCellDomains(c) == 2: return 2
        updateAdjacentCellDomains(c)



jump = 1
time_m = 1
def draw():
    global jump
    global time_m
    time_m += 1
    background(240)
    
    a,b = wfc()
    if a == 2:
        print("restore")
        #restoreStateGridDomains(jump)
        jump += 1
        resetCells(b.x,b.y)
    #else:
        #jump = 1
        #if time_m % 10 == 0: # Backup every 5th frame
        #    backupStateGridDomains()
    drawStateGrid()
    


def wfc():
    for cell in sum(STATE_GRID, []):
        cell.getEntropy()
    
    m = 9999
    smallest_entropy = []
    for cell in sum(STATE_GRID, []):
        if not cell.collapsed:
            if cell.getEntropy() < m:
                m = cell.getEntropy()
                smallest_entropy = [cell]
            elif cell.getEntropy() == m:
                smallest_entropy.append(cell)
    
    if len(smallest_entropy) == 0:
        no_loop()
        return None,None
    
    
    next_cell = random.choice(smallest_entropy)
    next_cell.collapsed = True
    
    if len(next_cell.domain) == 0:
        #resetCells(next_cell.x, next_cell.y)
        return 2, next_cell
    
    probabilities = [ALL_TILES_HASH[x.getHash()] for x in next_cell.domain]
    next_cell.domain = random.choices(next_cell.domain, probabilities)
    
    
    # Propagate to neighbors
    #print("UACD:", next_cell.x,next_cell.y)
    if updateAdjacentCellDomains(next_cell) == 2: return 2, next_cell
    # reduceEntropy(c, 0)
    
    # Collapse len(domain) == 1 cells
    for cell in sum(STATE_GRID, []):
        if len(cell.domain) == 1 and cell.collapsed == False:
            cell.collapsed = True
            
            if updateAdjacentCellDomains(cell) == 2: return 2, cell
            #reduceEntropy(c, 0)
    
    return None,None
def updateAdjacentCellDomains(mycell, rec_depth=16):
    #print("##UACD:", mycell.x,mycell.y)
    
    if rec_depth <= 0 or mycell.checked:
        return
    if len(mycell.domain) == 0:
        #resetCells(mycell.x,mycell.y)
        return 2
    mycell.checked = True
    nbs = getNeighborCells(mycell)
    
    #print(mycell.x,mycell.y)
    #print("##NBS:", len(nbs)) 
    for nb, d in nbs:
        r = limit(mycell, nb, d)
        if r == 2: return 2
        nb.entropy = nb.getEntropy()
        #if r != None:
            
        
        if len(mycell.domain) != len(nb.domain):
           #print("RECURSE ON", nb.x,nb.y)
           if updateAdjacentCellDomains(nb, rec_depth - 1) == 2: return 2
           
        
def limit(mycell, nb, d):
    if nb.collapsed: return
    if not nb: return
    
    if len(nb.domain) == 0:
        nb.collapsed = True
    if len(mycell.domain) == 0:
        return 2
    
    valid_tiles_for_neighbor = []
    for tile_o in mycell.domain:
        valid_tiles_for_neighbor += tile_o.dir_adj[d]
    
    filtered_tiles_for_neighbor = []
    for tile_n in nb.domain:
        if tile_n in valid_tiles_for_neighbor:
            filtered_tiles_for_neighbor.append(tile_n)
    
    
    #print(len(nb.domain), len(filtered_tiles_for_neighbor))
    if len(filtered_tiles_for_neighbor) == 0: return 2
    if len(filtered_tiles_for_neighbor) < len(nb.domain):
        nb.domain = filtered_tiles_for_neighbor
    
    return True
            
def drawStateGrid():
    for cell in sum(STATE_GRID, []):
        cell.checked = False
        drawCell_center(cell=cell)

class Cell:
    def __init__(self, x,y):
        
        # A cell starts with every tile in its domain
        # Domain is a list because we're not doing weighted probabilities,
        # We're just filling the list with unique tiles that may have the same overlap data
        self.domain = [tile for tile in ALL_TILES] # So glad Python is a reference-based language
        self.entropy = self.getEntropy()
        self.checked = False
        self.collapsed = False
        self.outline = False
        
        self.x = x
        self.y = y
        
    def getEntropy(self):
        return len(self.domain)
    
    def collapse(self):
        # Choose a tile at random from the domain
        if len(self.domain) == 1: return
        
        probabilities = [ALL_TILES_HASH[x.getHash()] for x in self.domain]
        self.domain = random.choices(self.domain, probabilities)
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
    
    def getHash(self):
        return hash(self.data)
    
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
    try:
        return STATE_GRID[y][x]
    except:
        return

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
    # ALL TILES: 2116 for FlowersBig before tile reduction
    
    present_hashes = []
    for y in range(IMG_HEIGHT):
        for x in range(IMG_WIDTH):
            T = Tile(x,y, IMG)
            T.extractColorData()
            hsh = T.getHash()
            
            if hsh in ALL_TILES_HASH:
                ALL_TILES_HASH[hsh] += 1
            else:
                ALL_TILES_HASH[hsh] = 1
                ALL_TILES.append(T)
            
    
def extractTileAdjacencies():
    # For every tile, for all 4 directions, identify what tiles I am adjacent to
    print("ALL TILES:", len(ALL_TILES))
    
    for orig_tile in ALL_TILES:
        # Not checking neighbors, checking ALL tiles in the dataset
        for s in ["NORTH", "EAST", "SOUTH", "WEST"]:
            for other_tile in ALL_TILES:
                if orig_tile.isCompatible(other_tile, s):
                    orig_tile.dir_adj[s].append(other_tile)

def drawTile(x=None,y=None,tile=None):
    if x == None or y == None:
        x = tile.img_x
        y = tile.img_y
    anchor_x = x * CELL_SIZE
    anchor_y = y * CELL_SIZE
    mini_cell_size = CELL_SIZE / N
    for x in range(N):
        for y in range(N):
            colr = tile.getColorFromData(x, y)
            fill(colr)
            stroke(140)
            #no_stroke()
            rect(anchor_x + (x * mini_cell_size),
                 anchor_y + (y * mini_cell_size), mini_cell_size, mini_cell_size)

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
            stroke(190)
            #no_stroke()
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
    
    if len(cell.domain) > 1:
        colr = ("#FFAAFFFF") # Some random color

    elif len(cell.domain) == 0:
        colr = ("#FF0000FF")
    else:
        #print(cell.x,cell.y,len(cell.domain))
        colr = cell.domain[0].getColorFromData(0,0)
        
    fill(colr)
    #stroke(240)
    no_stroke()
    rect(anchor_x,
         anchor_y, CELL_SIZE, CELL_SIZE)
    #fill(255)
    #print(cell.x,cell.y,len(cell.domain))
    #text(str(len(cell.domain)), anchor_x+10, anchor_y + 10)
    
    if cell.outline:
        
        stroke(*cell.outline[1])
        cell.outline = False
        no_fill()
        rect(anchor_x,
        anchor_y, CELL_SIZE, CELL_SIZE)
        #no_loop()
    
    #if len(cell.domain) == 0:
    #    no_loop()
    #    return
