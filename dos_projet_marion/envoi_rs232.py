#tests python

import serial 
import time

ser = serial.Serial(port="COM3", baudrate=38400, timeout=1, parity="O", stopbits=1) 
#ser.open()

#MSG = [1B,51,36,43]  #b'12340D'
#MSG = bytes(MSG)

#MSG = "1B 51 36 43"
#MSG = [255]
#MSG = bytearray(MSG)

MSG = b'$6530.86631.66C 18 6D33.36E   0C2 0.8E4 176EC  55F1   5F3 101C6'

time.sleep(1)
serial.write(MSG)

"""def reception_rs232():
    global line
    line = ser.readline()
    while line == None: 
        try:
            line = ser.readline()  # copie d’une ligne entiere jusqu’à \n 
        except:
            print("attente d'une trame")
            time.sleep(0.2)
    return line"""


#while True: 
"""ser.write(b'\x1B\x51\x36\x43')
print("envoi 1")
line = reception_rs232()
print("donnees recues :: ",line)
if line == b'\x1bQ6C': 
    ser.write(b'\x01\x51\x35\x32')
    print("envoi 2")
    line = reception_rs232()
    print("donnees recues :: ",line)
    if line == b'\x1bR6D': 
        ser.write(b'\x01\x52\x35\x37\x30\x30\x27\x42\x61\x62\x79\x6C\x65\x6F\x20\x54\x4E\x35\x30\x30\x27\x30\x34\x3A\x30\x36\x2E\x30\x30\x41\x33')
        print("envoi 3")
        time.sleep(1)
        ser.write(b'\x1B\x52\x36\x44')
        print("envoi 4")
        line = reception_rs232()
        print("donnees recues :: ",line)
        if line == b"\x01R01'PC Medibus Core Agent'01.06:06.00B9": 
            print("initialisation terminee")"""
#time.sleep(2)
#ser.write(b'1B 51 36 43')
"""if line == b'\x1bQ6C': 
    ser.write(b'\x01\x52\x35\x37\x30\x30\x27\x42\x61\x62\x79\x6C\x65\x6F\x20\x54\x4E\x35\x30\x30\x27\x30\x34\x3A\x30\x36\x2E\x30\x30\x41\x33')
    print("envoye")
    if line == b'\x1bQ6C': 
        ser.read()
        ser.write(b'\x1B\x52\x36\x44')
        #ser.read()"""
#ser.write(0x1B + 0x02)
#ser.write('1B 51 36 43 0D'.encode('ascii'))
#time.sleep(1)
#ser.write('01 51 35 32 0D'.encode('ascii'))
#time.sleep(1)
#ser.write('1B 52 36 44 0D'.encode('ascii'))
#print(ser.readline())
#ser.write(bytearray.fromhex(MSG))
#print("envoye")