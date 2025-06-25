from PIL import Image
from math import *
import time


startTime = time.time()


size = (1000, 1000)
# Default loop depth: 200
im = Image.new("RGB", (size[0], size[1]), "#ddd")
pix = im.load()
zoom = 4.0
asp_ratio = float(size[1])/float(size[0])


class ComplexNum:
    def __init__(self, real, complex): # Args = float values
        self.complexPart = complex
        self.realPart = real


    def addNumToSelf(self, numToAdd): # numToAdd = ComplexNum obj
        newReal = self.realPart + numToAdd.realPart
        newComplex = self.complexPart + numToAdd.complexPart
        self.realPart = newReal
        self.complexPart = newComplex


    def squareNum(self):
        newReal = (self.realPart**2.0)-(self.complexPart**2.0)
        newComplex = 2*self.realPart*self.complexPart
        self.realPart = newReal
        self.complexPart = newComplex


    def cnabs(self):
        rSq = self.realPart**2.0
        cSq = self.complexPart**2.0
        abs = sqrt(rSq+cSq)
        return abs


def checkPasses(x, y, iterations = 50):
    z = ComplexNum(0, 0)
    num = ComplexNum(x, y)
    count = 1
    while True:
        if (z.cnabs() > 2):
            return count
        elif (count > iterations):
            return 0
        z.squareNum()
        z.addNumToSelf(num)
        count += 1


def GenerateValues():
    """
    I wouldn't ordinarily make this into a function because it only needs to happen once. The only
    reason I did was to be able to more easily reference this block of code
    """
    graphxrange = []
    graphyrange = []
    values = []
    
    # Create the x and y value range for the set
    for i in range(size[0]):
            graphxrange.append(i*(3.0 / size[0]) - 2.3)


    for i in range(size[1]):
            graphyrange.append(i*(3.0 / size[1]) - 1.49)
            
            
    
    # With the value ranges, create the actual values for the set using checkPasses()
    for i in graphyrange:
        l = []
        for j in graphxrange:
            newVal = checkPasses(j, i)
            l.append(newVal)
        values.append(l)
    return values


def Draw():
    values = GenerateValues()
    colors = [(6*x, 4*x, 2*x) for x in range(50)]
    for i, row in enumerate(values):
        for j, value in enumerate(row):
            
            if value > 0:
                pix[j, i] = colors[value % len(colors)]


Draw()
im.save("MB.png", "png")
print time.time() - startTime # Total time taken to run the program






