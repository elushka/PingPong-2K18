import urllib2

ret = urllib2.urlopen('https://enabledns.com/ip')

SERVER_IP = ret.read()
SERVER_PORT = 50090

WINDOW_WIDTH = 697
WINDOW_HEIGHT = 353

MOVE_SPEED = 12
BALL_IMG = 'assets/ball.png'
RACKET_IMG = 'assets/racket.png'
FIELD_IMG = 'assets/field.png'
