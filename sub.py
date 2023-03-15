import paho.mqtt.client as mqtt
#import pandas as pd
import time
import connectDB
import random




client_id = str(random.randint(1000, 9999))
db = connectDB.connectDB(client_id)
db.createTable()
BigDic = {}
SmallDic = {}

#use to create ui and recive input from user
def ui(client_id):
    print("This is server "+client_id)
    print("1) print all data")
    print("2) print only humidity")
    print("3) print only temperature")
    print("4) print only thermalarray")
    print("5) print menu again")
    print("6) clsoe server")

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %s." % rc)
    ui(client_id)


#Merge 2 data then push to database
def pushToDB(key, BackPayload):
    global BigDic
    global db

    if key not in BigDic:
        thermal = str(BackPayload[0]).split("'")    
        pubID = BackPayload[1]
        time = str(BackPayload[2])+ " " + str(BackPayload[3])
        db.insertIntoNotAll(time,thermal[1],pubID)
    else:
        frontPayload = BigDic.pop(key)
        dummytime = str(frontPayload[0]).split("'")
        time = dummytime[1]+ " " + frontPayload[1]
        hum = frontPayload[2]
        temp = frontPayload[3]
        hum = float(hum)
        temp = float(temp)
        dummyTher = str(BackPayload[0]).split("'")   
        thermal = frontPayload[4] + dummyTher[1]
        pubID = BackPayload[1]
        db.insertIntoAll(time,hum,temp,thermal,pubID)

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    global db
    global BigDic
    global SmallDic
    
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    key = msg.topic
    x = str(msg.payload).split()
    if (len(str(msg.payload)) >= 245):
        if key not in BigDic:
            BigDic[key] = list()
        BigDic[key].extend(x)
    else:
        pushToDB(key, x)

# Create a MQTT client instancepip3 install pandas
client = mqtt.Client(client_id)
client.on_connect = on_connect
# Connect to the MQTT broker
broker_address = "127.0.0.1"
#client.username_pw_set("ss", "Abc12345")
client.connect(broker_address, 1883)
client.on_message = on_message
# Publish each row of the datca
topic = "#"
client.subscribe(topic)
# Disconnect from the MQTT broker
#client.loop_start()
client.loop_start()
exit = 0
while(exit == 0):

    x = input()
    if (x == "6"):
        exit = 1
        break
    elif (x == "1"):
        db.printAllData()
    elif (x == "2"):
        db.printOnlyHum()
    elif (x == "3"):
        db.printOnlyTemp()
    elif (x == "4"):
        db.printOnlyThe()
    elif (x == "5"):
        ui(client_id)

client.loop_stop()