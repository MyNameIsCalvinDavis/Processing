from slider import Slider
import math
import random

HEIGHT = 600
WIDTH = 800
smooth_slider = Slider(1, 200, 50, 200)
amp_slider = Slider(0.1, 20, 1, 200)
#mk_slider = Slider(0.1, 10, 1, 200)
step = 10

def generate_line(pt, smoothness, amp, sz, mk=1):
    # Given a single point, calculate a line and the flow field
    ln = []
    x,y = pt
    ln.append((x, y))
    
    while x < WIDTH and x > 0 and y < HEIGHT and y > 0:
        n = noise(x / smoothness, y / smoothness) 
        n = map(n, 0, 1, -mk, mk)
    
        stroke(100)
        x = x + cos(n * amp) * step
        y = y + sin(n * amp) * step
        ln.append((x, y))
        if len(ln) > sz: return ln
    return ln
    
def draw_line(ln):
    for p in range(len(ln)-1):
        line(ln[p][0], ln[p][1], ln[p+1][0], ln[p+1][1])
    
#initial_points = [(x, y) for y in range(0, HEIGHT, 5) for x in [random.randint(0, WIDTH)]]
initial_points = [(x, y) for y in range(0, HEIGHT, 10) for x in range(0, WIDTH, 10)]

def setup():
    size(WIDTH, HEIGHT + 100)
    smooth_slider.position(10, HEIGHT + 30)
    amp_slider.position(250, HEIGHT + 30)
    #mk_slider.position(10, 580)


def draw():
    background(255)
    
    smoothness = smooth_slider.value()
    amp = amp_slider.value()
    #mk = mk_slider.value()
    
    
    
    #print(ln)
    #delay(500)
    for pt in initial_points:
        ln = generate_line(pt, smoothness, amp, 1)
        if len(ln) > 1: # Draw the line
            draw_line(ln)
    ln = generate_line((250, 250), smoothness, amp, 100)
    stroke(0)
    strokeWeight(16)
    draw_line(ln)

    line(ln[0][0], ln[0][1], ln[1][0], ln[1][1])
    # Calculate next point on the line

        
            
            
            
            
            
