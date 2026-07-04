import pygame
import math 
import random
pygame.init()

SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
scaler=min(WIDTH, HEIGHT)
centerx, centery=WIDTH/2, HEIGHT/2
timer=pygame.time.Clock()
fps=60

class Block:
	def __init__(self, x, y, width, height, vel):
		self.x=x
		self.y=y
		self.width=width
		self.height=height
		self.prev_pos=[self.x, self.y]
		
		self.velx=vel[0]
		self.vely=vel[1]
		
		self.color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
	
	def draw(self, surf):
		pygame.draw.rect(surf, self.color, (self.x, self.y, self.width, self.height))
	
	def move(self, theta , player_vel=0):
		self.wall_collision()
		if not player_vel:
			self.x+=self.velx
			self.y+=self.vely
		else:
			if theta:
				self.x+=player_vel*math.cos(theta)
				self.y+=player_vel*math.sin(theta)
	def wall_collision(self, ret=1):
		if self.x <0:
			self.x=0
			self.velx*=-ret
		if self.x+self.width>WIDTH:
			self.x=WIDTH-self.width
			self.velx*=-ret
		if self.y <0:
			self.y=0
			self.vely*=-ret
		if self.y+self.height>HEIGHT:
			self.y=HEIGHT-self.height
			self.vely*=-ret
			
		


# ===the function that makes rects=====		
def constructor(rects_num, speed_limit):
	blocks=[]
	for _ in range(rects_num):
		width=int(random.uniform(scaler*0.07, scaler*0.225))
		height=int(random.uniform(scaler*0.07, scaler*0.225))
		previntor=max(width, height)
		x=random.randint(previntor, WIDTH-previntor)
		y=random.randint(previntor, HEIGHT-previntor)
		vel=(random.uniform(-speed_limit, speed_limit), random.uniform(-speed_limit, speed_limit))
		rect=Block(x, y, width, height, vel)
		blocks.append(rect)
	return blocks
#=================================

def rect_collision(rect1, rect2):
	x1, y1, w1, h1=rect1.x, rect1.y, rect1.width, rect1.height
	x2, y2, w2, h2=rect2.x, rect2.y, rect2.width, rect2.height
	return (
	x2< x1 <x2+w2 and y2-h1<y1<y2+h2 or
	x2< x1+w1<x2+w2 and y2-h1<y1<y2+h2)

def resolve_collision(a, b):
	ax1, ay1=a.x, a.y
	ax2, ay2=a.x+a.width, a.y+a.height
	
	bx1, by1=b.x, b.y
	bx2, by2=b.x+b.width, b.y+b.height
	
	if ax2 <bx1 or ax1>bx2  or ay2<by1 or ay1 > by2:
		return False
	
	overlap_x1=ax2-bx1
	overlap_x2=bx2-ax1
	overlap_y1=ay2-by1
	overlap_y2=by2-ay1
	
	min_overlap=min(overlap_x1, overlap_x2, overlap_y1, overlap_y2)
	if min_overlap==overlap_x1:
		a.x-=min_overlap/2
		b.x+=min_overlap/2
	elif min_overlap==overlap_x2:
		a.x+=min_overlap/2
		b.x-=min_overlap/2
	elif min_overlap==overlap_y1:
		a.y-=min_overlap/2
		b.y+=min_overlap/2
	elif min_overlap==overlap_y2:
		a.y+=min_overlap/2
		b.y-=min_overlap/2
	
	
def collision(rects):
	for i in range(len(rects)):
		for j in range(i+1, len(rects)):
			a=rects[i]
			b=rects[j]
			resolve_collision(a, b)
	
	
def main():
	#======rects setting=======
	rects=constructor(5, 0)
	#=======================
	
	# =====player setting====
	player_width=int(scaler*0.09)
	player_height=int(scaler*0.15)
	player_vel=10
	player=Block(centerx-player_width, centery-player_height, player_width, player_height, (0, 0))
	rects.append(player)
	#===========================
	
	while True:
		SCREEN.fill((20, 20, 20))
		
		#=======finding theta========
		theta=None
		if pygame.mouse.get_pressed()[0]:
			mx, my=pygame.mouse.get_pos()
			dx=mx-player.x
			dy=my-player.y
			theta=math.atan2(dy, dx)
		#==========================
		
		collision(rects)
		
		for rect in rects:
			if rect is player:
				rect.color='blue'
				rect.move(theta, player_vel=player_vel)
			else:
				rect.move(theta)
			rect.draw(SCREEN)
			
		timer.tick(fps)
		pygame.display.update()

main()

