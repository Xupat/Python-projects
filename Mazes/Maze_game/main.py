import pygame
import math
import numpy as np
import gui_tools as tools
from random import choice, random
from colorsys import hsv_to_rgb
pygame.init()

#screen should be horizontal

SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
centerx, centery=WIDTH/2, HEIGHT/2
scaler=min(WIDTH, HEIGHT)
timer=pygame.time.Clock()
fps=60

#player class this si the small rectangle the user controls, it includes basic methods for collision detecion, and ui stuff
class Player:
	def __init__(self, x, y, size, vel):
		self.x=x
		self.y=y
		self.vel=vel
		self.size=size
		
	def draw(self, surf):
		color=(0, 125, 250)
		pygame.draw.rect(surf, color, (self.x, self.y, self.size, self.size), border_radius=5)
	
	def collide(self, rect, walls):
		for w in walls:
			if rect.colliderect(w):
				return True
		return False
	
	def move(self, substeps, theta, walls):
		if not theta:
			return 
		dx=self.vel*np.cos(theta)
		dy=self.vel*np.sin(theta)
		
		stepx=dx/substeps
		stepy=dy/substeps
		
		for _ in range(substeps):
			rect=pygame.Rect(self.x+stepx, self.y, self.size, self.size)
			collide=False
			for w in walls:
				if rect.colliderect(w):
					collide=True
					break
			if not collide:
				self.x+=stepx
				
			rect=pygame.Rect(self.x, self.y+stepy, self.size, self.size)
			collide=False
			for w in walls:
				if rect.colliderect(w):
					collide=True
					break
			if not collide:
				self.y+=stepy
					
		
#this draws th wall in a way it doesnt include a whole cell (thin line)		
class Cell:
	def __init__(self, x, y, size):
		self.x=x
		self.y=y
		self.size=size
		
		self.visited=False
		self.walls=[True,  True, True, True]
	
	def draw(self, surf, lw):
		x=self.x
		y=self.y
		size=self.size
		msize=size*0.07
			
		#top
		if self.walls[0]:
			pygame.draw.line(surf, 'white', (x, y), (x+size, y), lw)
		#right
		if self.walls[1]:
			pygame.draw.line(surf, 'white', (x+size, y+size), (x+size, y), lw)
		#bottom
		if self.walls[2]:
			pygame.draw.line(surf, 'white', (x+size, y+size), (x, y+size), lw)
		#left
		if self.walls[3]:
			pygame.draw.line(surf, 'white', (x, y), (x, y+size), lw)
			
#generate a mze, its all numpy stuff, god I LOVE numpy 	
# it uses a a depth first search maze generstor algorithem
# it returns an array of values where
""""
2 is wall
50 is walkable
99 is visited cell for a colored track
1 is a cell we are yet to modify cuz the arra
"""
def maze_genrtator(cells):
	rcells=cells*2+1
	sx=1
	sy=1
	grid=np.ones((rcells, rcells))
	grid[:, ::2]=2
	grid[::2, :]=2
	grid[sx, sy]=99
	
	stack=[]
	while 1 in grid:
		top=grid[sx, sy+2] if sy+2 in range(rcells) else None
		right=grid[sx+2, sy] if sx+2 in range(rcells) else None
		bottom=grid[sx, sy-2] if sy-2 in range(rcells) else None
		left=grid[sx-2, sy] if sx-2 in range(rcells) else None
		nighbors=[]
		if top and top!=99:
			nighbors.append((top, (sx, sy+2), 'top'))
		if right and right!=99:
			nighbors.append((right, (sx+2, sy), 'right'))
		if bottom and bottom!=99:
			nighbors.append((bottom,(sx, sy-2),'bottom'))
		if left and left!=99:
			nighbors.append((left, (sx-2, sy), 'left'))
		if nighbors:
			nighbor=choice(nighbors)
			stack.append(nighbor)
		else:
			if stack:
				nighbor=stack.pop()
			else:
				break
		next, pos, dire=nighbor
		grid[pos[0], pos[1]]=99
		sx, sy=pos
		if dire=='top':
			grid[sx, sy-1]=50
		if dire=='bottom':
			grid[sx, sy+1]=50
		if dire=='right':
			grid[sx-1, sy]=50
		if dire=='left':
			grid[sx+1, sy]=50
			
	return grid

