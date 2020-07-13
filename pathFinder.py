from copy import copy
from math import sqrt, inf
from statistics import mean
from operator import sub

def difference(list1,list2):
	result = [value for value in list1 if value not in list2]
	return result
	
def getLowestIndex(list):
	lowestIndex = 0
	for i, spot in enumerate(list[1:],1):
		if spot.f < list[lowestIndex].f:
			lowestIndex = i
	return lowestIndex
	
def getNeighbors(grid,index,radius,includeSelf=False):
	(rowIndex,colIndex) = index
	neighbors = [grid[j][i] for j in range(rowIndex-radius, rowIndex+radius+1) for i in range(colIndex-radius, colIndex+radius+1) if j >= 0 and j < len(grid) and i >= 0 and i < len(grid[0]) and (j,i) != (rowIndex,colIndex)]
	if includeSelf:
		neighbors.append(grid[rowIndex][colIndex])
	return neighbors
	
def distanceBetween(pos1,pos2,direct=True):
	#initialize vars
	(y1,x1) = pos1
	(y2,x2) = pos2
	(yDiff,xDiff) = tuple(map(sub,pos2,pos1)) #pos2 - pos1
	
	#account for indirect travel
	if not direct:
		if abs(xDiff) < abs(yDiff):
			tempPos = (y1+xDiff, x1+xDiff)
		else:
			tempPos = (y1+yDiff, x1+yDiff)
		return distanceBetween(pos1,tempPos) + distanceBetween(tempPos,pos2)
		
	#pythagorean theorem
	return round(sqrt(xDiff**2 + yDiff**2),3)
	
def sameDirection(pos1,pos2,pos3):
	change1 = tuple(map(sub,pos2,pos1)) #pos2 - pos1
	change2 = tuple(map(sub,pos3,pos2)) #pos3 - pos2
	return  change1 == change2
	
def heuristic(parent,current,neighbor,scale):
	if parent and sameDirection(parent.index, current.index, neighbor.index):
		return distanceBetween(current.index,parent.index)*((scale-1)/scale)**2
	return distanceBetween(current.index,neighbor.index)

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
		self.scale = mean((rows,cols))
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
		self.oldPath = []
		
		#update spots neighbors and g scores
		for row in self.grid:
			for spot in row:
				#spot.updateNeighbors(self.grid)
				spot.neighbors = getNeighbors(self.grid,spot.index,1)
				spot.h = distanceBetween(spot.index,self.end.index,False)
		
	def takeStep(self):
		#we can keep going
		if len(self.openSet) > 0:
			#get node with lowest f cost
			current = self.openSet.pop(getLowestIndex(self.openSet))
			self.closeSet.append(current)
				
			#pop path spots into old path
			self.oldPath = []
			while len(self.path) > 0:
				self.oldPath.append(self.path.pop())
				
			#find path to current
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
				tempG = current.g + heuristic(current.parent,current,neighbor,self.scale)#distanceBetween(current.index,neighbor.index)
				if tempG < neighbor.g:
					neighbor.g = tempG
					neighbor.f = neighbor.g + neighbor.h
					neighbor.parent = current
				
		#no solution
		else:
			pass

