import pygame
import time
import numpy as np
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
pygame.init()

SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH , HEIGHT = SCREEN.get_size()
clock = pygame.time.Clock()

res = 64
smooth = 6

def calculate(C):
	Z = np.full_like(C, 0+0j, dtype=np.complex64)
	
	times = np.zeros_like(Z, dtype=np.uint8)
	mask = np.ones_like(Z, dtype=bool)
	
	for i in range(res):
		Z = Z ** 2 + C
		#Z = Z ** 100 + 1/C
		#Z = Z ** 2 + C ** 6 - 1
		#Z = np.cos(Z) + 1/C
		#Z = np.sin(Z * C**2) # 1+0j
		#Z = np.cos(Z * C ** 3)
		#Z = np.exp(Z ** 3 / C ** 3)
		#Z = np.exp((Z ** 2 - 1.00001 * Z)/ np.sqrt(C ** 3))
		
		new_mask = (Z.real ** 2 + Z.imag ** 2) < 4
		just_escaped = mask & (~new_mask)
		times[just_escaped] = i
		
		mask = new_mask
		times[mask] += 1
		
	return times

def worker(C, results, i):
	results[i] = calculate(C)
	
def threading_calculate(C, workers = 4):
	parts = np.array_split(C, workers)
	thread = []
	results = [None] * workers
	for i in range(workers):
		t = threading.Thread(target=worker, args=(parts[i], results, i))
		thread.append(t)
	
	for t in thread:
		t.start()
	for t in thread:
		t.join()
	
	return np.concatenate(results)

def multiprocessing_calculate(C):
	cores = 2#multiprocessing.cpu_count()
	parts = np.array_split(C, cores)
	with multiprocessing.Pool(cores) as p:
		results = p.map(calculate, parts)
		
	return np.concatenate(results)

def thread_pool_calculate(C, workers = 4):
	parts = np.array_split(C, workers)
	with ThreadPoolExecutor(workers) as pool:
		results = list(pool.map(calculate, parts))
		
	return np.concatenate(results)

def render(surf, arr):
	rgb = np.zeros((arr.shape[0], arr.shape[1], 3), dtype = np.uint8)
	
	finished = (arr == res)
	c = (arr * smooth).astype(np.uint8)
	
	r = c % 255
	g = (c * 2) % 255
	b = (c * 5) % 255
	rgb[:, :, 0] = r
	rgb[:, :, 1] = g
	rgb[:, :, 2] = b
	
	rgb[finished] = (0, 0, 0)
	
	pygame.surfarray.blit_array(surf, rgb)

def init(dx, dy, cx, cy, w, h):
	sx, ex = cx - dx, cx + dx
	sy, ey = cy - dy, cy + dy
	xs = (dx * 2) / w
	ys = (dy * 2) / h
	
	x = np.linspace(sx, ex, w)
	y = np.linspace(sy, ey, h)
	x, y = np.meshgrid(x, y)
	C = (x + y * 1j).astype(np.complex64)
	C = C.T
	
	return (sx, ex, sy, ey, xs, ys, C)
	
def main():
	res_scale = 1
	w, h = WIDTH // res_scale, HEIGHT // res_scale
	surf = pygame.Surface((w, h)).convert()
	
	dx = 3
	dy = dx / 2
	zoom_power = 3
	cx, cy = 0, 0
	sx, ex, sy, ey, xs, ys, C = init(dx, dy, cx, cy, w, h)
	
	t0 = time.time()
	#arr = calculate(C)
	#arr = multiprocessing_calculate(C)
	#arr = thread_pool_calculate(C)
	arr = threading_calculate(C)
	t1 = time.time()
	render(surf, arr)
	t2 = time.time()
	run = True
	while run:
		
		for e in pygame.event.get():
			if e.type == pygame.MOUSEBUTTONDOWN:
				mx, my = pygame.mouse.get_pos()
				cx = sx + mx * xs
				cy = sy + my * ys
	
				dx /= zoom_power
				dy /= zoom_power
				
				sx, ex, sy, ey, xs, ys, C = init(dx, dy, cx, cy, w, h)
				arr = threading_calculate(C)
				render(surf, arr)
				
				
				
			
		#if pygame.mouse.get_pressed()[0]:
#			print(f"clacute time: {t1 - t0}")
#			print(f"render time: {t2 - t1}")
#			print(f"total time: {t2 - t0}")
#			raise
		
		scaled = pygame.transform.scale(surf, (WIDTH, HEIGHT))
		SCREEN.blit(scaled, (0, 0))
		
		pygame.display.update()
		clock.tick(60)
if __name__ == "__main__":
	multiprocessing.freeze_support()
	main()