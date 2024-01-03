from slider import Slider
import math
import random

HEIGHT = 500
WIDTH = 500
smooth_slider = Slider(1, 100, 50, 200)
amp_slider = Slider(0.1, 8, 1, 200)
#mk_slider = Slider(0.1, 10, 1, 200)
step = 10

def generate_line(pt, smoothness, amp, mk=1):
    # Given a single point, calculate a line and the flow field
    ln = []
    x,y = pt
    ln.append((x, y))
    
    while x < WIDTH and x > 0 and y < HEIGHT and y > 0:
        n = noise(x / smoothness, y / smoothness) 
        n = map(n, 0, 1, -mk, mk)
    
        stroke(0)
        x = x + cos(n * amp) * step
        y = y + sin(n * amp) * step
        ln.append((x, y))
        if len(ln) > 1000: return ln
    return ln
    

#initial_points = [(x, y) for y in range(0, HEIGHT, 5) for x in [random.randint(0, WIDTH)]]
initial_points = [(2, y) for y in range(0, HEIGHT, 5)]

def setup():
    size(WIDTH, HEIGHT + 100)
    smooth_slider.position(10, 530)
    amp_slider.position(250, 530)
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
            for p in range(len(ln)-1):
                line(ln[p][0], ln[p][1], ln[p+1][0], ln[p+1][1])
    
    # Calculate next point on the line

        
            
            
            
            
            
