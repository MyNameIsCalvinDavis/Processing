from slider import Slider
from grid import Grid
import math
import random

# Global variables are kind of a curse but Python Processing has been designed
# with them in mind since it's thinly veiled Java, so I can't complain too much
HEIGHT = 600
WIDTH = 600
smooth_slider = Slider(1, 200, 200, 200)
amp_slider = Slider(-10, 10, 2, 200)
sep_slider = Slider(1, 30, 10, 200)
step = 10
prev_points = []
#grid_points = [(x, y) for y in range(0, HEIGHT, pt_step) for x in range(0, WIDTH, pt_step)]
sq_pts = [(x, y) for x in range(WIDTH/3, 2*WIDTH/3, 10) for y in range(HEIGHT/3, 2*HEIGHT/3, 10)]

d_sep = 16 # Must be greater than step
d_test = d_sep/2
grid = Grid(WIDTH, HEIGHT, int(d_sep * 1.5))

def setup():
    size(WIDTH, HEIGHT + 100)
    smooth_slider.position(10, HEIGHT + 30)
    amp_slider.position(250, HEIGHT + 30)
    sep_slider.position(10, HEIGHT + 60)
    noiseSeed(123)

def draw_line(ln):
    for p in range(len(ln)-1):
        stroke(0)
        line(ln[p][0], ln[p][1], ln[p+1][0], ln[p+1][1])
        
def draw_circles(ln, r=15):
    for p in range(len(ln)-1):
        fill(255)
        #noFill()
        circle(ln[p][0], ln[p][1], r)

def generate_line(pt, smoothness, amp):
    # Generating a single streamline just involves following whatever flow field
    # We're currently using and evaluating points on either end of the line
    px,py = pt
    nx,ny = pt
    
    streamline = []
    while True:
        if px < WIDTH and px > 0 and py < HEIGHT and py > 0 and len(streamline) < 100:
            n = noise(px / smoothness, py / smoothness) * amp # In this case perlin noise
            n = map(n, 0, 1, -1, 1)
            t = (px, py, n)
            streamline.append(t) # Add to end of list
            grid.add_to_cell(t)
            
            px = px + cos(n) * step
            py = py + sin(n) * step
            #pts = grid.get_neighbor_cell_points((px, py))
            ID = grid.find_cell_ID((px, py))
            pts = grid.get_cell(ID)

            # Does our new point overlap with any of the neighboring points?
            if overlap_check((px,py), pts, streamline):
                # Stop adding points in this direction
                px = WIDTH + 1
        elif nx < WIDTH and nx > 0 and ny < HEIGHT and ny > 0 and len(streamline) < 100:
            n = noise(nx / smoothness, ny / smoothness) * amp # In this case perlin noise
            n = map(n, 0, 1, -1, 1)
            t = (nx, ny, n)
            streamline.insert(0, t) # Add to end of list
            grid.add_to_cell(t)
            
            nx = nx - cos(n) * step
            ny = ny - sin(n) * step
            #pts = grid.get_neighbor_cell_points((nx, ny))
            ID = grid.find_cell_ID((nx, ny))
            pts = grid.get_cell(ID)

            if overlap_check((nx,ny), pts, streamline):
                # Stop adding points in this direction
                nx = WIDTH + 1
        else:
            return streamline

def find_candidate_seed(streamline):
    # Given a point on a streamline we can calculate two points
    # perpendicular to either side of the point with relation
    # to a point's vector value
    for x,y,n in streamline:
        
        nx = x + cos(n + PI/2) * d_sep
        ny = y + sin(n + PI/2) * d_sep
        p1 = (nx, ny)
        
        neighbors = grid.get_neighbor_cell_points(p1)
        if not overlap_check(p1, neighbors) and nx < WIDTH and nx > 0 and ny < HEIGHT and ny > 0:
            return p1
        
        px = x + cos(n - PI/2) * d_sep
        py = y + sin(n - PI/2) * d_sep
        p2 = (px, py)
        
        neighbors = grid.get_neighbor_cell_points(p2)
        if not overlap_check(p2, neighbors) and px < WIDTH and px > 0 and py < HEIGHT and py > 0:
            return p2
        
def distance(p1, p2):
    x1,y1 = p1[0], p1[1]
    x2,y2 = p2[0], p2[1]
    return (  ((x1 - x2)**2) + ((y1 - y2) ** 2))**0.5

def overlap_check(p1, points, exclude=[]):
    for p in points:
        if p in exclude:
            continue
        if exclude and p != exclude[0]: # If its not the first point, use a different spacing metric
            if distance(p, p1) < d_test:
                return True
        else:
            if distance(p, p1) < d_sep:
                return True
    return False

streamlines = []
def draw():
    global streamlines
    global d_sep
    grid.reset()
    background(150)
    
    smoothness = smooth_slider.value()
    amp = amp_slider.value()
    d_sep = sep_slider.value()
    #d_test = d_sep / 2
    # smoothness = 200.0
    # amp = 4.0
    # l = 40.0
    
    # Derive all the seed points possible from an existing streamline before
    # trying with a different existing one

    # Compute an initial streamline and put it into the queue

    # Figure 3 page 6
    initial_streamline = generate_line((200, 200), smoothness, amp)
    streamlines.append(initial_streamline)
    draw_circles(initial_streamline, step)
    
    finished = False
    current_streamline = streamlines.pop(0) # Queue
    while not finished:
        # Select a candidate seedpoint at d=d_dep apart from current streamline
        c_seed = find_candidate_seed(current_streamline)

        if c_seed: # If valid candidate selected, compute new SL and add to queue
            new_sl = generate_line(c_seed, smoothness, amp)
            streamlines.append(new_sl)
            draw_circles(new_sl, step)
        else: # No more valid candidates on current streamline
            if not streamlines: # No more streamlines in queue
                finished = True
            else:
                current_streamline = streamlines.pop(0)
