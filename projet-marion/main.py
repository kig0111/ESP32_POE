#fonction principale de l'ESP32 

import machine
import time 
import ubinascii
import publisher
from machine import UART 
from machine import Timer


ICC = b'\x1bQ6C'    #initialize communication 
ECHO = b'\x01Q52\r' #reponse de l'esp32 
ID_INCUB = b"\x01R5700'Babyleo TN500'01.06:06.00A5"   #id incub du 30 
ID_ESP   = b'\x01R53\r' #id vide car on ne connait pas celui de esp32 
ASK_ID = b'\x1bR6D'     #demande de s'id


SET=b'\x1B'     #Demande 
DAT=b'\x24'     #Données mesurées 
LAL=b'\x25'     #Low Alarm Limit 
HAL=b'\x26'     #High Alarm Limit 
ALR=b'\x27'     #Alarme 
ALR_2=b'\x2E'   #Alarme
STG=b'\x29'     #device setting 
TXT=b'\x2A'     #Texte

data  = b""
line = b" "

#paramètrage du port série (RS232)
uart1 = UART(2,baudrate=38400,bits=8,parity=1,stop=1,tx=4,rx=36)

#lecture sur port série rs232
def reception_rs232() :
    delay_attente = time.time() + 15    #15 secondes : delay d'attente pour recevoir une donnee de l'incub 
    global line 
    line = uart1.read()
    while line == None: 
        if time.time() < delay_attente:     
            try:
                line = uart1.readline()  # copie d’une ligne entiere jusqu’à \r 
            except:
                print("attente d'une trame")
                time.sleep(0.5)
        else: 
            print("delay d'attente pour l'initialisation depassee")
            line = b" "
    #print("uart : ",line)
    return line

#communication avec l'incubateur 
boucle = True
INITIALISATION = False 
def init_demarrage(data): 
    print("debut init demarrage")
    global boucle, INITIALISATION 
    boucle = True 
    while boucle: 
        data = data.split(b"\r")[0]             #premiere valeur de la liste créée en enlevant le \r  
        print("recu 1 : ",data)
        #print("reponse 1 : ",data)
        if data == ICC:                         #si on a recu la 1ere trame de communication de l'incub 
            #print("reponse 1 : ",data)
            uart1.write(ECHO)           #renvoi la meme trame
            print("donnee 1 envoyee : ",ECHO)
            time.sleep(0.1)
            #uart1.write(ASK_ID + b'\r')
            #print("donnee 2 envoyee : ",ASK_ID + b'\r')
            data = reception_rs232()          
            data = data.split(b"\r")[0]
            print("recu 2 : ",data)
            if data == ASK_ID: 
                #print("reponse 2 : ",data)
                uart1.write(ID_ESP) 
                print("donnee 2 envoyee : ",ID_ESP) 
                time.sleep(0.1)
                uart1.write(ASK_ID + b'\r')
                print("donnee 3 envoyee : ",ASK_ID) 
                time.sleep(0.1)
                data = reception_rs232() 
                data = data.split(b"\r")[0]
                print("recu 3 : ",data) 
                if data == ID_INCUB: 
                    print("recu 3 : ",data) 
                    print("fini !!!!!!!")
                    INITIALISATION = True   #init faite
                    boucle = False
                    time.sleep(0.5)
                else: 
                    time.sleep(0.5) 
                    print("aucune/mauvaise donnee")
                    data = reception_rs232()
            else:
                time.sleep(0.5) 
                print("aucune/mauvaise donnee")
                data = reception_rs232()
        else: 
            time.sleep(0.5) 
            print("aucune/mauvaise donnee")
            data = reception_rs232()
    print("fini")


#calcul du checksum (somme des données)
def set_checksum(stream):
    return stream+"{:2X}\r".format(sum(stream))[-3:]

#verifie la trame : envoi sur le serveur les donnees ou recommence la comm avec incub 
"""def verif(data):
    print("apres premiere com : ",data)
    data1 = data.split(b'\r')[0]
    data2 = data.split(b'\r')[1]
    print("apres split : ",data)
    if data1 == ICC:
        print("réinitialisation (incub redemande l'init)")
        init_demarrage(data) 
    elif data2 == ICC: 
        print("réinitialisation (incub redemande l'init)")
        init_demarrage(data) 
    elif data1 == ASK_ID_TO_ESP: 
        uart1.write(ID_ESP)
    elif data2 == ASK_ID_TO_ESP:
        uart1.write(ID_ESP)
    elif data1 == ECHO: 
        uart1.write(ASK_ID_TO_INCUB)
    elif data2 == ECHO:
        uart1.write(ASK_ID_TO_INCUB)
    else: """
        
        
