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
            4:("Pattern4", 2,2),
            1:("Flower", 5,5),
            6:("Pattern6", 4,4),
            7:("FlowersBig", 46,46),
            8:("BeachLand2", 20,10), # Complex big one
            9:("BeachLand3", 10,5), # River
            10:("BeachLand4", 4,7), # git example
            11:("BeachLand", 5,5) # Diagonal of yellow
        }
        choice = 11

        self.WIDTH = self.imgs[choice][1]
        self.HEIGHT = self.imgs[choice][2]

        self.STATE_GRID = []

        self.COLLAPSED = []
        
        self.img = load_image("patterns/{}.png".format(self.imgs[choice][0]))
    
    def getCell(self, x, y):
        return self.STATE_GRID[y][x]
    
    def updateAdjacentCellDomains(self, cell):
        #print("\nENTER UACD", cell.pos, GYBtoString(cell.domain))
        
        stack = [cell]
        
        # Get neighbors of this cell
        while stack:
            mycell = stack.pop(0)
            x = mycell.pos[0]
            y = mycell.pos[1]
            
            
            nbs = []
            for d in (NORTH, EAST, SOUTH, WEST):
                
                if ((x + d[0]) < 0 or (x + d[0]) >= OUTW or (y + d[1]) < 0 or (y + d[1]) >= OUTH):
                    continue
                nb_c = m.getCell(x+d[0], y+d[1])
                nbs.append((nb_c, d))

            # N E S W
            #self.pprint_w_colors()
            #print("##Main:", mycell.pos, GYBtoString(mycell.domain))
            #print("##NBs:", [x[0].pos for x in nbs])
            
            for nb, d in nbs:
                # Where d is the direction from the original tile to the neighbor
                if len(nb.domain) == 1: continue
                if nb.pos == mycell.pos: raise

                '''
                for m_color in mycell.domain:
                    invalid_domains = []
                    for n_color in nb.domain:
                        pattern = (n_color, m_color, dirToString(getOppositeDir(d)))
                        pattern = (n_color, m_color, dirToString(d))

                        if pattern not in PATTERNS_DICT:
                            invalid_domains.append(n_color)
                '''
                #invalid_domains = []
                #print("I'm", nb.pos, GYBtoString(nb.domain))
                invalid_domains = []
                for n_color in nb.domain:
                    
                    for m_color in mycell.domain:
                        # BWG --E--> BWGY
                        # f2		f1
                        pattern = (n_color, m_color, dirToString(d))
                        #print("Can", GYBtoString(n_color), "be", dirToString(d), "of", GYBtoString(m_color), "?")
                        #print("    ", GYBtoString(pattern))
                        
                        if pattern in PATTERNS_DICT:
                            #print("Yes, check next neighbor color")
                            break
                        else:
                            pass
                            #print("No, check next main color")
                    else:
                        #print("Checked all main colors (", GYBtoString(mycell.domain), ") against", GYBtoString(n_color), "and found no matches")
                        #print("-- (mark for deletion)", nb.pos, GYBtoString(nb.domain), "Remove --->", GYBtoString(n_color))
                        invalid_domains.append(n_color)
                        stack.append(nb)
                
                if invalid_domains:
                    for invalid in invalid_domains:
                        #print("--", nb.pos, GYBtoString(nb.domain), "Remove --->", GYBtoString(invalid))
                        #print("-- Before:", GYBtoString(nb.domain))
                        nb.domain.remove(invalid)
                        #print("-- After:", GYBtoString(nb.domain))
                
                '''
                if invalid_domains:
                    for invalid in invalid_domains:
                        print("--", nb.pos, GYBtoString(nb.domain), "Remove --->", GYBtoString(invalid))
                        nb.domain.remove(invalid)
                    stack.append(nb)
                '''
                nb.shannonEntropy()
                
                #print("  Final neighbor domain:", nb.pos, GYBtoString(nb.domain))
            #print("After going through these neighbors:")
            #self.pprint_w_colors()
    
    def pickLowestEntropyCell(self):
        # Pick the lowest entropy cell
        one_d_list = sum(self.STATE_GRID, [])
        sorted_x = sorted(one_d_list, key=operator.attrgetter('se'))
        
        minn = sorted_x[0]
        #print("Minn:", minn.pos, len(minn.domain), minn.se)
        options = []
        for x in sorted_x:
            #print(x.se, len(x.domain), end="-")
            if (len(x.domain) > 1) and (x.se >= minn.se):
                options.append(x)
        
        #options = [x for x in sorted_x if (x.se == minn.se) and (x.pos not in self.COLLAPSED)]
        #print("\nOptions:", len(options))
        try:
            a = random.choice(options)
            #print("Lowest cell", a.pos)
            return a
        except:
            #print("Lowest cell(m)", minn.pos)
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
    for pattern in list(PATTERNS):
        print(GYBtoString(pattern[0]), GYBtoString(pattern[1]), pattern[2])
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
            
            val = 100 if len(m.STATE_GRID[row][col].domain) > 1 else m.STATE_GRID[row][col].value
            try: fill(val)
            except: fill(100)
            rect(x,y,square_size,square_size)
            fill(255)
            text(len(m.STATE_GRID[row][col].domain),x+10,y+10)
    
    
    next_cell = m.pickLowestEntropyCell()
    print("#####\nPick lowest cell:", next_cell.pos, next_cell.domain)
    if len(next_cell.domain) == 1:
        time.sleep(1)
        return
    
    next_cell.collapse()
    print("After collapse next cell:", next_cell.pos, next_cell.domain)
    
    print("Update ACD", next_cell.pos)
    m.updateAdjacentCellDomains(next_cell)
    
    print("Finding 1 domain cells")
    one_d_list = sum(m.STATE_GRID, [])
    for x in one_d_list:
        if len(x.domain) == 1 and x.pos not in m.COLLAPSED:
            
            x.collapse()
            m.COLLAPSED.append(x.pos)

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

            




    

