from slider import Slider
import math
import random

HEIGHT = 600
WIDTH = 600
smooth_slider = Slider(1, 200, 200, 200)
amp_slider = Slider(-10, 10, 2, 200)
length_slider = Slider(1, 30, 10, 200)
step = 10
pt_step = 10

prev_points = []
def generate_line(pt, smoothness, amp, sz, mk=1):
    global prev_points
    # Given a single point, calculate a line and the flow field
    x,y = pt
    ln = [(x, y, 0)]
    
    while x < WIDTH and x > 0 and y < HEIGHT and y > 0:
        n = noise(x / smoothness, y / smoothness) * amp
        #n = map(n, 0, 1, 0, 2*math.pi)
        n = map(n, 0, 1, -mk, mk)
    
        x = x + cos(n) * step
        y = y + sin(n) * step
        t = (x, y, n)
        
        # if overlap_check(t, prev_points, (step/2) - 0.1):
            # if len(ln) > 5:
            #     return ln
            # else:
                # return []
        ln.append(t)
        prev_points.append(t)
        if len(ln) > sz:
            return ln
    return ln

def draw_line(ln):
    for p in range(len(ln)-1):
        stroke(0)
        line(ln[p][0], ln[p][1], ln[p+1][0], ln[p+1][1])

def draw_line_circles(ln, sz=5):
    for p in range(len(ln)-1):
        stroke(p*30 % 255, p*10 % 255, p*50 % 255)
        circle(ln[p][0], ln[p][1], sz)

#initial_points = [(x, y) for y in range(0, HEIGHT, 5) for x in [random.randint(0, WIDTH)]]
initial_points = [(x, y) for y in range(0, HEIGHT, pt_step) for x in range(0, WIDTH, pt_step)]
#initial_points = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for y in range(100) for x in range(100)]

# Square points
tlx = HEIGHT / 3
trx = tlx*2
blx = HEIGHT / 3
brx = tlx*2
sq_pts = [(x, y) for x in range(tlx, trx, 10) for y in range(blx, brx, 10)]

def distance(p1, p2):
    x1,y1 = p1[0], p1[1]
    x2,y2 = p2[0], p2[1]
    return (  ((x1 - x2)**2) + ((y1 - y2) ** 2))**0.5

def overlap(p1, p2, r=4):
    d = distance(p1, p2)
    return d < 2*r

def overlap_check(p1, points, r=4):
    for p in points:
        if overlap(p1, p, r): return True
    return False

def setup():
    size(WIDTH, HEIGHT + 100)
    smooth_slider.position(10, HEIGHT + 30)
    amp_slider.position(250, HEIGHT + 30)
    length_slider.position(10, 580)


def draw():
    background(255)
    global prev_points
    prev_points=[]
    
    smoothness = smooth_slider.value()
    amp = amp_slider.value()
    l = length_slider.value()
    # smoothness = 200.0
    # amp = 4.0
    # l = 40.0
    

    #Drawing the flow field
    # if False:
    #     stroke(0)
    #     for pt in initial_points:
    #         ln = generate_line(pt, smoothness, amp, 1)
    #         if len(ln) > 3: # Draw the line
    #             draw_line(ln)
    #             circle(pt[0], pt[1], 1)
    
    
    prev_points=[]
    for pt in sq_pts:
        ln = generate_line(pt, smoothness, amp, l)
        if ln: # Draw the line
            draw_line(ln)
    

        
            
            
            
            
            
