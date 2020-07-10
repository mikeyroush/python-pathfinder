from scene import *
from adjustColor import *
from touch import *

class Button(ShapeNode):
	def __init__(self,id,fillColor,*args,**kwargs):
		ShapeNode.__init__(self,*args,**kwargs)
		#save default fill color
		self.defaultColor = fillColor
		#change fill color
		self.fill_color = self.defaultColor
		self.id = id
		self.text = LabelNode(str(id),parent=self)
		self.active = False
		self.locked = False
		
	def moveAndScale(self,dimensions):
		#initialize vars
		(x,y,w,h) = dimensions
		
		#move and scale button
		self.path = ui.Path.rect(0,0,w,h)
		self.position = (x,y)
		
		#scale fontSize
		fontSize = w/len(str(self.id))
		font = ('Helvetica', fontSize)
		self.text.font = font
		
	def isPressed(self,point):
		pressed = isTouched(self,point)
		if pressed:
			self.active = True
			self.fill_color = adjustColor(self.defaultColor,0.75)
		return pressed
			
	def release(self):
		self.fill_color = self.defaultColor
		self.active = False
		
	def lock(self):
		self.locked = True
