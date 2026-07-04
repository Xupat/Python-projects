import pygame
import math, cmath
from random import uniform
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
BLUE=(50, 50, 200)
FPS=30
gui_font=pygame.font.Font('fonts/segoe-ui-symbol.ttf', 50)

max=2.2
step=0.2
zoom=(WIDTH/2) / math.ceil(max/step)


itr=20

centerx, centery=(WIDTH/2, HEIGHT/2)
while True:
	SCREEN.fill(WHITE)
	Grid((SCREEN, WIDTH, HEIGHT), (step, max, zoom), int(WIDTH*0.013), False)
	press=pygame.mouse.get_pressed()[0]
	x, y=pygame.mouse.get_pos()
	
	pointx=((x-centerx)/(zoom))*step
	grid_point=(pointx/step*zoom)+centerx
	pointy=(((y-centery)/zoom)*step)
	grid_point2=HEIGHT-((pointy/step*zoom)+centery)
	
	C=(pointx +pointy*1j)
	
	last_Z=C
	for m in range(itr):
		try:
			Z=last_Z**2
		except:
			continue
		x=(Z.real/step*zoom)+centerx
		y=(Z.imag/step*zoom)+centery
		x2=(last_Z.real/step*zoom)+centerx
		y2=(last_Z.imag/step*zoom)+centery
		pygame.draw.line(SCREEN, RED, (x, y), (x2, y2), 5)
		pygame.draw.circle(SCREEN,BLACK, (x2, y2),5)
		last_Z=Z
	
	radius=(1/step*zoom)
	pygame.draw.circle(SCREEN,BLUE,(centerx, centery), radius, 8)
	
	pygame.display.update()
	CLOCK.tick(FPS)