import random, string, threading, time
from .bag import randint_se


def transform_coordinates(x, y):
	result = 50*(y-1)+x
	return result


def restoration_coordinates(point):
	y = round(point/50)
	x = point - 50*(y-1)
	return [x, y]


class Cell:
	
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def move_to(self, x, y):
		self.x = x
		self.y = y



def checkLose(my_snake, room, direction):


	if direction==1:
		if my_snake.cells[0].y==1:
			my_snake.room.kill_snake(my_snake)
			return 1

		for snake in room.snakes:
			if snake.key == my_snake.key:
				for i in range(2, snake.length):
					if (snake.cells[0].y-1==snake.cells[i].y) and (snake.cells[0].x == snake.cells[i].x):
						return 1
			else:
				for i in range(snake.length):
					if (my_snake.cells[0].y-1==snake.cells[i].y) and (my_snake.cells[0].x == snake.cells[i].x):
						return 1



	if direction==2:
		if my_snake.cells[0].x==50:
			my_snake.room.kill_snake(my_snake)
			return 1

		for snake in room.snakes:
			if snake.key == my_snake.key:
				for i in range(2, snake.length):
					if (snake.cells[0].y==snake.cells[i].y) and (snake.cells[0].x+1 == snake.cells[i].x):
						return 1
			else:
				for i in range(snake.length):
					if (my_snake.cells[0].y==snake.cells[i].y) and (my_snake.cells[0].x+1 == snake.cells[i].x):
						return 1


	if direction==3:
		if my_snake.cells[0].y==35:
			my_snake.room.kill_snake(my_snake)
			return 1

		for snake in room.snakes:
			if snake.key == my_snake.key:
				for i in range(2, snake.length):
					if (snake.cells[0].y+1==snake.cells[i].y) and (snake.cells[0].x == snake.cells[i].x):
						return 1
			else:
				for i in range(snake.length):
					if (my_snake.cells[0].y+1==snake.cells[i].y) and (my_snake.cells[0].x == snake.cells[i].x):
						return 1


	if direction==4:
		if my_snake.cells[0].x==1:
			return 1

		for snake in room.snakes:
			if snake.key == my_snake.key:
				for i in range(2, snake.length):
					if (snake.cells[0].y==snake.cells[i].y) and (snake.cells[0].x-1 == snake.cells[i].x):
						return 1
			else:
				for i in range(snake.length):
					if (my_snake.cells[0].y==snake.cells[i].y) and (my_snake.cells[0].x-1 == snake.cells[i].x):
						return 1


	return 0



