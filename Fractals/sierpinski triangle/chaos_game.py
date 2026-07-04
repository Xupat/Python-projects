import pygame
import random
import math
pygame.init()

SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
centerx, centery=(WIDTH/2, HEIGHT/2)
CLOCK=pygame.time.Clock()
FPS=60

size=WIDTH
half=size/2
points=[(centerx-half, centery+half), (centerx+half, centery+half), (centerx, centery-half)]

def make_line(point):
	connect=random.randint(0, 2)
	new_point=((points[connect][0]+point[0])/2, (points[connect][1]+point[1])/2)
	pygame.draw.circle(SCREEN, (255, 200, 50), new_point, 1)
	return new_point

prev_point=(centerx, centery)
while True:
	for _ in range(10):
		prev_point=make_line(prev_point)
	
	pygame.display.update()
	CLOCK.tick(FPS)