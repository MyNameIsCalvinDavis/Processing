class Slider:
    def __init__(self,low,high,default,linelength=120):
        '''slider has range from low to high
        and is set to default'''
        self.linelength = linelength
        self.low = low
        self.high = high
        self.val = default
        self.clicked = False
        self.label = '' #blank label
        
    def position(self,x,y):
        '''slider's position on screen'''
        self.x = x
        self.y = y
        #the position of the rect you slide:
        self.rectx = self.x + map(self.val,self.low,self.high,0,self.linelength)
        self.recty = self.y - 10
        
    def value(self):
        '''updates the slider and returns value'''
        #gray line behind slider
        strokeWeight(4)
        stroke(200)
        line(self.x,self.y,self.x + self.linelength,self.y)
        #press mouse to move slider
        if mousePressed and dist(mouseX,mouseY,self.rectx,self.recty) < 20:
            self.rectx = mouseX
        #constrain rectangle
        self.rectx = constrain(self.rectx, self.x, self.x + self.linelength)
        #draw rectangle
        strokeWeight(1)
        stroke(0)
        fill(255)
        rect(self.rectx,self.recty,10,20)
        self.val = map(self.rectx,self.x,self.x + self.linelength,self.low,self.high)
        #draw label
        fill(0)
        textSize(10)
        text(int(self.val),self.rectx,self.recty + 35)
        #text label
        text(self.label,self.x + self.linelength + 15,self.y);
        return self.val
