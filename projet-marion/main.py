#fonction principale de l'ESP32 

import machine
import time 
import ubinascii
import _thread 
import publisher
from machine import UART 
from machine import Timer


ICC = b'\x1bQ6C'  #initialize communication 
ECHO = b'\x01Q52'
ID_INCUB = b"\x01R5700'Babyleo TN500'01.06:06.00A5"         #id incub du 30 
ASK_ID_TO_ESP = b'\x1bR6D'
ID_ESP = b'\x01\x52\x30\x31\x27\x50\x43\x20\x4D\x65\x64\x69\x62\x75\x73\x20\x43\x6F\x72\x65\x20\x41\x67\x65\x6E\x74\x27\x30\x31\x2E\x30\x31\x3A\x30\x34\x2E\x30\x30\x42\x39\x0D'
ASK_ID_TO_INCUB = b'\x1B\x52\x36\x44'   


SET=b'\x1B'     #Demande 
GET=b'\x01'     #Réponse 
IC=b'\x51'     #initialisation communication 
ID=b'\x52'      #? 
DAT=b'\x24'     #Données mesurées 
LAL=b'\x25'     #Low Alarm Limit 
HAL=b'\x26'     #High Alarm Limit 
ALR=b'\x27'     #Alarme 
ALR_2=b'\x2E'   #Alarme
STG=b'\x29'     #device setting 
TXT=b'\x2A'     #Texte


TOPIC = 'test_topic'

data  = b""
line = b" "

#paramètrage du port série (RS232)
uart1 = UART(2,baudrate=38400,bits=8,parity=1,stop=1,tx=4,rx=36)

#lecture sur port série rs232
def reception_rs232() :
    delay_attente = time.time() + 15    #15 secondes : delay d'attente pour recevoir une donnee de l'incub 
    global line, fin
    fin = True
    line = uart1.readline()
    while line == None: 
        if time.time() < delay_attente:     
            try:
                line = uart1.readline()  # copie d’une ligne entiere jusqu’à \r 
                #line = line[:-1]
            except:
                #print("attente d'une trame")
                time.sleep(0.01)
        else: 
            print("delay d'attente pour l'initialisation depassee")
            line = b" "
    #print("uart : ",line)
    return line

#communication avec l'incubateur 
boucle = True
INITIALISATION = False 
def init_demarrage(data): 
    print("init")
    global boucle, INITIALISATION 
    boucle = True 
    while boucle: 
        data = data.split(b"\r")[0]             #premiere valeur de la liste créée en enlevant le \r  
        print("uart : ",data, ICC)
        if data == ICC:                         #si on a recu la 1ere trame de communication de l'incub 
            uart1.write(data + b'\r')           #renvoi la meme trame
            print("etape 1 faite")
            data = reception_rs232()            #doit recevoir l'echo 
            data = data.split(b"\r")[0]
            print("uart : ",data)
            if data == ECHO: 
                uart1.write(ASK_ID_TO_INCUB + b'\r')    #envoi une demande d'identification 
                print("etape 2 faite")
                #time.sleep(0.5)
                data = reception_rs232()        #doit recevoir l'id de l'incub
                """try: 
                    data1, data2 = data.split(b"\r")
                except:
                    data1 = data.split(b"\r")
                    data2 = b" """
                data1 = data.split(b"\r")[0]
                data2 = data.split(b"\r")[1]
                print("uart : ",data1)
                print("uart : ",data2)
                if data1 == ID_INCUB: 
                    print("etape 3 faite")
                    if data2 == ASK_ID_TO_ESP: 
                        print("etape 4 faite")
                        uart1.write(ID_ESP)     #esp envoi son id 
                        INITIALISATION = True   #init faite
                        boucle = False
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
        else: 
            time.sleep(0.5) 
            print("aucune/mauvaise donnee")
            data = reception_rs232()
    print("fini")


#calcul du checksum (somme des données)
def set_checksum(stream):
    return stream+"{:2X}\r".format(sum(stream))[-3:]

def verif(data):
    print(data)
    if data != ICC: 
        now = time.localtime()
        date = "{}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(now[0], now[1], now[2], now[3], now[4], now[5])       #bon format de la date 
        #publisher.publication(TOPIC, ubinascii.hexlify(machine.unique_id()) + "|" + date + "|" + "$6530.86631.66C 18 6D33.36E   0C2 0.8E4 176EC  53F1   4F3 101C3")
        publisher.publication(TOPIC, ubinascii.hexlify(machine.unique_id()) + "|" + date + "|" + data)
        time.sleep(0.1)
        print("trame envoyee")
    elif data == ASK_ID_TO_ESP: 
        uart1.write(ID_ESP)
    else: 
        print("réinitialisation (incub redemande l'init)")
        init_demarrage(data)


#envoi des données au serveur 
def sent_data(): 
    while True: 
        uart1.write(set_checksum(SET + DAT))    #demande de donnees 
        data = reception_rs232()
        verif(data)
        """uart1.write(set_checksum(SET + LAL))   
        data = reception_rs232()
        data = data.split(b"\r")[0]
        verif(data)
        uart1.write(set_checksum(SET + HAL))
        data = reception_rs232()
        data = data.split(b"\r")[0]
        verif(data)
        uart1.write(set_checksum(SET + ALR))
        data = reception_rs232()
        data = data.split(b"\r")[0]
        verif(data)
        uart1.write(set_checksum(SET + ALR_2))  
        data = reception_rs232()
        data = data.split(b"\r")[0]
        verif(data)
        uart1.write(set_checksum(SET + STG))
        data = reception_rs232()
        data = data.split(b"\r")[0]
        verif(data)
        uart1.write(set_checksum(SET + TXT))
        data = reception_rs232()
        data = data.split(b"\r")[0]
        verif(data)"""
        


#enoie sur serveur des données toutes les 10sec 
while True: 
    time.sleep(5)
    print("Début")
    data = reception_rs232()
    print("attente de la trame de comunic de l'incub")
    if data != b" ": 
        init_demarrage(data)   
    if INITIALISATION == True:  
        sent_data() 


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
