#!/usr/bin/python
import socket, select, sys, time, simplejson, redis, urllib2

ret = urllib2.urlopen('https://enabledns.com/ip')

#configure IP of the hosting server
IP_SERVER = ret.read()

r = redis.Redis(
    host='redis-16907.c15.us-east-1-4.ec2.cloud.redislabs.com',
    port=16907,
    password='pingpong')

r.set("ip",IP_SERVER)
r.get("ip")

print "This is first one:"
print r.get("ip")
print "This is second one:"
print r

buffer_size = 2000
delay = 0.0
rackets = {}
SERVER_IP = r.get("ip")
SERVER_PORT = 50090

class GameServer:

    def __init__(self, host, port):
        self.input_list = []
        self.channel = {}

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(0)

    #loop for continuous data transfer
    def main_loop(self):
        self.input_list.append(self.server)
        while 1:
            #todo: disconnect new clients if the number is > 2
            time.sleep(delay)
            inputr, outputr, exceptr = select.select(self.input_list, [], [])
            for self.s in inputr:
                if self.s == self.server:
                    self.on_accept()
                    break
                else:
                    self.data = self.s.recv(buffer_size)
                if len(self.data) == 0:
                    self.on_close()
                else:
                    self.on_recv()

    #feedback for server connection
    def on_accept(self):
        clientsock, clientaddr = self.server.accept()
        print clientaddr, "has connected"
        rackets[clientaddr[1]] = {}
        self.input_list.append(clientsock)

    def on_close(self):
        clientaddr = self.s.getpeername()
        print clientaddr, "has disconnected"
        del(rackets[clientaddr[1]])
        self.input_list.remove(self.s)

    def on_recv(self):
        player_id = self.s.getpeername()[1]
        rackets[player_id] = simplejson.loads(self.data)
        self.s.send(simplejson.dumps(rackets))

if __name__ == '__main__':
        server = GameServer(SERVER_IP, SERVER_PORT)
        print SERVER_IP
        print "Server listening..."
        try:
            server.main_loop()
        except KeyboardInterrupt:
            print "Ctrl C - Stopping server"
            sys.exit(1)
