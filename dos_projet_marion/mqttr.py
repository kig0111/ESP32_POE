import machine
import time
from machine import Pin, PWM
from umqtt.simple import MQTTClient
from time import sleep
import random
import json
import network
#################MQTT###################

def connect():
    username ="pub_client"
    broker =  "10.83.102.24"
    topic = "test_topic"
    Mqtt_CLIENT_ID = "ID9869686687"        # Max. Number is 23 due to MQTT specs
    PASSWORD="%mqtt%"
    client = MQTTClient(client_id=Mqtt_CLIENT_ID, server=broker, port=1883, user=username, password=PASSWORD, keepalive=6000)
    try:
        client.connect()
    except OSError:
        print('Connection failed')

    data = dict()
    data["see"] = 15
    data2=json.dumps(data)#convert it to json   
    print('connection finished')
    client.publish(topic,data2)
    print("Data_Published")
    time.sleep(5)
#print("Sending OFF")
connect()