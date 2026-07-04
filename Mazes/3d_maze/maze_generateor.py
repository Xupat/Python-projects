import numpy as np
from random import choice

def maze_genrtator(cells):
	cells=cells*2+1
	sx=1
	sy=1
	grid=np.ones((cells, cells))
	grid[:, ::2]=2
	grid[::2, :]=2
	grid[sx, sy]=99
	
	stack=[]
	loop=0
	while 1 in grid:
		loop+=1
		top=grid[sx, sy+2] if sy+2 in range(cells) else None
		right=grid[sx+2, sy] if sx+2 in range(cells) else None
		bottom=grid[sx, sy-2] if sy-2 in range(cells) else None
		left=grid[sx-2, sy] if sx-2 in range(cells) else None
		nighbors=[]
		if top and top!=99:
			nighbors.append((top, (sx, sy+2), 'top'))
		if right and right!=99:
			nighbors.append((right, (sx+2, sy), 'right'))
		if bottom and bottom!=99:
			nighbors.append((bottom,(sx, sy-2),'bottom'))
		if left and left!=99:
			nighbors.append((left, (sx-2, sy), 'left'))
		try:
			nighbor=choice(nighbors)
			stack.append(nighbor)
		except:
			if stack:
				nighbor=stack.pop()
			else:
				break
		next, pos, dire=nighbor
		grid[pos[0], pos[1]]=99
		sx, sy=pos
		if dire=='top':
			grid[sx, sy-1]=99
		if dire=='bottom':
			grid[sx, sy+1]=99
		if dire=='right':
			grid[sx-1, sy]=99
		if dire=='left':
			grid[sx+1, sy]=99
	
		
	rows, cols=grid.shape
	for i in range(rows):
		for j in range(cols):
			if grid[i, j]==2:
				grid[i, j]=1
			else:
				grid[i, j]=0	
	return grid


#h=maze_genrtator(7)

#print(h)