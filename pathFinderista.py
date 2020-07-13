#todo list
#add resistance to some obstacles

from scene import *
from pathFinder import *
from board import *
from noise import *
from button import *
from adjustColor import *
from statistics import median

class PathFinderGUI(Scene):
	
	def setup(self):
		#initialize vars
		strokeColor = 'white'
		self.fillColor = '#c8cdff'
		self.pathColor = adjustColor(self.fillColor,0.25)
		self.obstacleColor = adjustColor(self.fillColor,0.5)
		self.boardDims = (40,40)
		self.background_color = self.fillColor
		self.generateNoise = True
		self.debug = True
		
		#build board
		self.board = Board(self.boardDims,self.fillColor,stroke_color=strokeColor,parent=self)
		
		#build pathfinder
		self.pathfinder = PathFinder(self.boardDims)
		
		#build start button
		self.startButton = Button('Start',adjustColor(self.fillColor,0.75),stroke_color=strokeColor,parent=self)
		
		#place elements
		self.moveAndScale()
		
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
				
				#if there are no obstacles, generate some
				if self.generateNoise:
					self.noise = perlinNoise2D(self.boardDims)
					diff = 0.5 - median([x for row in self.noise for x in row])
					for j in range(1,self.boardDims[0]-1):
						for i in range(1,self.boardDims[1]-1):
							val = self.noise[j][i] + diff
							#color = adjustColor(self.fillColor,val+0.5)
							if val > 0.55 or val < 0.45:
								self.board.selectSpace((j,i),self.obstacleColor,True)
					
				#add locked spaces to pathfinder obstacleSet
				for row in self.board.spaces:
					for space in row:
						if space.locked:
							(j,i) = space.index
							spot = self.pathfinder.grid[j][i]
							self.pathfinder.obstacleSet.append(spot)
				#lock start button
				self.startButton.lock()
			#otherwise, restart
			else:
				self.startButton.unlock()
				self.startButton.release("Start")
				self.pathfinder = PathFinder(self.boardDims)
				self.board.clearSpaces()
				
		
	def touch_moved(self,touch):
		if not self.startButton.locked:
			self.board.isSpacePressed(touch,self.obstacleColor)
			if self.generateNoise:
				self.generateNoise = False
		
		
	def update(self):
		if self.startButton.locked and len(self.pathfinder.openSet) > 0:
			#take a step
			self.pathfinder.takeStep()
			
			#if debug is on, show openSet and closeSet blocks
			if self.debug:
				for spot in self.pathfinder.openSet:
					self.board.selectSpace(spot.index, adjustColor(self.fillColor,0.8))
					
				for spot in self.pathfinder.closeSet:
					self.board.selectSpace(spot.index, adjustColor(self.fillColor,1.2))
			else:
				for spot in difference(self.pathfinder.oldPath,self.pathfinder.path):
					self.board.selectSpace(spot.index, self.fillColor)
			
			#show optimal path
			for spot in self.pathfinder.path:
				self.board.selectSpace(spot.index,self.pathColor)
		
run(PathFinderGUI())
