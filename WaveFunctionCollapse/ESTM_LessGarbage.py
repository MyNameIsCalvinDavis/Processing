from pprint import pprint
import operator
import time
import random
import numpy as np

NORTH = (0,-1)
EAST = (1,0)
SOUTH = (0,1)
WEST = (-1,0)

OUTW = 5
OUTH = 5

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
            weights.append(WEIGHTS[col])
        
        collapsed_value = random.choices(list_domain, weights=weights)
        self.domain = set(collapsed_value)
        self.shannonEntropy()
        self.value = collapsed_value
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
        
        self.img = load_image("patterns/{}.png".format(self.imgs[choice][0]))
    
    def getCell(self, x, y):
        return self.STATE_GRID[y][x]
    
    def updateAdjacentCellDomains(self, cell):
        x = cell.pos[0]
        y = cell.pos[1]
        print("Func call UACD on", cell.pos, x, y)
        
        stack = [cell]
        
        # Get neighbors of this cell
        while stack:
            
            print(len(stack))
            mycell = stack.pop(0)
            print("Start while on", mycell.pos)
            
            nbs = []
            for d in (NORTH, EAST, SOUTH, WEST):
                
                if ((x + d[0]) < 0 or (x + d[0]) >= OUTW or (y + d[1]) < 0 or (y + d[1]) >= OUTH):
                    continue
                print("Check neighbor in", d, "direction (", m.getCell(x+d[0], y+d[1]).pos, ")", x, y)
                #nb_c = self.STATE_GRID[y + d[1]][x + d[0]]
                nb_c = m.getCell(x+d[0], y+d[1])
                nbs.append((nb_c, d))

            # N E S W
            print("Neighbors to", mycell.pos, ":", [x[0].pos for x in nbs])
            for nb, d in nbs:
                # Where d is the direction from the original tile to the neighbor
                if len(nb.domain) == 1: continue
                if nb.pos == mycell.pos: raise
                
                # Go through my colors, m_color
                    # What in my neighbors domain conforms to m_color?
                        # Can black be to the left of m_color?
                        # Can red be to the left of m_color?
                        # Can bldef updateAdjacentCellDomainue be to the left of m_color?
                            # If no, remove that item from the domain
                self.pprint_w_colors()
                pprint(self.STATE_GRID)
                #pprint(STATE_GRID)
                #print("#########\n-- NB cell:", nb.pos, GYBtoString(nb.domain), len(nb.domain))
                print("####################")
                print("-- Compare MAIN", mycell.pos, GYBtoString(mycell.domain), " ------- ", nb.pos, GYBtoString(nb.domain))
                old_domain = len(nb.domain)
                for m_color in mycell.domain:
                    #print("====Main cell color check", mycell.pos, ":", GYBtoString(m_color))
                    invalid_domains = []
                    for n_color in nb.domain:
                        #print("====NB cell color check", nb.pos, ":", GYBtoString(n_color))
                        # Original perspectvie: Can n_color be d      from m_color? 
                        #pattern = (m_color, n_color, dirToString(getOppositeDir(d)))
                        pattern = (n_color, m_color, dirToString(getOppositeDir(d)))
                        pattern = (n_color, m_color, dirToString(d))
                        #p_pattern = (GYBtoString(n_color), GYBtoString(m_color), dirToString(getOppositeDir(d)))
                        #print("Is this pattern in PATTERNS_DICT?", p_pattern)
                        # if no pattern is found that matches (mcolor, ncolor, d)
                        if pattern not in PATTERNS_DICT:
                            # remove n_color from nb domain
                            #nb.domain.remove(n_color)
                            print("Not in there, remove", GYBtoString(n_color), "from", nb.pos, "domain")
                            invalid_domains.append(n_color)
                        else:
                            pass
                            #print("------------It's in there!!!!")
                if invalid_domains:
                    #print(type(nb.domain))
                    for invalid in invalid_domains: nb.domain.remove(invalid)
                    stack.append(nb)
                    print("add", nb.pos, "to stack")
                nb.shannonEntropy()
                
                new_domain = len(nb.domain)
                
                print("Final neighbor domain:", nb.pos, GYBtoString(nb.domain))
                
                if new_domain != old_domain:
                    #print("Old / new domain not same for", nb.pos, old_domain, new_domain)
                    #print("Add", nb.pos, "to end of cell queue")
                    #cell_queue.append(nb)
                    pass
                else:
                    pass
                    #print("OLD/NEW domain is same, skip", nb.pos)
            #print("NBs done, end of loop, next stack item:", stack[0].pos)
    
    def pickLowestEntropyCell(self):
        # Pick the lowest entropy cell
        one_d_list = sum(self.STATE_GRID, [])
        sorted_x = sorted(one_d_list, key=operator.attrgetter('se'))
        
        minn = sorted_x[0]
        options = []
        for x in sorted_x:
            if (x.se != 0) and (x.se == minn.se):
                options.append(x)
        
        options = [x for x in sorted_x if (x.se == minn.se) and (x.pos not in self.COLLAPSED)]
        try:
            a = random.choice(options)
            print("Lowest cell", a.pos)
            return a
        except:
            print("Lowest cell", minn.pos)
            return minn
    
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
                the_row.append( Cell( set([j[0] for j in PATTERNS_DICT.keys()]), (x,y)) )
            self.STATE_GRID.append(the_row)

    def pprint_w_colors(self):
        # Assuming GYB
        buffer = ""
        print("W", OUTW, "H", OUTH)
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
    global img
    global LAST_CELL
    m = Model()
    
    #size(WIDTH,HEIGHT)
    
    m.genRules()
    pprint(list(PATTERNS))
    m.initGrid()
    
    #pprint(STATE_GRID)
    
