import pygame
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
	def __init__(self, x, y, rad, vel, id):
		self.pos=vec(x, y)
		self.radius=rad
		self.vel=vel
		self.id=id
		self.color=(random.randint(30, 255),random.randint(0, 255),random.randint(0, 255))
	
	def move(self):
		self.pos+=self.vel
	
	def wall_collision(self, radius):
		cen_vec=vec(centerx, centery)
		diff=self.pos-cen_vec
		dist=diff.length()
		normal=diff.normalize()
		overlab=dist-(radius-self.radius)
		if overlab>0:
			self.pos-=overlab*normal
			v_dot=self.vel.dot(normal)
			self.vel-=2*v_dot*normal
			return ((radius*normal)+cen_vec, self)
			
	def render(self, surf):
		pygame.draw.circle(surf, self.color, self.pos, self.radius)
		
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
	
	
def circle_line_collision(ball, A, B):
	minx=min(A.x, B.x)-ball.radius
	maxx=max(A.x, B.x)+ball.radius
	miny=min(A.y, B.y)-ball.radius
	maxy=max(A.y, B.y)+ball.radius
	px, py=ball.pos
	if not(minx<=px<=maxx and miny<=py<=maxy):
		return False
	
	AC=ball.pos-A
	AB=B-A
	ab_len=AB.length_squared()
	if ab_len==0:
		return 
	t=AC.dot(AB)/ab_len
	t=max(0, min(1, t))
	closest=A+AB*t
	dist = (ball.pos - closest).length()
	return dist<=ball.radius


def make_balls(rad, vel):
	diffx=int(centerx/3)
	bul=Ball(centerx-diffx, centery-diffx, rad, vec(-vel, -vel), 0)
	bur=Ball(centerx+diffx, centery-diffx, rad, vec(vel, -vel), 1)
	bdl=Ball(centerx-diffx, centery+diffx, rad, vec(-vel, vel), 2)
	bdr=Ball(centerx+diffx, centery+diffx, rad, vec(vel, vel), 3)
	
	return [bul, bdl, bdr, bur]

		
def main():
	bw=WIDTH/5
	nbtn=gui_tools.Button((WIDTH-bw, 0, bw, 80), 'Restart', int(scaler*0.05))
	

	circle_width=15
	radius=centerx-circle_width
	ball_rad=int(scaler*0.05)
	ball_vel=random.uniform(6, 7)
	balls=make_balls(ball_rad, ball_vel)
	balls.sort(key=lambda x:x.id)
	
	lines=[]
	run=True
	while run:
		SCREEN.fill('black')
		pygame.draw.circle(SCREEN, 'white', (centerx, centery), centerx, circle_width)
		events=pygame.event.get()
		
		for b in range(len(balls)):
			balls[b].move()
			for b2 in range(b+1, len(balls)):
				if ball_collision(balls[b], balls[b2]):
					resolve_collision(balls[b], balls[b2])
		
		
		new_lines=[]
		connected_balls=set()
		for p, owner in lines:
			for b in balls:
				if b !=owner and circle_line_collision(b, p, owner.pos):
					owner=b
			connected_balls.add(owner)
			pygame.draw.line(SCREEN, owner.color, p, owner.pos, 1)
			new_lines.append((p, owner))
		lines=new_lines
		if lines:
			balls=[b for b in balls if b in connected_balls]
	
	
		for b in balls:
			hit=b.wall_collision(radius)
			if hit and len(lines)<140:
				lines.append(hit)
			b.render(SCREEN)
		

		nbtn.draw(SCREEN)
		if nbtn.touch(events):
			run=False
		pygame.display.update()
		timer.tick(FPS)

while True:		
	main()