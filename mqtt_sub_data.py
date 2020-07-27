#!/usr/bin/python3
import paho.mqtt.client as mqtt
import save_data_to_DB

# MQTT Settings 
MQTT_broker = "140.117.189.242"
MQTT_port = 1883
Keep_Alive_Interval = 45
MQTT_topic = "Home/Force"

# Subscribe to all Sensors for the Topic
def on_connect(mosq, obj, rc):
	mqttc.subscribe(MQTT_topic, 0)

# Save Data into DB Table
def on_message(mosq, obj, msg):
	# This is the Master Call for saving MQTT Data into DB
	# refer to "save_data_to_DB.py" "sensor_Data_Handler" function
	print("MQTT Data Received...")
	print("MQTT Topic: " + msg.topic)
	print("Data: " + msg.payload)
	sensor_Data_Handler(msg.topic, msg.payload)

def on_subscribe(mosq, obj, mid, granted_qos):
    pass

mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

#mqttc.username_pw_set(user, password)

# Connect
mqttc.connect(MQTT_broker, int(MQTT_port), int(Keep_Alive_Interval))
print("MQTT connect!")

# Continue the network loop
mqttc.loop_forever()
