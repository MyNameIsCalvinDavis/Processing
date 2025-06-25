from math import *
from graphics import *

win = GraphWin("Rule 30", 1200, 600)

currentframe = [0 for x in range(402)]
nextframe = [0 for x in range(402)]
currentframe[201] = 1
print currentframe

for k in range(120):
    for i in range(len(currentframe) - 1):
        if currentframe[i - 1] == 0 and currentframe[i] == 0 and currentframe[i + 1] == 0:
            # ---
            nextframe[i] = 0
            a = Rectangle(Point((i*3) + 3, (k*3) + 3), Point((i*3) + 6, (k*3) + 6))
            a.setOutline(color_rgb(216,216,216))
            a.setFill("white")
            a.draw(win)
        elif currentframe[i - 1] == 0 and currentframe[i] == 0 and currentframe[i + 1] == 1:
            # --X
            nextframe[i] = 1
            a = Rectangle(Point((i*3) + 3, (k*3) + 3), Point((i*3) + 6, (k*3) + 6))
            a.setFill("red4")
            a.draw(win)
        elif currentframe[i - 1] == 0 and currentframe[i] == 1 and currentframe[i + 1] == 0:
            # -X-
            nextframe[i] = 1
            a = Rectangle(Point((i*3) + 3, (k*3) + 3), Point((i*3) + 6, (k*3) + 6))
            a.setFill("red4")
            a.draw(win)
        elif currentframe[i - 1] == 0 and currentframe[i] == 1 and currentframe[i + 1] == 1:
            # -XX
            nextframe[i] = 1
            a = Rectangle(Point((i*3) + 3, (k*3) + 3), Point((i*3) + 6, (k*3) + 6))
            a.setFill("red4")
            a.draw(win)
        elif currentframe[i - 1] == 1 and currentframe[i] == 0 and currentframe[i + 1] == 0:
            # X--
            nextframe[i] = 1
            a = Rectangle(Point((i*3) + 3, (k*3) + 3), Point((i*3) + 6, (k*3) + 6))
            a.setFill("red4")
            a.draw(win)
        elif currentframe[i - 1] == 1 and currentframe[i] == 0 and currentframe[i + 1] == 0:
            # X-X
            nextframe[i] = 0
            a = Rectangle(Point((i*3) + 3, (k*3) + 3), Point((i*3) + 6, (k*3) + 6))
            a.draw(win)
        elif currentframe[i - 1] == 1 and currentframe[i] == 1 and currentframe[i + 1] == 0:
            # XX-
            nextframe[i] = 0
        elif currentframe[i - 1] == 1 and currentframe[i] == 1 and currentframe[i + 1] == 0:
            # XXX
            nextframe[i] = 0
            a = Rectangle(Point((i*3) + 3, (k*3) + 3), Point((i*3) + 6, (k*6) + 6))
            a.draw(win)
    print nextframe
    currentframe = nextframe
    nextframe = [0 for x in range(402)]
win.getMouse()
#raw_input()
