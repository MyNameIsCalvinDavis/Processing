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
length_slider = Slider(1, 30, 10, 200)
step = 8
prev_points = []
#grid_points = [(x, y) for y in range(0, HEIGHT, pt_step) for x in range(0, WIDTH, pt_step)]
sq_pts = [(x, y) for x in range(WIDTH/3, 2*WIDTH/3, 10) for y in range(HEIGHT/3, 2*HEIGHT/3, 10)]

d_sep = 16 # Must be greater than step
d_test = d_sep/2
grid = Grid(WIDTH, HEIGHT, d_sep)

def setup():
    size(WIDTH, HEIGHT + 100)
    smooth_slider.position(10, HEIGHT + 30)
    amp_slider.position(250, HEIGHT + 30)
    length_slider.position(10, 580)
    noiseSeed(123)

def draw_line(ln):
    for p in range(len(ln)-1):
        stroke(0)
        line(ln[p][0], ln[p][1], ln[p+1][0], ln[p+1][1])
        
def draw_circles(ln, r=15):
    for p in range(len(ln)-1):
        stroke(0)
        noFill()
        circle(ln[p][0], ln[p][1], r)

def generate_line(pt, smoothness, amp):
    # Generating a single streamline just involves following whatever flow field
    # We're currently using and evaluating points on either end of the line
    x,y = pt
    bl = []
    ln = []
    
    # Positive direction
    #print("Pos direction")
    while x < WIDTH and x > 0 and y < HEIGHT and y > 0 and len(ln) < 100:
        n = noise(x / smoothness, y / smoothness) * amp # In this case perlin noise
        n = map(n, 0, 1, -1, 1)
    
        t = (x, y, n)
        ln.append(t)
        grid.add_to_cell(t)

        x = x + cos(n) * step
        y = y + sin(n) * step
        t = (x, y, n)
        # During construction, a new sample point is only valid if it is at a separating
        # distance greater than d_sep. If it's not the case, this direction is stopped.

        # A new sample point is valid if the distance between it and all sampled points
        # in a local area are greater than d_sep

        # Get points in local area
        pts = grid.get_neighbor_cell_points((x, y))

        # Does our new point overlap with any of the neighboring points?
        if overlap_check((x,y), pts, ln):
            bl += ln
            break
            #return ln
        # If not, calculate next point
    
    # Neg direction
    if not bl: bl += ln
    x,y = pt
    ln = []
    while x < WIDTH and x > 0 and y < HEIGHT and y > 0 and len(ln) < 150:
        n = noise(x / smoothness, y / smoothness) * amp # In this case perlin noise
        n = map(n, 0, 1, -1, 1)
    

        t = (x, y, n)
        ln.insert(0, t)
        grid.add_to_cell(t)

        x = x - cos(n) * step
        y = y - sin(n) * step
        pts = grid.get_neighbor_cell_points((x, y))

        if overlap_check((x,y), pts, bl + ln):
            bl = ln + bl
            break
    else:
        bl = ln + bl
    return bl

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
        if exclude and p != exclude[0]:
            if distance(p, p1) < d_test:
                return True
        else:
            if distance(p, p1) < d_sep:
                return True
    return False


streamlines = []
def draw():
    global streamlines
    grid.reset()
    background(255)
    
    smoothness = smooth_slider.value()
    amp = amp_slider.value()
    l = length_slider.value()
    # smoothness = 200.0
    # amp = 4.0
    # l = 40.0
    #circle(200, 200, 5)
    
    # Derive all the seed points possible from an existing streamline before
    # trying with a different existing one

    # Compute an initial streamline and put it into the queue

    
    # pt = find_candidate_seed(initial_streamline)
    # #circle(pt[0], pt[1], 10)
    # l2 = generate_line(pt, smoothness, amp)
    # draw_line(l2)
    
    # # for i in range(5):
    # pt = find_candidate_seed(l2)
    # #circle(pt[0], pt[1], 5)
    # l2 = generate_line(pt, smoothness, amp)
    # draw_line(l2)
    # Figure 3 page 6
    
    # noFill()
    
    initial_streamline = generate_line((200, 200), smoothness, amp)
    streamlines.append(initial_streamline)
    draw_line(initial_streamline)
    
    finished = False
    current_streamline = streamlines.pop(0) # Queue
    while not finished:
        # Select a candidate seedpoint at d=d_dep apart from current streamline
        c_seed = find_candidate_seed(current_streamline)

        if c_seed: # If valid candidate selected, compute new SL and add to queue
            new_sl = generate_line(c_seed, smoothness, amp)
            streamlines.append(new_sl)
            draw_line(new_sl)
        else: # No more valid candidates on current streamline
            if not streamlines: # No more streamlines in queue
                finished = True
            else:
                current_streamline = streamlines.pop(0)
