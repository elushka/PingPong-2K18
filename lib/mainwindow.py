import simplejson, socket, sys, pyglet
import settings
import game
from pyglet.gl import *

class MainWindow(pyglet.window.Window):
    keys = None
    game = None

    img1 = pyglet.image.load(settings.FIELD_IMG)

    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args, **kwargs)

        self.game = game.Game(multiplayer_mode=True)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)

    def parse_keys(self):
        if self.keys[pyglet.window.key.UP] and self.game.racket_me.y < settings.WINDOW_HEIGHT:
            self.game.racket_me.move(0, settings.MOVE_SPEED)

        if self.keys[pyglet.window.key.DOWN] and self.game.racket_me.y > 0:
            self.game.racket_me.move(0, -settings.MOVE_SPEED)

    def on_draw(self):
        self.clear()
        self.parse_keys()

        self.img1.blit(0, 0)
        self.game.draw()

        self.game.ball.draw()
        self.game.score_lp.draw()
        self.game.score_rp.draw()
        self.game.racket_left.draw()
        self.game.racket_right.draw()
