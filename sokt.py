#!/usr/bin/python3
# -*- coding: utf-8 -*-
from socket import *

# server: receive json or sound file
serverIP = ""
serverPort = 12000

def receive_json_of_sound():
	server = socket(AF_INET, SOCK_STREAM) # welcoming client
	server.bind((serverIP, serverPort))
	server.listen(1)
	print("The server is ready to receive.")

	connSocket, addr = server.accept() # accept socket
	with open('output', 'wb') as f:
		while True:
			l = connSocket.recv(1024)
			if not l:
				break
			f.write(l)

	server.close()

receive_json_of_sound()