import pygame
import math
import random

class Button():
	def __init__(self, rect, text, font_size, font_color='white', font_name=None, press_color=(50, 150, 150), color=(100, 100, 100), border=4, border_radius=4, border_color=(0, 0, 0)):
		self.rect=pygame.Rect(rect)
		
		self.gui_font=pygame.font.Font(font_name, font_size)
		self.text=text
		self.font_color=font_color
		
		self.border=border
		self.border_radius=border_radius
		self.border_color=border_color
		
		self.color=color
		self.press_color=press_color
		self.now_color=self.color
		
		self.wright_text=self.gui_font.render(str(self.text), True, self.font_color, self.now_color)
		self.text_rect=self.wright_text.get_rect(center=self.rect.center)
		
		self.press=False
	def draw(self, surf):
		pygame.draw.rect(surf, self.now_color, self.rect, border_radius=self.border_radius)
		if self.border:
			pygame.draw.rect(surf, self.border_color,  self.rect, self.border, border_radius=self.border_radius)
			
		self.wright_text=self.gui_font.render(str(self.text), True, self.font_color, self.now_color)
		self.text_rect=self.wright_text.get_rect(center=self.rect.center)
		surf.blit(self.wright_text, self.text_rect)
	
	def touch(self, events):
		for event in events:
			if event.type==pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos()):
				self.press=True
				self.now_color=self.press_color
				return True
			if event.type==pygame.MOUSEBUTTONUP:
				self.press=False
				self.now_color=self.color
				
class Image_Button():
	def __init__(self, rect, img, pressed_img, alpha=None):
		self.rect=pygame.Rect(rect)
		
		if not alpha:
			self.img=pygame.image.load(img).convert()
			self.press_img=pygame.image.load(pressed_img).convert()
		else:
			self.img=pygame.image.load(img).convert_alpha()
			self.press_img=pygame.image.load(pressed_img).convert_alpha()
			
		self.img=pygame.transform.scale(self.img, (self.rect.width, self.rect.height))
		self.press_img=pygame.transform.scale(self.press_img, (self.rect.width, self.rect.height))
		self.now_img=self.img
	
		self.press=False
	def draw(self, surf):
		surf.blit(self.now_img, (self.rect.x, self.rect.y))
		
	
	def touch(self, events):
		for event in events:
			if event.type==pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos()):
				self.press=True
				self.now_img=self.press_img
				return True
			if event.type==pygame.MOUSEBUTTONUP:
				self.press=False
				self.now_img=self.img


class Switch_Button():
	def __init__(self, rect, text, font_size, font_color='white', font_name=None, press_color=(50, 150, 150), color=(100, 100, 100), change_color=True, border=4, border_radius=4, border_color=(0, 0, 0)):
		self.rect=pygame.Rect(rect)
		
		self.gui_font=pygame.font.Font(font_name, font_size)
		self.font_color=font_color
		self.text=text
		self.text_font=self.gui_font.render(str(self.text), True, self.font_color)
		self.text_rect=self.text_font.get_rect(center=self.rect.center)
		
		self.border=border
		self.border_radius=border_radius
		self.border_color=border_color
		
		self.color=color
		self.change_color=change_color
		self.press_color=press_color
		self.now_color=self.color
		
		self.press='off'
	def draw(self, surf):
		if not self.change_color:
			self.now_color=self.color
			
		pygame.draw.rect(surf, self.now_color, self.rect, border_radius=self.border_radius)
		if self.border:
			pygame.draw.rect(surf, self.border_color,  self.rect, self.border, border_radius=self.border_radius)
			
		surf.blit(self.text_font, self.text_rect)
	
	def touch(self, events):
		for event in events:
			if event.type==pygame.MOUSEBUTTONDOWN and self.press=='on':
				self.press='off'
				self.now_color=self.color
				return self.press
			if event.type==pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos()):
				self.press='off' if self.press!='off' else 'on'
				self.now_color=self.color if self.now_color!=self.color else self.press_color
				return self.press
			
				
				
class Image_Switch_Button():
	def __init__(self, rect, img, pressed_img, alpha=None):
		self.rect=pygame.Rect(rect)
		
		if not alpha:
			self.img=pygame.image.load(img).convert()
			self.press_img=pygame.image.load(pressed_img).convert()
		else:
			self.img=pygame.image.load(img).convert_alpha()
			self.press_img=pygame.image.load(pressed_img).convert_alpha()
			
		self.img=pygame.transform.scale(self.img, (self.rect.width, self.rect.height))
		self.press_img=pygame.transform.scale(self.press_img, (self.rect.width, self.rect.height))
		self.now_img=self.img
	
		self.press='off'
	def draw(self, surf):
		surf.blit(self.now_img, (self.rect.x, self.rect.y))
		
	
	def touch(self):
		for event in pygame.event.get():
			if event.type==pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos()):
				self.press='off' if self.press!='off' else 'on'
				self.now_img=self.img if self.now_img!=self.img else self.press_img
				return self.press				
				
				
