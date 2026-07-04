import pygame
pygame.init()
SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
SCREEN=pygame.display.set_mode((HEIGHT, WIDTH))
SCREEN.fill((20, 20, 20))

def add_points(rect, points):
	points.append((rect.topleft, 'tl'))
	points.append((rect.bottomleft, 'bl'))
	points.append((rect.topright, 'tr'))
	points.append((rect.bottomright, 'br'))
	return points
	
points=[]
size=int(HEIGHT*0.4)
center=(WIDTH/2.35, HEIGHT/3)
start_rect=pygame.Rect(center[0]-size/2, center[1]-size/2, size, size)
pygame.draw.rect(SCREEN, '#FFFFFF', start_rect,  7)
points=add_points(start_rect, points)

def fractal():
	global size, points
	size*=0.5
	new=[]
	for rect, dire in points[:]:
		new_rect=pygame.Rect(rect[0], rect[1], size, size)
		pygame.draw.rect(SCREEN, '#FFFFFF', new_rect, 7)
		new=add_points(new_rect, points)
	points=new
	if size<3:
		return 
	fractal()
		
fractal()


while True:
	
	pygame.display.update()
	