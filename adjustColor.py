from colorsys import rgb_to_hls, hls_to_rgb
from matplotlib.colors import hex2color

def adjustColor(hex,factor):
	#convert hex to hls
	(r,g,b) = hex2color(hex)
	(h,l,s) = rgb_to_hls(r,g,b)
	#adjust color
	l = max(min(l * factor, 1.0), 0.0)
	#convert back
	(r,g,b) = hls_to_rgb(h,l,s)
	(r,g,b) = int(r*255),int(g*255),int(b*255)
	return '#{:02x}{:02x}{:02x}'.format(r,g,b)
