#!/usr/bin/python3
import pymysql

DB_Name =  "project"

# Connect to the database
db = pymysql.connect(host='localhost',
                     user='',
                     password='',
                     db="project")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

print ("Database version : %s " % data)

# Create table as per requirement
cursor.execute("DROP TABLE IF EXISTS `member`;");

sql1 = """
CREATE TABLE `member` (
  `Name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Weight` int NOT NULL,
  `Height` int NOT NULL,
  `LowwerChest` int DEFAULT NULL,
  `ArmCircuit` int DEFAULT NULL,
  `CalfCircuit` int DEFAULT NULL,
  `Gender` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  PRIMARY KEY (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""
cursor.execute(sql1);

cursor.execute("LOCK TABLES `member` WRITE;");
cursor.execute("UNLOCK TABLES;");
cursor.execute("DROP TABLE IF EXISTS `percussion`;");

sql2 = """
CREATE TABLE `percussion` (
  `PerNo` int NOT NULL AUTO_INCREMENT,
  `AvgPressure` int NOT NULL,
  `AvgPressureStr` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Time` datetime NOT NULL,
  `Percussion_Name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TotalTimes` int DEFAULT NULL,
  `LowTimes` int DEFAULT NULL,
  `MediumTimes` int DEFAULT NULL,
  `HighTimes` int DEFAULT NULL,
  PRIMARY KEY (`PerNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""
cursor.execute(sql2);
cursor.execute("LOCK TABLES `percussion` WRITE;");
cursor.execute("UNLOCK TABLES;");
cursor.execute("DROP TABLE IF EXISTS `soundrecord`;");

sql3 = """
CREATE TABLE `soundrecord` (
  `idsoundrecord` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Filename` varchar(100) DEFAULT NULL,
  `FileSize` decimal(10,0) DEFAULT NULL,
  `FileStreamCol` blob,
  PRIMARY KEY (`idsoundrecord`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""
cursor.execute(sql3);
cursor.execute("LOCK TABLES `soundrecord` WRITE;");
cursor.execute("UNLOCK TABLES;");
cursor.execute("SHOW TABLES;");

row = cursor.fetchone()
while row is not None:
    print(row)
    row = cursor.fetchone()

# disconnect from server
db.close()