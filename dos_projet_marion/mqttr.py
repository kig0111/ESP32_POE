#
# This file is part of the BIOM_AID distribution (https://bitbucket.org/kig13/dem/).
# Copyright (c) 2023 Romuald Kliglich, Marion Normand, Loic Degrugilliers.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#


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