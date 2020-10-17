#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import pymysql
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sklearn.preprocessing
import os
import pandas as pd
from PIL import Image
from socket import *
from pydub import AudioSegment
from keras.models import load_model
from keras.utils import to_categorical
from percussion_data import *

# spectrogram setting
output_extension = ".png"
my_dpi = 24
figsize = (4,6)

# MySQL DB Name
DB_Name = "project"
SOFT = 300
MDEIUM = 500
HARD = 1000
sound_file_cnt = 0

# server: receive json or sound file
serverIP = ""
serverPort = 12000

# open wave file (assume it is 64 ms frame)
label_dict = {"incorrect":0, "correct":1}
my_dpi = 24
x_test = None
y_test_label = []
input_label = "correct" # default

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

def Force_Data_Handler(jsonData):
	# 1. receive force data
	# Parse Data 
	json_dict = json.loads(jsonData)
	pat_no = json_dict['No']
	pat_level = json_dict['level']
	pat_force = json_dict['force']

	force_data_list.append(pat_force)

	if pat_level == 0:
		pat_str = "Soft"
	elif pat_level == 1:
		pat_str = "Medium"
	elif pat_level == 2:
		pat_str = "Hard"

	if pat_str in pat_level_dict:
		pat_level_dict[pat_str] += 1
	else:
		pat_level_dict[pat_str] = 1

	# 2. Push into DB Table
	dbObj = DatabaseManager()

	if pat_no < 250: # patting times
		print("Save Force Data into Database")
		#sql_query = "INSERT INTO percussion (PerNo, AvgPressureStr, Force) values ("
		#sql_query += pat_no + ',' pat_str + ',' + pat_force + ')'
		#dbObj.add_del_update_db_record(sql_query)
		#del(dbObj)
	else: # record a course of treatment
		print("Save Treatment Data into Database")
		# calculate average force
		print(force_data_list)
		average_force = sum(force_data_list) / len(force_data_list)

		if average_force <= SOFT:
			avg_pressure_str = "Too Soft"
		elif average_force >= HARD:
			avg_pressure_str = "Too Hard"
		else:
			avg_pressure_str = "Moderate"

		sql_query = "INSERT INTO treatment (Percussion_Name, AvgPressureStr, Time, LowTimes, MediumTimes, HighTimes) VALUES ("
		sql_query += '\"tester\", \"' + avg_pressure_str + '\", now(), ' + str(pat_level_dict["Soft"]) + ', ' + str(pat_level_dict["Medium"]) + ', ' + str(pat_level_dict["Hard"]) + ');'
		dbObj.add_del_update_db_record(sql_query)
		force_data_list.clear()
		print("Inserted Force Data into Database.", end="\n\n")

		# waiting for receive sound file and save filename into DB: use sokt.py
		sound_file_name = sound_file_cnt + ".aac"
		receive_json_of_sound()

		sql_query = "INSERT INTO soundrecord (Name, Filename, FileSize) VALUES ("
		sql_query += '\"tester\", \"' + sound_file_name + '\", ' + str(file_size) + ');'
		dbObj.add_del_update_db_record(sql_query)
		del(dbObj)

		# split into frame: use split.py
		auto_create_frame(sound_file_name, out_path)

		# create spectrogram: use spectrogram.py 
		call_Transform(intput_audio_path, save_image_path)

		# sound recognition: use validation.py
		sound_recognition(correct_path, incorrect_path)


def receive_json_of_sound(filename):

	server = socket(AF_INET, SOCK_STREAM) # welcoming client
	server.bind((serverIP, serverPort))
	server.listen(1)
	print("The server is ready to receive.")

	connSocket, addr = server.accept() # accept socket
	with open(filename, 'wb') as f:
		while True:
			l = connSocket.recv(1024)
			if not l:
				break
			f.write(l)

	server.close()


def call_Transform(intput_audio_path, save_image_path):
	global intput_audio_path, save_image_path
	global output_extension
	y, sr = None, 20480

	print('Input  File： ', intput_audio_path)
	print('Output Path： ', save_image_path)

	audio_files = os.listdir(intput_audio_path)
	fig = plt.figure(dpi=my_dpi, figsize=figsize, frameon=False)

	for file in audio_files:
		filename = intput_audio_path + file
		if os.path.isdir(filename) or file.split('.')[1] != "wav":
			continue
		y, sr = librosa.load(filename, sr=20480) # sr: sample rate / sample frequency

		# STFT
		stft_data = librosa.stft(y, n_fft=4096)
		Xdb1 = librosa.amplitude_to_db(abs(stft_data))
		librosa.display.specshow(Xdb1)

		fig.savefig(save_image_path + file.split('.')[0] + output_extension, dpi=my_dpi, bbox_inches='tight')
		plt.clf()

	plt.close('all')

	print("\nSTFT Spectrogram Has Created!")


