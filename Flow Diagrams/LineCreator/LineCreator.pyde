from slider import Slider
from grid import Grid
import math
import random

HEIGHT = 400
WIDTH = 400
smooth_slider = Slider(1, 200, 200, 200)
amp_slider = Slider(-10, 10, 2, 200)
length_slider = Slider(1, 30, 10, 200)
step = 5
prev_points = []
#grid_points = [(x, y) for y in range(0, HEIGHT, pt_step) for x in range(0, WIDTH, pt_step)]
sq_pts = [(x, y) for x in range(WIDTH/3, 2*WIDTH/3, 10) for y in range(HEIGHT/3, 2*HEIGHT/3, 10)]

d_sep = 10 # Must be greater than step
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
    while x < WIDTH and x > 0 and y < HEIGHT and y > 0 and len(ln) < 100:
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

def distance(p1, p2):
    x1,y1 = p1[0], p1[1]
    x2,y2 = p2[0], p2[1]
    return (  ((x1 - x2)**2) + ((y1 - y2) ** 2))**0.5

def overlap_check(p1, points, exclude):
    for p in points:
        #print("evaluating", p)
        if p in exclude:
            #print("excluding bc its in line", p)
            continue
        if distance(p, p1) < d_sep:
            #print(p, p1, distance(p, p1))
            return True
    return False


streamlines = []
def draw():
    #global grid
    grid.reset()

    background(255)
    
    smoothness = smooth_slider.value()
    amp = amp_slider.value()
    l = length_slider.value()
    # smoothness = 200.0
    # amp = 4.0
    # l = 40.0
    #circle(200, 200, 5)
    
    # Compute an initial streamline and put it into the queue
    initial_streamline = generate_line((200, 200), smoothness, amp)
    #print(initial_streamline)
    #delay(1000)
    #print(initial_streamline)
    #delay(1000)
    draw_line(initial_streamline)

    initial_streamline = generate_line((280, 200), smoothness, amp)
    draw_line(initial_streamline)
            
            
            
            
