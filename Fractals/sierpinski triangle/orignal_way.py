import pygame
import math
pygame.init()

SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
centerx, centery=(WIDTH/2, HEIGHT/2)
CLOCK=pygame.time.Clock()
FPS=1
half=WIDTH*0.45


tringels=[]
def start(color):
	orign=[(centerx-half, centery+half), (centerx+half, centery+half), (centerx, centery-half)]
	pygame.draw.polygon(SCREEN, color, orign)
	tringels.append(orign)


def draw(color):
	new=[]
	for tringle in tringels:
		p1, p2, p3=tringle
		half_point=((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)
		dx=p3[0]-half_point[0]
		dy=p3[1]-half_point[1]
		dist=math.sqrt(dx**2+dy**2)
		half_dist=dist/2
		
		dx2=p2[0]-p1[0]
		dy2=p2[1]-p1[1]
		dist2=math.sqrt(dx2**2+dy2**2)
		half_dist2=dist2/4
		
		left_point=(half_point[0]-half_dist2, half_point[1]-half_dist)
		right_point=(half_point[0]+half_dist2, half_point[1]-half_dist)
		
		tri=[left_point, right_point, half_point]
		tri1=[p1, half_point, left_point]
		tri2=[half_point, p2, right_point]
		tri3=[left_point, right_point, p3]
	
		pygame.draw.polygon(SCREEN, color, tri1)
		pygame.draw.polygon(SCREEN, color, tri2)
		pygame.draw.polygon(SCREEN, color, tri3)
		new.append(tri1)
		new.append(tri2)
		new.append(tri3)
		

	return new
		
		
		
itr=0
max_itr=12
color=(255, 200, 50)
back_color=(20, 20, 20)
while True:
	if itr==0:
		SCREEN.fill(back_color)
		start(color)
	elif itr<max_itr:
		SCREEN.fill(back_color)
		tringels=draw(color)
	itr+=1
	
	pygame.display.update()
	CLOCK.tick(FPS)