def auto_create_frame(inputfile, outputPath):
	print('Input  File：', inputfile)
	print('Output Path：', outputPath)

	# inport
	file_extension = inputfile.split('.')[1] # wav gpp ... etc
	sound = AudioSegment.from_file(inputfile, format=file_extension)

	patting_frame_range = []
	i = 0
	# large volume percussion
	while i < int(sound.duration_seconds*1000):
		x = sound[i].dBFS
		if x > -30:
			patting_frame_range.append([i-20, i+180])
			i += 300
		else:
			i += 1

	# export sound
	num_of_file = 0
	files = os.listdir(outputPath)
	print(len(files))
	for f in files:
		if os.path.isfile(outputPath+f):
			num_of_file += 1
	for cnt, data in enumerate(patting_frame_range):
		sound[data[0]:data[1]].export(outputPath+"frame_"+ str(cnt+num_of_file)+".wav", format="wav")
	print("Totally create" , cnt+1, "wave files!")
	print("Output Path：[", outputPath, "] has", len(os.listdir(outputPath)), "wave files")


def sound_recognition(correct_path, incorrect_path):
	global x_test, y_test_label,
	print("Input  Correct Path: ", correct_path)
	print("Input Inorrect Path: ", incorrect_path, end="\n\n")
	add_img_data_into_validation_set(correct_path, "correct")
	add_img_data_into_validation_set(incorrect_path, "incorrect")
	
	x_test = x_test / 255 # normalize
	y_test_label_hot = to_categorical(y_test_label)

	print(x_test.shape) # (379, 116, 80, 3)
	print(y_test_label_hot.shape) # (379, 1) -> (379, 2)

	# Load CNN trained model
	model = load_model("ASR.h5")
	prediction = model.predict_classes(x_test)
	#print("Predict: ", prediction)
	score = model.evaluate(x_test, y_test_label_hot, verbose=0)
	# Output result
	print('\nTest loss:', score[0])
	print('Test accuracy:', score[1], end="\n\n")

	# show confusion matrix
	print(pd.crosstab(y_test_label, prediction, rownames=['label'], colnames=['predict']))

	print('\nSound Validation has Done!')


def add_img_data_into_validation_set(file_or_path, label):
	global x_test, y_test_label

	file_list = []
	if os.path.isdir(file_or_path):
		file_list = [f for f in os.listdir(file_or_path) if os.path.isfile(file_or_path+f)]
		input_path = file_or_path
	else:
		file_num = 1
		file_list.append(file_or_path)
		# parse file path
		path_idx = file.find('/', 2)
		if path_idx > 0:
			while path_idx >= 0:
				pre_idx = path_idx
				path_idx = file.find('/', path_idx+1)
			input_path = file[:pre_idx+1]

	file_num = len(file_list)

	fig = plt.figure(dpi=my_dpi, figsize=(4,6), frameon=False)

	for i, file in enumerate(file_list):
		f = input_path+file
		if file.split('.')[1] != 'wav':
			continue
		sound = AudioSegment.from_file(f)
		if len(sound) == 200:
			# create spectrogram (wave to STFT)
			y, sr = librosa.load(f, sr=20480)
			stft_data = librosa.stft(y)
			Xdb1 = librosa.amplitude_to_db(abs(stft_data))
			librosa.display.specshow(Xdb1)
			fig.savefig(input_path+"test.png", dpi=my_dpi, bbox_inches='tight')
			plt.clf()

			# Load Image data, shape = (116,80,3)
			if file_num > 1:
				if len(y_test_label) == 0:
					x_test = np.array(Image.open(input_path+"test.png").convert('RGB'))
					x_test = np.expand_dims(x_test, axis=0)
					y_test_label = np.zeros(x_test.shape[0])
					y_test_label[0] = label_dict[input_label]
				else:
					data = np.array(Image.open(input_path+"test.png").convert('RGB'))
					data = np.expand_dims(data, axis=0)
					x_test = np.vstack((x_test, data))
					y_test_label = np.append(y_test_label, np.full(data.shape[0], fill_value=label_dict[label]))
			else:
				x_test = np.array(Image.open(input_path+"test.png").convert('RGB'))
				x_test = np.expand_dims(x_test, axis=0)
				y_test_label = np.zeros(x_test.shape[0])
				y_test_label[0] = label_dict[input_label]

		else:
			print("This is not standard frame (not 64ms)!\n")
	
	if file_num > 1:
		assert x_test.shape[0] == len(y_test_label)


def sensor_Data_Handler(Topic, jsonData):
	if Topic == "Home/Force":
		Force_Data_Handler(jsonData)
