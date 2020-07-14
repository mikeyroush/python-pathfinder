#todo list
#have spaces remember new default color
#add resistance to some obstacles

from scene import *
from pathFinder import *
from board import *
from noise import *
from button import *
from adjustColor import *
from statistics import median, stdev

class PathFinderGUI(Scene):
	
	def setup(self):
		#initialize colors
		strokeColor = 'white'
		self.fillColor = '#c2c58d'
		self.pathColor = adjustColor(self.fillColor,0.25)
		self.obstacleColor = adjustColor(self.fillColor,0.15)
		self.openSetColor = adjustColor(self.fillColor,0.8)
		self.closeSetColor = adjustColor(self.fillColor,1.2)
		self.background_color = self.fillColor
		
		#initialize number vars
		self.boardDims = (40,40)
		self.terrainConsideration = 1
		self.terrainFactor = 3
		self.obstacleFactor = 2
		self.colorFactor = 0.7
		
		#initialize booleans
		self.manualMode = False
		self.generateObstacles = False
		self.generateTerrain = True
		self.debug = False
		
		#build board
		self.board = Board(self.boardDims,self.fillColor,stroke_color=strokeColor,parent=self)
		
		#build load terrain
		self.loadTerrain()
		
		#build start button
		self.startButton = Button('Start',adjustColor(self.fillColor,0.75),stroke_color=strokeColor,parent=self)
		
		#place elements
		self.moveAndScale()
		
	def loadTerrain(self):
		if self.generateTerrain:
			terrain = perlinNoise2D(self.boardDims,self.terrainFactor)
			terrainVector = [x for row in terrain for x in row]
			#center the range of values on 0
			diff = 0 - median(terrainVector)
			terrainVector = list(map(lambda i:i+diff, terrainVector))
			#map values to new range
			heighestPoint, lowestPoint = max(terrainVector), min(terrainVector)
			factor = self.colorFactor/max(abs(heighestPoint),abs(lowestPoint))
			terrainVector = list(map(lambda i:i*factor, terrainVector))
			terrain = [[terrainVector[i+j*len(terrain)] for j in range(len(terrain))] for i in range(len(terrain[0]))]
			
			self.pathfinder = PathFinder(terrain,self.terrainConsideration)
			for j, row in enumerate(terrain):
				for i, ele in enumerate(row):
					self.board.selectSpace((j,i),adjustColor(self.fillColor,1+ele),True)
		else:
			self.pathfinder = PathFinder.fromTuple(self.boardDims)
			
	def loadObstacles(self):
		#if there are no obstacles, generate some
		if self.generateObstacles and not self.manualMode:
			obstacles = perlinNoise2D(self.boardDims)
			obstacleVector = [x for row in obstacles for x in row]
			diff = 0.5 - median(obstacleVector)
			std = stdev(obstacleVector)
			for j in range(1,self.boardDims[0]-1):
				for i in range(1,self.boardDims[1]-1):
					val = obstacles[j][i] + diff
					#color = adjustColor(self.fillColor,val+0.5)
					if val > 0.5+self.obstacleFactor*std or val < 0.5-self.obstacleFactor*std:
						self.board.selectSpace((j,i),self.obstacleColor,False,True)
			
		#add locked spaces to pathfinder obstacleSet
		for row in self.board.spaces:
			for space in row:
				if space.locked:
					(j,i) = space.index
					spot = self.pathfinder.grid[j][i]
					self.pathfinder.obstacleSet.append(spot)
		
	def moveAndScale(self):
		#move and scale board
		self.board.moveAndScale()
		
		#move and scale start button
		self.center = (self.size.w/2,self.size.h/2)
		(x,y) = self.center
		buttonDims = (x,y-self.board.size.h/2,200,50)
		self.startButton.moveAndScale(buttonDims)		
		
		
	def did_change_size(self):
		self.moveAndScale()
		
	
	def touch_began(self,touch):
		self.startButton.isPressed(touch.location)
		
		
	def touch_ended(self,touch):
		if self.startButton.active:
			#if button is not locked, find path
			if not self.startButton.locked:
				self.startButton.release("Restart")
				
				#load obstacles
				self.loadObstacles()
							
				#lock start button
				self.startButton.lock()
				
			#otherwise, restart
			else:
				self.startButton.unlock()
				self.startButton.release("Start")
				self.manualMode = False
				self.board.clearSpaces()
				self.loadTerrain()
				
		
	def touch_moved(self,touch):
		if not self.startButton.locked:
			if self.board.isSpacePressed(touch,self.obstacleColor):
				self.manualMode = True
		
		
	def update(self):
		if self.startButton.locked and len(self.pathfinder.openSet) > 0:
			#take a step
			self.pathfinder.takeStep()
			
			#if debug is on, show openSet and closeSet blocks
			if self.debug:
				for spot in self.pathfinder.openSet:
					self.board.selectSpace(spot.index, self.openSetColor)
					
				for spot in self.pathfinder.closeSet:
					self.board.selectSpace(spot.index, self.closeSetColor)
			else:
				for spot in difference(self.pathfinder.oldPath,self.pathfinder.path):
					self.board.undoSpace(spot.index)
			
			#show optimal path
			for spot in self.pathfinder.path:
				self.board.selectSpace(spot.index,self.pathColor)
		
run(PathFinderGUI())
