#se connecte au réseau Ethernet et connecte un webrepl et au serveur et met à l'heure l'esp32

import webrepl
import network
import machine
import time
import ubinascii
import gc
import ntpchu
import publisher
from config_IP import * 
from local_config import * 
from os import uname

gc.collect()

#démarrage webrepl 
webrepl.start()

#configuration du LAN (Ethernet) 
def do_connect():
    lan_power = machine.Pin(12, machine.Pin.OUT)
    lan_power.value(1)
    lan = network.LAN(mdc = machine.Pin(23), \
                      mdio = machine.Pin(18), \
                      phy_type = network.PHY_LAN8720, \
                      phy_addr = 0, \
                      clock_mode = network.ETH_CLOCK_GPIO17_OUT)
    lan.active(1)

    sta_if = network.LAN(network.STA_IF)
    sta_if.active(True)
    sta_if.ifconfig((IP_ESP32, MASK_ESP32, GW_ESP32, DNS_ESP32))  #tuple (ip, subnet, gateway, dns)
    time.sleep(2)
    #print('LAN config: ',lan.ifconfig())
    #print(' MAC : ', ubinascii.hexlify(network.LAN().config('mac'),':').decode())
    
 
do_connect()

#connection au serveur 
OK = True
while OK:
    try: 
        publisher.connection_server()
        OK = False
    except:
        #print("connection au serveur...")
        time.sleep(1)


#mise à l'heure de l'ESP32 
ntpchu.settime()