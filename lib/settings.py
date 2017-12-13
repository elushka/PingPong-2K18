import redis

#configure IP of the hosting server
r = redis.Redis(
    host='redis-16907.c15.us-east-1-4.ec2.cloud.redislabs.com',
    port=16907,
    password='pingpong')

SERVER_IP = r.get("ip")
SERVER_PORT = 50090

#pyglet window size
WINDOW_WIDTH = 697
WINDOW_HEIGHT = 353

#the move speed defines the racket here, not the ball
MOVE_SPEED = 12
BALL_IMG = 'assets/ball.png'
RACKET_IMG = 'assets/racket.png'
FIELD_IMG = 'assets/field.png'
