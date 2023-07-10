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
ID_INCUB = b"\x01R5700'Babyleo TN500'04:06.00A3" 
ASK_ID_TO_ESP = b'\x1bR6D'
ID_ESP = b'\x01\x52\x30\x31\x27\x50\x43\x20\x4D\x65\x64\x69\x62\x75\x73\x20\x43\x6F\x72\x65\x20\x41\x67\x65\x6E\x74\x27\x30\x31\x2E\x30\x31\x3A\x30\x34\x2E\x30\x30\x42\x39'
ASK_ID_TO_INCUB = b'\x1B\x52\x36\x44'

TOPIC = 'test_topic'

data  = ""
line = b" "

#paramètrage du port série (RS232)
uart1 = UART(2,baudrate=9600,bits=8,parity=1,stop=1,tx=4,rx=36)

#lecture sur port série rs232
def reception_rs232() :
    delay_attente = time.time() + 15    #15 secondes : delay d'attente pour recevoir une donnee de l'incub 
    global line, fin
    fin = True
    line = uart1.readline()
    while line == None: 
        if time.time() < delay_attente:     
            try:
                line = uart1.readline()  # copie d’une ligne entiere jusqu’à \n 
            except:
                print("attente d'une trame")
                time.sleep(0.2)
        else: 
            print("delay d'attente pour l'initialisation depassee")
            line = b" "
    print("uart : ",line)
    return line

#communication avec l'incubateur 
boucle = True
INITIALISATION = False 
def init_demarrage(data): 
    print("init")
    global boucle, INITIALISATION 
    boucle = True 
    while boucle: 
        if data == ICC:                         #si on a recu la 1ere trame de communication de l'incub 
            uart1.write(data)                   #renvoi la meme trame
            print("etape 1 faite")
            data = reception_rs232()            #doit recevoir l'echo 
            if data == ECHO: 
                uart1.write(ASK_ID_TO_INCUB)    #envoi une demande d'identification 
                print("etape 2 faite")
                #time.sleep(0.5)
                data = reception_rs232()        #doit recevoir l'id de l'incub
                if data == ID_INCUB: 
                    time.sleep(0.5) 
                    print("etape 3 faite")
                    data = reception_rs232()    #doit recevoir l'incu qui demande a l'esp de s'id
                    if data == ASK_ID_TO_ESP: 
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
        time.sleep(0.5)
    print("fini")


#envoi des données au serveur 
def sent_data(): 
    data = reception_rs232()
    while True: 
        if data != ICC: 
            now = time.localtime()
            date = "{}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(now[0], now[1], now[2], now[3], now[4], now[5])       #bon format de la date 
            publisher.publication(TOPIC, ubinascii.hexlify(machine.unique_id()) + "|" + date + "|" + "$6530.86631.66C 18 6D33.36E   0C2 0.8E4 176EC  53F1   4F3 101C3")
            print("trame envoyee")
        else: 
            print("réinitialisation (incub redemande l'init)")
            init_demarrage(data)


#enoie sur serveur des données toutes les 10sec 
while True: 
    data = reception_rs232()
    print("attente de la trame de com de l'incb")
    if data != b" ": 
        #data_byte = bytes(data, 'utf-8')
        #print("data : ", data)
        init_demarrage(data)   
    if INITIALISATION == True:  
        sent_data() 
    #time.sleep(1)  #envoie les données sur le serveur  
    #time.sleep(5)


#_thread.start_new_thread(reception_rs232, ())

#calcul du checksum (somme des données)
def set_checksum(stream):
    return stream+"{:2X}\r".format(sum(stream))[-3:]

#demande des données à l'appareil 
def keep_awake(timer):
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
    timer2.init(period = 1000, mode = Timer.PERIODIC, callback = socks)
