import machine
import time 
import ubinascii
import publisher
from machine import UART 
from machine import Timer

#trames à recevoir et à envoyer lors de l'init
ICC = b'\x1bQ6C'    #initialize communication 
ECHO = b'\x01Q52\r' #reponse de l'esp32 
ID_INCUB = b"\x01R5700'Babyleo TN500'01.06:06.00A5"   #id incub du 30 
ID_ESP   = b'\x01R53\r' #id vide car on ne connait pas celui de esp32 
ASK_ID = b'\x1bR6D'     #demande de s'id

#variables de trames pour les demandes à l'incub (data, setting,...) 
SET=b'\x1B'     #Demande 
DAT=b'\x24'     #Données mesurées 
LAL=b'\x25'     #Low Alarm Limit 
HAL=b'\x26'     #High Alarm Limit 
ALR=b'\x27'     #Alarme 
ALR_2=b'\x2E'   #Alarme
STG=b'\x29'     #device setting 
TXT=b'\x2A'     #Texte

data  = b" "
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
                #print("attente d'une trame")
                time.sleep(0.5)
        else: 
            #print("delay d'attente pour l'initialisation depassee")
            line = b" "
    return line

#communication avec l'incubateur 
boucle = True
INITIALISATION = False 
def init_demarrage(data): 
    global boucle, INITIALISATION 
    boucle = True 
    while boucle: 
        data = data.split(b"\r")[0]     #premiere valeur de la liste créée en enlevant le \r de la trame recue 
        if data == ICC:                 #si on a recu la demande de communication de l'incub 
            uart1.write(ECHO)           #renvoi la meme trame
            time.sleep(0.1)
            data = reception_rs232()          
            data = data.split(b"\r")[0]
            if data == ASK_ID: 
                uart1.write(ID_ESP) 
                time.sleep(0.1)
                uart1.write(ASK_ID + b'\r')
                time.sleep(0.1)
                data = reception_rs232() 
                data = data.split(b"\r")[0]
                if data == ID_INCUB: 
                    INITIALISATION = True   #init faite
                    boucle = False          #on sort de la boucle while
                    time.sleep(0.5)
                else: 
                    time.sleep(0.5) 
                    data = reception_rs232()
            else:
                time.sleep(0.5) 
                data = reception_rs232()
        else: 
            time.sleep(0.5) 
            data = reception_rs232()


#calcul du checksum (somme des données)
def set_checksum(stream):
    return stream+"{:2X}\r".format(sum(stream))[-3:]

        
#envoi les données recues vers le serveur 
def envoi_serveur(data): 
    now = time.localtime()
    date = "{}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(now[0], now[1], now[2], now[3], now[4], now[5])       #bon format de la date 
    publisher.publication(publisher.TOPIC, ubinascii.hexlify(machine.unique_id()) + "|" + date + "|" + data)    #trame complete 
    time.sleep(0.1)


#notre main
time.sleep(5)
print("Début")
data = reception_rs232()
if data != b" ":    #b" " = quand le temps a été dépassé (15sec) 
    init_demarrage(data)   
if INITIALISATION == True:  
    while True:
        uart1.write(set_checksum(SET + DAT))    #demande des données 
        data = reception_rs232()
        data = data.split(b'\r')[0]
        if data == ICC:         #demande de communication 
            init_demarrage(data)
        else: 
            envoi_serveur(data)
            time.sleep(0.5)
        time.sleep(0.5)