def envoi_serveur(data): 
    now = time.localtime()
    date = "{}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(now[0], now[1], now[2], now[3], now[4], now[5])       #bon format de la date 
    #publisher.publication(TOPIC, ubinascii.hexlify(machine.unique_id()) + "|" + date + "|" + "$6530.86631.66C 18 6D33.36E   0C2 0.8E4 176EC  53F1   4F3 101C3")
    publisher.publication(publisher.TOPIC, ubinascii.hexlify(machine.unique_id()) + "|" + date + "|" + data)
    time.sleep(0.1)


#envoi les demandes de donnees 
"""def sent_data(): 
    while True: 
        #uart1.write(set_checksum(SET + DAT) + set_checksum(SET + LAL) + set_checksum(SET + HAL) + set_checksum(SET + ALR) + set_checksum(SET + ALR_2) + set_checksum(SET + STG) + set_checksum(SET + TXT))    #demande de donnees 
        uart1.write(set_checksum(SET + DAT)) 
        data = reception_rs232()
        verif(data)
        time.sleep(0.5)
        uart1.write(set_checksum(SET + LAL))   
        data = reception_rs232()
        data = data.split(b"\r")[0]
        verif(data)
        time.sleep(0.5)
        uart1.write(set_checksum(SET + HAL))
        data = reception_rs232()
        data = data.split(b"\r")[0]
        verif(data)
        time.sleep(0.5)
        uart1.write(set_checksum(SET + ALR))
        data = reception_rs232()
        data = data.split(b"\r")[0]
        verif(data)
        time.sleep(0.5)
        uart1.write(set_checksum(SET + ALR_2))  
        data = reception_rs232()
        data = data.split(b"\r")[0]
        verif(data)
        time.sleep(0.5)
        uart1.write(set_checksum(SET + STG))
        data = reception_rs232()
        data = data.split(b"\r")[0]
        verif(data)
        time.sleep(0.5)
        uart1.write(set_checksum(SET + TXT))
        data = reception_rs232()
        data = data.split(b"\r")[0]
        verif(data)
        time.sleep(0.5)"""
        
  

#notre main
#while True: 
time.sleep(5)
print("Début")
data = reception_rs232()
if data != b" ": 
    init_demarrage(data)   
if INITIALISATION == True:  
    print("INITIALISATION TRUE")
    #uart1.write(set_checksum(SET + DAT)) 
    #sent_data() 
    while True:
        uart1.write(set_checksum(SET + DAT)) 
        data = reception_rs232()
        data = data.split(b'\r')[0]
        print("trame recue ::: ", data)
        if data == ICC: 
            init_demarrage(data)
        else: 
            envoi_serveur(data)
            time.sleep(0.5)
        time.sleep(0.5)


#_thread.start_new_thread(reception_rs232, ())


#demande des données à l'appareil 
"""def keep_awake(timer):
    uart1.write(set_checksum(SET+DAT))

#boucle au démarage (demandes/réponses)
def fast_start():
    uart1.write(set_checksum(SET+ICC))
    uart1.write(set_checksum(SET+ID))
    uart1.write(set_checksum(GET+ICC))
    uart1.write(set_checksum(GET+ID+WHO))
    uart1.write(set_checksum(SET+ID))
    uart1.write(set_checksum(GET+ICC))
    uart1.write(set_checksum(GET+ID+WHO))

#active les fonctions de récupération des données dans la pile 
def activate():
    timer0 = Timer(0)
    timer0.init(period = 2000, mode = Timer.PERIODIC, callback = wask)    #Timer.init(*, mode=Timer.PERIODIC, freq=- 1, period=- 1, callback=None)
    timer1 = Timer(1)
    timer1.init(period = 100, mode = Timer.PERIODIC, callback = push)
    timer2 = Timer(2)
    timer2.init(period = 1000, mode = Timer.PERIODIC, callback = socks)"""
