from pprint import pprint
import operator
import time
import random
import numpy as np

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

    def shannonEntropy(self):
        result = 0
        for t in domain:
            result += WEIGHTS[t] * log(WEIGHTS[t])
        self.se = round(-result, 4)
        
    def collapse(self):
        # cell = STATE_GRID[y][x]
        
        # Pick a cell from a domain, weighted
        # {'#FFFFFFFF': 0.8125, '#03FF00FF': 0.0625, '#001CFFFF': 0.0625, '#FF0000FF': 0.0625}
        weights = []
        list_domain = list(self.domain) # Sets are unordered
        for col in list_domain:
            weights.append(WEIGHTS[col])

        domain = set(random.choices(domain, weights=weights))
        cell.domain = domain.copy()
        cell.se = shannonEntropy(cell.domain)
        cell.value = list(domain.copy())[0]
        self.COLLAPSED.append(cell.pos)
        if len(cell.domain) == 0: raise

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
        self.choice = 10

        self.WIDTH = self.imgs[choice][1]
        self.HEIGHT = self.imgs[choice][2]

        self.OUTW = 15
        self.OUTH = 15

        self.NORTH = (0,-1);
        self.EAST = (1,0);
        self.SOUTH = (0,1);
        self.WEST = (-1,0);

        self.PATTERNS_DICT = {}
        self.PATTERNS = set()
        self.WEIGHTS = {}
        self.STATE_GRID = []

        self.COLLAPSED = []
        
        self.img = load_image("patterns/{}.png".format(self.imgs[self.choice][0]))
    

    
    def pickLowestEntropyCell(self.):
        one_d_list = sum(self.STATE_GRID, [])
        sorted_x = sorted(one_d_list, key=operator.attrgetter('se'))
        minn = sorted_x[0]
        options = []
        for x in sorted_x:
            if (x.se != 0) and (x.pos not in self.COLLAPSED) and (x.se == minn.se):
                options.append(x)
        try:
            a = random.choice(options)
            print("Lowest cell", a.pos)
            return a
        except:
            print("Lowest cell", minn.pos)
            return minn
    
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
                    if (dir_loc < 0 or dir_loc >= WIDTH * HEIGHT or (x + d[0]) >= WIDTH or (x + d[0]) < 0 or (y + d[1]) >= HEIGHT or (y + d[1]) < 0):
                        continue
                    
                    checked_dir = hex_color(img.pixels[dir_loc])
                    pattern = (c, checked_dir, dirToString(getOppositeDir(d)))
                    
                    if pattern in PATTERNS_DICT: PATTERNS_DICT[pattern] += 1
                    else: PATTERNS_DICT[pattern] = 1
                    
                    PATTERNS.add(pattern)
        for k,v in weights.items():
            self.WEIGHTS[k] = v / (WIDTH * HEIGHT)
            
    def initGrid(self):
        for row in range(self.OUTH):
            the_row = []
            for col in range(self.OUTW):
                the_row.append( Cell(set([x[0] for x in PATTERNS_DICT.keys()]), (row,col)) )
            self.STATE_GRID.append(the_row)

    def getIndex(self, x, y):
        return x + y * WIDTH

    def getOppositeDir(self, di):
       if (di == self.NORTH): return self.SOUTH
       if (di == self.SOUTH): return self.NORTH
       if (di == self.EAST): return self.WEST
       if (di == self.WEST): return self.EAST
       else: raise

    def dirToString(self, di):
       if (di == NORTH): return "N"
       if (di == SOUTH): return "S"
       if (di == EAST): return "E"
       if (di == WEST): return "W"
       else: raise
                            
    def StringToDir(self, di):
        if (di == "N"): return NORTH
        if (di == "S"): return SOUTH
        if (di == "E"): return EAST
        if (di == "W"): return WEST
        else: raise

def setup():
    global img
    global LAST_CELL
    size(OUTW*20,OUTH*20)
    #size(WIDTH,HEIGHT)
    
    genRules()
    pprint(list(PATTERNS))
    initGrid()
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
            val = 100 if len(STATE_GRID[row][col].domain) > 1 else STATE_GRID[row][col].value
            try: fill(val)
            except: fill(100)
            rect(x,y,square_size,square_size)
            fill(255)
            text(len(STATE_GRID[row][col].domain),x+10,y+10)
    
    #pprint_w_colors()
    
    next_cell = pickLowestEntropyCell()
    #print("Next Cell:", next_cell.pos)
    
    #print("Collapsing lowest cell", next_cell.pos)
    collapse(next_cell.pos[0], next_cell.pos[1])
    #print(next_cell.pos, "=", GYBtoString(next_cell.value))
    
    #print("\n===lowest entropy cell:", next_cell.pos, next_cell.se)
    #observe(next_cell)
    
    #print("Updating adjacent cells to", next_cell.pos)
    updateAdjacentCellDomains(next_cell.pos[0], next_cell.pos[1])
    #pprint(STATE_GRID)
    #pprint_w_colors()
    
    print("Finding 1 domain cells")
    # Find 1-domain cells
    one_d_list = sum(STATE_GRID, [])
    for x in one_d_list:
        if len(x.domain) == 1:
            
            #collapse(x.pos[0], x.pos[1])
            x.value = list(x.domain)[0]
            COLLAPSED.append(x.pos)
            print(x.pos, "is collapsed, len:", len(COLLAPSED))
            print(COLLAPSED[:5])
    
    #exit_sketch()







def pprint_w_colors():
    # Assuming GYB
    buffer = ""
    for row in STATE_GRID:
        for col in row:
            if len(col.domain) > 1:
                #print(col, end=" ")
                buffer += str(col) + " "
            else:
                buffer += GYBtoString(list(col.domain)[0]) + " "
        buffer += "\n"
    print(buffer)

def updateAdjacentCellDomains(x, y):
    print("Func call UACD on", x,y)
    mycell = STATE_GRID[y][x]
    
    stack = [mycell]
    
    # Get neighbors of this cell
    while stack:
        
        print(len(stack))
        mycell = stack.pop(0)
        print("Start while on", mycell.pos)
        
        nbs = []
        for d in (NORTH, EAST, SOUTH, WEST):
            if ((x + d[0]) < 0 or (x + d[0]) >= OUTH or (y + d[1]) < 0 or (y + d[1]) >= OUTH):
                continue
            
            nb_c = STATE_GRID[y + d[1]][x + d[0]]
            nbs.append((nb_c, d))

        # N E S W
        for nb, d in nbs:
            # Where d is the direction from the original tile to the neighbor
            if len(nb.domain) == 1: continue
            
            # Go through my colors, m_color
                # What in my neighbors domain conforms to m_color?
                    # Can black be to the left of m_color?
                    # Can red be to the left of m_color?
                    # Can blue be to the left of m_color?
                        # If no, remove that item from the domain
            pprint_w_colors()
            #pprint(STATE_GRID)
            print("#########\n-- NB cell:", nb.pos, GYBtoString(nb.domain), len(nb.domain))
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
            nb.se = shannonEntropy(nb.domain)
            
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
        
        
def GYBtoString(x):
    d = {'#2200FFFF':"B", '#F0FF00FF':"Y", '#03FF00FF':"G"}
    if type(x) == type("S"):
        if x not in d: return x
        return d[x]
    else:
        j = [d[y] for y in x]
        return j

            




    

