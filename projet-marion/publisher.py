#envoie  données sur le serveur 

import time
import ubinascii
import machine
from umqtt.simple import MQTTClient


SERVER = "10.83.102.24"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())  #id de l'ESP32 
TOPIC = 'trame_complete'    #nom du serveur 
username="pub_client"
PASSWORD="%mqtt%"

#reset l'ESP32 
def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()

def sub_cb(TOPIC, MSG):
    print(TOPIC, MSG)

#se connecte au serveur 
def connection_server():
    global CLIENT_ID, SERVER, TOPIC, mqttClient
    mqttClient = MQTTClient(CLIENT_ID, SERVER, user=username, password=PASSWORD, keepalive=60)
    mqttClient.set_callback(sub_cb)
    mqttClient.connect()
    print("Connected to MQTT  Broker :: ", SERVER)

#fonction qu envoie le message 
def publication(TOPIC, MSG): 
    mqttClient.publish(TOPIC, str(MSG).encode())
    print("message envoyé")

#déconnecte le serveur 
def deconnecte():
    mqttClient.disconnect()
    print("mqtt déconnecté")
    
    
if __name__ == "__main__":
    try:
        connection_server()
        publication(TOPIC, "MSG_TEST")
    except OSError as e:
        print("Error: " + str(e))
        reset()