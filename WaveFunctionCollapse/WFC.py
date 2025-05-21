from pprint import pprint
import operator
import time
import random
import numpy as np

WIDTH = 5;
HEIGHT = 5;

OUTW = 10
OUTH = 10

NORTH = (0,-1);
EAST = (1,0);
SOUTH = (0,1);
WEST = (-1,0);

PATTERNS_DICT = {}
PATTERNS = set()
WEIGHTS = {}

COLLAPSED = []

def setup():
    global img
    global LAST_CELL
    size(OUTW*20,OUTH*20)
    #size(WIDTH,HEIGHT)
    img = load_image("patterns/Pattern5.png")
    genRules()
    pprint(list(PATTERNS))
    initGrid()
    pprint(STATE_GRID)
    
def draw():
    #image(img, 0, 0)
    time.sleep(0.1)
    background(255)
    num_rows = OUTW
    num_cols = OUTH
    
    square_size = 20
    
    for row in range(num_rows):
        for col in range(num_cols):
            x = col * square_size
            y = row * square_size
            
            #print("Draw:", STATE_GRID[row][col].pos, STATE_GRID[row][col].domain), 
            val = 100 if len(STATE_GRID[row][col].domain) > 1 else STATE_GRID[row][col].value
            try: fill(val)
            except: fill(100)
            rect(x,y,square_size,square_size)
            fill(255)
            text(len(STATE_GRID[row][col].domain),x+10,y+10)
    
    #pprint(STATE_GRID)
    
    next_cell = pickLowestEntropyCell()
    print("Next Cell:", next_cell.pos)
    
    #print("Collapsing lowest cell", next_cell.pos)
    collapse(next_cell.pos[0], next_cell.pos[1])
    print(next_cell.pos, "=", next_cell.value)
    
    # print("\n===lowest entropy cell:", next_cell.pos, next_cell.se)
    #observe(next_cell)
    
    #print("Updating adjacent cells to", next_cell.pos)
    updateAdjacentCellDomains(next_cell.pos[0], next_cell.pos[1], [next_cell])
    #pprint(STATE_GRID)
    
    #print("Finding 1 domain cells")
    # Find 1-domain cells
    one_d_list = sum(STATE_GRID, [])
    for x in one_d_list:
        if len(x.domain) == 1:
            #collapse(x.pos[0], x.pos[1])
            x.value = list(x.domain)[0]
    
    #exit_sketch()

'''
def observe(cell):
    #print("OBSERVING CELL:", cell.pos, len(cell.domain))
    #print("Current domain:", cell.domain)
    r = random.choice(list(cell.domain))
    #print("Randomly choose:", r)
    cell.domain = set()
    cell.domain.add(r)
    #print("new cell domain:", cell.domain, len(cell.domain))
    #print(cell.domain)
    collapse(cell.pos[0], cell.pos[1])
'''

def genRules():
    global img
    global PATTERNS_DICT
    global WEIGHTS
    img.load_pixels()
    
    numberOf = {}
    weights = {}
    
    # Make Patterns
    color_mode(RGB)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            loc = getIndex(x, y)
            c = hex_color(img.pixels[loc])

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
                # #print(x, y, c, "===", x + d[0], y + d[1])
                checked_dir = hex_color(img.pixels[dir_loc])
                pattern = (c, checked_dir, dirToString(getOppositeDir(d)))
                # #print(pattern)
                if pattern in PATTERNS_DICT: PATTERNS_DICT[pattern] += 1
                else: PATTERNS_DICT[pattern] = 1
                
                PATTERNS.add(pattern)
    #pprint(PATTERNS_DICT)
    
    # Weight calc
    for k,v in weights.items():
        WEIGHTS[k] = v / (WIDTH * HEIGHT)

def pickLowestEntropyCell():
    one_d_list = sum(STATE_GRID, [])
    sorted_x = sorted(one_d_list, key=operator.attrgetter('se'))
    for x in sorted_x:
        if x.se != 0 and x.pos not in COLLAPSED:
            return x

def collapse(x, y):
    #print("Collapsing cell", x, y)
    cell = STATE_GRID[y][x]
    
    # Pick a cell from a domain, weighted
    # {'#FFFFFFFF': 0.8125, '#03FF00FF': 0.0625, '#001CFFFF': 0.0625, '#FF0000FF': 0.0625}
    weights = []
    domain = list(cell.domain) # sets are unordered
    for col in domain:
        weights.append(WEIGHTS[col])

    domain = set(random.choices(domain, weights=weights))
    #print(domain)
    cell.domain = domain
    cell.se = shannonEntropy(cell.domain)
    COLLAPSED.append(cell.pos)
    #print("final collapsed cell:", cell.pos, cell.domain, cell.se)
    if len(cell.domain) == 0: raise
    
    
    #print("Cell", cell.pos, "domains:", len(cell.domain))
    #if len(cell.domain) == 1:
    #    cell.value = list(cell.domain)[0]
    #    cell.domain = {}
    #    cell.se = shannonEntropy(cell.domain)
    #print("Final collapsed cell", cell.pos)
    #print(cell.value, cell.domain, cell.se)
    #pprint(STATE_GRID)
    #COLLAPSED.append(cell.pos)

