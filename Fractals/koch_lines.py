import pygame
from math import sin, cos, sqrt, atan2, degrees, radians
import numpy

pygame.init()

SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
centerx, centery=(WIDTH/2, HEIGHT/2)

BLACK=(20, 20, 20)
WHITE=(230, 230, 230)
SCREEN.fill(BLACK)

CLOCK=pygame.time.Clock()
FPS=1

size=int(WIDTH*0.8)
half=size*0.5
line_width=1
lines=[]
itr=0
max_itr=6
instante=False

tp1=(centerx-half, centery+half)
tp2=(centerx+half, centery+half)
tp3=(centerx, centery-half)
lines=[(tp1, tp2), (tp2, tp3), (tp3, tp1)]


def draw():
	new=[]
	SCREEN.fill(BLACK)
	for line in lines:
		p1, p2=line
		dx=(p2[0]- p1[0])
		dy=(p2[1]- p1[1])
		dist=sqrt(dx**2 + dy**2)
		theta=atan2(dy, dx)
		third=dist/3
		
	
		p3=(p1[0]+third*cos(theta), p1[1]+third*sin(theta))
		p4=(p2[0]-third*cos(theta), p2[1]-third*sin(theta))
		sp=((p3[0]+p4[0])/2, (p3[1]+p4[1])/2)
		
		nx=-dy/dist
		ny=dx/dist
		h=third*sqrt(3)/2
		
		p5=(sp[0]+nx*h, sp[1]+ny*h)
		
		
		
		pygame.draw.line(SCREEN, WHITE, p1, p3, line_width)
		new.append((p1, p3))
		pygame.draw.line(SCREEN, WHITE, p2, p4, line_width)
		new.append((p4, p2))
		
		pygame.draw.line(SCREEN, WHITE, p3, p5, line_width)
		new.append((p3, p5))
		pygame.draw.line(SCREEN, WHITE, p5, p4 , line_width)
		new.append((p5, p4))
	
	return new
		
while True:
	if itr==0:
		for p1, p2 in lines:
			pygame.draw.line(SCREEN, WHITE, p1, p2, line_width)
	if instante:
		for i in range(max_itr):
			lines=draw()
	elif itr <max_itr:
		lines=draw()
	itr+=1

	pygame.display.update()
	CLOCK.tick(FPS)