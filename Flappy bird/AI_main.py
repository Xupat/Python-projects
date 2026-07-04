import pygame
import os
import time
import random
import neat
pygame.init()

#=========settings========
SCREEN=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT=SCREEN.get_size()
scaler=min(WIDTH, HEIGHT)
TIMER=pygame.time.Clock()
FPS=60
colorkey=(0, 255, 255)
gui=pygame.font.SysFont(None, 50)
pause_gui=pygame.font.Font(None, 70)
score_gui=pygame.font.SysFont('comicsans' ,int(scaler*0.1))

#====preparing imgs and scaling them====
bird_scale=2.5
BIRD_IMGS=[
pygame.transform.scale_by(pygame.image.load('imgs/bird1.png').convert(), bird_scale), 
pygame.transform.scale_by(pygame.image.load('imgs/bird2.png').convert(), bird_scale),
pygame.transform.scale_by(pygame.image.load('imgs/bird3.png').convert(), bird_scale)]
BIRD_IMGS.append(BIRD_IMGS[1])

BG_IMG=pygame.transform.scale(pygame.image.load('imgs/bg.png').convert(), (WIDTH, HEIGHT))
GROUND_IMG=pygame.image.load('imgs/base.png').convert()
GROUND_IMG=pygame.transform.scale(GROUND_IMG, (WIDTH+1, GROUND_IMG.get_height()*2))
pipe_scale=2.5
PIPE_IMG=pygame.transform.scale_by(pygame.image.load('imgs/big_pipe.png').convert(), pipe_scale)

GROUND_IMG.set_colorkey(colorkey)
PIPE_IMG.set_colorkey(colorkey)
BG_IMG.set_colorkey(colorkey)
for b in BIRD_IMGS:b.set_colorkey(colorkey)

