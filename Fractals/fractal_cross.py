import pygame

pygame.init()
SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()

CLOCK=pygame.time.Clock()
FPS=1
SCREEN.fill((220, 220, 220))
crosses=[]
dirs=[(1,0),(-1,0), (0,-1), (0,1)]

def drawCross(points, size, width, block_dir):
	x, y=points
	half=size//2
	new_points=[]
	for i ,(dx, dy) in enumerate(dirs):
		if i==block_dir:
			continue
		px=x+dx*half
		py=y+dy*half
		pygame.draw.line(SCREEN, (0, 0, 0), (x, y), (px,py),width)
		new_points.append(((px, py), (i^1)))
	
	
	return new_points
def main():
	global crosses
	s=0.4
	size=WIDTH*s
	w=0.03
	width=int(WIDTH*w)
	
	points = [((WIDTH//2, HEIGHT//2), -1)]
	while True:
		new=[]
		for pos, last_dir in points:
			new.extend(drawCross(pos , size, width, last_dir))
		
		points=new
		
		s=min(1, s*0.5)
		size=WIDTH*s
		w=min(1, w*0.65)
		width=int(WIDTH*w)
		pygame.display.update()
		CLOCK.tick(FPS)
		
main()