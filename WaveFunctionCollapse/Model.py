# PY5 IMPORTED MODE CODE

from Tile import *
from Cell import *
import operator
import random


NORTH = (0,-1)
EAST = (1,0)
SOUTH = (0,1)
WEST = (-1,0)

OUTW = 30
OUTH = 30

PATTERNS_DICT = {}
PATTERNS = set()



class Model:
    def __init__(self, n=3):
        self.imgs = {
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
            12:("BlueDots2", 15,15)
        }
        choice = 11

        self.WIDTH = self.imgs[choice][1]
        self.HEIGHT = self.imgs[choice][2]
        self.N = 3

        self.STATE_GRID = []
        self.TILE_GRID = []
        self.COLLAPSED = []
        
        self.img = load_image("patterns/{}.png".format(self.imgs[choice][0]))
        self.img_pixels = []
    
    def getCell(self, x, y):
        return self.STATE_GRID[y][x]
    
    def getNbs(self, cell):
        x = cell.pos[0]
        y = cell.pos[1]
        
        nbs = []
        for d in (NORTH, EAST, SOUTH, WEST):
            if ((x + d[0]) < 0 or (x + d[0]) >= OUTW or (y + d[1]) < 0 or (y + d[1]) >= OUTH):
                continue
            nb_c = self.getCell(x+d[0], y+d[1])
            nbs.append((nb_c, d))
        return nbs
    
    def updateAdjacentCellDomains(self, cell):
        # Do we add a list of already visited cells? Dunno
        
        stack = [cell]
        while stack:
            mycell = stack.pop(0)
            nbs = self.getNbs(mycell) # ( (nb_cell, dirToNb_cell), ... )
            
            # N E S W
            #print("\n-- Main:", mycell.pos, mycell.domain)
            for nb, d in nbs: # d is maincell -> nb direction
                if len(nb.domain) == 1: continue
                if nb.pos == mycell.pos: raise
                
                #print("-- NB:", nb.pos, nb.domain)
                for n_color in nb.domain.copy():
                    for m_color in mycell.domain.copy():
                        pattern = (n_color, m_color, dirToString(d))
                        
                        #print("Is", pattern, "in PATTERNS_DICT?", end=" ")
                        if pattern in PATTERNS_DICT:
                            #print(pattern in PATTERNS_DICT)
                            #print("Yes, go to next NB tile")
                            break
                        else:
                            pass
                            #print("No, check next main tile")
                    else:
                        #print("Remove", n_color, "from neighbor cell", nb.pos)
                        nb.domain.remove(n_color)
                        stack.append(nb)
                
                nb.shannonEntropy()
                #print("Final NB domain", nb.pos, len(nb.domain), nb.domain)
        # After the stack is empty, collapse all of the 1-domain cells
        one_d_list = sum(self.STATE_GRID, [])
        for x in one_d_list:
            if len(x.domain) == 1 and x.pos not in self.COLLAPSED:
                x.collapse()
                self.COLLAPSED.append(x.pos)
    
    def pickLowestEntropyCell(self):
        sorted_x = sorted(
            sum(self.STATE_GRID, []),
            key=operator.attrgetter('se')
        )
        #print([float(x.se) for x in sorted_x])
        # Return the lowest non-zero entropy
        options = []
        for x in sorted_x:
            if (len(x.domain) > 1) and (x.se >= sorted_x[0].se):
                options.append(x)
        #print([(float(x.se), x.pos) for x in options])
        try:
            return random.choice(options)
        except Exception as e:
            #print(e)
            return sorted_x[0]
    
    def getIndex(self, x, y):
        return x + y * self.WIDTH
    
    def getTile(self, x, y):
        # Return tile from tile index
        if x >= len(self.TILE_GRID[0]) or x < 0: return
        if y >= len(self.TILE_GRID) or y < 0: return
        return self.TILE_GRID[y][x]
    
    def genRules(self):
        self.img.load_pixels()
        self.img_pixels = [hex_color(x) for x in self.img.pixels]
        
        numberOf = {}
        weights = {}
        color_mode(RGB)
        
        # Process image into Tiles, add to Tile Grid
        for y in range(0, self.HEIGHT, self.N):
            row = []
            for x in range(0, self.WIDTH, self.N):
                
                # Extract NxN section at x,y
                cell_rows = []
                for i in range(self.N):
                    y_idx = self.getIndex(x, y + i)
                    # With that y index, get the associated x values & turn into a Tile
                    
                    cell_rows.append( tuple(self.img_pixels[y_idx : y_idx+self.N]) )
                new_tile = Tile(tuple(cell_rows))
                
                if new_tile in numberOf: numberOf[new_tile] += 1
                else: numberOf[new_tile] = 1
                
                # Weights
                if new_tile in weights: weights[str(new_tile)] += 1
                else: weights[str(new_tile)] = 1
                
                row.append(new_tile)
            self.TILE_GRID.append(row)
        
        # Process Tile Grid into patterns
        for i,row in enumerate(self.TILE_GRID):
            for j,tile in enumerate(row):
                
                # Check N E S W
                for d in (NORTH, EAST, SOUTH, WEST):
                    
                    nb_tile = self.getTile(j + d[0], i + d[1])
                    if not nb_tile: continue
                    
                    # tile can be opp<d> of nb_tile
                    pattern = (str(tile), str(nb_tile), dirToString(getOppositeDir(d)))
                    
                    if pattern in PATTERNS_DICT: PATTERNS_DICT[pattern] += 1
                    else: PATTERNS_DICT[pattern] = 1
                    
                    PATTERNS.add(pattern)
        for k,v in weights.items():
            WEIGHTS[k] = v / (self.WIDTH * self.HEIGHT)
            
    def initGrid(self):
        for y in range(OUTH):
            the_row = []
            for x in range(OUTW):
                the_row.append(
                    Cell( set( [j[0] for j in PATTERNS_DICT.keys()] ), 
                          (x,y)
                    )
                )
                
            self.STATE_GRID.append(the_row)

    def pprint_w_colors(self):
        # Assuming GYB
        buffer = ""
        for y in range(OUTH):
            for x in range(OUTW):
                if len(self.getCell(x,y).domain) > 1:
                    buffer += str(self.getCell(x,y)) + " "
                else:
                    buffer += GYBtoString(list(self.getCell(x,y).domain)[0]) + " "
            buffer += "\n"
        print(buffer)

def getOppositeDir(di):
   if (di == NORTH): return SOUTH
   if (di == SOUTH): return NORTH
   if (di == EAST): return WEST
   if (di == WEST): return EAST
   else: raise

def dirToString(di):
   if (di == NORTH): return "N"
   if (di == SOUTH): return "S"
   if (di == EAST): return "E"
   if (di == WEST): return "W"
   else: raise
                        
def StringToDir(di):
    if (di == "N"): return NORTH
    if (di == "S"): return SOUTH
    if (di == "E"): return EAST
    if (di == "W"): return WEST
    else: raise


def GYBtoString(x):
    d = {'#2200FFFF':"B", '#F0FF00FF':"Y", '#03FF00FF':"G", '#FFFFFFFF':"W"}
    if type(x) == type("S"):
        if x not in d: return x
        return d[x]
    elif type(x) == type((1,2,3)):
        l = list(x)
        for item in range(len(l)):
            if l[item] in d: l[item] = d[l[item]]
        return tuple(l)
    else:
        j = [d[y] for y in x]
        return j
