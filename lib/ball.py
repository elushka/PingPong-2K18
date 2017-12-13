import sprobj
from random import *

class Ball(sprobj.SprObj):

	MOVING_RIGHT = True
	MOVING_TOP = True
	HORIZONTAL_MOVEMENT = randint(1, 3)
	VERTICAL_MOVEMENT = randint(1, 3)

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
