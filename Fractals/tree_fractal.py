import pygame
from math import cos, pi, sin, cosh

pygame.init()
SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
SCREEN=pygame.display.set_mode((HEIGHT, WIDTH))
CLOCK=pygame.time.Clock()
FPS=60
SCREEN.fill((20, 20, 20))


def main():
	heads=[]
	length=HEIGHT*0.19
	
	angle=-pi/2
	delta=pi/8
	delta2=pi/11
	
	x0, y0=(WIDTH/2, HEIGHT)
	x1=x0+cos(angle)*length
	y1=y0+sin(angle)*length
	pygame.draw.line(SCREEN, '#FFFFFF', (x0, y0), (x1, y1))
	heads.append((x1, y1, angle))
	while True:
		while True:
			new=[]
			length*=0.81
			if length<=5:
				break
			for x, y, ang in heads:
				nx=x+cos(ang+delta)*length
				ny=y+sin(ang+delta)*length
				pygame.draw.line(SCREEN, '#FFFFFF', (x, y), (nx, ny))
				new.append((nx, ny, ang+delta))
				nx=x+cos(ang-delta)*length
				ny=y+sin(ang-delta)*length
				pygame.draw.line(SCREEN, '#FFFFFF', (x, y), (nx, ny))
				new.append((nx, ny, ang-delta))
				
			heads=new
	
		pygame.display.update()
		CLOCK.tick(FPS)
		
main()