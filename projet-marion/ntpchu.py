#horodatage de l'ESP32 grâce à l'Ethernet 

import utime
import machine
from local_config import * 

try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct

# The NTP host can be configured at runtime by doing: ntptime.host = 'myhost.org'
host = NTP_CHU    #   IP su serveur 
# host = "ntp.xx.xx
# The NTP socket timeout can be configured at runtime by doing: ntptime.timeout = 2
timeout = 1

# pour notre serveur du CHU, il a fallu essayer d'atteindre le serveur plusieurs fois
# de suite pour avoir un résultat probant. je suppose que c'est dû au protocole UDP...

st = True  #sendto
rf = True  #receptionfrom 

def time_ntp():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while rf:                #obligatoire pour que ca fonctionne 
        global rf, st
        st = True
        s.settimeout(timeout)
        while st:
            try :
                res = s.sendto(NTP_QUERY, addr)
                st = False
                print("sendto")
            except:
                utime.sleep(0.05)
        try: 
            msg = s.recv(48)
            rf = False
        except: 
            utime.sleep(0.05)
    val = struct.unpack("!I", msg[40:44])[0]
    delta = 2*60*60         #heure française
    val = val + delta
    s.close()

    EPOCH_YEAR = utime.gmtime(0)[0]
    if EPOCH_YEAR == 2000:
        NTP_DELTA = 3155673600
    elif EPOCH_YEAR == 1970:
        NTP_DELTA = 2208988800
    else:
        raise Exception("Unsupported epoch: {}".format(EPOCH_YEAR))
    return val - NTP_DELTA


# There's currently no timezone support in MicroPython, and the RTC is set in UTC time.
def settime():
    t = time_ntp()

    tm = utime.gmtime(t)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
    print("date/heure : ", utime.localtime())