#this just makes the grid we will use for drwing the maze in general
def make_grid(cells):
	grid=[[] for i in range(cells)]
	size=int(scaler*0.9/cells)
	revscal=max(WIDTH, HEIGHT)
	start_pos=((revscal - cells*size) /2,  scaler*0.05)
	for x in range(cells):
		for y in range(cells):
			cell=Cell(x*size+start_pos[0], y*size+start_pos[1], size)
			grid[x].append(cell)
	return grid, size, start_pos			

#iterates over each cell and draws it according to a direction that will be given in main loop
def draw_grid2(grid, array_grid, lw):
	for ix in range(len(grid)):
		for iy in range(len(grid[ix])):
			cell=grid[ix][iy]
			aix=ix*2+1
			aiy=iy*2+1
			acell=array_grid[aix, aiy]
			if acell==99:
				if array_grid[aix, aiy-1] ==50:
					cell.walls[0]=False
				if array_grid[aix+1, aiy] ==50:
					cell.walls[1]=False
				if array_grid[aix, aiy+1] ==50:
					cell.walls[2]=False
				if array_grid[aix-1, aiy] ==50:
					cell.walls[3]=False
					
			cell.draw(SCREEN, lw)
			
def bulid_walls(grid, lw):
	walls=[]
	for col in grid:
		for cell in col:
			x, y, s=cell.x, cell.y, cell.size
			if cell.walls[0]:
				walls.append(pygame.Rect(x, y, s, lw))
			if cell.walls[1]:
				walls.append(pygame.Rect(x+s,  y, lw, s))
			if cell.walls[2]:
				walls.append(pygame.Rect(x, y+s, s, lw))
			if cell.walls[3]:
				walls.append(pygame.Rect(x, y, lw, s))
	return walls

	
	
state=None
mins=0
secs=0
dt=0
cells=10

#this is the loop including the actual maze and game	
def main():
	global state, mins, secs, dt, cells
	SCREEN.fill((20, 20, 20))
	
	A_rad=int(scaler*0.18)
	A_pad=int(scaler*0.05)
	A_x=A_rad+A_pad
	A_y=HEIGHT-A_rad-A_pad
	analog=tools.Analog(A_x, A_y, A_rad)
	
	btn1w=200
	btn1h=100
	btn1=tools.Button((WIDTH-btn1w, 0, btn1w, btn1h), 'restart', int(scaler*0.05))
	
	
	walls_thick=2
	grid, cell_size, start_pos=make_grid(cells)
	grid_array=maze_genrtator(cells)
	draw_grid2(grid, grid_array, walls_thick)
	maze_surf=SCREEN.copy()
	
	walls=bulid_walls(grid, walls_thick)
	player_vel=5
	player_size=int(scaler*0.6/cells)
	player=Player(walls_thick+start_pos[0],walls_thick+start_pos[1], player_size, player_vel)
	
	goal_size=int(scaler*0.6/cells)
	goal_x=(cells-1)*cell_size+start_pos[0]+walls_thick+int(scaler*0.3)/cells/2
	goal_y=(cells-1)*cell_size+start_pos[1]+walls_thick+int(scaler*0.3)/cells/2
	goal_rect=pygame.Rect(goal_x, goal_y, goal_size, goal_size)
	
	
	gui=pygame.font.Font(None, int(scaler*0.1))
	
	dt=0
	mins=0
	secs=0
	run=True
	substeps=math.ceil(player_vel)
	
	trail=[]
	lifetime=player_size*0.5
	hue=0
	while run:
		SCREEN.fill((20, 20, 20))
		SCREEN.blit(maze_surf, (0, 0))
		
		events=pygame.event.get()
		if btn1.touch(events):
			state='Lost'
			run=False
			main_menu()
		player_rect=pygame.Rect(player.x, player.y, player.size, player.size)
		if player_rect.colliderect(goal_rect):
			state='Win'
			run=False
			main_menu()
		
		btn1.draw(SCREEN)
		
		analog.draw(SCREEN)
		theta=analog.move()
		player.move(substeps, theta, walls)
		
		if theta:
			hue+=0.001
			hue%=1
			r = int(50  + 40*math.sin(hue*3))
			g = int(180 + 60*math.sin(hue*2))
			b = int(255)
			color = (r, g, b)
			trail.append([player.x, player.y, lifetime, color])
			
		pygame.draw.rect(SCREEN, (255, 200, 0), goal_rect, border_radius=5)
		
		for t in trail[:]:
			x, y, r, c=t
			gll=lifetime/150
			t[2]-=gll
			if r<3:
				trail.remove(t)
			pygame.draw.circle(SCREEN, c, (x+player_size/2, y+player_size/2), r)
			
		player.draw(SCREEN)
		
		text=gui.render(f'{mins:02d}:{secs:02d}', True, 'white')
		SCREEN.blit(text, (10, 10))
		dt+=1
		if dt==60:
			dt=0
			secs+=1
		if secs==60:
			secs=0
			mins+=1
			
		pygame.display.update()
		timer.tick(fps)
	

