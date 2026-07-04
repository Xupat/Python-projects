import pygame
import math, cmath
from random import uniform
from sys import exit
import os
import time
import multiprocessing
from colorsys import hsv_to_rgb
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
FPS=60
gui_font=pygame.font.Font('fonts/segoe-ui-symbol.ttf', 50)

step=0.2
max_val=step*11

zoom=(WIDTH/2) / math.ceil(max_val/step)


draw_colored=True

centerx, centery=(WIDTH/2, HEIGHT/2)
SCREEN.fill(WHITE)
Grid((SCREEN, WIDTH, HEIGHT), (step, max_val, zoom), int(WIDTH*0.013), False)

def stabilty_test(C):
	last_Z=C
	itr=200
	last_itr=itr
	for m in range(itr):
		try:
			Z=last_Z**2+C
			#Z=complex(abs(last_Z.real), abs(last_Z.imag))**2+C
		except:
			continue
		if abs(Z) >2:
			nc=m+1 - math.log(math.log(abs(Z), 2), 2)
			return nc, itr
		last_Z=Z
	return (itr, itr)
	
drawx=0
drawy=0

def draw_a_row():
	cell=1
	global drawx, drawy, julia_set
	for i in range(500):
		real_pos=(drawx, drawy)
		pointx=((real_pos[0] - centerx)/(zoom))*step
		pointy=((real_pos[1]-centery)/(zoom))*step
		C=(pointx+pointy*1j)
		real1=(C.real/step*zoom)+centerx
		real2=(C.imag/step*zoom)+centery
		real=(drawx, drawy)
		
		last_itr, max_itr=stabilty_test(C)
		if last_itr == max_itr:
			colors=BLACK
		else:
			hue=1
			val=1
			sat=1
			hue=max(0.0, min(1.0, last_itr/max_itr))
			r, g, b=hsv_to_rgb(hue, sat, val)
			colors=(int(r*255), int(g*255), int(b*255))
		
		if draw_colored:
			pygame.draw.rect(SCREEN,colors, (drawx, drawy, cell, cell))
		else:
			if max_itr==last_itr:
				pygame.draw.rect(SCREEN,BLUE, (drawx, drawy, cell, cell))
			else:
				pygame.draw.rect(SCREEN,BLACK, (drawx, drawy, cell, cell))
			
		drawy+=cell
		if drawy >HEIGHT:
			drawy=0
			drawx+=cell

t0=time.time()						
while True:
	
	draw_a_row()

	pygame.display.update()
	CLOCK.tick(FPS)
	
	if drawx >WIDTH:
		#pygame.image.save(SCREEN, 'mandlebrot_test.png')
		print(time.time()-t0)
		pygame.qui()
		exit()