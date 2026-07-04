import pygame
from gui_tools import Button
import random
import math
import sys
sys.setrecursionlimit(10000)
pygame.init()

#=========SET UP========
SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
scaler=min(WIDTH, HEIGHT)
timer=pygame.time.Clock()
FPS=60
p1, p2='x', 'o'
gui=pygame.font.Font(None, int(scaler*0.1))
#=====Colors=====
BG=(230, 230, 230)
LINE=(50, 50, 50)
SYMPOLS=(0, 0, 0)
BTN=(29, 92, 221)
#=======Grid=====
cells= 3
max_depth = 9 if cells==3 else 3
lw=4
sw=lw*2
pad=int(scaler*0.02)
size=(WIDTH-pad*2)/cells
sx=pad
sy=(HEIGHT-size*cells)//2
#======== DRAWING THE GRID ==========
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
#======= DRAWING THE GAME =========
def draw_sympols(bored):
	s=int(size*(1/cells))
	for i in range(len(bored)):
		for j in range(len(bored[i])):
			x=sx+i*size+size/2
			y=sy+j*size+size/2
			if bored[i][j]==p2:
				pygame.draw.circle(SCREEN, SYMPOLS, (x, y), s, sw)
			elif bored[i][j]==p1:
				pygame.draw.line(SCREEN, SYMPOLS, (x-s, y-s), (x+s, y+s), sw)
				pygame.draw.line(SCREEN, SYMPOLS, (x-s, y+s), (x+s, y-s), sw)

#======== UTILS ========
def get_rects():
	rects=[]
	for i in range(cells):
		for j in range(cells):
			x=sx+i*size
			y=sy+j*size
			rects.append(pygame.Rect(x, y, size, size))
	return rects
def other(p):
	if p==p1:return p2
	elif p==p2:return p1

#======= CHECKS THE WINNER =======
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
#======== Shows who won ========
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
	w=size*cells-sx*2
	h=int(size*0.8)
	rect=pygame.Rect(sx*2, sy-size, w, h)
	pygame.draw.rect(SCREEN, c, rect, border_radius=15)
	text=gui.render(t, True, 'White')
	text_rect=text.get_rect(center=rect.center)
	SCREEN.blit(text, text_rect)

def evaluate(bored):
	score=0
	lines=[]
	
	for i in range(cells):
		lines.append(bored[i])
		lines.append([bored[j][i] for j in range(cells)])
	lines.append([bored[i][i] for i in range(cells)])
	lines.append([bored[i][cells-1-i] for i in range(cells)])
	
	for line in lines:
		if ai in line and player not in line:
			score+=1
		if ai not in line and player in line:
			score-=1
	return score

def minimax(bored, alpha, beta, isMax, depth, max_depth=max_depth):
	result=check_winner(bored)
	if result:
		return scores[result]
	if depth>=max_depth:
		return evaluate(bored)
	
	if isMax:
		best_score=-math.inf
		for i in range(cells):
			for j in range(cells):
				if not bored[i][j]:
					bored[i][j]=ai
					score=minimax(bored, alpha, beta, False, depth+1)
					best_score=max(best_score,score)
					alpha=max(alpha, score)
					bored[i][j]=''
					if beta <=alpha:
						return best_score
		return best_score
	else:
		best_score=math.inf
		for i in range(cells):
			for j in range(cells):
				if not bored[i][j]:
					bored[i][j] = player
					score=minimax(bored, alpha, beta, True, depth+1)
					best_score=min(best_score,score)
					beta=min(beta, score)
					bored[i][j]=''
					if beta <=alpha:
						return best_score
		return best_score

def next_move(bored):
	best_score=-math.inf
	best_move=None
	for i in range(cells):
		for j in range(cells):
			if not bored[i][j]:
				bored[i][j]=ai
				score=minimax(bored, -math.inf, math.inf, False, 0)
				bored[i][j]=''
				if score>best_score:
					best_score=score
					best_move=(i, j)
	return  best_move

def reset(normal=True):
	global bored, player, ai, scores, turn, result
	bored = [[''] * cells for _ in range(cells)]
	player = p1 if normal else p2
	ai = p2 if normal else p1
	scores = {ai: 1, player: -1, 'draw': 0}
	turn = p1
	result = None
	
def main():
	global bored, player, ai, scores, turn, result
	rects=get_rects()
	btn_size=int(scaler*0.35)
	btn=Button((0, 0, btn_size, btn_size//3), 'Restart', int(scaler*0.06), border=0, border_radius=15, color=BTN)
	
	reset()
	run=True
	while run:
		pressed=False
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
							pressed=True
							turn=other(turn)
			elif e.type==pygame.MOUSEBUTTONDOWN and result:
				reset()
				
		if ai==turn and not pressed and not result:
			i, j=next_move(bored)
			bored[i][j]=turn
			turn=other(turn)
			
		draw_grid()
		draw_sympols(bored)
		
		result=check_winner(bored)
		show_winner(result, player)
	
	
		btn.draw(SCREEN)
		if btn.touch(events):
			reset()
		pygame.display.update()
		timer.tick(FPS)

main()