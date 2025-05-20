from pprint import pprint
import random

WIDTH = 3;
HEIGHT = 3;

OUTW = 10
OUTH = 10

NORTH = (0,-1);
EAST = (1,0);
SOUTH = (0,1);
WEST = (-1,0);

PATTERNS_DICT = {}
PATTERNS = set()
WEIGHTS = {}


def setup():
    global img
    size(WIDTH,HEIGHT)
    img = load_image("patterns/Pattern2.png")
    genRules()
    initGrid()
    
    # Manually collapse one cell
    STATE_GRID[0][0].value = '-0x222223'
    STATE_GRID[0][0].domain = {('-0x222223', '-0x222223', 'W')} # Some random domain item
    updateAdjacentCellDomains(0, 0)
    
    pprint(STATE_GRID)

def draw():
    image(img, 0, 0)
    exit_sketch()

def genRules():
    global img
    global PATTERNS_DICT
    global WEIGHTS
    img.load_pixels()
    
    numberOf = {}
    weights = {}
    
    # Make Patterns
    for y in range(HEIGHT):
        for x in range(WIDTH):
            loc = getIndex(x, y)
            c = hex(img.pixels[loc])
            
            if c in numberOf: numberOf[c] += 1
            else: numberOf[c] = 1
            
            # Weights
            if c in weights: weights[c] += 1
            else: weights[c] = 1
            
            # Check N E S W
            
            for d in (NORTH, EAST, SOUTH, WEST):
                dir_loc = getIndex(x + d[0], y + d[1])
                if (dir_loc < 0 or dir_loc >= WIDTH * HEIGHT or (x + d[0]) >= WIDTH or (x + d[0]) < 0 or (y + d[1]) >= HEIGHT or (y + d[1]) < 0):
                    continue
                # print(x, y, c, "===", x + d[0], y + d[1])
                checked_dir = hex(img.pixels[dir_loc])
                pattern = (c, checked_dir, dirToString(getOppositeDir(d)))
                # print(pattern)
                if pattern in PATTERNS_DICT: PATTERNS_DICT[pattern] += 1
                else: PATTERNS_DICT[pattern] = 1
                
                PATTERNS.add(pattern)
    pprint(PATTERNS_DICT)
    
    # Weight calc
    for k,v in weights.items():
        WEIGHTS[k] = v / (WIDTH * HEIGHT)

def updateAdjacentCellDomains(x, y, already_updated=[]):
    mycell = STATE_GRID[y][x]
    
    # Get neighbors of this cell
    nbs = []
    for d in (NORTH, EAST, SOUTH, WEST):
        if ((x + d[0]) < 0 or (x + d[0]) >= OUTH or (y + d[1]) < 0 or (y + d[1]) >= OUTH):
            continue
        
        nb_c = STATE_GRID[y + d[1]][x + d[0]]
        if nb_c in already_updated:
            continue
        else:
            nbs.append((nb_c, d))
            
        #print(x + d[0],y + d[1])
    
    print("Main cell:", x, y, "== neighbors:", len(nbs))
    
    # Find my possible cell types
    possible_cell_types = set([x[0] for x in mycell.domain])
    if len(possible_cell_types) == 0: raise("Possible cell types is 0, I should already be collapsed with 0 domain & not an option")

    
    for nb, d in nbs:
        # Where d is the direction from the original tile to the neighbor
        
        # Pick a neighbor not in already_updated
        if nb in already_updated: continue
        
        # Do the complicated calc on that neighbor with rules
        filters = []
        
        # As a neighbor, either i'm collapsed or I'm not
        # If I'm not, I have multiple possibilities in the form of
        # (Me, originalTile, directionFromOriginalToMe)
        # Where the sum of "Me"s is all possible tiles I may assume
        nb_possible_cell_types = set([x[0] for x in nb.domain])
        
        # If I am collapsed, I don't need to be checked anyway and I must have been missed somehow
        # in whatever calculation collapses cells... I should alert to that
        # I should already be part of the already_updated list. Why am I not?
        if len(nb_possible_cell_types) == 0: raise("Ruh roh raggy - possible cell types is 0 for this neighbor because I'm already collapsed")
        
        print("Main Cel:", mycell.pos, "== possible cell types:", possible_cell_types)
        print("Neighbor:", nb.pos, "== possible cell types:", nb_possible_cell_types)
        
        
        # Generate a filter (A, B, X)
        # Find directionFromOriginalToMe, dir
        # Find directionFromMeToOriginal, opposite(dir)
        # Find color(s) of original tile, orig
        # Find my (nb) color, nbc
        
        # Loop through original's possible colors:
            # Find all patterns in original's domain that conform to: (orig, _, opposite(dir))
            # Find all patterns in neighbor's domain that conform to: (_   , orig, dir)
            # Maintain two lists
        
        filter1 = []
        filter2 = []
        for orig in possible_cell_types:
            print("Evaluating orig:", orig)
            for pattern in mycell.domain:
                print(pattern[0], "==", orig, pattern[0] == orig, "\t", pattern[2], "==", dirToString(getOppositeDir(d)), pattern[2] == dirToString(getOppositeDir(d))) 
                if pattern[0] == orig and pattern[2] == dirToString(getOppositeDir(d)):
                    filter1.append(pattern)
            for pattern in nb.domain:
                print(pattern[1], "==", orig, pattern[1] == orig, "\t", pattern[2], "==", dirToString(d), pattern[2] == dirToString(d)) 
                if pattern[1] == orig and pattern[2] == dirToString(d):
                    filter2.append(pattern)
        print(filter1, filter2)
        break
        
        # Union the two, set neighbor domain equal to the result
        
        # If I am collapsed, use my value to decide what my neighbors are
        # If I am not collapsed, take all the 
            # Because I'm this, you can no longer be that
            # Recalc entropy
        # Add that neighbor to the already_updated list
        # If that neighbors domain changes, recurse
        already_updated.append(nb)

def initGrid():
    global STATE_GRID
    global PATTERNS_DICT
    
    STATE_GRID = [[Cell(PATTERNS, (x,y)) for x in range(OUTW)] for y in range(OUTH)]

def getIndex(x, y):
    return x + y * WIDTH

def getOppositeDir(di):
   if (di == NORTH): return SOUTH
   if (di == SOUTH): return NORTH
   if (di == EAST): return WEST
   if (di == WEST): return EAST
   else:
       print("GOD:", di)

def dirToString(di):
   if (di == NORTH): return "N"
   if (di == SOUTH): return "S"
   if (di == EAST): return "E"
   if (di == WEST): return "W"

def shannonEntropy(domain):
        result = 0
        for t in domain:
            result += WEIGHTS[t[0]] * log(WEIGHTS[t[0]])
        return round(result, 4)

class Cell:
    def __init__(self, d, pos):
        self.domain = d
        self.pos = pos
        self.value = None
        self.se = shannonEntropy(d)
    def __str__(self):
        return str(len(self.domain))
    def __repr__(self):
        return self.__str__()
    

