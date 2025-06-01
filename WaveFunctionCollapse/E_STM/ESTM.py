from pprint import pprint
import operator
import time
import random
import numpy as np

NORTH = (0,-1)
EAST = (1,0)
SOUTH = (0,1)
WEST = (-1,0)

OUTW = 20
OUTH = 20

PATTERNS_DICT = {}
PATTERNS = set()
WEIGHTS = {}

class Cell:
    def __init__(self, d, pos):
        self.domain = d
        self.pos = pos
        self.value = None
        self.se = 0
    def __str__(self):
        return str(len(self.domain))
        #return str(self.se)
    def __repr__(self):
        return self.__str__()

    def shannonEntropy(self):
        result = 0
        for t in self.domain:
            result += WEIGHTS[t] * log(WEIGHTS[t])
        self.se = round(-result, 4)
        
    def collapse(self):
        # Collapse the cell into a single domain, chosen randomly & weighted
        
        # Pick a cell from a domain, weighted
        # {'#FFFFFFFF': 0.8125, '#03FF00FF': 0.0625, '#001CFFFF': 0.0625, '#FF0000FF': 0.0625}
        weights = []
        list_domain = list(self.domain) # Sets are unordered
        for col in list_domain:
            weights.append(WEIGHTS[col]*10)
        
        collapsed_value = random.choices(list_domain, weights=weights)
        self.domain = set(collapsed_value)
        self.shannonEntropy()
        self.value = collapsed_value[0]
        if len(self.domain) == 0: raise

class Model:
    def __init__(self):
        self.imgs = {
            3:("Pattern3", 3,3),
            2:("Pattern2", 3,3),
            5:("Pattern5", 5,5),
            4:("Pattern4", 3,3),
            1:("Flower", 10,10),
            6:("Pattern6", 4,4),
            7:("FlowersBig", 46,46),
            8:("BeachLand2", 20,10),
            9:("BeachLand3", 10,5),
            10:("BeachLand4", 4,7)
        }
        choice = 10

        self.WIDTH = self.imgs[choice][1]
        self.HEIGHT = self.imgs[choice][2]

        self.STATE_GRID = []
        self.COLLAPSED = []
        
        self.img = load_image("../patterns/{}.png".format(self.imgs[choice][0]))
    
    def getCell(self, x, y):
        return self.STATE_GRID[y][x]
    
    def getNbs(self, cell):
        x = cell.pos[0]
        y = cell.pos[1]
        
        nbs = []
        for d in (NORTH, EAST, SOUTH, WEST):
            if ((x + d[0]) < 0 or (x + d[0]) >= OUTW or (y + d[1]) < 0 or (y + d[1]) >= OUTH):
                continue
            nb_c = m.getCell(x+d[0], y+d[1])
            nbs.append((nb_c, d))
        return nbs
    
    def updateAdjacentCellDomains(self, cell):
        # Do we add a list of already visited cells? Dunno
        
        stack = [cell]
        while stack:
            mycell = stack.pop(0)
            nbs = self.getNbs(mycell) # ( (nb_cell, dirToNb_cell), ... )
            
            # N E S W
            for nb, d in nbs: # d is maincell -> nb direction
                if len(nb.domain) == 1: continue
                if nb.pos == mycell.pos: raise

                invalid_domains = []
                for n_color in nb.domain.copy():
                    for m_color in mycell.domain.copy():
                        pattern = (n_color, m_color, dirToString(d))
                        
                        if pattern in PATTERNS_DICT: break
                    else:
                        invalid_domains.append(n_color)
                        nb.domain.remove(n_color)
                        stack.append(nb)
                
                nb.shannonEntropy()
        
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
        
        # Return the lowest non-zero entropy
        options = []
        for x in sorted_x:
            if (len(x.domain) > 1) and (x.se >= sorted_x[0].se):
                options.append(x)
        
        try:
            return random.choice(options)
        except:
            return sorted_x[0]
    
    def getIndex(self, x, y):
        return x + y * self.WIDTH
    
    def genRules(self):
        self.img.load_pixels()
        
        numberOf = {}
        weights = {}
        color_mode(RGB)
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                loc = self.getIndex(x, y)
                c = hex_color(self.img.pixels[loc])

                if c in numberOf: numberOf[c] += 1
                else: numberOf[c] = 1
                
                # Weights
                if c in weights: weights[c] += 1
                else: weights[c] = 1
                
                # Check N E S W
                for d in (NORTH, EAST, SOUTH, WEST):
                    dir_loc = self.getIndex(x + d[0], y + d[1])
                    if (dir_loc < 0 or dir_loc >= self.WIDTH * self.HEIGHT or (x + d[0]) >= self.WIDTH or (x + d[0]) < 0 or (y + d[1]) >= self.HEIGHT or (y + d[1]) < 0):
                        continue
                    
                    checked_dir = hex_color(self.img.pixels[dir_loc])
                    pattern = (c, checked_dir, dirToString(getOppositeDir(d)))
                    
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

m = 0
def setup():
    global m
    size(OUTW*20,OUTH*20)
    m = Model()
    m.genRules()
    for pattern in list(PATTERNS):
        print(GYBtoString(pattern[0]), GYBtoString(pattern[1]), pattern[2])
    pprint(list(PATTERNS))
    m.initGrid()
    
def draw():
    
    background(255)
    square_size = 20
    for row in range(OUTW):
        for col in range(OUTH):
            x = col * square_size
            y = row * square_size
            
            val = 100 if len(m.STATE_GRID[row][col].domain) > 1 else m.STATE_GRID[row][col].value
            try: fill(val)
            except: fill(100)
            rect(x,y,square_size,square_size)
            fill(255)
            text(len(m.STATE_GRID[row][col].domain),x+10,y+10)
    
    next_cell = m.pickLowestEntropyCell()
    next_cell.collapse()
    m.updateAdjacentCellDomains(next_cell)

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

            




    

