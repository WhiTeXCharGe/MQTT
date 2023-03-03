import paho.mqtt.client as mqtt
import pandas as pd
import time

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    if rc==0:
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: ", mid)

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

# print log, useful for debugging
def on_log(client, userdata, level, buf):
    print("log: ",buf)

# Split a string into a list of strings by byte size
def split_string_by_byte_size(s, byte_size):
    utf8_bytes = s.encode('utf-8')
    return [utf8_bytes[i:i+byte_size] for i in range(0, len(utf8_bytes), byte_size)]


# Read the data from the excel file
excel_file = "SampleInput.xlsx"
data = pd.read_excel(excel_file)

# Create a MQTT client instance
client = mqtt.Client()
client.on_connect = on_connect

# Set the maximum payload size to 250 bytes
max_payload_size = 250

# Connect to the MQTT broker
broker_address = "broker.emqx.io"
client.username_pw_set("TestUser", "Abc12345")
client_id = "mqttx_947398f1"
client.connect(broker_address, 1883)


client.loop_start()

client.on_message = on_message
client.on_publish = on_publish
client.on_log = on_log

# Publish each row of the data
for index, row in data.iterrows():
    payload = f"{row['Time']} {row['Humidity']} {row['Temperature']} {row['ThermalArray']}"
    payload_tmp = payload
    payload_split = split_string_by_byte_size(payload_tmp, max_payload_size)
    topic = "BungkapTH/Device1"
    for i in range(len(payload_split)):
        client.publish(topic, payload_split[i])
        time.sleep(1)

client.loop_stop()

# Disconnect from the MQTT broker
client.disconnect()