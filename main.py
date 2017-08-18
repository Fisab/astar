import pygame
import math

class Window():
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("A*")

		self.cell_size = 25

		self.cell_amount = [50, 50]
		self.screen_size = [self.cell_amount[0] * self.cell_size, self.cell_amount[1] * self.cell_size]
		self.screen = pygame.display.set_mode(self.screen_size)

		self.grid_color = (200,200,200)
		self.clear_color = (255,255,255)

	def draw_grid(self):
		for y in range(self.cell_amount[1]):
			pygame.draw.line(self.screen, self.grid_color, [y * self.cell_size, 0], [y * self.cell_size, self.screen_size[1]], 1)
		for x in range(self.cell_amount[0]):
			pygame.draw.line(self.screen, self.grid_color, [0, x * self.cell_size], [self.screen_size[0], x * self.cell_size], 1)


	def clear(self):
		self.screen.fill(self.clear_color)
		self.draw_grid()

	def get_mouse_pos(self):
		pos = pygame.mouse.get_pos()
		pos = [math.floor(pos[0]/self.cell_size), math.floor(pos[1]/self.cell_size)]
		return pos

	def update(self):
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = self.get_mouse_pos()
			if event.button == 1:
				self.map.add_wall(pos)
				self.alg.update_barriers(self.map.walls)
				self.alg.restart()
			if event.button == 3:
				self.map.del_wall(pos)
				self.alg.update_barriers(self.map.walls)
				self.alg.restart()
			if event.button == 2:
				self.map.start = pos
				self.alg.start = self.map.start
				self.alg.restart()

	def draw(self):
		self.clear()
		#...

def scale(arr, cell_size):
	res_arr = []
	for i in arr:
		res_arr.append(i)
	if type(arr) == type(1):
		return arr * cell_size
	for i in range(len(arr)):
		if i > 1:
			break
		if type(arr[i]) == type([]):
			for j in range(len(arr[i])):
				res_arr[i][j] *= cell_size
		else:
			res_arr[i] *= cell_size
	return res_arr

class Map():
	def __init__(self, cell_size, screen, cell_amount):
		self.start_color = (0, 100, 0)
		self.finish_color = (0, 0, 100)
		self.wall_color = (100, 100, 100)

		self.cell_size = cell_size
		self.cell_amount = cell_amount
		self.screen = screen

		self.load_barriers_1()
		self.load_AB_1()

	def add_wall(self, pos):
		if not pos in self.walls:
			self.walls.append(pos)

	def del_wall(self, pos):
		if pos in self.walls:
			self.walls.remove(pos)

	def load_barriers_1(self):
		self.walls = [[5,4], [5,5], [5,6], [5,7], [5,8], [5,9]]

		for i in range(self.cell_amount[0]):
			self.walls.append([i,0])
			self.walls.append([i, self.cell_amount[1]-1])
		for i in range(self.cell_amount[1]):
			self.walls.append([0,i])
			self.walls.append([self.cell_amount[0]-1, i])

	def load_AB_1(self):
		self.start = [2,6]
		self.finish = [8,6]

	def draw_walls(self):
		for i in self.walls:
			pos = scale(i, self.cell_size)
			pygame.draw.rect(self.screen, self.wall_color, (pos[0], pos[1], self.cell_size, self.cell_size))

	def draw_AB(self):
		s = scale(self.start, self.cell_size)
		f = scale(self.finish, self.cell_size)
		pygame.draw.rect(self.screen, self.start_color, (s[0], s[1], self.cell_size, self.cell_size))
		pygame.draw.rect(self.screen, self.finish_color, (f[0], f[1], self.cell_size, self.cell_size))

	def draw(self):
		self.draw_walls()
		self.draw_AB()

