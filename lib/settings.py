import urllib2

ret = urllib2.urlopen('https://enabledns.com/ip')

#configure IP of the hosting server
SERVER_IP = ret.read()
SERVER_PORT = 50090

#pyglet window size
WINDOW_WIDTH = 697
WINDOW_HEIGHT = 353

#the move speed defines the racket here, not the ball
MOVE_SPEED = 12
BALL_IMG = 'assets/ball.png'
RACKET_IMG = 'assets/racket.png'
FIELD_IMG = 'assets/field.png'
