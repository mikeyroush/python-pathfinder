import numpy as np
from copy import copy
from math import sqrt, inf

def difference(list1,list2):
	result = [value for value in list1 if value not in list2]
	return result
	
def getLowestIndex(list):
	lowestIndex = 0
	for i, spot in enumerate(list[1:],1):
		if spot.f < list[lowestIndex].f:
			lowestIndex = i
	return lowestIndex
	
def distanceBetween(pos1,pos2):
	(y1,x1) = pos1
	(y2,x2) = pos2
	xDiff = x2 - x1
	yDiff = y2 - y1
	return round(sqrt(xDiff**2 + yDiff**2),1)


class Spot:
	
	def __init__(self,index):
		self.index = index
		self.f = inf
		self.g = inf
		self.h = 0
		self.neighbors = []
		self.parent = None
		
	def __repr__(self):
		return f'{self.index}: {self.f}'
		
	def updateNeighbors(self,grid):
		radius = 1
		(rowIndex,colIndex) = self.index
		self.neighbors = [grid[j][i] for j in range(rowIndex-radius, rowIndex+radius+1) for i in range(colIndex-radius, colIndex+radius+1) if j >= 0 and j < len(grid) and i >= 0 and i < len(grid[0]) and (j,i) != (rowIndex,colIndex)]
		

class PathFinder:
	
	def __init__(self,dimensions):
		(rows,cols) = dimensions
		#access y (row) then x (col)
		self.grid = [[Spot((j,i)) for i in range(cols)] for j in range(rows)]
		
		#start top left with g of 0, end bottom right
		self.start = self.grid[0][0]
		self.start.g = 0
		self.end = self.grid[rows-1][cols-1]
		self.openSet = [self.start]
		self.closeSet = []
		self.obstacleSet = []
		self.path = []
		
		#update spots neighbors and g scores
		for row in self.grid:
			for spot in row:
				spot.updateNeighbors(self.grid)
				spot.h = distanceBetween(spot.index,self.end.index)
		
	def takeStep(self):
		#we can keep going
		if len(self.openSet) > 0:
			#get node with lowest f cost
			current = self.openSet.pop(getLowestIndex(self.openSet))
			self.closeSet.append(current)
				
			#find path to current
			self.path = [];
			temp = copy(current)
			self.path.append(temp)
			while temp.parent:
				self.path.append(temp.parent)
				temp = copy(temp.parent)
			
			#check if we reached the end
			if current == self.end:
				self.openSet = []
				return
				
			#update f,g,h for each neighbor
			for neighbor in difference(difference(current.neighbors,self.closeSet), self.obstacleSet):
				#add neighbor to openSet
				if neighbor not in self.openSet:
					self.openSet.append(neighbor)
					
				#update neighbor's f and g score
				tempG = current.g + distanceBetween(current.index,neighbor.index)
				if tempG < neighbor.g:
					neighbor.g = tempG
					neighbor.f = neighbor.g + neighbor.h
					neighbor.parent = current
				
		#no solution
		else:
			pass


#main
'''pathfinder = PathFinder((5,5))
while len(pathfinder.openSet) > 0:
	pathfinder.takeStep()'''
