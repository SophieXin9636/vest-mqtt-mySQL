#!/usr/bin/python3
# -*- coding: utf-8 -*-
from socket import *
import json
import time

# server: receive json or sound file
serverIP = ""
serverPort = 12000

client = socket(AF_INET, SOCK_STREAM) # welcoming client
client.connect((serverIP, serverPort))

print("The client is ready to send.")

l = client.send(b'Newest')

time.sleep(5)

file = open("", "rb")
data = file.read(1024)
cnt = 0
while data:
	print(cnt)
	cnt += 1
	client.send(data)
	data = file.read(4096)

client.close()
print('client close.')