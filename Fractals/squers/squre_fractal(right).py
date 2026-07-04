import pygame
from colorsys import hsv_to_rgb
pygame.init()
SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
SCREEN=pygame.display.set_mode((HEIGHT, WIDTH))
SCREEN.fill((20, 20, 20))
CLOCK=pygame.time.Clock()

instante=False
is_hsv=False

c=1
hue=(c)/360
sat=1
val=1
r, g, b=hsv_to_rgb(hue, sat, val)
if is_hsv:
	color=(int(r*255), int(g*255), int(b*255))
else:
	color=(255, 255, 255)

def add_points(rect, points, before):
	points.append((rect.topleft, 'tl', before))
	points.append((rect.bottomleft, 'bl', before))
	points.append((rect.topright, 'tr', before))
	points.append((rect.bottomright, 'br', before))
	return points
	
points=[]
size=int(HEIGHT*0.32)
center=(WIDTH/2, HEIGHT/2)
start_rect=pygame.Rect(center[0]-size/2, center[1]-size/2, size, size)
pygame.draw.rect(SCREEN, color, start_rect,  7)
points=add_points(start_rect, points, None)

def fractal():
	global size, points, hue, c
	c+=45
	hue=c/360
	r, g, b=hsv_to_rgb(hue, sat, val)
	if is_hsv:
		color=(int(r*255), int(g*255), int(b*255))
	else:
		color=(255, 255, 255)
	size*=0.5
	new=[]
	for rect, dire, last in points[:]:
		if dire==last:
			continue
		x, y=rect
		if dire=='br':
			new_rect=pygame.Rect(x, y ,size, size)
			before='tl'
		elif dire=='tr':
			new_rect=pygame.Rect(x, y-size, size, size)
			before='bl'
		elif dire=='bl':
			new_rect=pygame.Rect(x-size, y, size, size)
			before='tr'
		else:
			new_rect=pygame.Rect(x-size, y-size, size, size)
			before='br'
		pygame.draw.rect(SCREEN, color, new_rect, 7)
		new=add_points(new_rect, new, before)
	points=new
	if size<1:
		return 
	if instante:
		fractal()
		
if instante:
	fractal()


while True:
	if not instante:
		fractal()
		
	hue+=20
	
	pygame.display.update()
	CLOCK.tick(30)
	