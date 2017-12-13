import sprobj
from random import *

class Ball(sprobj.SprObj):
	HORIZONTAL_MOVEMENT = randint(1, 10)
	VERTICAL_MOVEMENT = randint(1, 10)
	MOVING_RIGHT = True
	MOVING_LEFT = True
	if(randint(0,1)):
		MOVING_RIGHT = True
	else:
		MOVING_RIGHT = False
	if(randint(0,1)):
		MOVING_TOP = True
	else:
		MOVING_TOP = False
		
	def reset(self):
		self.HORIZONTAL_MOVEMENT = randint(1, 10)
		self.VERTICAL_MOVEMENT = randint(1, 10)
		if(randint(0,1)):
			self.MOVING_RIGHT = True
		else:
			self.MOVING_RIGHT = False
		if(randint(0,1)):
			self.MOVING_TOP = True
		else:
			self.MOVING_TOP = False

	def hit_racket(self):
		self.MOVING_RIGHT = not self.MOVING_RIGHT

	def hit_lateral(self):
		self.MOVING_TOP = not self.MOVING_TOP

	#ball speed control
	def prevent_stick(self, racket):
		self.move(self.get_x_moviment() *.1* racket.width, 0)

	def moving(self, clock):
		self.move(self.get_x_moviment(), self.get_y_moviment())

	def get_x_moviment(self):
		if self.MOVING_RIGHT:
			return self.HORIZONTAL_MOVEMENT
		else:
			return -self.HORIZONTAL_MOVEMENT

	def get_y_moviment(self):
		if self.MOVING_TOP:
			return self.VERTICAL_MOVEMENT
		else:
			return -self.VERTICAL_MOVEMENT

	#helper function for checking when the ball goes out of bound for sides.
	def check_collision_sides(self, window_width):
		if(self.left < 1):
			print "Left collision detected"
			return 1
		elif(self.right > window_width - 1):
			print "Right collision detected"
			return 2
		else:
			return 0
