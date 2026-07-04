import pygame
import random
import math
pygame.init()

SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
centerx, centery=(WIDTH/2, HEIGHT/2)
CLOCK=pygame.time.Clock()
FPS=60

scale=WIDTH*0.17
offset_x=WIDTH*0.45
offset_y=HEIGHT*0.08

def make_line(point):
	x, y=point
	percent=random.randint(1, 100)
	case1=(percent==1)
	case2=(1<percent<=8)
	case3=(8<percent<=15)
	case4=(15<percent)
	
	if case1:
		newx=0.2*x-0.26*y
		newy=0.23*x+0.22*y+1.6
	elif case2:
		newx=0.15*x+0.28*y
		newy=0.26*x+0.24*y+0.44
	elif case3:
		newx=0
		newy=0.16*y
	else:
		newx=0.85*x+0.04*y
		newy=-0.04*x+0.85*y+1.6
	
	px=int(newx*scale+offset_x)
	py=int(newy*scale + offset_y)
	pygame.draw.circle(SCREEN, (50, 255, 50), (px, HEIGHT-py), 1)
	return(newx, newy)
	
prev_point=(0, 0)
while True:
	for _ in range(5000):
		prev_point=make_line(prev_point)
	
	pygame.display.update()
	CLOCK.tick(FPS)