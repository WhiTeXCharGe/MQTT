import paho.mqtt.client as mqtt
#import pandas as pd
import time
import connectDB
import random

payload1 = "1"
payload2 = "2"
payload = "3"
i = 0

client_id = str(random.randint(1000, 9999))
db = connectDB.connectDB(client_id)
db.createTable()

#use to create ui and recive input from user
def ui(client_id):
    print("This is server "+client_id)
    print("1) print all data")
    print("4) clsoe server")

#use to seperate to time hum, temp, thermal
def seperateWord(payload):
    string = payload.split()
    dsenTime = string[0] + " " +string[1]
    d2senTime = dsenTime.split("'")
    senTime = d2senTime[1]
    hum = string[2]
    temp = string[3]
    thermal = string[4]
    #change to float
    hum = float(hum)
    temp = float(temp)

    return senTime, hum, temp, thermal

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %s." % rc)

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    global payload1
    global payload
    global i
    global payload2
    global db
   # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if i == 0:
        payload1 = str(msg.payload)
        i = i+1
    else:
        dpayload2 = str(msg.payload)
        payload2 = dpayload2.split("'")
        payload = payload1 + payload2[1]
        senTime,hum,temp,thermal = seperateWord(payload)
        db.insertInto(senTime,hum,temp,thermal)
        i = 0

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
exit = 0
while(exit == 0):
    x = input()
    client.on_message = on_message
    ui(client_id)
    if (x == "4"):
        exit = 1
        break

client.loop_stop()