#!/usr/bin/python3
import json
import pymysql

# MySQL DB Name
DB_Name =  "Pat_IoT.db"

class DatabaseManager():
	def __init__(self):
		self.connect = pymysql.connect(host='localhost', 
			                           user='user', 
			                           password='passwd', 
			                           db=DB_Name)
		self.connect.execute('pragma foreign_keys = on')
		self.connect.commit()
		self.cur = self.connect.cursor()
		
	def add_del_update_db_record(self, sql_query, args=()):
		self.cur.execute(sql_query)
		self.connect.commit()
		return

	def __del__(self):
		self.cur.close()
		self.connect.close()

def Force_Data_Handler(jsonData):
	#Parse Data 
	json_dict = json.loads(jsonData)
	SensorID = json_dict['No']
	timestamp = json_dict['Date']
	Force = json_dict['Force']

	# TODO: Add other Attributes
	
	#Push into DB Table
	dbObj = DatabaseManager()
	dbObj.add_del_update_db_record("insert into force_Data (SensorID, timestamp, Force) values (?,?,?)",[SensorID, timestamp, Force])
	del(dbObj)
	print("Inserted Force Data into Database.", end="\n\n")

def sensor_Data_Handler(Topic, jsonData):
	if Topic == "Home/Force":
		Force_Data_Handler(jsonData)
