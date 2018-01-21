#!/usr/bin/python
import numpy as np 

import sys
import socket
import select
# test networking on computer without using robot 

vehicle_id = '1'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
	print("Correct usage: script, IP address, port number")
	exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))

# drive(1, 0.5)
connected = False
while not connected:
	print("...")
	server.send(vehicle_id.encode('utf-8'))
	message = server.recv(2048)
	if message == "Connected to server":
		connected = True
		
print("connected")

while True:
	server.send('Hello from the other side')

	print("listening and executing")
	
	message = server.recv(2048)
	print(message)
print("Disconnecting...")
server.close()