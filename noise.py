from random import random
from math import ceil, log2
	
def nextFactorTwo(num):
	return 2**ceil(log2(num))
	
def perlinNoise1D(size,scaleFactor=2):
	length = nextFactorTwo(size)
	rand = [random() for _ in range(length)]
	result = [None for _ in rand]
	for i in range(length):
		noise = 0
		scale = 1
		scaleSum = 0
		for o in range(int(log2(length))+1):
			#find indexes to sample from
			pitch = length >> o
			index1 = int(i/pitch)*pitch
			index2 = (index1 + pitch) % length
			
			#linearly interpolate between the two samples
			blend = (i - index1) / pitch
			sample = (1-blend) * rand[index1] + blend * rand[index2]
			
			#add sample to the accumulative noise at scaling factor
			noise += sample * scale
			scaleSum += scale
			scale /= scaleFactor
		
		#divide noise by scaleSum to get numbers between 1 and 0
		result[i] = noise / scaleSum
	return result[:size]
	
def perlinNoise2D(dims,scaleFactor=2):
	(rows, cols) = dims
	size = max(nextFactorTwo(rows), nextFactorTwo(cols))
	rand = [[random() for _ in range(size)] for _ in range(size)]
	result = [[None for _ in row] for row in rand]
	for x in range(size):
		for y in range(size):
			noise = 0
			scale = 1
			scaleSum = 0
			for o in range(int(log2(size))+1):
				#find indexes to sample from
				pitch = size >> o
				indexX1 = int(x/pitch)*pitch
				indexY1 = int(y/pitch)*pitch
				indexX2 = (indexX1 + pitch) % size
				indexY2 = (indexY1 + pitch) % size
				
				#linearly interpolate across the x
				blendX = (x - indexX1) / pitch
				blendY = (y - indexY1) / pitch
				sampleA = (1-blendX) * rand[indexY1][indexX1] + blendX * rand[indexY1][indexX2]
				sampleB = (1-blendX) * rand[indexY2][indexX1] + blendX * rand[indexY2][indexX2]
				
				#linearly interpolate across the y and add it to the accumulative noise at scaling factor
				noise += (blendY*(sampleB-sampleA)+sampleA) * scale
				scaleSum += scale
				scale /= scaleFactor
			
			#divide noise by scaleSum to get numbers between 1 and 0
			result[y][x] = noise / scaleSum
	return  [col[:cols] for col in result[:rows]]