#bad naming :)
#this actually have the winning/posing menu screen
#i really hate doing ui for anything, this is a total mess sorry
def main_menu():
	global state, mins, secs, dt, cells
	padding=20
	
	background=pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
	background.fill((0, 0, 0, 150))
	SCREEN.blit(background, (0, 0))
	
	
	pw=WIDTH*0.6
	ph=HEIGHT*0.8
	popup=pygame.Surface((pw, ph))
	start=((WIDTH-pw)/2, (HEIGHT-ph)/2)
	
	bw=pw*0.5
	bh=ph*0.2
	btn1=tools.Button((start[0]+bw/2, start[1]+ph-bh-padding, bw, bh), 'start', int(scaler*0.1), color=(50, 150, 150), border=6, border_color=(50, 50, 50))
	
	slider=tools.Slider((start[0]+pw/6, start[1]+ph-ph/3), (start[0]+pw-pw/6, start[1]+ph-ph/3), 5, 50, 1, cells)
	
	state_gui=pygame.font.Font(None, int(scaler*0.15))
	state_outline=gui=pygame.font.Font(None, int(scaler*0.1575))
	time_gui=gui=pygame.font.Font(None, int(scaler*0.1))
	
	popup.fill((100, 100, 100))
	color='green' if state=='Win' else (250, 50,50)
	text1=state_gui.render(str(state), True, color)
	outline1=state_outline.render(str(state), True, 'black')
	text_rect1=text1.get_rect(midtop=(pw/2,  padding))
	popup.blit(outline1, text_rect1)
	popup.blit(text1, text_rect1)
		
	text2=time_gui.render(f'Totel time:{mins:02d}:{secs:02d}.{dt:02d}', True, 'white')
	text2_rect=text2.get_rect(topleft=(padding, ph/4))
	popup.blit(text2, text2_rect)
		
	text3=time_gui.render(f'Maze size:{cells}', True, 'white')
	text3_rect=text3.get_rect(topleft=(padding, ph/2.75))
	popup.blit(text3, text3_rect)
	
	run=True
	value=cells
	while run:
		events=pygame.event.get()
		
		popup.fill((100, 100, 100))
		popup.blit(outline1, text_rect1)
		popup.blit(text1, text_rect1)
		popup.blit(text3, text3_rect)
		
		text4=time_gui.render(f'Cells :{value}', True, 'white')
		text4_rect=text4.get_rect(center=(pw/2,ph/1.8))
		popup.blit(text4, text4_rect)
	
		pygame.draw.line(popup, (50, 50, 50), (0, ph/5), (pw, ph/5), int(padding/4))
		pygame.draw.rect(popup, (50, 50, 50), (0, 0, pw, ph), int(padding/2))
		SCREEN.blit(popup, start)
		
		if btn1.touch(events):
			cells=value
			main()
			run=False
			return 
		slider.draw(SCREEN)
		value=slider.touch(events)
		
		btn1.draw(SCREEN)
	
		pygame.display.update()
		timer.tick(fps)

#"REAL" main menu the first thing you see when running
def real_main_menu():
	
	run=True
	gui=pygame.font.Font('fonts/Orbitron-VariableFont_wght.ttf', int(scaler*0.15))
	guime=pygame.font.Font('fonts/mine.ttf', int(scaler*0.05))
	bw=400
	bh=150
	btn=tools.Button((centerx-bw/2, centery*1.5-bh, bw, bh), 'Start', 60)
	
	while run:
		SCREEN.fill((20, 20, 20))
		
		text=gui.render('Maze Maniac', True, 'white')
		text_rect=text.get_rect(center=(centerx, centery/3))
		SCREEN.blit(text, text_rect)

		btn.draw(SCREEN)
		if btn.touch(pygame.event.get()):
			main()
			run=False
		
		pygame.display.update()
		timer.tick(fps)
		
real_main_menu()