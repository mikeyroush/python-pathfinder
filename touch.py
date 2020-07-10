def isTouched(obj,point):
	(x,y) = point
	(X,Y) = obj.position
	boundX = obj.size.w/2
	boundY = obj.size.h/2
	return X - boundX < x and X + boundX > x and Y - boundY < y and Y + boundY > y
