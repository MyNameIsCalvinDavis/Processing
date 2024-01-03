from slider import Slider
import math

HEIGHT = 500
WIDTH = 500
smooth_slider = Slider(1, 100, 50, 200)
amp_slider = Slider(0.1, 8, 1, 200)

# https://math.stackexchange.com/questions/1832177/sigmoid-function-with-fixed-bounds-and-variable-steepness-partially-solved
# def sigmoid(x, k=2):
#     return 1 - ( 1 / (1 + ((1/x+0.5)-1)**(-k) ))

def draw_field(smoothness, amp, step):
    for y in range(0, HEIGHT, step):
        for x in range(0, WIDTH, step):
            n = noise(x / smoothness, y / smoothness)
            n = map(n, 0, 1, -amp, amp)
            stroke(150)
            line(x, y, x + cos(n) * step, y + sin(n) * step)
            #circle(x, y, n*10)

def setup():
    size(WIDTH, HEIGHT + 100)
    smooth_slider.position(10, 530)
    amp_slider.position(250, 530)

x = 50
y = 200
step = 10
points = []
def draw():
    global x
    global points
    global y
    background(255)
    
    smoothness = smooth_slider.value()
    amp = amp_slider.value()
    points.append((x, y))
    
    
    if len(points) > 1: # Draw the line
        for p in range(len(points)-1):
            line(points[p][0], points[p][1], points[p+1][0], points[p+1][1])
    
    # Calculate next point on the line
    n = noise(x / smoothness, y / smoothness) 
    n = map(n, 0, 1, -1, 1)
    
    stroke(0)
    x = x + cos(n * amp) * step
    y = y + sin(n * amp) * step
    
    if x > WIDTH or x < 0:
        x = 10
        points = []
    if y > HEIGHT or y < 2:
        y = HEIGHT / 2
    draw_field(smoothness, amp, 20)
        
            
            
            
            
            
