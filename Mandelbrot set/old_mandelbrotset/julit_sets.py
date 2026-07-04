import pygame
import math, cmath
from random import uniform
from sys import exit
import os
import random
import numpy as np
import multiprocessing
from colorsys import hsv_to_rgb
from grid import Grid
pygame.init()

pygame.init()
SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH , HEIGHT=SCREEN.get_size()

CLOCK=pygame.time.Clock()
WHITE=(220, 220, 220)
BLACK=(30, 30, 30)
GRAY=(200,200,200)
RED=(200,50,50)
BLUE=(50, 50, 200)
FPS=60
gui_font=pygame.font.Font('fonts/segoe-ui-symbol.ttf', 50)

step=0.2
max_val=step*11

zoom=(WIDTH/2) / math.ceil(max_val/step)

draw_colored=True
num=0

centerx, centery=(WIDTH/2, HEIGHT/2)
SCREEN.fill(WHITE)
Grid((SCREEN, WIDTH, HEIGHT), (step, max_val, zoom), int(WIDTH*0.013), False)
	
set_number=0
sets=[complex(-1.25, 0),
complex(0.35, 0.35),
complex(0.4, 0.4),
complex(-0.7269, 0.1889),
complex(0, -0.8),
complex(-0.835, -0.2321),
complex(-0.70176, -0.3842),
complex(0.45, 0.1428),
complex(-0.4, 0.6), 
complex(-0.8,0.156), 
complex(0,0), 
complex(0.285, 0.01), 
complex(0.3, 0.5), 
]
julia_set=sets[set_number]

cores=os.cpu_count()
max_itr=360

def make_section(cpu_id, julia_c, q, max_itr=max_itr):
	rows=math.ceil(WIDTH/cores)
	start_x=cpu_id*rows
	end_x=min(start_x+rows, WIDTH)
	
	x=np.arange(start_x, end_x)-centerx
	y=np.arange(HEIGHT)-centery
	px, py=np.meshgrid(x/zoom*step, y/zoom*step, indexing='ij')
	
	Z=px+1j*py
	C=julia_c
	
	output=np.zeros(Z.shape, dtype=np.float32)
	mask=np.ones(Z.shape, dtype=bool)
	
	for i in range(max_itr):
		Z[mask]=Z[mask]**2+C
		escaped=np.abs(Z)>2
		output[escaped & mask]= i- np.log(np.log(np.abs(Z[escaped & mask])))/np.log(2)
		mask&= ~escaped
		if not mask.any():
			break
	output[mask]=max_itr
	q.put((cpu_id, output))
	
def merge_lists(lists):
	lists.sort(key=lambda x:x[0])
	return np.vstack([item[1] for item in lists])
		
def render_shape_hsv(pixels):
	rgb=np.zeros((pixels.shape[0], pixels.shape[1], 3), dtype=np.uint8)
	
	mask=(pixels==max_itr)
	rgb[mask]=BLACK
	
	not_mask= ~mask
	vals=pixels[not_mask]/max_itr
	vals=(0.95 +10*vals)%1
	
	h=vals
	s=np.ones_like(vals)
	v=np.ones_like(vals)
	
	i=(h*6).astype(int)
	f=(h*6)-i
	p=v*(1-s)
	q=v*(1-f*s)
	t=v*(1-(1-f)*s)
	
	r=np.zeros_like(h)
	g=np.zeros_like(h)
	b=np.zeros_like(h)
	
	i_mod=i%6
	num=0
	r[i_mod==num]=v[i_mod==num]
	g[i_mod==num]=t[i_mod==num]
	b[i_mod==num]=p[i_mod==num]
	num+=1
	
	r[i_mod==num]=q[i_mod==num]
	g[i_mod==num]=v[i_mod==num]
	b[i_mod==num]=p[i_mod==num]
	num+=1
	
	r[i_mod==num]=p[i_mod==num]
	g[i_mod==num]=v[i_mod==num]
	b[i_mod==num]=t[i_mod==num]
	num+=1
	
	r[i_mod==num]=p[i_mod==num]
	g[i_mod==num]=q[i_mod==num]
	b[i_mod==num]=v[i_mod==num]
	num+=1
	
	r[i_mod==num]=t[i_mod==num]
	g[i_mod==num]=p[i_mod==num]
	b[i_mod==num]=v[i_mod==num]
	num+=1
	
	r[i_mod==num]=v[i_mod==num]
	g[i_mod==num]=p[i_mod==num]
	b[i_mod==num]=q[i_mod==num]
	num+=1
	
	rgb[not_mask]=np.column_stack((r, g, b))*255
	
	pygame.surfarray.blit_array(SCREEN, rgb)
	pygame.display.update()

def render_shape_histogram(pixels):
	rgb=np.zeros((pixels.shape[0], pixels.shape[1], 3), dtype=np.uint8)
	
	mask=(pixels==max_itr)
	rgb[mask]=BLACK
	
	not_mask= ~mask
	vals=pixels[not_mask]
	
	c=(vals*12).astype(np.uint32)
	
	r=c%256
	g=(c*2)%256
	b=(c*5)%256
	
	rgb[not_mask]=np.stack((r, g, b), axis=1)
	pygame.surfarray.blit_array(SCREEN, rgb)
	pygame.display.update()
	
def draw_set(pixels, max_itr=max_itr):
	count=0
	for x in range(pixels.shape[0]):
		for y in range(pixels.shape[1]):
			val=pixels[x, y]
			if np.isnan(val) or np.isinf(val):
				val=max_itr
			if val>=max_itr:
				colors=BLACK
			else:
				hue=(0.95 + 10*val/max_itr)%1
				r, g, b=hsv_to_rgb(hue, 1, 1)
				colors=(int(r*255), int(g*255), int(b*255))
			SCREEN.set_at((x, y), colors)
			#pygame.draw.rect(SCREEN,colors, (x, y, 1, 1))
			count+=1
			if count==700:
				pygame.display.update()
				count=0
				
num=0
julia_copy=sets[:]
random.shuffle(julia_copy)
for julia_c in julia_copy:
	q=multiprocessing.Queue()
	procs=[]
	for cpu in range(cores):
		p=multiprocessing.Process(target=make_section, args=(cpu,julia_c, q))
		procs.append(p)
		p.start()
	
	results=[q.get() for _ in range(cores)]
	for p in procs:
		p.join()
		
	pixels=merge_lists(results)
	instante=True
	save=False
	if instante:
		render_shape_hsv(pixels)
	else:
		draw_set(pixels)
		SCREEN.fill(WHITE)
		Grid((SCREEN, WIDTH, HEIGHT), (step, max_val, zoom), int(WIDTH*0.013), False)
	pygame.display.update()
	if save:
		num+=1
		name=f'julia set{num}.png'
		while os.path.exists(name):
			num+=1
			name=f'julia set{num}'
		pygame.image.save(SCREEN, name)
	
	
						
while True:

	pygame.display.update()
	CLOCK.tick(FPS)
	pygame.quit()
	exit()

