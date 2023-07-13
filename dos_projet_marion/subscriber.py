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


import time
from umqtt.simple import MQTTClient
import ubinascii
import machine 

#mqtt_server = 'REPLACE_WITH_YOUR_MQTT_BROKER_IP'
#EXAMPLE IP ADDRESS
MQTT_BROKER = '10.83.102.24'
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = 'test_topic'
#topic_pub = b'hello'


# Ping the MQTT broker since we are not publishing any message
last_ping = time.time()
ping_interval = 60

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    print((topic, msg))


def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()
    
def main():
    mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, keepalive=60)
    mqttClient.set_callback(sub_cb)
    mqttClient.connect()
    mqttClient.subscribe(TOPIC)
    print("En attente... MQTT : " + MQTT_BROKER)
    while True:
        if False:
            # Blocking wait for message
            mqttClient.wait_msg()
        else:
            # Non-blocking wait for message
            mqttClient.check_msg()
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
            global last_ping
            if (time.time() - last_ping) >= ping_interval:
                mqttClient.ping()
                last_ping = time.time()
                now = time.localtime()
                print("Pinging MQTT Broker, last ping :: ")
            time.sleep(1)     
    print("Disconnecting...")
    mqttClient.disconnect()


if __name__ == "__main__":
    try:
        main()
    except OSError as e:
        print("Error: " + str(e))
        reset()




"""last_message = 0
message_interval = 5
counter = 0

print('Coucou')
print(client_id) 

def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'test_topic' and msg == b'received':
        print('ESP received hello message')


def main():
    mqttClient = MQTTClient(client_id, mqtt_server, keepalive=60)
    mqttClient.set_callback(sub_cb)
    mqttClient.connect()
    mqttClient.subscribe(TOPIC)
    print(f"Connected to MQTT  Broker :: {mqtt_server}, and waiting for callback function to be called!")
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


def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    print('essai de connexion')
    client.connect()
    print('connecte')
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

while True:
    try:
        client.check_msg()
        if (time.time() - last_message) > message_interval:
            msg = b'Hello #%d' % counter
            client.publish(topic_pub, msg)
            last_message = time.time()
            counter += 1
    except OSError as e:
        restart_and_reconnect()"""