import pygame
from math import cos, sin
from matrixes import Matrix
import random
pygame.init()

SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
centerx, centery=WIDTH/2, HEIGHT/2
scaler=min(WIDTH, HEIGHT)
timer=pygame.time.Clock()
fps=60
vec=pygame.math.Vector3

def shape(scale, shape):
	points=[]
	if shape!=1:
		points=[
		vec(-1, -1, -1),
		vec(-1, 1, -1),
		vec(1, -1, -1),
		vec(1, 1, -1),
		vec(-1, -1, 1),
		vec(-1, 1, 1),
		vec(1, -1, 1),
		vec(1 ,1, 1)]
	elif shape==1:
		points= [
	vec(1, 1, 1),
	vec(-1, -1, 1),
	vec(-1, 1, -1),
	vec(1, -1, -1)
]
	
	
	for p in points:
		p*=scale
	return points
	
#applies rotation matrix to vector baded on a given angle	
def rotations(angle):
	rotationZ=Matrix([
	[cos(angle), -sin(angle), 0],
	[sin(angle), cos(angle), 0], 
	[0, 0, 1]])
	
	rotationX=Matrix([
	[1, 0, 0],
	[0, cos(angle), -sin(angle)],
	[0, sin(angle), cos(angle)]])
	
	rotationY=Matrix([
	[cos(angle), 0, -sin(angle)],
	[0, 1, 0],
	[sin(angle), 0, cos(angle)]])
	
	return rotationX, rotationY, rotationZ
#draws lines between points in spac
def conect(a, b):
	pygame.draw.line(SCREEN, 'white', (a.x, a.y), (b.x, b.y), 4)

#returns a list of edges as tuples
def generate_edges(points):
	edges=[]
	dist=points[0].distance_to(points[1])
	for i in range(len(points)):
		for j in range(i+1, len(points)):
			if abs(points[i].distance_to(points[j])-dist)<1:
				edges.append((i, j))
	return edges

#main loop	
def main():
	points=shape(150, 10) #first parameter controls the size
	edges=generate_edges(points)
	originx, originy=centerx, centery
	view=Matrix([[1, 0, 0], [0, 1, 0]])
	
	angle=0
	run=True
	while run:
		projected_points=[]
		SCREEN.fill((20, 20, 20))
		
		rotationX, rotationY, rotationZ=rotations(angle)
		
		for p in points:
			point=Matrix([[p.x], [p.y], [p.z]])
			r2d=point
			r2d=rotationY*r2d
			r2d=rotationZ*r2d
			r2d=rotationX*r2d
			
			p2d=view*r2d
			
			x=p2d.matrix[0][0]+originx
			y=p2d.matrix[1][0]+originy
			pygame.draw.circle(SCREEN, 'white',(x, y), 10)
			projected_points.append(vec(x, y, 0))
		
		for a, b in edges:
			conect(projected_points[a], projected_points[b])
		
		angle+=0.02
		pygame.display.update()
		timer.tick(fps)

while True:
	main()