def draw():
    #image(img, 0, 0)
    #time.sleep(0.1)
    background(255)
    num_rows = OUTW
    num_cols = OUTH
    
    square_size = 20
    
    for row in range(num_rows):
        for col in range(num_cols):
            x = col * square_size
            y = row * square_size
            
            #print("Draw:", STATE_GRID[row][col].pos, STATE_GRID[row][col].domain), 
            val = 100 if len(m.STATE_GRID[row][col].domain) > 1 else m.STATE_GRID[row][col].value
            try: fill(val)
            except: fill(100)
            rect(x,y,square_size,square_size)
            fill(255)
            text(len(m.STATE_GRID[row][col].domain),x+10,y+10)
    
    #pprint_w_colors()
    
    next_cell = m.pickLowestEntropyCell()
    #print("Next Cell:", next_cell.pos)
    
    #print("Collapsing lowest cell", next_cell.pos)
    next_cell.collapse()
    #print(next_cell.pos, "=", GYBtoString(next_cell.value))
    
    #print("\n===lowest entropy cell:", next_cell.pos, next_cell.se)
    #observe(next_cell)
    
    #print("Updating adjacent cells to", next_cell.pos)
    m.updateAdjacentCellDomains(next_cell)
    #pprint(STATE_GRID)
    #pprint_w_colors()
    
    print("Finding 1 domain cells")
    # Find 1-domain cells
    one_d_list = sum(m.STATE_GRID, [])
    for x in one_d_list:
        if len(x.domain) == 1:
            
            #collapse(x.pos[0], x.pos[1])
            x.value = list(x.domain)[0]
            m.COLLAPSED.append(x.pos)
            print(x.pos, "is collapsed, len:", len(m.COLLAPSED))
            print(m.COLLAPSED[:5])
    
    #exit_sketch()


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
    d = {'#2200FFFF':"B", '#F0FF00FF':"Y", '#03FF00FF':"G"}
    if type(x) == type("S"):
        if x not in d: return x
        return d[x]
    else:
        j = [d[y] for y in x]
        return j

            




    

