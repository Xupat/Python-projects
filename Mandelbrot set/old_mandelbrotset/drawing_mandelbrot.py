import pygame
import math
import os
import time
import multiprocessing
import numpy as np
from colorsys import hsv_to_rgb
pygame.init()

pygame.init()
SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH , HEIGHT=SCREEN.get_size()
SCREEN=pygame.display.set_mode((HEIGHT, WIDTH))
CLOCK=pygame.time.Clock()
WHITE=(220, 220, 220)
BLACK=(30, 30, 30)


step=0.2
max_val=step*11
centerx=WIDTH-WIDTH*0.5
centery=HEIGHT-HEIGHT/2
zoom=(WIDTH/2) / math.ceil(max_val/step)

cores=os.cpu_count()
smooth=6
max_itr=256

def stabilty_test(px, py, max_itr):
	C=px+1j*py
	Z=np.zeros_like(C, dtype=np.complex128)
	output=np.zeros(C.shape, dtype=np.float32)
	mask=np.ones(C.shape, dtype=bool)
	
	for i in range(max_itr):
		Z[mask]=Z[mask]**2+C[mask]
		#Z[mask]=complex(abs(Z.real[mask]), abs(Z.imag[mask]))**2+C[mask]
		escaped=np.abs(Z)>2
		output[escaped & mask]=i-np.log(np.log(np.abs(Z[escaped & mask])))/np.log(2)
		mask &= ~escaped
		if not mask.any():
			break
		
	output[mask]=500
	return output
		
		
	
def make_section(cpu_id, q):
	rows=math.ceil(WIDTH/cores)
	start_x=cpu_id*rows
	end_x=min(start_x+rows, WIDTH)
	w=end_x-start_x
	
	x=np.arange(start_x, end_x)-centerx
	y=np.arange(HEIGHT)-centery
	px, py=np.meshgrid(x/ zoom *step, y/zoom *step, indexing='ij')
	
	pixels=stabilty_test(px, py, max_itr)
	q.put((cpu_id, pixels))
			
def render_shape_hsv(pixels):
	rgb=np.zeros((pixels.shape[0], pixels.shape[1], 3), dtype=np.uint8)
	
	mask=(pixels==500)
	rgb[mask]=BLACK
	
	not_mask= ~mask
	vals=pixels[not_mask]/max_itr
	
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
	
	mask=(pixels==500)
	rgb[mask]=BLACK
	
	not_mask= ~mask
	vals=pixels[not_mask]
	
	#sampels=12
#	accum=np.zeros_like(vals)
#	for i in range(sampels):
#		accum+=vals*i
#	accum/=sampels

#	
#	r=(accum*150).astype(np.uint8)
#	g=(accum*200).astype(np.uint8)
#	b=(accum*255).astype(np.uint8)
#
	
	c=(vals*smooth).astype(np.uint32)
	
	r=c%256
	g=(c*2)%256
	b=(c*5)%256
	
	rgb[not_mask]=np.stack((r, g, b), axis=1)
	pygame.surfarray.blit_array(SCREEN, rgb)
	pygame.display.update()

def draw_a_row(pixels, method):
	count=0
	for x, row in enumerate(pixels):
		for y, hue in enumerate(row):
			if hue==500:
				colors=BLACK
			else:
				if method=='hsv':
					hue=hue/max_itr
					#hue=(0.95 + 10*hue)%1
					r, g, b=hsv_to_rgb(hue, 1, 1)
					colors=(int(r*255), int(g*255), int(b*255))
				if method=='histo':
					c=hue*12
					r=c%256
					g=(c*2)%256
					b=(c*5)%256
					colors=(r, g, b)
				
			SCREEN.set_at((x, y),colors)
			#pygame.draw.rect(SCREEN, colors, (x, y, 1, 1))
			count+=1
			if count==700:
				pygame.display.update()
				count=0
 
				
def merge_lists(lists):
	lists.sort(key=lambda x:x[0])
	return np.vstack([item[1] for item in lists])


def start_drawing():
	t0=time.time()
	q=multiprocessing.Queue()
	procs=[]
	for cpu in range(cores):
		p=multiprocessing.Process(target=make_section, args=(cpu, q))
		procs.append(p)
		p.start()
	
	results=[q.get() for _ in range(cores)]
	for p in procs:
		p.join()
		
	pixels=merge_lists(results)
	
	t1=time.time()-t0
	print(t1)
	instante=False
	if instante:
		render_shape_histogram(pixels)
	else:
		draw_a_row(pixels, 'histo')
	print(time.time()-t0)

start_drawing()

running=True
while running:
	pygame.display.update()
	
	