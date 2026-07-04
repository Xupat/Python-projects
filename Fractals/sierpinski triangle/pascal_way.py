import pygame
import math
import numpy as np
pygame.init()

SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
centerx, centery=(WIDTH/2, HEIGHT/2)
CLOCK=pygame.time.Clock()
FPS=1
size=128
block_size=(WIDTH/size)

def make_pascal_array(size):
	pascal=np.zeros((size, size), dtype=np.int32)
	pascal[0, 0]=1
	for x in range(pascal.shape[0]):
		for y in range(pascal.shape[1]):
			if pascal[x, y]!=0 and x+1 < pascal.shape[0]:
				
				if y-1 in range(pascal.shape[1]):
					pascal[x+1, y]=pascal[x, y] +pascal[x, y-1]
				else:
					pascal[x+1, y]=pascal[x, y] 
				pascal[x+1, y+1]=pascal[x, y] +pascal[x, y+1]
				
	return pascal

pascal=make_pascal_array(size)

def draw_tringle(pascal):
	wh, hi=pascal.shape
	half=block_size/2
	start_y=centery -(size/2 * block_size)
	for x in range(wh):
		start_x=centerx - ((x+1)*block_size)/2
		for y in range(hi):
			if pascal[x, y]%2!=0:
				pygame.draw.rect(SCREEN, (255, 50, 0), (start_x+y*block_size, start_y+x*block_size, block_size, block_size))

draw_tringle(pascal)

while True:
	pygame.display.update()
	CLOCK.tick(FPS)
	