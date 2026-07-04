import pygame
import math

def Grid(window, x_spaces, font_size, is_ball):
	screen, width, height=window
	centerx, centery=(width//2, height//2)
	black=(0, 0, 0)
	
	marks_length=width*0.007
	real, max, zoom=x_spaces
	
	if not zoom:
		zoom=(width/2) / math.ceil(max/real)
	limit=math.ceil(math.ceil(max/real)*1.5)
	
	gui_font=pygame.font.Font('fonts/segoe-ui-symbol.ttf', font_size)
	line_width=1
	tick_width=2
	pygame.draw.line(screen, black, (0, centery), (width, centery), line_width)
	pygame.draw.line(screen, black, (centerx, 0), (centerx, height), line_width)
	
	for tick in range(limit):
		num=tick*real
		if num==0:
			continue
		x1=centerx+tick*zoom
		y1=centery-marks_length
		x2=x1
		y2=centery+marks_length
		pygame.draw.line(screen, black, (x1, y1), (x2, y2), tick_width)
		text=gui_font.render(str(round(tick*real, 2)), True, black)
		text_rect=text.get_rect(center=(x1, y2+marks_length))
		screen.blit(text, text_rect)
		
	for tick in range(limit):
		num=tick*real
		if num==0:
			continue
		x1=centerx-tick*zoom
		y1=centery-marks_length
		x2=x1
		y2=centery+marks_length
		pygame.draw.line(screen, black, (x1, y1), (x2, y2), tick_width)
		text=gui_font.render(str(round(-tick*real, 2)), True, black)
		text_rect=text.get_rect(center=(x1, y2+marks_length))
		screen.blit(text, text_rect)
			
	
	for tick in range(limit):
		num=tick*real
		if num==0:
			continue
		x1=centerx-marks_length
		y1=centery+tick*zoom
		x2=centerx+marks_length
		y2=y1
		pygame.draw.line(screen, black, (x1, y1), (x2, y2), tick_width)
		text=gui_font.render(str(round(-tick*real, 2)), True, black)
		text_rect=text.get_rect(center=(x2+marks_length*2, y2))
		screen.blit(text, text_rect)
	
	for tick in range(limit):
		num=tick*real
		if num==0:
			continue
		x1=centerx-marks_length
		y1=centery-tick*zoom
		x2=centerx+marks_length
		y2=y1
		pygame.draw.line(screen, black, (x1, y1), (x2, y2), tick_width)
		text=gui_font.render(str(round(tick*real, 2)), True, black)
		text_rect=text.get_rect(center=(x2+marks_length*2, y2))
		screen.blit(text, text_rect)
	if is_ball:
		pygame.draw.circle(screen, (200, 50, 50), (centerx, centery), 5)