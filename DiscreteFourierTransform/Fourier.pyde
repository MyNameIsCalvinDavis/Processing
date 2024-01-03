# Your namespaces are not welcome here
from Load import *

w = 800
h = 700
tpi = pi*2

def complexMult(a,b,c,d):
    return (a*c) - (b*d), (b*c) + (a*d)

# Perform a discrete fourier transform on x, a set of (x, y) tuples.
def dft(x):
    X = []
    N = len(x)
    for k in range(N):
        Xk = {"r":0, "i":0}
        for n in range(N):
            phi = (tpi * k * n) / N
            r = cos(phi)
            i = -sin(phi)

            nr, ni = complexMult(x[n][0], x[n][1], r, i)
            Xk["r"] += nr
            Xk["i"] += ni

        Xk["freq"] = k
        Xk["amp"] = (Xk["r"] * Xk["r"] + Xk["i"] * Xk["i"]) ** 0.5 / N
        Xk["phase"] = atan2(Xk["i"], Xk["r"])
        X.append(Xk)
    
    return X

def DrawCirclesForPoint(X, t, center, rotation=0, scale=10, transparency=255):
    xp = center[0]
    yp = center[1]
    
    # Draws all of the waves on top of each other for a single time slice,
    # and extracts a point from the result
    for x in X:
        # For each wave: 
        # * Draw a circle whose radius is the amplitude of the wave at the current center
        # * Move the center of the circle to the point on the circle where the angle (phase) is
        #   * This is the only important calculation, everything else is just drawing shapes
        # * Draw a line between the two
        
        oldxp = xp
        oldyp = yp
        
        amp = x["amp"] / scale
        freq = x["freq"]
        phase = x["phase"]
        
        stroke(70,70,70, transparency)
        noFill()
        circle(xp, yp, amp*2)
        
        # Add to the current center this wave, giving us the point to start from next loop
        xp += amp * cos(t * freq + phase + rotation)
        yp += amp * sin(t * freq + phase + rotation)

        stroke(255, 255, 255, transparency)
        line(oldxp, oldyp, xp, yp)
    
    return (xp, yp)

def initGlobals():
    global path, X, x, y
    path = RabbitPath(w, h)
    X = sorted( dft(path), key=lambda x: x["amp"], reverse=True)
    x = sorted( dft([ (0, item[0]) for item in path ]), key=lambda x: x["amp"], reverse=True)
    y = sorted( dft([ (0, item[1]) for item in path ]),  key=lambda x: x["amp"], reverse=True)
    
    print("Done parsing DFT")

path = []
X = []
x = []
y = []
pointsx = []
pointsy = []


def setup():
    # Processing doesn't know where this project file is located
    # until setup(), so in order to load relative file paths,
    # we must ensure setup() runs first.
    
    initGlobals()
    size(w, h)

t = 0
def draw():
    # Because the main entry point of the program is a loop, we have to use globals
    # instead of creating a main(). No this is not pythonic, but Processing isn't Python.
    global t, pointsx, pointsy
    
    background(0)
    fill(255)
    stroke(255)
    
    """
    Each wave in X is a representation of a wave.
    When we add these waves together at time=0, we get some point. At t=1, we get another point.
    Eventually at t=2pi, the arbitrary set of points repeats itself, so the "period" for the summed-up wave
    can be considered 2pi, even if individual waves within the function may have higher or lower periods.
    
    A fourier transform takes an arbitrary set of points and turns them into a continuous function - specifically,
    this function is a bunch of sin waves with various amplitudes, frequencies, and phases. The thinking is each point in
    the set y can be represented as y=f(x).
    
    With that in mind, we should be able to draw each wave over and over again for different times from [0, 2pi)
    and see our original set of points.
    """
    
    pointx = DrawCirclesForPoint(x, t, (w/1.5, h/4), scale=2, rotation=3*pi/2)
    pointy = DrawCirclesForPoint(y, t, (w/6, h/1.5), scale=2)
    pointsx.append( pointx )
    pointsy.append( pointy )
    
    # For the middle set of circles, we dont care about the points
    DrawCirclesForPoint(X, t, (w/1.5, h/1.5), scale=2, transparency=50)
    combined = [ (px[0], py[1]) for px, py in zip(pointsx, pointsy) ]
    
    beginShape()
    noFill()
    stroke(100,150,200)
    for p in combined:
        vertex(p[0], p[1])
        
    endShape()
    stroke(255, 0, 0)
    line(pointx[0], pointx[1], combined[-1][0], combined[-1][1])
    line(pointy[0], pointy[1], combined[-1][0], combined[-1][1])
    
    t += tpi / len(X)
    if t > tpi:
        t = 0
        #points = []
        pointsx = []
        pointsy = []
        combined = []
