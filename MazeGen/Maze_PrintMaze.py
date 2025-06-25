import random
import copy
from graphics import *
import time
import sys
import os

cls = lambda: os.system('cls' if os.name=='nt' else 'clear')

class Node:
	def __init__(self, x, y): # Position on grid
		self.x = x
		self.y = y
		self.position = (x, y)
		self.explored = False
		self.selected = False
		self.tile = "." if self.explored == False else "X"
		self.nb = [] # Filled with NeighBoring node positions, no diagonals
		self.connectedTo = [] # Not necessarily connected to all neighbors
	def updateTile(self):
		self.tile = "." if self.explored == False else "X"
		if self.explored == True:
			self.tile = "O" if self.selected == True else "X"
		
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

	while path:
		cls()
		g.updateTiles()
		time.sleep(0.01)
		try:
			valid = [x for x in selected.nb if x.explored == False]
		except Exception as e:
			continue # Random fucking stupid error that is apparently fixed magically by just trying again
			print e
		if valid:
			choice = random.choice(valid)
			choice.connectedTo.append(selected.position)
			selected.connectedTo.append(choice.position)
			selected.selected = False
			selected = choice
			selected.explored = True
			selected.selected = True
			path.append(selected)
			strpath = [x.position for x in path]
			pprint(g.tgrid)
		else:
			selected.selected = False
			selected = path.pop()
			selected.selected = True
			strpath = [x.position for x in path]
			pprint(g.tgrid)
		g.updateTiles()
createMaze()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
				
