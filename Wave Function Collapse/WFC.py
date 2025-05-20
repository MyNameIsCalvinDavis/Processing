from pprint import pprint

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
    STATE_GRID[0][0].value = list(WEIGHTS.keys())[0]
    STATE_GRID[0][0].domain = {}
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
    mycell = STATE_GRID[getIndex(x, y)]
    
    # Get neighbors of this cell
    nbs = []
    for d in (NORTH, EAST, SOUTH, WEST):
        if ((x + d[0]) < 0 or (x + d[0]) >= OUTH or (y + d[1]) < 0 or (y + d[1]) >= OUTH):
            continue
        
        nb_c = STATE_GRID[x + d[0]][y + d[1]]
        if nb_c in already_updated:
            continue
        else:
            nbs.append(nb_c)
            already_updated.append(nb_c)
        #print(x + d[0],y + d[1])
    
    # Pick a neighbor not in already_updated
        # Do the complicated calc on that neighbor with rules
            # Because I'm this, you can no longer be that
            # Recalc entropy
        # Add that neighbor to the already_updated list
        # If that neighbors domain changes, recurse
        

def initGrid():
    global STATE_GRID
    global PATTERNS_DICT
    
    STATE_GRID = [[Cell(PATTERNS) for x in range(OUTW)] for y in range(OUTH)]

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
    def __init__(self, p):
        self.domain = p
        self.value = None
        self.se = shannonEntropy(p)
    def __str__(self):
        return str(len(self.domain))
    def __repr__(self):
        return self.__str__()
    
# run_sketch()
