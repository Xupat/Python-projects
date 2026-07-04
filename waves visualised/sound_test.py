import pygame
import math
import numpy as np
pygame.init()

SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
centerx, centery=WIDTH/2, HEIGHT/2
scaler=min(WIDTH, HEIGHT)
timer=pygame.time.Clock()
fps=60

class Wave:
	def __init__(self, x, y, speed):
		self.x=x
		self.y=y
		self.rad=0
		self.speed=speed
		
	def draw(self, surf):
		pygame.draw.circle(surf, 'white', (self.x, self.y), self.rad, 2)
	
	def update(self):
		self.rad+=self.speed


def main():
	waves=[]
	max_rad=int(max(WIDTH, HEIGHT))
	while True:
		SCREEN.fill((30, 30, 30))
		for event in pygame.event.get():
			if event.type==pygame.MOUSEMOTION:
				mx, my=pygame.mouse.get_pos()
				waves.append(Wave(mx, my, 10))
		
		for wave in waves[:]:
			if wave.rad>max_rad:
				waves.remove(wave)
			wave.update()
			wave.draw(SCREEN)
		
		pygame.display.update()
		timer.tick(fps)
		
main()
		