class Analog():
	def __init__(self, x, y, radius):
		self.mainx=x
		self.mainy=y
		self.rad=radius
		self.x, self.y, self.small_rad=(self.mainx, self.mainy, self.rad//3)
		self.is_pressed=False
	def draw(self, screen):
		c1=80
		c2=180
		pygame.draw.circle(screen, (c1, c1, c1), (self.mainx, self.mainy), self.rad)
		pygame.draw.circle(screen, (c2, c2, c2), (self.x, self.y), self.small_rad)
	def move(self):
		press=pygame.mouse.get_pressed()[0]
		mx, my=pygame.mouse.get_pos()
		if not press:
			self.is_pressed=False
			self.x=self.mainx
			self.y=self.mainy
			return
		if press and not self.is_pressed and (mx<self.rad*2 + self.mainx and my >self.mainy-self.rad*2):
			self.is_pressed=True
		if self.is_pressed:
			dx=mx-self.mainx
			dy=my-self.mainy
			dist=math.sqrt(dx**2 + dy**2)
			theta=math.atan2(dy, dx)
			
			limitx=self.rad*math.cos(theta)
			limity=self.rad*math.sin(theta)
			distx=dist*math.cos(theta)
			disty=dist*math.sin(theta)
			if dist < self.rad:
				limitx, limity=distx, disty
			self.x=self.mainx+limitx
			self.y=self.mainy+limity
			return theta
			
class Slider():
	def __init__(self, point1, point2, min_val, max_val,step_size,  stable, line_width=10):
		self.point1=point1
		self.point2=point2
		self.stable=stable
		
		if stable=='y':
			self.x=self.point1[0]
			self.y=self.point1[1]
		else:
			self.x=self.point1[0]
			self.y=self.point1[1]
		
		self.line_width=line_width
		self.rad1=int(self.line_width*1.15)
		self.rad2=int(self.rad1*2)
		self.rad3=int(self.rad2*1.25)
		
		self.min=min_val
		self.max=max_val
		self.step_size=step_size
		self.unit=(self.max-self.min)/self.step_size
		self.line_length=max(self.point2[0]-self.point1[0], self.point2[1]-self.point1[1])
		self.segmant=self.line_length/self.unit
		
		
		self.hold=False
		self.value=self.min
	def draw(self, surf, color=(50, 150, 200), color2=(69, 69, 69)):
		pygame.draw.line(surf, 'white', self.point1, self.point2, self.line_width)
		
		pygame.draw.circle(surf, color, (self.x, self.y), self.rad3)
		pygame.draw.circle(surf, color2, (self.x, self.y), self.rad2)
		pygame.draw.circle(surf, color, (self.x, self.y), self.rad1)
	
	def touch(self):
		rect=pygame.Rect(self.x-self.rad3, self.y-self.rad3, self.rad3*4, self.rad3*4)
		mx, my=pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type==pygame.MOUSEBUTTONDOWN and rect.collidepoint(mx, my):
				self.hold=True
			if event.type==pygame.MOUSEBUTTONUP:
				self.hold=False
		if pygame.mouse.get_pressed()[0] and self.hold:
			if self.stable=='y':
				if self.point1[0] < mx <self.point2[0]:
					self.x=mx
					length=mx-self.point1[0]
					self.value=math.floor(length/self.segmant)+self.min
					
				
			else:
				if self.point1[1] < my <self.point2[1]:
					self.y=my
					length=my-self.point1[1]
					self.value=int(length/self.segmant)+self.min
		return self.value

class Normal_Switch_Button():
	def __init__(self, rect, text, font_size, font_color='white', font_name=None, press_color=(50, 150, 150), color=(100, 100, 100), change_color=True, border=4, border_radius=4, border_color=(0, 0, 0)):
		self.rect=pygame.Rect(rect)
		
		self.gui_font=pygame.font.Font(font_name, font_size)
		self.font_color=font_color
		self.text=text
		self.text_font=self.gui_font.render(str(self.text), True, self.font_color)
		self.text_rect=self.text_font.get_rect(center=self.rect.center)
		
		self.border=border
		self.border_radius=border_radius
		self.border_color=border_color
		
		self.color=color
		self.change_color=change_color
		self.press_color=press_color
		self.now_color=self.color
		
		self.press='off'
	def draw(self, surf):
		if not self.change_color:
			self.now_color=self.color
			
		pygame.draw.rect(surf, self.now_color, self.rect, border_radius=self.border_radius)
		if self.border:
			pygame.draw.rect(surf, self.border_color,  self.rect, self.border, border_radius=self.border_radius)
			
		surf.blit(self.text_font, self.text_rect)
	
	def touch(self, events):
		for event in events:
			if event.type==pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos()):
				self.press='off' if self.press!='off' else 'on'
				self.now_color=self.color if self.now_color!=self.color else self.press_color
				return self.press