import simplejson, socket, pyglet
import settings
from racket import Racket
from ball import Ball

def connect():
	try:
		conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		conn.connect((settings.SERVER_IP, settings.SERVER_PORT))
		me = str(conn.getsockname()[1])
		print "Client connected to %s:%s with id: %s" % (settings.SERVER_IP, settings.SERVER_PORT, me)
		return [me, conn]
	except socket.error:
		print "Couldn't connect to game server in: %s:%s" % (settings.SERVER_IP, settings.SERVER_PORT)
		sys.exit(1)

class Game(pyglet.window.Window):
	running = False
	racket_left = None
	racket_right = None
	racket_me = None
	score_left = 0
	score_right = 0
	score_lp = None
	score_rp = None
	master_client = False
	multiplayer_mode = False

	def __init__(self, multiplayer_mode = False):
		self.load_sprites()
		self.multiplayer_mode = multiplayer_mode
		if self.multiplayer_mode:
			self.me, self.conn = connect()

	def draw(self):
		if self.multiplayer_mode:
			self.draw_multiplayer()
		else:
			self.draw_singleplayer()

	def run(self):
		if not self.running:
			pyglet.clock.schedule_interval(self.ball.moving, .005)
			self.running = True

	def pause(self):
		if self.running:
			pyglet.clock.unschedule(self.ball.moving)
			self.running = False

	def load_sprites(self):
		self.score_lp = pyglet.text.Label('', font_size=15, x=settings.WINDOW_WIDTH/2 - 30, y=settings.WINDOW_HEIGHT - 15, anchor_x='center', anchor_y='center')
		self.score_rp = pyglet.text.Label('', font_size=15, x=settings.WINDOW_WIDTH/2 + 30, y=settings.WINDOW_HEIGHT - 15, anchor_x='center', anchor_y='center')
		self.racket_left = Racket(pyglet.resource.image(settings.RACKET_IMG)).center_anchor_y(settings.WINDOW_HEIGHT)
		self.racket_right = Racket(pyglet.resource.image(settings.RACKET_IMG)).center_anchor_y(settings.WINDOW_HEIGHT)
		self.ball = Ball(pyglet.resource.image(settings.BALL_IMG)).center_anchor_y(settings.WINDOW_HEIGHT).center_anchor_x(settings.WINDOW_WIDTH)
		self.racket_right.x = settings.WINDOW_WIDTH - self.racket_right.width
		self.racket_me = self.racket_left
		self.ball.reset()

	def reset(self):
		self.racket_left = Racket(pyglet.resource.image(settings.RACKET_IMG)).center_anchor_y(settings.WINDOW_HEIGHT)
		self.racket_right = Racket(pyglet.resource.image(settings.RACKET_IMG)).center_anchor_y(settings.WINDOW_HEIGHT)
		self.ball = Ball(pyglet.resource.image(settings.BALL_IMG)).center_anchor_y(settings.WINDOW_HEIGHT).center_anchor_x(settings.WINDOW_WIDTH)
		self.racket_right.x = settings.WINDOW_WIDTH - self.racket_right.width
		self.racket_me = self.racket_left
		self.ball.reset()

	def define_players(self, server_response):
		if self.me == sorted(server_response.keys())[0]: #the first client connection
			self.master_client = True
			self.racket_me = self.racket_left
			self.racket_vs = self.racket_right
		else:
			self.master_client = False
			self.racket_me = self.racket_right
			self.racket_vs = self.racket_left
		self.score_lp.text = str(self.score_right)
		self.score_rp.text = str(self.score_left)

	def on_collision(self):
		player = self.ball.check_collision([self.racket_left, self.racket_right])
		if player:
			self.ball.hit_racket()
			self.ball.prevent_stick(player)
		if self.ball.check_collision_laterals(settings.WINDOW_HEIGHT):
			self.ball.hit_lateral()

		side = self.ball.check_collision_sides(settings.WINDOW_WIDTH)

		if side == 1:
			self.score_left += 1
		elif side == 2:
			self.score_right += 1
		if side > 0:
			self.pause()
			self.reset()
			self.run()
			print 'reset'

	def update_server_data(self):
		data = {
			"ball": {
				"x": self.ball.x,
				"y": self.ball.y,
			},
			"racket": {
				"x": self.racket_me.x,
				"y": self.racket_me.y,
			},
			"score": {
				"left": self.score_left,
				"right": self.score_right,
			}
		}
		self.conn.send(simplejson.dumps(data))
		return simplejson.loads(self.conn.recv(2000))

	def update_multiplayer_positions(self, data):
		for playerid in data.keys():
			try:
				if playerid != self.me:
					self.racket_vs.y = data[playerid]['racket']['y']

					if not self.master_client:
						self.ball.x = data[playerid]['ball']['x']
						self.ball.y = data[playerid]['ball']['y']
						self.score_right = data[playerid]['score']['right']
						self.score_left = data[playerid]['score']['left']
			except:
				pass

	def draw_multiplayer(self):
		data = self.update_server_data()
		self.define_players(data)

		if len(data.keys()) == 2:
			self.run()
		else:
			self.pause()

		if self.master_client:
			self.on_collision()

		self.update_multiplayer_positions(data)

	def draw_singleplayer(self):
		self.run()
		self.on_collision()
