import pygame
from gui_tools import Button
import random
pygame.init()

SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
scaler=min(WIDTH, HEIGHT)
timer=pygame.time.Clock()
FPS=60
p1, p2='x', 'o'
gui=pygame.font.Font(None, int(scaler*0.1))

BG=(230, 230, 230)
LINE=(50, 50, 50)
SYMPOLS=(0, 0, 0)
BTN=(29, 92, 221)

cells=3
lw=4
sw=lw*2
pad=int(scaler*0.02)
size=(WIDTH-pad*2)/cells
sx=pad
sy=(HEIGHT-size*cells)//2

def draw_grid():
	for i in range(1, cells):
		x=sx+i*size
		y=sy+size*cells
		pygame.draw.line(SCREEN, LINE, (x, sy), (x, y), lw)
	for i in range(1, cells):
		x=sx+size*cells
		y=sy+size*i
		pygame.draw.line(SCREEN, LINE, (sx, y), (x, y), lw)
	pygame.draw.rect(SCREEN, LINE, (sx, sy, size*cells, size*cells), lw)

def draw_sympols(bored):
	s=int(size*(1/cells))
	for i in range(len(bored)):
		for j in range(len(bored[i])):
			x=sx+i*size+size/2
			y=sy+j*size+size/2
			if bored[i][j]==p2:
				pygame.draw.circle(SCREEN, SYMPOLS, (x, y), s, sw)
			elif bored[i][j]==p1:
				pygame.draw.line(SCREEN, SYMPOLS, (x, y), (x+s, y+s), sw)
				pygame.draw.line(SCREEN, SYMPOLS, (x, y), (x+s, y-s), sw)
				pygame.draw.line(SCREEN, SYMPOLS, (x, y), (x-s, y+s), sw)
				pygame.draw.line(SCREEN, SYMPOLS, (x, y), (x-s, y-s), sw)

def get_rects():
	rects=[]
	for i in range(cells):
		for j in range(cells):
			x=sx+i*size
			y=sy+j*size
			rects.append(pygame.Rect(x, y, size, size))
	return rects

def check_winner(bored):
	for i in range(cells):
		if bored[i][0] and all(bored[i][j]==bored[i][0] for j in range(cells)):
			return bored[i][0]
	
	for j in range(cells):
		if bored[0][j] and all(bored[i][j]==bored[0][j] for i in range(cells)):
			return bored[0][j]
	
	if bored[0][0] and all(bored[i][i]==bored[0][0] for i in range(cells)):
		return bored[0][0]
	
	if bored[0][cells-1] and all(bored[i][cells-1-i]==bored[0][cells-1] for i in range(cells)):
		return bored[0][cells-1]
	
	if all(bored[i][j] for i in range(cells) for j in range(cells)):
		return 'draw'

def show_winner(result, player):
	if not result:
		return 
	w=(30, 200, 10)
	l=(250, 20, 20)
	d=(100, 100, 100)
	if result==player:
		c=w
		t='You won'
	elif result!=player and result!='draw':
		c=l
		t='You lost'
	else:
		c=d
		t='Draw'
	w=size*3-sx*2
	h=int(size*0.8)
	rect=pygame.Rect(sx*3, sy+size+(size-h)//2, w, h)
	rect=pygame.Rect(sx*2, sy-size, w, h)
	pygame.draw.rect(SCREEN, c, rect, border_radius=15)
	text=gui.render(t, True, 'White')
	text_rect=text.get_rect(center=rect.center)
	SCREEN.blit(text, text_rect)

def main():
	bored=[['']*cells for i in range(cells)]
	rects=get_rects()
	btn_size=int(scaler*0.35)
	btn=Button((0, 0, btn_size, btn_size//3), 'Restart', int(scaler*0.06), border=0, border_radius=15, color=BTN)
	player=random.choice([p1, p2])
	turn=p1
	result=None
	run=True
	while run:
		SCREEN.fill(BG)
		events=pygame.event.get()
		for e in events:
			if e.type==pygame.MOUSEBUTTONDOWN and not result and player==turn:
				mx, my=pygame.mouse.get_pos()
				for idx, r in enumerate(rects):
					if r.collidepoint(mx, my):
						i=idx//cells
						j=idx%cells
						if bored[i][j] not in [p1, p2]:
							bored[i][j]=turn
							if turn==p1:turn=p2
							else:turn=p1
			elif e.type==pygame.MOUSEBUTTONDOWN and result:
				bored=[['']*cells for i in range(cells)]
		
		if turn!=player:
			avs=[(i, j) for i in range(cells) for j in range(cells) if not bored[i][j]]
			if avs:
				i, j=random.choice(avs)
				bored[i][j]=turn
				if turn==p1:turn=p2
				else:turn=p1
		draw_grid()
		draw_sympols(bored)
		
		result=check_winner(bored)
		show_winner(result, player)
		btn.draw(SCREEN)
		if btn.touch(events):
			bored=[['']*cells for i in range(cells)]
		
		pygame.display.update()
		timer.tick(FPS)

main()