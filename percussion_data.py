from socket import *
from colorama import Fore, Style
import json
import pymysql

DEBUG = True

# server: receive json or sound file
serverIP = "s192.168.43.30"
serverPort2 = 14000

DB_Name = "project"
pat_level_dict = {}
force_data_list = []

pat_level_dict["Soft"] = 0
pat_level_dict["Medium"] = 0
pat_level_dict["Hard"] = 0
sound_file_cnt = 0

def print_dbg(msg, dbg, type):
	"""
	# type:
	  0: red  (Stage)
	  1: green (success)
	  2: bule (server info)
	  3: yellow (receive and send)
	  4: skyblue (data info)
	"""
	if dbg:

		if type == 0:
			print(Fore.RED + msg)
		if type == 1:
			print(Fore.GREEN + msg)
		if type == 2:
			print(Fore.BLUE + msg)
		if type == 3:
			print(Fore.YELLOW + msg)
		if type == 4:
			print(Fore.CYAN + msg)
		#print(msg)

print_dbg("Initialize Data ...", DEBUG, 0)

class DatabaseManager():
	def __init__(self):
		global sound_file_cnt
		self.connect = pymysql.connect(host='localhost', 
			                           user='root', 
			                           password='03135040', 
			                           db=DB_Name,
			                           charset='utf8')

		self.cur = self.connect.cursor()
		self.cur.execute("SELECT idsoundrecord FROM soundrecord WHERE idsoundrecord = (SELECT MAX(idsoundrecord) FROM soundrecord);")
		self.connect.commit()
		test = self.cur.fetchone()
		if test == None or "Empty" in test:
			sound_file_cnt = 0
		else:
			sound_file_cnt = int(test[0])
		print_dbg("DB connection!", DEBUG, 0)
		
	def add_del_update_db_record(self, sql_query):
		print_dbg(sql_query, DEBUG, 4)
		self.cur.execute(sql_query)
		self.connect.commit()
		test = self.cur.fetchone()
		if type(test) == type(tuple()):
			return ''.join(test)

	def __del__(self):
		self.cur.close()
		self.connect.close()
		print_dbg("Delete DB connection", DEBUG, 2)


server = socket(AF_INET, SOCK_STREAM) # welcoming client
server.bind(("192.168.43.30", 12000))
server.listen(5)
print_dbg("The server is ready to receive socket.", DEBUG, 2)

connSocket, addr = server.accept() # accept socket
print_dbg("Socket Connect!", DEBUG, 0)
l = connSocket.recv(1024).decode()

if l == "Newest":
	print_dbg(l, DEBUG, 1)
	# Time, AvgPressureStr, LowTimes, MediumTimes, HighTimes, 
	dbObj = DatabaseManager()
	"""
	sql_query = 'SELECT json_object("AvgPressureStr", AvgPressureStr, "Time", Time, "LowTimes", LowTimes, "MediumTimes", MediumTimes, "HighTimes", HighTimes) FROM treatment WHERE PerNo = (SELECT MAX(PerNo) FROM treatment)'
	newest_force_json_data = dbObj.add_del_update_db_record(sql_query)
	"""
	#print(newest_force_json_data.encode())
	"""
	connSocket.sendall(newest_force_json_data.encode())
	print_dbg(str(connSocket), DEBUG, 4)
	"""