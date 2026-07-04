import pygame
pygame.init()
SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
SCREEN=pygame.display.set_mode((HEIGHT, WIDTH))
SCREEN.fill((20, 20, 20))

def add_points(rect, points, before):
	points.append((rect.topleft, 'tl', before))
	points.append((rect.bottomleft, 'bl', before))
	points.append((rect.topright, 'tr', before))
	points.append((rect.bottomright, 'br', before))
	return points
	
points=[]
size=int(HEIGHT*0.33)
center=(WIDTH/2, HEIGHT/2)
start_rect=pygame.Rect(center[0]-size/2, center[1]-size/2, size, size)
pygame.draw.rect(SCREEN, '#FFFFFF', start_rect,  7)
points=add_points(start_rect, points, None)

def fractal():
	global size, points
	size*=0.5
	new=[]
	for rect, dire, last in points[:]:
		if dire==last:
			continue
		if dire=='br':
			new_rect=pygame.Rect(rect[0], rect[1], size, size)
			before='br'
		elif dire=='tr':
			new_rect=pygame.Rect(rect[0], rect[1]-size, size, size)
			before='tr'
		elif dire=='bl':
			new_rect=pygame.Rect(rect[0]-size, rect[1], size, size)
			before='bl'
		else:
			new_rect=pygame.Rect(rect[0]-size, rect[1]-size, size, size)
			before='tl'
		pygame.draw.rect(SCREEN, '#FFFFFF', new_rect, 7)
		new=add_points(new_rect, points, before)
	points=new
	if size<5:
		return 
	fractal()
		
fractal()


while True:
	
	pygame.display.update()
	