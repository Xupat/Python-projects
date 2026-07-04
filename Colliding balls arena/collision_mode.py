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
	def __init__(self, x, y, rad, vel):
		self.pos=vec(x, y)
		self.radius=rad
		self.vel=vel
		r, g, b=hsv_to_rgb(random.uniform(0, 1), 1, 1)
		self.color=(int(r*255), int(g*255), int(b*255))
	
	def move(self):
		self.pos+=self.vel
	
	def wall_collision(self, radius):
		diff=self.pos-vec(centerx, centery)
		dist=diff.length()
		normal=diff.normalize()
		overlab=dist-(radius-self.radius)
		if overlab>0:
			self.pos-=overlab*normal
			v_dot=self.vel.dot(normal)
			self.vel-=2*v_dot*normal
			
	def render(self, surf, color):
		pygame.draw.circle(surf, self.color, self.pos, self.radius)
		if color:
			pygame.draw.circle(surf, color,self.pos, self.radius, 3)
		
def ball_collision(b1,b2):
	diff=b2.pos-b1.pos
	dist=diff.length_squared()
	min_dist=(b1.radius+b2.radius)**2
	return dist<min_dist

def resolve_collision(b1, b2, e=1):
	diff=b2.pos-b1.pos
	dist=diff.length()
	normal=diff.normalize()
	min_dist=b1.radius+b2.radius
	overlab=min_dist-dist
	if overlab<0:
		return 
	b1.pos-=normal*(overlab/2)
	b2.pos+=normal*(overlab/2)
	
	rel_vel=b1.vel-b2.vel
	rel_vel_unit=rel_vel.dot(normal)
	J=-(1+e)*rel_vel_unit/2
	vectorj=J*normal
	b1.vel+=vectorj
	b2.vel-=vectorj

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
	pygame.draw.circle(SCREEN, 'white', (centerx, centery), centerx, cw)
	return cw, color		

def make_balls(rad, vel):
	diffx=int(centerx/3)
	bul=Ball(centerx-diffx, centery-diffx, rad, vec(-vel, -vel))
	bur=Ball(centerx+diffx, centery-diffx, rad, vec(vel, -vel))
	bdl=Ball(centerx-diffx, centery+diffx, rad, vec(-vel, vel))
	bdr=Ball(centerx+diffx, centery+diffx, rad, vec(vel, vel))
	
	return [bul, bdl, bdr, bur]
	
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
	ball_rad=int(scaler*0.06)
	vel=7
	balls=make_balls(ball_rad, vel)
	
	
	run=True
	while run:
		if not mode:
			SCREEN.fill('black')
			pygame.draw.circle(SCREEN, 'white', (centerx, centery), centerx, circle_width)
	
		events=pygame.event.get()
		for e in events:
			if e.type==pygame.MOUSEBUTTONDOWN:
				balls.append(Ball(*pygame.mouse.get_pos(), ball_rad, vec(vel or -vel, vel or -vel)))
		
		for b in range(len(balls)):
			balls[b].move()
			
			for b2 in range(b+1, len(balls)):
				if ball_collision(balls[b], balls[b2]):
					resolve_collision(balls[b], balls[b2])
			balls[b].wall_collision(radius)
			balls[b].render(SCREEN, color)
		
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