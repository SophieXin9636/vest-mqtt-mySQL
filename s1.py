#!/usr/bin/python3
# -*- coding: utf-8 -*-
from socket import *
import json

# server: receive json or sound file
serverIP = ""
serverPort = 12000

client = socket(AF_INET, SOCK_STREAM) # welcoming client
client.connect((serverIP, serverPort))

print("The client is ready to send.")

l = client.send(b'Newest')
client.close()
print('client close.')