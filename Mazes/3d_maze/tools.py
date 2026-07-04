import pygame
import numpy as np
import math
import gui_tools

vec=pygame.math.Vector2
class Map:
	def __init__(self, grid, size):
		self.grid=grid
		self.size=size
	
	def wall_at(self, x, y, start_pos):
		h = (int((x - start_pos[0]) / self.size), int((y - start_pos[1]) / self.size))
		if 0 <= h[0] < self.grid.shape[0] and 0 <= h[1] < self.grid.shape[1]:
			return h if self.grid[h] == 1 else None
		return None
	
	def wall_at2(self, x, y, start_pos):
		h = (int((x - start_pos[0]) / self.size), int((y - start_pos[1]) / self.size))
		if x>start_pos[0] and y>start_pos[1]:
			try:
				self.grid[h]
			except:
				return 
			return h
	
	def render(self, surf, start_pos):
		for i in range(len(self.grid)):
			for j in range(len(self.grid[i])):
				x=i*self.size+start_pos[0]
				y=j*self.size+start_pos[1]
				if self.grid[i, j]==0:
					pygame.draw.rect(surf, 'white', (x, y, self.size-1, self.size-1))
				else:
					pygame.draw.rect(surf, (80, 80, 80), (x, y, self.size-1, self.size-1))

class Player:
	def __init__(self, x, y, rad, vel):
		self.pos=vec(x, y)
		self.rad=rad
		self.vel=vel
	def draw(self, surf):
		pygame.draw.circle(surf, (250, 50, 0), self.pos, self.rad)
		
	def move(self, theta, walls, substeps):
		if theta:
			dx=self.vel*math.cos(theta)
			dy=self.vel*math.sin(theta)
			
			stepx=dx/substeps
			stepy=dy/substeps
			for _ in range(substeps):
				rect=pygame.Rect(self.pos.x-self.rad+stepx, self.pos.y-self.rad, self.rad*2, self.rad*2)
				h=False
				for w in walls:
					if rect.colliderect(w):
						h=True
						break
				if not h:
					self.pos.x+=stepx
				
				rect=pygame.Rect(self.pos.x-self.rad, self.pos.y-self.rad+stepy, self.rad*2, self.rad*2)
				h=False
				for w in walls:
					if rect.colliderect(w):
						h=True
						break
				if not h:
					self.pos.y+=stepy
			
