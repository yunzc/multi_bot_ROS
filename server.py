# Python program to implement server side of chat room.
import socket
import select
import sys
from _thread import * # for python 2 it is thread without the '_'

class Server(object):
    # server object for incoming clients 
    def __init__(self, IP_address='localhost', Port=1024):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((IP_address, Port))
        self.server.listen(100)
        self.client_list = []

    def client_thread(self, conn, addr):
        message = "Connected to server"
        conn.send(message.encode('utf-8'))
        while True:
            try: 
                message = conn.recv(2048).decode('utf-8')
                if message: 
                    print("<" + addr[0] + "> " + message)
                else:
                    # message has no content if connection broken 
                    self.remove(conn)
            except:
                continue

    def remove(self, conn):
        if conn in self.client_list:
            self.client_list.remove(conn)

    def broadcast(self):
        while True:
            message = sys.stdin.readline()
            for conn in self.client_list:
                try:
                    conn.send(message.encode('utf-8'))
                except:
                    conn.close()
                    self.remove(conn)

    def run(self):
        start_new_thread(self.broadcast, ())
        while True:
            conn, addr = self.server.accept() # accept connection requests 
            self.client_list.append(conn)
            print(addr[0] + " connected")
            start_new_thread(self.client_thread, (conn, addr))
        conn.close()
        server.close()


if __name__ == '__main__':
    s = Server()
    s.run()