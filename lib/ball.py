import sprobj

class Ball(sprobj.SprObj):

	MOVING_RIGHT = True
	MOVING_TOP = True
	HORIZONTAL_MOVIMENT = 2.4
	VERTICAL_MOVIMENT = 2

	def hit_racket(self):
		self.MOVING_RIGHT = not self.MOVING_RIGHT

	def hit_lateral(self):
		self.MOVING_TOP = not self.MOVING_TOP

	def prevent_stick(self, racket):
		self.move(self.get_x_moviment() *.1* racket.width, 0)

	def moving(self, clock):
		self.move(self.get_x_moviment(), self.get_y_moviment())

	def get_x_moviment(self):
		if self.MOVING_RIGHT:
			return self.HORIZONTAL_MOVIMENT
		else:
			return -self.HORIZONTAL_MOVIMENT

	def get_y_moviment(self):
		if self.MOVING_TOP:
			return self.VERTICAL_MOVIMENT
		else:
			return -self.VERTICAL_MOVIMENT
			
	def check_collision_sides(self, window_width):
		if(self.left < 1):
			print "Left collision detected"
			return 1
		elif(self.right > window_width - 1):
			print "Right collision detected"
			return 2
		else:
			return 0