class Ray:
	def __init__(self, x1, y1, angle):
		self.a=vec(x1, y1)
		self.dire=vec(math.cos(angle), math.sin(angle))
		self.wall_hitx=self.a.x
		self.wall_hity=self.a.y
		self.dist=0
		
		self.color=255
	
	def distance(self, x1, y1, x2, y2):
		return math.sqrt((x2-x1)**2+(y2-y1)**2)
		
	def cast(self, csize, map, start_pos, WIDTH, HEIGHT):
		dire=math.atan2(self.dire[1], self.dire[0])
		is_down = 0<dire<math.pi
		is_up = not is_down
		is_right = -0.5*math.pi<dire<0.5*math.pi
		is_left = not is_right
		
		horz_hit=None
		horz_hitx=None
		horz_hity=None
		
		first_x=None
		first_y=None
		
		if is_up:
			first_y=math.floor((self.a.y-start_pos[1])/csize)*csize-0.001+start_pos[1]
		elif is_down:
			first_y=math.floor((self.a.y-start_pos[1])/csize)*csize+csize +start_pos[1]
		if math.tan(dire):
			first_x=self.a.x+(first_y-self.a.y)/math.tan(dire)
		else:
			first_x=self.a.x+(first_y-self.a.y)/0.00001
		
		next_x=first_x
		next_y=first_y
		
		xa=0
		ya=0
		
		if is_up:
			ya=-csize
		elif is_down:
			ya=csize
		
		try:
			xa=ya/math.tan(dire)
		except:
			xa=ya/0.0001
		
		while (start_pos[0]<=next_x<=WIDTH-start_pos[0] and start_pos[1]<=next_y<=HEIGHT-start_pos[1]):
			h=map.wall_at(next_x, next_y, start_pos)
			if h and map.grid[h[0], h[1]]==1:
				horz_hit=True
				horz_hitx=next_x
				horz_hity=next_y
				break
			else:
				next_x+=xa
				next_y+=ya
		
		vert_hit=None
		vert_hitx=None
		vert_hity=None
		
		first_vert_x=None
		first_vert_y=None
		
		posx=int((self.a.x-start_pos[0])/csize)
		if is_left:
			first_vert_x=posx*csize-0.001 + start_pos[0]
		elif is_right:
			first_vert_x=posx*csize+csize+start_pos[0]
	
		first_vert_y=self.a.y+(first_vert_x-self.a.x)*math.tan(dire)
		
		next2_x=first_vert_x
		next2_y=first_vert_y
		
		xa2=0
		if is_right:
			xa2=csize
		elif is_left:
			xa2=-csize
		
		ya2=xa2*math.tan(dire)
		
		while (start_pos[0]<=next2_x<=WIDTH-start_pos[0] and start_pos[1]<=next2_y<=HEIGHT-start_pos[1]):
			h=map.wall_at(next2_x, next2_y, start_pos)
			if h and map.grid[h]==1:
				vert_hit=True
				vert_hitx=next2_x
				vert_hity=next2_y
				break
			else:
				next2_x+=xa2
				next2_y+=ya2
		
		horz_dist=0
		vert_dist=0
		if horz_hit:
			horz_dist=self.distance(self.a.x, self.a.y, horz_hitx, horz_hity)
		else:
			horz_dist=math.inf
		if vert_hit:
			vert_dist=self.distance(self.a.x, self.a.y, vert_hitx, vert_hity)
		else:
			vert_dist=math.inf
		if horz_dist<vert_dist:
			self.wall_hitx=horz_hitx
			self.wall_hity=horz_hity
			self.dist=horz_dist
			self.color=160
		elif vert_dist<horz_dist:
			self.wall_hitx=vert_hitx
			self.wall_hity=vert_hity
			self.dist=vert_dist
			self.color=255
		
		if self.dist:
			self.color=255/(1+self.dist*(1/csize))
		if self.color>255:self.color=255
		if self.color<0:self.color=0
		
	
	def draw(self, surf):
		if self.wall_hitx is not None and self.wall_hity is not None:
			pygame.draw.line(surf, (255,0,0), self.a, (self.wall_hitx, self.wall_hity))
	

class Ray_caster:
	def __init__(self, rays_num, size, Map, start_pos, FOV, w, h):
		self.rays=[]
		self.rays_num=rays_num
		self.size=size
		self.Map=Map
		self.start_pos=start_pos
		self.Fov=FOV
		self.w=w
		self.h=h
	def cast_all_rays(self, x, y, angle):
		angle=math.degrees(angle)
		ray_angle=angle-self.Fov/2
		for _ in range(self.rays_num):
			ray=Ray(x, y, math.radians(ray_angle))
			ray.cast(self.size, self.Map, self.start_pos, self.w, self.h)
			self.rays.append(ray)
			ray_angle+=(self.Fov/self.rays_num)
		
	def render(self, surf):
		for r in self.rays:
			r.draw(surf)
	def render_3d(self, surf, orgih, proj_planeh, res, screenh, theta):
		i=0
		for r in self.rays:
			dire=math.atan2(r.dire[1], r.dire[0])
			if theta:
				r.dist*=math.cos(theta-dire)
			if not r.dist:
				r.dist=0.0001
			line_height=(orgih/r.dist)*proj_planeh
			draw_start=(screenh/2)-(line_height/2)
			draw_end=line_height
			pygame.draw.rect(surf, (r.color, r.color, r.color), (i*res, draw_start, res, draw_end))
			i+=1

			
def settings2(vel, WIDTH, HEIGHT, rows, cols, size, start_pos):
	scaler=min(WIDTH, HEIGHT)
	analog_rad=scaler*0.15
	padding=scaler*0.025
	x=analog_rad+padding
	y=HEIGHT-analog_rad-padding
	analog=gui_tools.Analog(x, y, analog_rad)
	
	player_x=start_pos[0]+1*size+size/2
	player_y=start_pos[1]+size/2+size
	player_rad=int(size/4)
	player=Player(player_x, player_y, player_rad, vel)
	
	bw=200
	bh=100
	btn=gui_tools.Button((WIDTH-bw, 0, bw, bh), 'return', int(scaler*0.075))
	return analog, player, btn
	