class A_star():
	def __init__(self, start, finish, barriers, cs, screen):
		self.start = start
		self.finish = finish

		self.barriers = barriers

		self.old_color = (100,150,150)
		self.cur_color = (0,150,170)

		self.done_color = (255,0,0)

		self.cell_size = cs
		self.screen = screen

		self.cur_cell = self.start
		self.open_cells = [self.start]
		self.close_cells = []

		self.done_cells = []

	def restart(self):
		self.cur_cell = self.start
		self.open_cells = [self.start]
		self.close_cells = []

		self.done_cells = []

	def update_barriers(self, barriers):
		self.barriers = barriers

	def get_distance(self, pos1, pos2):
		dist = int(math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2))
		return dist

	def get_dir_pr(self, old_pos, new_pos):
		g_diag = 14
		g_orth = 10
		#return True/False = Orthogonal/Diagonal
		if old_pos[0] == new_pos[0] or old_pos[1] == new_pos[1]:
			return g_orth
		else:
			return g_diag

	def calc_price(self, h, g):
		return h*10+g

	def check_collision(self, pos):
		for i in self.barriers:
			if i == pos:
				return True
		return False

	def draw(self):
		for i in self.open_cells:
			pos = scale(i, self.cell_size)
			color = self.cur_color
			pygame.draw.rect(self.screen, color, (pos[0]+5, pos[1]+5, self.cell_size-10, self.cell_size-10))
		for i in self.close_cells:
			pos = scale(i, self.cell_size)
			color = self.old_color
			#if i == self.close_cells[len(self.close_cells)-1]:
			#	color = self.done_color
			pygame.draw.rect(self.screen, color, (pos[0]+5, pos[1]+5, self.cell_size-10, self.cell_size-10))

		for i in self.done_cells:
			pos = scale(i, self.cell_size)
			pygame.draw.rect(self.screen, self.done_color, (pos[0]+5, pos[1]+5, self.cell_size-10, self.cell_size-10))

	def check_exist(self, pos, arr):
		for i in arr:
			if i[0] == pos[0] and i[1] == pos[1]:
				return False
		return True

	def look_around(self, pos):
		around_arr = [[0,1],[1,0],[1,1],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
		new_cells = []
		for i in around_arr:
			new_pos = [pos[0]+i[0], pos[1]+i[1], [i[0],i[1]]]
			p = [new_pos[0], new_pos[1]]
			if not self.check_collision(p) and self.check_exist(p, self.close_cells) and self.start != p and self.check_exist(p, self.open_cells):
				self.open_cells.append(new_pos)
	def rm(self, arr, pos):
		for i in arr:
			if i[0] == pos[0] and i[1] == pos[1]:
				arr.remove(i)
				break
		return arr

	def find_path(self):
		pos = self.cur_cell
		if len(self.done_cells) != 0:
			return True
		self.done_cells.append(pos)
		while True:
			for i in self.close_cells:
				if pos[0] == i[0] and pos[1] == i[1]:
					pos = [ i[0]-i[2][0], i[1]-i[2][1] ]
					self.done_cells.append(pos)
				if pos[0] == self.start[0] and pos[1] == self.start[1]:
					return


	def main(self):
		if self.cur_cell[0] == self.finish[0] and self.cur_cell[1] == self.finish[1]:
			if len(self.done_cells) != 0:
				return
			a = self.find_path()
			return
		smallest_price = 0
		best_cell = []
		new_cells = self.look_around(self.cur_cell)
		if len(self.open_cells) == 0:
			return
		for i in self.open_cells:
		 	g = self.get_dir_pr(self.cur_cell, i)
		 	h = self.get_distance(i, self.finish)
		 	f = self.calc_price(h, g)
		 	if smallest_price > f or smallest_price == 0:
		 		smallest_price = f
		 		best_cell = i
		self.open_cells.remove(best_cell)
		self.close_cells.append(best_cell)
		self.cur_cell = best_cell

if __name__ == '__main__':
	window = Window()
	window.map = Map(window.cell_size, window.screen, window.cell_amount)
	window.alg = A_star(window.map.start, window.map.finish, window.map.walls, window.cell_size, window.screen)
	clock = pygame.time.Clock()
	done = False

	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
		window.alg.main()
		window.clear()
		window.update()
		window.map.draw()
		window.alg.draw()
		pygame.display.flip()
		clock.tick(60)
	pygame.quit()