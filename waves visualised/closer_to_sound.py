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
vec=pygame.math.Vector2

class Wave:
	def __init__(self, x, y, speed, circle=True):
		self.x=x
		self.y=y
		self.rad=0
		self.speed=speed
		self.circle=circle

	def draw(self, surf):
		x=self.x
		y=self.y
		r=self.rad
		pi=np.pi
		if self.circle:
			pygame.draw.circle(surf, 'white', (x, y), r, 2)
		else:
			v1=vec(self.x, self.y)
			v2=vec(centerx, centery)
			delta=vec(v2-v1)
			theta=delta.angle_to(vec(centerx, centery))
			theta=np.atan2(delta.y, delta.x)
			a1=theta-pi/4
			a2=theta+pi/4
			pygame.draw.arc(surf, 'white', (x-r, y-r, r*2, r*2), a1, a2, 2)
	
	def update(self):
		self.rad+=self.speed

def main():
	waves_center=[]
	waves=[]
	max_rad=int(max(WIDTH, HEIGHT))
	speed=5
	dt=0
	while True:
		dt+=1
		SCREEN.fill((30, 30, 30))
		for event in pygame.event.get():
			if event.type==pygame.MOUSEBUTTONDOWN:
				mx, my=pygame.mouse.get_pos()
				waves_center.append((mx, my))
		
		for x, y in waves_center:
			if dt%20==0:
				waves.append(Wave(x, y, speed, circle=False))
			pygame.draw.circle(SCREEN, 'white', (x, y), 5)
		for wave in waves[:]:
			if wave.rad>max_rad/2:
				waves.remove(wave)
			wave.update()
			wave.draw(SCREEN)
		
		pygame.display.update()
		timer.tick(fps)
		
main()
		