#!/usr/bin/python3
# -*- coding: utf-8 -*-
from socket import *
import json

# server: receive json or sound file
serverIP = ""
serverPort = 12000

class DatabaseManager():
	def __init__(self):
		global sound_file_cnt
		self.connect = pymysql.connect(host='localhost', 
			                           user='', 
			                           password='', 
			                           db=DB_Name,
			                           charset='utf8')

		self.cur = self.connect.cursor()
		self.cur.execute("SELECT idsoundrecord from soundrecord;")
		self.connect.commit()
		sound_file_cnt = self.cur.fetchone()
		if "Empty" in sound_file_cnt:
			sound_file_cnt = 0
		print(sound_file_cnt)
		#print("DB connection!")
		
	def add_del_update_db_record(self, sql_query):
		print(sql_query)
		self.cur.execute(sql_query)
		self.connect.commit()
		print(self.cur.fetchone())
		return

	def __del__(self):
		self.cur.close()
		self.connect.close()
		print("Delete connection")

def receive_json_of_sound():
	server = socket(AF_INET, SOCK_STREAM) # welcoming client
	server.bind((serverIP, serverPort))
	server.listen(10)
	print("The server is ready to receive.")

	connSocket, addr = server.accept() # accept socket
	l = connSocket.recv(1024)
	print(l)
	if l == "Newest":
		# Time, AvgPressureStr, LowTimes, MediumTimes, HighTimes, 
		dbObj = DatabaseManager()
		sql_query = "INSERT INTO treatment (Percussion_Name, AvgPressureStr, Time, LowTimes, MediumTimes, HighTimes) VALUES ("
		sql_query += '\"tester\", \"' + avg_pressure_str + '\", now(), ' + str(pat_level_dict["Soft"]) + ', ' + str(pat_level_dict["Medium"]) + ', ' + str(pat_level_dict["Hard"]) + ');'
		dbObj.add_del_update_db_record(sql_query)

	server.close()

receive_json_of_sound()