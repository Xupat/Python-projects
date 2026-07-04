import pygame
import math
import tools
import gui_tools
from maze_generateor import maze_genrtator
pygame.init()
#gui tools is my personal module to make some buttons, sliders, switch buttons, analogs, and few more stuff
#tools module does a lot of the heavy liftting here, it houses the Map class which is the grid the maze is built on player class which user controls, it houses the ray and ray caster classes which are used to detect walls and render them, and it has modifys and include some settings for starting up
#maze generator genrates s maze as an array which then used to actually make the maze visually
#=================================#
SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
centerx, centery=WIDTH/2, HEIGHT/2
scaler=min(WIDTH, HEIGHT)
timer=pygame.time.Clock()
fps=60
vec=pygame.math.Vector2

Grid_width=int(WIDTH*0.65)
Grid_height=int(HEIGHT)
size=48
rows=int(Grid_width/size)
cols=int(Grid_height/size)
start_pos=((WIDTH-rows*size)/2, (HEIGHT-cols*size)/2)
start_pos=((WIDTH-rows*size)/2, (HEIGHT-cols*size)/2)

Res=15
Rays=math.ceil(WIDTH/Res)
FOV=60

Map=None

#=================================#
#updates a bunch of varaibles 
def update_vals(nsize, nres, nmap):
	global Grid_width, Grid_height, size, rows, cols, start_pos, Res, Rays, FOV, Map
	Grid_width=int(WIDTH)
	Grid_height=int(HEIGHT)
	size=nsize
	rows=int(Grid_width/size)
	cols=int(Grid_height/size)
	rows, cols=nmap.shape
	start_pos=((WIDTH-rows*size)/2, (HEIGHT-cols*size)/2)
	Map=nmap
	
	Res=nres
	Rays=math.ceil(WIDTH/Res)
	FOV=60
	
#main menu with title and start button	
def main_menu():
	run=True
	gui=pygame.font.Font('fonts/Orbitron-VariableFont_wght.ttf', int(scaler*0.15))
	guime=pygame.font.Font('fonts/mine.ttf', int(scaler*0.05))
	bw=400
	bh=150
	btn=gui_tools.Button((centerx-bw/2, centery*1.5-bh, bw, bh), 'Start', 60)
	
	while run:
		SCREEN.fill((20, 20, 20))
		
		text=gui.render('Maze Maniac', True, 'white')
		text_rect=text.get_rect(center=(centerx, centery/3.5))
		SCREEN.blit(text, text_rect)
		
		text3=gui.render('3d', True, 'white')
		text_rect3=text3.get_rect(center=(centerx, centery/1.5))
		SCREEN.blit(text3, text_rect3)
		
		btn.draw(SCREEN)
		if btn.touch(pygame.event.get()):
			setting_game()
			run=False
			return 
		
		pygame.display.update()
		timer.tick(60)
		
#the setting screen right before you start the maze
def setting_game():
	gui_font=pygame.font.Font(None, int(scaler*.09))
	
	gui=pygame.font.Font('fonts/Orbitron-VariableFont_wght.ttf', int(scaler*0.15))
	
	s1p1=(centerx-centerx/2, centery*0.9)
	s1p2=(centerx+centerx/2, s1p1[1])
	slider1=gui_tools.Slider(s1p1, s1p2, 2, 30, 1, 5)
	
	s2p1=(centerx-centerx/2, HEIGHT-centery*0.75)
	s2p2=(centerx+centerx/2, s2p1[1])
	slider2=gui_tools.Slider(s2p1, s2p2, 1, 50, 1, 15)
	
	text=gui_font.render(f'Cells number: {str(0)}', True, 'white')
	text_rect=text.get_rect(center=(centerx-10, centery*0.75))

	text_rect2=text.get_rect(center=(centerx, HEIGHT-centery*0.9))
	
	bw=600
	bh=120
	btn=gui_tools.Button((centerx-bw/2, HEIGHT-centery*0.5, bw, bh), 'Start', int(scaler*0.1))
	
	nsize=size
	nres=Res
	
	run=True
	while run:
		SCREEN.fill((20, 20, 20))
		events=pygame.event.get()
		
		text1=gui.render('Choose your HELL', True, 'white')
		text1_rect=text1.get_rect(center=(centerx, centery/3.5))
		SCREEN.blit(text1, text1_rect)
		
		slider1.draw(SCREEN)
		value=slider1.touch(events)
		nsize=value
		
		slider2.draw(SCREEN)
		value2=slider2.touch(events)
		nres=value2
		

		
		text=gui_font.render(f'Cells number: {str(value)}', True, 'white')
		SCREEN.blit(text, text_rect)
		
		btn.draw(SCREEN)
		if btn.touch(events):
			nmap=maze_genrtator(nsize)
			cell_size=int(min(WIDTH, HEIGHT)/max(nmap.shape))
			update_vals(cell_size, nres, nmap)
			main_2d()
			run=False
			return 
		
		pygame.display.update()
		timer.tick(fps)
