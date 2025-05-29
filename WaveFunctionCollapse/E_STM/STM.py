from pprint import pprint
from Model import *
import time
#import numpy as np

"""
TODO
- Read in NxN tiles from the input image and turn them into tiles with rulesets like ESTM
    - When that works, add rotation data and deconflict existing rotated / flipped tiles
- NxN tiles must be hashed and represented in human-readable ways (A-Z, AA-ZZ)
    - Model class should handle this
    - Go through and hash tiles / assign to Tile objects / create pattern dict
        - THEN go through and deconflict with copied tiles... rotations and flips
- Cell domain contains Tiles
- Tile Class
    - Tile Hash/ID
    - Tile data (draw)
    - Rotation Data
- Draw method needs to be redone to accomodate for each hashed tile
    - Dict: Hash to Tile Object
    - Dict: Tile Object to Hash


"""

m = 0
def setup():
    global m
    size(OUTW*20,OUTH*20)
    m = Model()
    m.genRules()
    for pattern in list(PATTERNS):
        #print(GYBtoString(pattern[0]), GYBtoString(pattern[1]), pattern[2])
        print(pattern)
    m.initGrid()    

def drawDataAt(col,row, square_size=20, n=3):
    mycell = m.getCell(col,row)
    #print("DDA:", mycell.pos)
    if len(mycell.domain) > 1: return
    if len(mycell.domain) == 0: raise
    
    # oof
    # (('#FFFFFFFF', '#FFFFFFFF', '#FFFFFFFF'), ('#FFFFFFFF', '#2200FFFF', '#FFFFFFFF'), ('#FFFFFFFF', '#FFFFFFFF', '#FFFFFFFF'))
    data = NAME_TO_TILE[list(mycell.domain)[0]].data
    rect_size = square_size / n
    

    for i,rw in enumerate(data):
        for j,clr in enumerate(rw):
            fill(clr)
            stroke(255)
            rect(
                col*square_size + j*rect_size,
                row*square_size + i*rect_size,
                rect_size, rect_size) # PITA
            
    
            
            
    

def draw():
    background(100)
    
    cell_size_scale = 1
    square_size = 20
    for row in range(OUTW):
        for col in range(OUTH): # I've never enumerated on range() before, weird
            x = col * square_size
            y = row * square_size
            # Draw a cell at x,y
            # Get the cell at j,i
            # cell = m.getCell(j,i)
            # This cell will have a value that's a tile, let's draw that Tile
            # print(m.STATE_GRID[row][col].value, type(m.STATE_GRID[row][col].value))
            
            '''
            val = 100 if len(m.STATE_GRID[row][col].domain) > 1 else m.STATE_GRID[row][col].value
            try: fill(val)
            except: fill(100)
            rect(x,y,square_size,square_size)
            '''
            fill(0)
            text(len(m.STATE_GRID[row][col].domain),x+10,y+10)
            drawDataAt(col,row, square_size, m.N)

    
    #m.pprint_w_colors()
    next_cell = m.pickLowestEntropyCell()
    print("LEC:", next_cell.pos, next_cell)
    next_cell.collapse()
    print("val:", next_cell.pos, next_cell.domain)
    
    #print("Enter UACD", next_cell.pos, next_cell)
    m.updateAdjacentCellDomains(next_cell)




            




    