def updateAdjacentCellDomains(x, y, already_updated=[], cell_queue=[]):
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

    #print("\nMain cell:", x, y, "== neighbors:", len(nbs), mycell.domain)
    
    # Find my possible cell types
    
    # N E S W
    for nb, d in nbs:
        # Where d is the direction from the original tile to the neighbor
        
        
        # Go through my colors, m_color
            # What in my neighbors domain conforms to m_color?
                # Can black be to the left of m_color?
                # Can red be to the left of m_color?
                # Can blue be to the left of m_color?
                    # If no, remove that item from the domain
        #print("#########\n-- NB cell:", nb.pos, nb.domain, len(nb.domain))
        old_domain = len(nb.domain)
        for m_color in mycell.domain:
            #print("====Main cell color check", mycell.pos, ":", m_color)
            invalid_domains = []
            for n_color in nb.domain:
                #print("====NB cell color check", nb.pos, ":", n_color)
                # Original perspectvie: Can n_color be d      from m_color? 
                pattern = (m_color, n_color, dirToString(getOppositeDir(d)))
                #print("Is this pattern in PATTERNS_DICT?", pattern)
                # if no pattern is found that matches (mcolor, ncolor, d)
                if pattern not in PATTERNS_DICT:
                    # remove n_color from nb domain
                    #nb.domain.remove(n_color)
                    #print("Not in there, remove", n_color, "from", nb.pos, "domain")
                    invalid_domains.append(n_color)
                else:
                    pass
                    #print("------------It's in there!!!!")
        for invalid in invalid_domains: nb.domain.remove(invalid)
        nb.se = shannonEntropy(nb.domain)
        
        new_domain = len(nb.domain)
        
        if new_domain != old_domain:
            #print("Old / new domain not same for", nb.pos, old_domain, new_domain)
            #print("Add", nb.pos, "to end of cell queue")
            cell_queue.append(nb)
        else:
            pass
            #print("OLD/NEW domain is same, skip", nb.pos)
    
    try:
        front = cell_queue.pop(0)
        updateAdjacentCellDomains(front.pos[0], front.pos[1], already_updated, cell_queue)
    except:
        return
                
                
    '''
    possible_cell_types = mycell.domain
    if len(possible_cell_types) == 0: #raise("Possible cell types is 0, I should already be collapsed with 0 domain & not an option")
        possible_cell_types = [mycell.value]

    
    for nb, d in nbs:
        #print("\nMain Cel:", mycell.pos, "== possible cell types:", possible_cell_types)
        #print("Neig Cel:", nb.pos)
        #print("--", nb.domain)
        # valid patterns
        # For every color represented in the original domain,
            # For every color in my (nb) domain,
                # Flip the direction to neighbor > original (it starts as original > neighbor)
                # Create the following pattern X: (nb_color , orig_colr , flip_direction)
                # If X is in my global patterns,
                    # add X to valid patterns
        
        # new_domain = [x[0] for x in valid_patterns]
        
        valid_patterns = []
        #print("Finding valid patterns for cell")
        for o_color in possible_cell_types:
            #print("Check original cell color:", o_color)
            for n_color in nb.domain:
                #print("Check neighbor cell color:", n_color)
                new_dir = dirToString(getOppositeDir(d))
                X = (n_color, o_color, new_dir)
                #print("Find this pattern: ", X)
                if X in PATTERNS_DICT:
                    #print("Found")
                    valid_patterns.append(X)
        
        new_domain = set([x[0] for x in valid_patterns])
        old_domain = nb.domain
        #print("New / old domain:", new_domain, old_domain)
        
        
        already_updated.append(nb)
        
        if new_domain != old_domain:
            #print("Domain not the same, add", nb.pos, "to cell queue")
            nb.domain = new_domain
            cell_queue.append(nb)
        else:
            #print("Domain is the same between", mycell.pos, nb.pos)
            pass
        try:
            #pprint(STATE_GRID)
            
            front = cell_queue.pop(0)
            #print("Pop front of queue, eval:", front.pos)
            #print("Recurse on front", front.pos)
            updateAdjacentCellDomains(front.pos[0], front.pos[1], already_updated, cell_queue)
        except Exception as e:
            #print("--", e)
            #print("Returning from cell, original:", mycell.pos, "nb:", nb.pos)
            return
        
        ####################
        valid = []
        #print("Checking patterns of nb")
        for nb_pattern in nb.domain:
            if (nb_pattern[1] in possible_cell_types) and (nb_pattern[2] == dirToString(getOppositeDir(d))):
                valid.append(nb_pattern)
        
        
        old_length = len(nb.domain)
        new_length = len(valid)
        #print("Old / new", old_length, new_length)
        
        nb.domain = valid
        already_updated.append(nb)
        
        if old_length != new_length:
            #print("Add", nb.pos, "to cell queue")
            # Add this neighbor to cell queue
            cell_queue.append(nb)
        
    try:
        #pprint(STATE_GRID)
        #print("Pop front of queue")
        front = cell_queue.pop(0)
        #print("Front of cell queue:", front.pos)
        #print("Recurse on front", front.pos)
        updateAdjacentCellDomains(front.pos[0], front.pos[1], already_updated, cell_queue)
    except:
        return
        '''
        


def initGrid():
    global STATE_GRID
    global PATTERNS_DICT
    
    #domain = set([x[0] for x in PATTERNS_DICT.keys()])
    STATE_GRID = [[Cell(set([x[0] for x in PATTERNS_DICT.keys()]), (x,y)) for x in range(OUTW)] for y in range(OUTH)]

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
                        
def StringToDir(di):
    if (di == "N"): return NORTH
    if (di == "S"): return SOUTH
    if (di == "E"): return EAST
    if (di == "W"): return WEST              

def shannonEntropy(domain):
        result = 0
        for t in domain:
            result += WEIGHTS[t] * log(WEIGHTS[t])
        result = -result
        return round(result, 4)

class Cell:
    def __init__(self, d, pos):
        self.domain = d
        self.pos = pos
        self.value = None
        self.se = shannonEntropy(d)
    def __str__(self):
        return str(len(self.domain))
        #return str(self.se)
    def __repr__(self):
        return self.__str__()
    

