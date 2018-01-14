import socket
import select
import sys

class Client(object):
    # client to run on each individual bot in a team 
    def __init__(self, IP_address, Port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((IP_address, Port))

    def run(self):
        while True:
         
            # maintains a list of possible input streams
            sockets_list = [sys.stdin, self.server]

            read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])
         
            for socks in read_sockets:
                if socks == self.server:
                    message = socks.recv(2048)
                    print(message.decode('utf-8'))
                else:
                    message = sys.stdin.readline()
                    self.server.send(message.encode('utf-8'))
                    sys.stdout.write("<You> ")
                    sys.stdout.write(message)
                    sys.stdout.flush()
        self.server.close()

if __name__ == "__main__":
    c = Client('localhost', 1024)
    c.run()