class Snake:
	

	def __init__(self, name, x, y, direction, room, length=3):
		self.name = name
		self.length = length
		self.direction = direction
		self.room = room
		self.cells = [Cell(x, y), Cell(x, y+1), Cell(x, y+2)]
		# random string key
		self.key = "".join(random.choice(string.ascii_lowercase+string.ascii_uppercase+string.digits) for x in range(34)) 

		def motor(snake):
			while 1:
				# Checking is there a snake's head at the apple point
				if (snake.cells[0].x==snake.room.apple.x) and (snake.cells[0].y==snake.room.apple.y):
					snake.extend()
					snake.room.apple = Apple(random.randint(1, 50), random.randint(1,35))

				# Will smash a snake
				if snake.direction==1:
					if checkLose(snake, snake.room, 1) == 1: 
						snake.room.kill_snake(snake)
						return
					snake.move_top()

				if snake.direction==2:
					if checkLose(snake, snake.room, 2) == 1: 
						snake.room.kill_snake(snake)
						return
					snake.move_right()
			
				if snake.direction==3:
					if checkLose(snake, snake.room, 3) == 1:
						snake.room.kill_snake(snake)
						return
					snake.move_bottom()
				
				if snake.direction==4:
					if checkLose(snake, snake.room, 4) == 1:
						snake.room.kill_snake(snake)
						return
					snake.move_left()


				time.sleep(0.1) 	# Interval time to move snake's cells

		threading.Thread(target=motor, args=(self, )).start()


	def move_top(self):
		if self.cells[1].y < self.cells[0].y: return

		oldcells = []
		for cell in self.cells:
			oldcells.append([cell.x, cell.y]);
		

		self.cells[0].move_to(self.cells[0].x, self.cells[0].y-1)
		for i in range(1, self.length):
			self.cells[i].move_to(oldcells[i-1][0], oldcells[i-1][1])
		

	def move_right(self):
		if self.cells[1].x > self.cells[0].x: return

		oldcells = []
		for cell in self.cells:
			oldcells.append([cell.x, cell.y])


		self.cells[0].move_to(self.cells[0].x+1, self.cells[0].y)
		for i in range(1, self.length):
			self.cells[i].move_to(oldcells[i-1][0], oldcells[i-1][1])


	def move_bottom(self):
		if self.cells[1].y > self.cells[0].y: return

		oldcells = []
		for cell in self.cells:
			oldcells.append([cell.x, cell.y])


		self.cells[0].move_to(self.cells[0].x, self.cells[0].y+1)
		for i in range(1, self.length):
			self.cells[i].move_to(oldcells[i-1][0], oldcells[i-1][1])


	def move_left(self):
		if self.cells[1].x < self.cells[0].x: return

		oldcells = []
		for cell in self.cells:
			oldcells.append([cell.x, cell.y])


		self.cells[0].move_to(self.cells[0].x-1, self.cells[0].y)
		for i in range(1, self.length):
			self.cells[i].move_to(oldcells[i-1][0], oldcells[i-1][1])


	def move(self, direction):
		if (direction==1) and (self.direction != 3) and not ( (self.cells[0].x == self.cells[1].x) and (self.cells[0].y == self.cells[1].y+1) ):
			self.direction = direction
		if (direction == 2) and (self.direction != 4) and not ( (self.cells[0].x+1 == self.cells[1].x) and (self.cells[0].y == self.cells[1].y) ):
			self.direction = 2
		if (direction == 3) and (self.direction != 1) and not ( (self.cells[0].x == self.cells[1].x) and (self.cells[0].y+1 == self.cells[1].y) ): 
			self.direction = 3 
		if (direction == 4) and (self.direction != 2) and not ( (self.cells[0].x == self.cells[1].x+1) and (self.cells[0].y == self.cells[1].y) ): 
			self.direction = 4


	def extend(self):

		if (self.direction == 1):
			self.cells.append(Cell(self.cells[self.length-1].x, self.cells[self.length-1].y+1))
			self.length += 1
			return

		if (self.direction == 2):
			self.cells.append(Cell(self.cells[self.length-1].x-1, self.cells[self.length-1].y))
			self.length += 1
			return

		if (self.direction == 3):
			self.cells.append(Cell(self.cells[self.length-1].x, self.cells[self.length-1].y-1))
			self.length += 1
			return

		if (self.direction == 4):
			self.cells.append(Cell(self.cells[self.length-1].x+1, self.cells[self.length-1].y))
			self.length += 1
			return


class Apple:

	def __init__(self, x, y):
		self.x = x
		self.y = y



class Room:

	amount = 0
	collector = []

	def __init__(self, free_places):
		self.__class__.amount += 1
		self.id = self.__class__.amount
		self.width = 50
		self.height = 35
		self.free_places = free_places

		self.apple = Apple(random.randint(1, self.width), random.randint(1, self.height))
		self.snakes = []
		self.__class__.collector.append(self)

	def init_snake(self, name, x, y, direction):
		snake = Snake(name, x, y, direction, self)
		self.snakes.append(snake)
		return snake.key

	def kill_snake(self, delete_snake):
		for snake in self.snakes:
			if snake.key == delete_snake.key:
				self.snakes.remove(snake)

	def is_auth(self, key):
		for snake in self.snakes:
			if snake.key == key: return True

		return False

	def get_snake(self, key):
		for snake in self.snakes:
			if snake.key == key: return snake



def get_room(id=None):
	rooms = Room.collector

	if id == None:
		if ( len(rooms) == 0 ) or ( len(rooms[-1].snakes) >= 4 ):
			return Room(4)

	elif len(rooms) >= id:
		return rooms[id-1]
