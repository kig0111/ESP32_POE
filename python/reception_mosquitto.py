#recoit et analyse la tram reçu 

import datetime
import random
import envoi_bdd
import analyse_donnees 
import paho.mqtt.client as mqtt
from pathlib import Path
from datetime import datetime
import re 

# vérification de l' existence de la BDD sinon, on la crée

database = 'C:/Users/drbstag/Desktop/BDD/rea_V3.db'
sql_create_donnees_table = """ CREATE TABLE IF NOT EXISTS donnees (
                                    id integer PRIMARY KEY,
                                    unique_id text NOT NULL,
                                    timestamp date,
                                    T_centr text,
                                    humidite text,
                                    t_air text,
                                    rwp text,
                                    d_skin text,
                                    lum text,
                                    NL text,
                                    CHP text,
                                    W_date text
                                ); """

'''sql_create_autre_table = """CREATE TABLE IF NOT EXISTS autre (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                divers integer,
                                project_id integer NOT NULL,
                                date text NOT NULL,
                                FOREIGN KEY (donnees_id) REFERENCES donnees (id)
                            );""" '''

if Path(database).is_file():
    print("Le fichier existe, on l'utilise.")
else:
    print("Le fichier n'existe pas, on le crée.")
    conn = envoi_bdd.create_connection(database)
    envoi_bdd.create_table(conn, sql_create_donnees_table)
    conn.commit()
conn = envoi_bdd.create_connection(database)
cursor = conn.cursor()


SERVEUR = "B2003880"
msg = {'topic':"test_topic", 'payload':"", 'qos':0, 'retain':False}
       
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")
    client.subscribe("test_topic")  #récupération des données du serveur "test_topic"
    client.subscribe("test_romu")

i = 0 
res = ""
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global res
    global i
    print(msg.topic+" "+str(msg.payload)) 
    res = str(msg.payload).split("|")    #a chaque | on divise les caracteres 
    res_unique_id = res[0]
    res_date =  res[1]
    rand = random.randrange(1000, 9999)
    res_data = res[2] + str(rand)

    debut = ''
    while debut != '66': 
        global i
        debut = res_data[i:i+2] 
        i = i+1
    
    print("i = ",i)
    i = i - 1


    #PST = res_data[(2+i):(6+i)].strip()   #peripheral skin temperature     #ON NE RECOIT PAS CETTE DONNEE 
    CST = res_data[(2+i):(6+i)].strip()   #central skin temperature
    HUMIDITE = res_data[(8+i):(12+i)].strip()
    T_AIR = res_data[(14+i):(17+i)].strip()
    RWP = res_data[(20+i):(24+i)].strip()   #radiant warmer power 
    DELTA_SKIN = res_data[(26+i):(30+i)].strip()
    LUMIERE = res_data[(32+i):(36+i)].strip()
    NL = res_data[(38+i):(42+i)].strip()    #noise level
    CHP = res_data[(44+i):(48+i)].strip()
    WEIGHT_DATE = res_data[(50+i):(54+i)].strip()

    print("ID        :", res_unique_id )
    print("TIMESTAMP :", res_date)
    print("DATA      :", res_data)
    print("CST       :", CST)
    print("HUMIDITE  :", HUMIDITE)
    print("TEMP AIR  :", T_AIR)
    print("RWP       :", RWP)
    print("DELTA SKIN  :", DELTA_SKIN)
    print("NIV LUM   :", LUMIERE)
    print("NOISE     :", NL)
    print("CHP       :", CHP)
    print("WEIGHT DATE  :", WEIGHT_DATE)

    sqlite_insert_query = """INSERT INTO donnees (unique_id, timestamp, T_centr, humidite, t_air, rwp, d_skin, lum, NL, CHP, w_date)  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    valeurs = (res_unique_id, res_date, CST, HUMIDITE, T_AIR, RWP, DELTA_SKIN, LUMIERE, NL, CHP, WEIGHT_DATE)   #la trame 

    print("valeurs :: ",valeurs)

    count = cursor.execute(sqlite_insert_query, valeurs)
    conn.commit()

 
client = mqtt.Client()
client.on_connect = on_connect 
client.on_message = on_message 
#print("......",type(msg.payload))


client.connect(SERVEUR, 1883, 60)   #port 1883

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()