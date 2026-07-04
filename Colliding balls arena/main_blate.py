import pygame
import math
import random
from colorsys import hsv_to_rgb
import gui_tools
pygame.init()
pygame.event.set_grab(True)

SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
centerx, centery=WIDTH/2, HEIGHT/2
scaler=min(WIDTH, HEIGHT)
timer=pygame.time.Clock()
FPS=60
vec=pygame.math.Vector2

class Ball:
	def __init__(self, x, y, rad):
		self.pos=vec(x, y)
		self.radius=rad
		self.vel=vec(0, 0)
		self.acc=vec(0, 0.6)
		r, g, b=hsv_to_rgb(random.uniform(0, 1), 1, 1)
		self.color=(int(r*255), int(g*255), int(b*255))
	
	def move(self):
		self.vel+=self.acc
		self.pos+=self.vel
	
	def wall_collision(self, radius, ret=0.98):
		diff=self.pos-vec(centerx, centery)
		dist=diff.length()
		normal=diff.normalize()
		overlab=dist-(radius-self.radius)
		if overlab>0:
			self.pos-=overlab*normal
			v_dot=self.vel.dot(normal)
			self.vel-=2*v_dot*normal
			self.vel*=ret
			
		
	def render(self, surf, color):
		pygame.draw.circle(surf, self.color, self.pos, self.radius)
		if color:
			pygame.draw.circle(surf, color ,self.pos, self.radius, 3)

def start(mode):
	if mode=='b':
		cw=15
		color='white'
	elif mode=='w':
		cw=0
		color='black'
	else:
		cw=15
		color=None
	
	SCREEN.fill('black')
	pygame.draw.circle(SCREEN, 'white', (centerx, centery), centerx, cw)
	return cw, color
	

mode=None
def main():
	global mode
	SCREEN.fill('black')
	bw=WIDTH/3
	nbtn=gui_tools.Button((WIDTH-bw, 0, bw, 80), 'Normal', int(scaler*0.05))
	wbtn=gui_tools.Button((0, 0, bw, 80), 'Black', int(scaler*0.05))
	bbtn=gui_tools.Button((bw, 0, bw, 80), 'White', int(scaler*0.05))

	circle_width, color=start(mode)
	radius=centerx-circle_width
	ball_rad=int(scaler*0.04)
	balls=[]
	run=True
	while run:
		if not mode:
			SCREEN.fill('black')
			pygame.draw.circle(SCREEN, 'white', (centerx, centery), centerx, circle_width)
		events=pygame.event.get()
		for event in events:
			if event.type==pygame.MOUSEMOTION:
				mx, my=pygame.mouse.get_pos()
				diff=vec(centerx, centery)-vec(mx, my)
				dist=math.sqrt(diff.y**2+diff.x**2)
				if abs(dist)+ball_rad>radius:
					continue
				balls.append(Ball(mx, my, ball_rad))
		
		for b in balls:
			b.move()
			b.wall_collision(radius)
			b.render(SCREEN, color)
		
		nbtn.draw(SCREEN)
		bbtn.draw(SCREEN)
		wbtn.draw(SCREEN)
		
		if wbtn.touch(events):
			mode='w'
			run=False
		if bbtn.touch(events):
			mode='b'
			run=False
		if nbtn.touch(events):
			mode=None
			run=False
			
		pygame.display.update()
		timer.tick(FPS)

while True:		
	main()