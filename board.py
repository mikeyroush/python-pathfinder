from scene import *
from adjustColor import *
from touch import *
from math import ceil,floor

class Space(ShapeNode):
	def __init__(self,index,sizeFactors,fillColor,*args,**kwargs):
		ShapeNode.__init__(self,*args,**kwargs)
		mainFont = ('Helvetica', min(self.size.w,self.size.h)*0.9)
		self.startCharacter = ''
		self.charactar = LabelNode(self.startCharacter,font=mainFont,parent=self)
		self.index = index
		self.sizeFactors = sizeFactors
		self.defaultColor = fillColor
		self.currentColor = self.defaultColor
		self.fill_color = self.defaultColor
		self.locked = False
		
	def moveAndScale(self):
		#initialize vars
		(j,i) = self.index
		(hFactor,wFactor) = self.sizeFactors
		
		#calculate size
		w = self.parent.size.w / wFactor
		h = self.parent.size.h / hFactor
		self.offset = self.parent.size - (w*wFactor,h*hFactor)
		
		#calculate position
		x = -self.parent.size.w/2 + w/2 + i*w
		y = +self.parent.size.h/2 - h/2 - j*h
		
		#move and scale
		self.path = ui.Path.rect(0,0,w,h)
		self.position = (x,y)
		self.adjustFont()
		
	def adjustFont(self):
		mainFont = ('Helvetica', min(self.size.w,self.size.h)*0.9)
		self.charactar.font = mainFont
		
	def isPressed(self,point,color=None):
		pressed = isTouched(self,point)
		if pressed:
			if not color:
				color = adjustColor(self.defaultColor,1.2)
			self.fillColor(color, False, True)
		return pressed
		
	def fillColor(self, color, save=False, locked=False, char=""):
		self.locked = locked
		self.charactar.text = str(char)	
		self.fill_color = color
		if save:
			self.currentColor = color
		
	def clear(self):
		self.charactar.text = self.startCharacter
		self.fill_color = self.defaultColor
		self.locked = False
		
	def undoColorChange(self):
		self.fill_color = self.currentColor
		
		
class Board(ShapeNode):
	def __init__(self,dimensions,fillColor,*args,**kwargs):
		ShapeNode.__init__(self,*args,**kwargs)
		self.dimensions = dimensions
		(rows,cols) = self.dimensions
		self.fill_color = fillColor
		self.spaces = [[Space((j,i),self.dimensions,fillColor,stroke_color=self.stroke_color,parent=self) for i in range(cols)] for j in range(rows)]
		self.margin = 40
		
	def moveAndScale(self):
		#calculate size of board
		availableSize = min(self.parent.size.w,self.parent.size.h)
		size = availableSize - 2*self.margin
		(w,h) = (size, size)
		
		#calculate position of board
		pos = (self.parent.size.w/2, self.parent.size.h/2)
		
		#move and scale board
		self.path = ui.Path.rect(0,0,w,h)
		self.position = pos
		
		#move and scale spaces
		for row in self.spaces:
			for space in row:
				space.moveAndScale()
		
	def isSpacePressed(self,touch,color):
		#human interaction with spaces
		point = self.point_from_scene(touch.location)
		
		#calculate index of space
		offset = self.position - self.size/2
		(i,j) = (touch.location-offset)/(self.size.w/self.dimensions[0])
		(i,j) = (floor(i),self.dimensions[0] - floor(j) - 1)
		if j < self.dimensions[0] and i < self.dimensions[1]:
			return self.spaces[j][i].isPressed(point,color)
		return False
			
	def selectSpace(self,index,color,save=False,lock=False):
		#computer interaction with spaces
		(j,i) = index[:2]
		space = self.spaces[j][i]
		space.fillColor(color,save,lock)
		
	def undoSpace(self,index):
		(j,i) = index[:2]
		space = self.spaces[j][i]
		space.undoColorChange()
				
	def clearSpaces(self):
		for row in self.spaces:
			for space in row:
				space.clear()
				
	def clearUnlockedSpaces(self):
		for row in self.spaces:
			for space in row:
				if not space.locked:
					space.clear()
