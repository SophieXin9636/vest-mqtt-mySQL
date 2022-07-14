#!/usr/bin/python3
import paho.mqtt.client as mqtt
from api_handler import *

# MQTT Settings 
MQTT_broker = "192.168.43.30"
Keep_Alive_Interval = 45
MQTT_topic = "Home/Force"

# Subscribe to all Sensors for the Topic
def on_connect(mosq, data, flags, rc):
	#print("Connected with result code: " + str(rc))
	print_dbg("MQTT connect!", DEBUG, 2)
	client.subscribe(MQTT_topic)

# Save Data into DB Table
def on_message(mosq, data, msg):
	# This is the Master Call for saving MQTT Data into DB
	# refer to "save_data_to_DB.py" "sensor_Data_Handler" function
	print_dbg("MQTT Data Received... " + msg.payload.decode(), DEBUG, 3)
	#print("MQTT Topic: " + msg.topic)
	#print("Data: " + msg.payload)
	sensor_Data_Handler(msg.topic, msg.payload.decode())

def on_subscribe(mosq, data, mid, granted_qos):
	pass

client = mqtt.Client()

# Assign event callbacks
client.on_message = on_message
client.on_connect = on_connect
client.on_subscribe = on_subscribe

user = "sophie"
password = "12345"
client.username_pw_set(user, password)

# MQTT Client Connect
client.connect("192.168.43.30", 1883, int(Keep_Alive_Interval))

# Continue the network loop
client.loop_forever()