import paho.mqtt.client as mqtt
#import pandas as pd
import time
import random

payload1 = "1"
payload2 = "2"
payload = "3"
i = 0
# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %s." % rc)

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    global payload1
    global payload
    global i
    global payload2
   # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if i == 0:
        payload1 = str(msg.payload)
        i = i+1
    else:
        payload2 = str(msg.payload)
        payload = payload1 + payload2
        print(payload)
        i = 0

# Read the data from the excel file
excel_file = "SampleInput.xlsx"
#data = pd.read_excel(excel_file)

client_id = str(random.randint(1000, 9999))
# Create a MQTT client instancepip3 install pandas
client = mqtt.Client(client_id)
client.on_connect = on_connect

# Connect to the MQTT broker
broker_address = "127.0.0.1"
#client.username_pw_set("ss", "Abc12345")
client.connect(broker_address, 1883)
client.on_message = on_message
# Publish each row of the datca
topic = "BungkapTH/Device"
client.subscribe(topic)
# Disconnect from the MQTT broker
client.loop_start()
while(1):
    client.on_message = on_message
    x = input()
    if (x == "s"):
        break;
client.loop_stop()