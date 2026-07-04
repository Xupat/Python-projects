import pygame
import math
from grid import Grid
pygame.init()

pygame.init()
SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH , HEIGHT=SCREEN.get_size()
SCREEN=pygame.display.set_mode((HEIGHT, WIDTH))
CLOCK=pygame.time.Clock()
WHITE=(220, 220, 220)
BLACK=(30, 30, 30)
GRAY=(200,200,200)
RED=(200,50,50)
FPS=30
gui_font=pygame.font.Font('fonts/segoe-ui-symbol.ttf', 50)

max=5.5
step=0.5
zoom=(WIDTH/2) / math.ceil(max/step)


itr=5
centerx, centery=(WIDTH/2, HEIGHT/2)
while True:
	SCREEN.fill(WHITE)
	Grid((SCREEN, WIDTH, HEIGHT), (step, max, zoom), int(WIDTH*0.013), False)
	press=pygame.mouse.get_pressed()[0]
	x=pygame.mouse.get_pos()[0]
	
	point=((x-centerx)/(zoom))*step
	grid_point=(point/step*zoom)+centerx
	new_point=point
	pygame.draw.circle(SCREEN,BLACK, (grid_point, centery),5)

	for m in range(itr):
		new_point=new_point**2
		new_grid_point=(new_point/step*zoom)+centerx
		pygame.draw.line(SCREEN, RED, (centerx, centery), (new_grid_point, centery), 4)
		pygame.draw.circle(SCREEN,BLACK, (new_grid_point, centery),5)
		
	print(point, grid_point)
	text=gui_font.render(str(point), True, BLACK)
	text_rect=text.get_rect(topleft=(0,0))
	#SCREEN.blit(text, text_rect)
	
	pygame.display.update()
	CLOCK.tick(FPS)