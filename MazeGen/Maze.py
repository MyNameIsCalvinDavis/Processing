import random
import copy
from graphics import *
import time
import sys

class Node:
	def __init__(self, x, y): # Position on grid
		self.x = x
		self.y = y
		self.position = (x, y)
		self.explored = False
		self.tile = "O" if self.explored == False else "X"
		self.nb = [] # Filled with NeighBoring node positions, no diagonals
		self.connectedTo = [] # Not necessarily connected to all neighbors
	def updateTile(self):
		self.tile = "O" if self.explored == False else "X"
		
class Grid:
	def __init__(self, x, y): # Size of grid
		self.x = x
		self.y = y
		self.grid = [["" for k in xrange(x)] for u in xrange(y)] # Object-based non-visual grid, do not edit
		self.pgrid = [] # Position-based visual grid
		self.tgrid = [] # Tile-based visual grid
		self.create()
	def create(self):
		for j in xrange(self.y):
			for i in xrange(self.x):
				self.grid[i][j] = Node(i, j)
		self.vgrid = [[self.grid[i][j].position for i in xrange(self.x)] for j in range(self.y)]
		self.tgrid = [[self.grid[i][j].tile for i in xrange(self.x)] for j in range(self.y)]
		self.initnb()
	def initnb(self):
		for i in self.grid:
			for j in i:
				if j.x-1 != -1:
					try: j.nb.append(self.grabNode((j.x-1, j.y)))
					except: pass
				if j.x+1 != -1:
					try: j.nb.append(self.grabNode((j.x+1, j.y)))
					except: pass
				if j.y-1 != -1:
					try:j.nb.append(self.grabNode((j.x, j.y-1)))
					except: pass
				if j.y+1 != -1:
					try:j.nb.append(self.grabNode((j.x, j.y+1)))
					except: pass
	def updateTiles(self):
		for i in self.grid:
			for j in i:
				j.updateTile()
				self.tgrid = [[self.grid[i][j].tile for i in xrange(self.x)] for j in range(self.y)]
	def grabNode(self, position): # Where position is an (x,y) tuple, returns node object
			return self.grid[position[0]][position[1]]

a = Grid(3,3) # so pretty!
# pprint(a.grid)
# pprint(a.vgrid)
# pprint(a.tgrid)

def pprint(thing): # pprint isnt working for what I have in mind
	for i in thing:
		print i



def createMaze(g = Grid(15,15)):
	"""
	
	Using the greedy back propagation method
	
	"""
	start = (0,0)
	path = [g.grabNode(start)]
	strpath = [x.position for x in path]
	selected = path[0]
	g.grabNode(start).explored = True
	following = 0
	boxsize = 35 # Change this to edit grid size
	
	vdict = {}
	win = GraphWin("Maze", g.x*boxsize, g.y*boxsize)
	for i in g.grid: # Draw the original, unexplored squares
		for j in i:
			pos = j.position
			pos = (pos[0] + 0.09375, pos[1] + 0.09375)
			c = Rectangle(Point(pos[0]*boxsize, pos[1]*boxsize), Point((pos[0]*boxsize) + boxsize, (pos[1]*boxsize) + boxsize))
			c.setOutline("white")
			c.draw(win)
			
			vdict[j.position] = c
			
	while path:
		sys.stdout.write(".")
		sys.stdout.flush()
		g.updateTiles()
		try:
			valid = [x for x in selected.nb if x.explored == False]
		except Exception as e:
			continue # Random fucking stupid error that is apparently fixed magically by just trying again
			print e
		if valid:
			choice = random.choice(valid)
			choice.connectedTo.append(selected.position)
			selected.connectedTo.append(choice.position)
			selected = choice
			selected.explored = True
			path.append(selected)
			strpath = [x.position for x in path]
		else:
			selected = path.pop()
			strpath = [x.position for x in path]
		g.updateTiles()
		for key in vdict.keys():
			if g.grabNode(key).explored == True:
				if g.grabNode(key).position in strpath:
					vdict[key].setFill("red")
				else:
					vdict[key].setFill("white")
			try:
				if g.grabNode(key).position == path[-1].position:
					vdict[key].setFill("orange")
			except IndexError:
				pass # It's done drawing, we dont care anymore
	for i in g.grid: # Draw the lines
		for j in i:
			notConnectedTo = [x for x in [y.position for y in j.nb] if x not in j.connectedTo]
			t = [x for x in notConnectedTo]
			for x in notConnectedTo:
				if j.y - x[1] == 1: # Above
					l = Line(Point(j.x*boxsize, j.y*boxsize), Point((j.x*boxsize) + boxsize, j.y*boxsize))
					#l.setFill("red")
					l.draw(win)
				if j.x - x[0] == 1: # Left
					l = Line(Point(j.x*boxsize, j.y*boxsize), Point((j.x*boxsize), (j.y*boxsize) + boxsize))
					#l.setFill("blue")
					l.draw(win)
	win.getMouse()
createMaze()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
				
