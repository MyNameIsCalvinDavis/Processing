"""
Provides functionality to load and manipulate input data into a readble form.
Most of these functions read in data of with an arbitrary format and output a list
of (x, y) tuples.
"""

from math import cos, sin, pi, atan2

# Maps a value in one range to another range
def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

def SquarePath():
    path = []
    path += [(x, 50) for x in range(50, 600, 10)]
    path += [(600, x) for x in range(50, 600, 10)]
    path += [(x, 600) for x in range(600, 50, -10)]
    path += [(50, x) for x in range(600, 50, -10)]
    path = [(x[0]-350, x[1]-330) for x in path]
    return path

def MLPath(w, h):
    # Get point locations first
    cities = []
    with open("mona-lisa100K.tsp") as f:
        for line in f:
            line = line.replace("\n", "").split(" ")
            cities.append((
                          #int(line[0]),
                          #int(line[1])
                          translate(int(line[0]), 0, 20000, -w/2, w/2), 
                          translate(int(line[1]), 0, 20000, -h/2, h/2)         
            ))
    
    path = []
    with open("/home/ppc/Projects/Four/monalisa_shortest.tour") as f:
        for line in f:
            line = line.replace("\n", "")
            line = int(line)
            path.append(cities[line-1])
    return path[::400]

def BoobPath(w, h):
    path = []
    with open("Boob.txt") as f:
        for line in f:
            line = line.replace("\n", "").split(" ")
            line = line[0].split(".")[0] + " " + line[1].split(".")[0]
            line = line.split(" ")
            print(line)
            path.append((
                translate(int(line[0]), 300, 500, -w/2, w/2), 
                translate(int(line[1]), 800, 1000, -h/2, h/2)         
            ))
        return path

def RabbitPath(w, h):
    path = []
    with open("Rabbit.txt") as f:
        for line in f:
            line = line.replace("\n", "").split(" ")
            line = line[0].split(".")[0] + " " + line[1].split(".")[0]
            line = line.split(" ")
            #print(line)
            path.append((
                translate(int(line[0]), 0, 600, -w/2, w/2), 
                translate(int(line[1]), 0, 600, -h/2, h/2)         
            ))
        return path

def MLPath2(w, h):
    path = []
    with open("ML.txt") as f:
        for line in f:
            line = line.replace("\n", "").split(" ")
            line = line[0].split(".")[0] + " " + line[1].split(".")[0]
            line = line.split(" ")
            path.append((
                translate(int(line[0]), 0, 800, -w/2, w/2), 
                translate(int(line[1]), 0, 900, -h/2, h/2)         
            ))
        return path
