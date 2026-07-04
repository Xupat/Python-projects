import pygame
import math
import random

SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
centerx, centery=WIDTH/2, HEIGHT/2
scaler=min(WIDTH, HEIGHT)
timer=pygame.time.Clock()
fps=60
vec=pygame.math.Vector2
boundry_width=4

class Boundry:
	def __init__(self, x1, y1, x2, y2):
		self.a=vec(x1, y1)
		self.b=vec(x2, y2)
	def draw(self, surf):
		pygame.draw.line(surf, 'white', self.a, self.b, boundry_width)

class Ray:
	def __init__(self, x1, y1, angle):
		self.a=vec(x1, y1)
		self.dire=vec(math.cos(angle), math.sin(angle))
	
	def draw(self, surf, walls):
		closest=math.inf
		draw=None
		for w in walls:
			pt=self.cast(w)
			if pt:
				dist=(pt-self.a).length_squared()
				if dist<closest:
					closest=dist
					draw=pt
		if draw:
			pygame.draw.line(SCREEN, 'white', self.a, draw)
		else:
			pygame.draw.line(surf, 'white', self.a, self.a+self.dire*max(WIDTH, HEIGHT))
	
	def cast(self, wall):
		x1=wall.a.x
		y1=wall.a.y
		x2=wall.b.x
		y2=wall.b.y
		
		x3=self.a.x
		y3=self.a.y
		x4=x3+self.dire.x
		y4=y3+self.dire.y
		
		den=(x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
		if den==0:
			return
		t=((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/den
		u=-((x1-x2)*(y1-y3)-(y1-y2)*(x1-x3))/den
		if t>0 and t<1 and u>0:
			pt=vec(0, 0)
			pt.x=x1+t*(x2-x1)
			pt.y=y1+t*(y2-y1)
			return pt

class Light_orb:
	def __init__(self, x, y):
		self.pos=vec(x, y)
	
	def draw(self, surf):
		pygame.draw.circle(surf, 'white', self.pos, 16)
	def generate_rays(self, start_angle, end_angle, step_size):
		rays=[]
		for i in range(start_angle, end_angle):
			if (i-start_angle)%step_size==0:
				angle=math.radians(i)
				rays.append(Ray(self.pos.x, self.pos.y, angle))
		return rays
		
def make_boundry(num, limit, padding):
	lines=[]
	for _ in range(num):
		x1=random.randint(padding, WIDTH-padding)
		y1=random.randint(padding, HEIGHT-padding)
		x2=random.randint(x1-limit[0], x1+limit[0])
		y2=random.randint(y1-limit[1], y1+limit[1])
		lines.append(Boundry(x1, y1, x2, y2))
	return lines

def main():
	start_angle=0
	end_angle=360
	step_size=4
	boundry_num=15
	
	boundrys=make_boundry(boundry_num, (300, 600), 50)
	light_orb=Light_orb(centerx, centery)
	rays=[Ray(0, 0, math.radians(i)) for i in range(start_angle, end_angle, step_size)]
	while True:
		SCREEN.fill((20, 20, 20))
		
		light_orb.pos=vec(*pygame.mouse.get_pos())
		
		
		for r in rays:
			r.a=light_orb.pos
			r.draw(SCREEN, boundrys)
		for b in boundrys:
			b.draw(SCREEN)
		
		light_orb.draw(SCREEN)
		pygame.display.update()
		timer.tick(fps)
		
main()