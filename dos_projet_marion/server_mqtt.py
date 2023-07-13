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


#gestion du serveur MQTT
import time
import machine 
import ubinascii
from umqtt.simple import MQTTClient


# Default MQTT MQTT_BROKER to connect to
MQTT_BROKER = "10.83.102.24"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = 'test_topic'

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    print((topic, msg))

co = True
def main():
    mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, keepalive=60)
    mqttClient.set_callback(sub_cb)
    while co:
        global co
        try: 
            print(mqttClient.connect())
            co = False
        except: 
            print("connection...")
            time.sleep(0.5)
    mqttClient.subscribe(TOPIC)
    print("Connected to MQTT  Broker :: , and waiting for callback function to be called!")
    while True:
        if True:
            # Blocking wait for message
            mqttClient.wait_msg()
        else:
            # Non-blocking wait for message
            mqttClient.check_msg()
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
            time.sleep(1)
    mqttClient.disconnect()


if __name__ == "__main__":
    main()




"""import time
import ubinascii
from umqtt.simple import MQTTClient

# Default MQTT MQTT_BROKER to connect to
MQTT_BROKER = "10.83.102.24"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = 'test_topic'

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    print((topic, msg))

co = True
def main():
    mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, keepalive=60)
    mqttClient.set_callback(sub_cb)
    while co:
        global co
        try: 
            mqttClient.connect()
            co = False
        except: 
            print("connection...")
            time.sleep(0.5)
    mqttClient.subscribe(TOPIC)
    print("Connected to MQTT  Broker :: , and waiting for callback function to be called!")
    while True:
        if True:
            # Blocking wait for message
            mqttClient.wait_msg()
        else:
            # Non-blocking wait for message
            mqttClient.check_msg()
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
            time.sleep(1)

    mqttClient.disconnect()


if __name__ == "__main__":
    main()"""