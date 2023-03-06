import paho.mqtt.client as mqtt
import pandas as pd
import time

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    if rc==0:
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)

def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

# print log, useful for debugging
def on_log(client, userdata, level, buf):
    print("log: ",buf)

# Create a MQTT client instance
client = mqtt.Client()
client.on_connect = on_connect
subscribe(client)

# Connect to the MQTT broker
broker_address = "broker.emqx.io"
client.username_pw_set("TestUser", "Abc12345")
client_id = "mqttx_947398f1"
client.connect(broker_address, 1883)

client.on_message = on_message
client.on_log = on_log
topic = "BungkapTH/Device1"

client.subscribe(topic)

client.loop_forever()