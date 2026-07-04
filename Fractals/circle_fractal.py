import pygame
pygame.init()

SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
SCREEN=pygame.display.set_mode((HEIGHT, WIDTH))
SCREEN.fill((220, 220, 220))

x, y=(WIDTH/2, HEIGHT/2)
radius=HEIGHT*0.29
pygame.draw.circle(SCREEN, '#000000', (x, y),radius,5)
diff=0.7
def draw_more(x, y, rad):
	pygame.draw.circle(SCREEN, '#000000', (x, y),rad*diff,5)
	if rad <70:
		return
	draw_more(x+rad*diff, y, rad*diff)
	draw_more(x-rad*diff, y, rad*diff)
	draw_more(x, y+rad*diff, rad*diff)
	draw_more(x, y-rad*diff, rad*diff)
	
	
draw_more(x, y, radius)


while True:
	pygame.display.update()