#this is where all the magic happens lol, the grid which is the maze itself, is amatrix witgvalues 0,1 this would add a wall if the it sees a 1 in the maze and nothing when it sees a 0
def make_walls(grid):
	walls=[]
	for i in range(rows):
		for j in range(cols):
			if grid.grid[i, j]==0:
				continue
			x=i*size+start_pos[0]
			y=j*size+start_pos[1]
			walls.append(pygame.Rect(x, y, size, size))
	return walls

#this doesnt work the screens actually appear on top of each other, but it is nice fir testing purposes
def main_2d():
	grid=tools.Map(Map, size)
	grid.render(SCREEN, start_pos)
	current_surf=SCREEN.copy()
	walls=make_walls(grid)
	
	player_vel=2
	
	analog, player, btn=tools.settings2(player_vel, WIDTH, HEIGHT, rows, cols, size, start_pos)

	angle=90
	ray_caster=tools.Ray_caster(Rays, size, grid, start_pos, FOV, WIDTH, HEIGHT)

	gui_font=pygame.font.Font(None, 40)
	while True:
		ray_caster.rays=[]
		events=pygame.event.get()
		theta=None
		SCREEN.blit(current_surf, (0, 0))
		
		btn.draw(SCREEN)
		if btn.touch(events):
			SCREEN.fill('black')	
			setting_game()
			return 

		theta=analog.move()
		player.move(theta, walls, player_vel)
		if theta:
			angle=theta
			
	
		ray_caster.cast_all_rays(player.pos.x, player.pos.y, angle)
		ray_caster.render(SCREEN)
		
		player.draw(SCREEN)
		analog.draw(SCREEN)
		pygame.display.update()
		timer.tick(fps)
		
#this is the actual maze being played, it is mostly a collection of rendering a wall and taking analog input, badically uses all the stuff weve been making
def main_3d():
	grid=tools.Map(Map, size)
	this_fps=60
	walls=make_walls(grid)
	player_vel=20/max(grid.grid.shape)
	
	analog, player, btn=tools.settings2(player_vel, WIDTH, HEIGHT, rows, cols, size, start_pos)

	angle=0
	turn_speed=0.15
	
	ray_caster=tools.Ray_caster(Rays, size, grid, start_pos, FOV, WIDTH, HEIGHT)

	gui_font=pygame.font.Font(None, 40)
	background=pygame.image.load('imgs/background.png').convert()
	background=pygame.transform.scale(background, (WIDTH, HEIGHT))
	while True:
		ray_caster.rays=[]
		events=pygame.event.get()
		theta=None
		SCREEN.fill('black')
		SCREEN.blit(background, (0, 0))
		
		theta=analog.move()
		ts=0.05
		if theta:
			if -math.pi/4<theta<math.pi/4:
				angle+=ts
			elif math.pi*3/4<abs(theta)<math.pi:
				angle-=ts
			elif -3*math.pi/4 < theta < -math.pi/4:
				player.move(angle, walls, 1)
			elif  math.pi/4 < theta < 3*math.pi/4:
				player.move(angle, walls, 1)
		
			
		ray_caster.cast_all_rays(player.pos.x, player.pos.y, angle)
		ray_caster.render_3d(SCREEN, size, ((WIDTH/2)/math.tan(math.radians(FOV/2))), Res, HEIGHT, angle)
	
		btn.draw(SCREEN)
		if btn.touch(events):
			SCREEN.fill('black')	
			setting_game()
			return 
		
		
		analog.draw(SCREEN)
		pygame.display.update()
		timer.tick(this_fps)

main_menu()

#final note: this matrix actually does not have an ending by default there is a an outer wall that sorround the matrix if i would improve it i would, work on the maze generator to generate a reasonable exit and check if its possible

#final final note: i did this lol, not here though re did it without tools module or maze generator, the things numpy can do for you... :)