#==========BIRD CLASS=========
class Bird:
	IMGS=BIRD_IMGS
	MAX_ROT=25
	MIN_ROT=-90
	ROT_LERP=.15
	ANIM_TIME=7
	GRAVITY=.8
	JUMP_POWER=14
	def __init__(self, x, y):
		self.x=x
		self.y=y
		self.vel=0
		self.tilt=0
		self.height=self.y
		self.img_count=0
		self.img=self.IMGS[0]
		self.rotated=self.img
	def jump(self):
		self.vel=-self.JUMP_POWER
		self.height=self.y
	def move(self):
		self.vel+=self.GRAVITY
		self.y+=self.vel
		target_tile=max(self.MIN_ROT, min(self.MAX_ROT, -self.vel*3))
		self.tilt+=(target_tile-self.tilt)*self.ROT_LERP
	def draw(self, win):
		self.img_count+=1
		img_idx=(self.img_count//self.ANIM_TIME)%len(self.IMGS)
		self.img=self.IMGS[img_idx]
		self.rotated=pygame.transform.rotate(self.img, self.tilt)
		new_rect=self.rotated.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
		win.blit(self.rotated, new_rect)
	def collide(self, pipes):
		bird_rect=self.rotated.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
		bird_rect=bird_rect.scale_by(0.8)
		for p in pipes:
			top_rect=p.pipe_top.get_rect(topleft=(p.x, p.top))
			bottom_rect=p.pipe_bottom.get_rect(topleft=(p.x, p.bottom))
			if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
				return True

#==========PIPE CLASS==========
class Pipe:
	VEL=6
	def __init__(self, win_size, ground, gap):
		self.x=win_size[0]
		self.height=0
		self.gap=gap
		
		self.top=0
		self.bottom=0
		self.pipe_bottom=PIPE_IMG
		self.pipe_top=pygame.transform.flip(PIPE_IMG, False, True)
		
		self.passed=False
		self.set_heights(win_size[1], ground)
	def set_heights(self, height, ground):
		theight=height-ground
		min_height=int(theight*0.075)+self.gap+ground
		self.height=random.randint(min_height, theight-min_height)
		self.top=self.height-self.pipe_top.get_height()-self.gap
		self.bottom=self.height
	def move(self):
		self.x-=self.VEL
	def draw(self, win):
		win.blit(self.pipe_top, (self.x, self.top))
		win.blit(self.pipe_bottom, (self.x, self.bottom))

#==========GROUND CLASS=========
class Base:
	VEL=Pipe.VEL
	IMG=GROUND_IMG
	BASE_W=WIDTH
	def __init__(self, y):
		self.y=y
		self.x1=0
		self.x2=WIDTH
	def move(self):
		self.x1-=self.VEL
		self.x2-=self.VEL
		if self.x1+self.BASE_W<0:self.x1=self.x2+self.IMG.get_width()
		if self.x2+self.BASE_W<0:self.x2=self.x1+self.IMG.get_width()
	def draw(self, win):
		win.blit(self.IMG, (self.x1, self.y))
		win.blit(self.IMG, (self.x2, self.y))

def Uppdate_window(win, birds, pipes, base, score):
	win.blit(BG_IMG, (0, 0))
	for p in pipes:
		p.draw(SCREEN)
	for bird in birds:
		bird.draw(win)
	base.draw(win)
	text=gui.render(f'Score:  {score}', True, 'white')
	win.blit(text, (WIDTH-10-text.get_width(), 0))
	pygame.display.update()

def make_pipe(bird):
	gap=int(bird.rotated.get_height()*4)
	return Pipe(SCREEN.get_size(), 0, gap)

auto_run=False
def main(genomes, config):
	global auto_run
	birds=[]
	nets=[]
	ge=[]
	for _, g in genomes:
		net=neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		birds.append(Bird(int(scaler*0.17), int(scaler*0.5)))
		g.fitness=0
		ge.append(g)
	
	base=Base(HEIGHT-GROUND_IMG.get_height())
	pipes=[make_pipe(birds[0])]
	
	score=0
	run=True
	while run:
		for e in pygame.event.get():
			if e.type==pygame.MOUSEBUTTONDOWN:
				auto_run=not auto_run
				t='Paused'
				text=pause_gui.render(t, True, 'red')
				text_rect=text.get_rect(center=(WIDTH//2, HEIGHT//2))
				SCREEN.blit(text, text_rect)
				pygame.display.update()
				
		add_pipe=False
		base.move()
		to_remove=set()
		if len(birds)==0:
			break
		
		for p in pipes:
			if p.x+p.pipe_top.get_width()<0:
				to_remove.add(p)
			if not p.passed and p.x<birds[0].x:
				p.passed=True
				add_pipe=True
			p.move()
		for r in to_remove:
			pipes.remove(r)
			
		if add_pipe:
			pipes.append(make_pipe(birds[0]))
			score+=1
			for g in ge:
				g.fitness+=5
		
		pipe_idx=0
		if len(birds)>0:
			if len(pipes)>1 and birds[0].x>pipes[0].x+pipes[0].pipe_top.get_width():
				pipe_idx=1
				
		for i, bird in enumerate(birds):
			bird.move()
			gap_center=(pipes[pipe_idx].top+pipes[pipe_idx].bottom)/2
			output=nets[i].activate(
				(bird.y/HEIGHT,
				(gap_center-bird.y)/HEIGHT)
			)
			dist=abs(bird.y-gap_center)
			ge[i].fitness+=max(0, 1-dist/HEIGHT)
			if output[0]>0.5:
				bird.jump()
			if bird.y>base.y or bird.y<0 or bird.collide(pipes):
				ge[i].fitness-=1
				birds.pop(i)
				ge.pop(i)
				nets.pop(i)


		if not auto_run:
			Uppdate_window(SCREEN, birds, pipes, base, score)
			TIMER.tick(FPS)

def run(config_file):
	config=neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
	
	p=neat.Population(config)
	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)
	p.run(main, 1000)
	
if __name__=='__main__':
	local_dir=os.path.dirname(__file__)
	config_path=os.path.join(local_dir, 'config-feedforward.txt')
	run(config_path)