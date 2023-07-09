# A fast way to get data from TN500
SET=b'\x1B'
GET=b'\x01'
ICC=b'\x51'
ID=b'\x52'
WHO=b'\x30\x31\x36\x31\x27\x50\x43\x20\x4D\x65\x64\x69\x62\x75\x73\x20\x43\x6F\x72\x65\x20\x41\x67\x65\x6E\x74\x27\x30\x32\x2E\x31\x30\x3A\x31\x30\x2E\x30\x30'
NOP=b'\x30'
DAT=b'\x24'
RTC=b'\x28'
CLS=b'\x55'
ALR=b'\x27'
STG=b'\x29'
TXT=b'\x2A'
TND=b'\x6C'

import time
import struct
import os

from machine import UART as Serial 
serial=Serial(2, baudrate=38400, bits=8, parity=0, stop=1, tx=4, rx=36)
# fast startup

#def push(timer):
#    global FIFO
#    if serial.any():
#        FIFO = serial.read()
#    return time.ticks_us()

def fast_start():
    serial.write(set_checksum(SET+ICC))
#     time.sleep_ms(5)
    serial.write(set_checksum(SET+ID))
#     time.sleep_ms(5)
    serial.write(set_checksum(GET+ICC))
#     time.sleep_ms(5)
    serial.write(set_checksum(GET+ID+WHO))
#     time.sleep_ms(5)
    serial.write(set_checksum(SET+ID))
#     time.sleep_ms(5)
    serial.write(set_checksum(GET+ICC))
#     time.sleep_ms(5)
    serial.write(set_checksum(GET+ID+WHO))
    
global FIFO
global pFIFO
def push(timer):
    global FIFO
    global pFIFO
    if serial.any():
        FIFO = serial.read(), time.ticks_us()/1000000
        pFIFO = struct.pack('>l',struct.calcsize('d') + struct.calcsize('l') + len(FIFO[0])) + struct.pack('>d',FIFO[1]) + struct.pack('>l',len(FIFO[0])) + struct.pack(str(len(FIFO[0]))+'s',FIFO[0])
#         pFIFO = (struct.pack('>l',struct.calcsize('d')+struct.calcsize('l')
#                              + len(FIFO[0])
#                              + struct.pack('>d',FIFO[1]) + struct.pack('>l',len(FIFO[0]))
#                              + struct.pack(str(len(FIFO[0]))+'s',FIFO[0])))               
                             
def pack(FIFO):
    global pFIFO
    pFIFO = struct.pack('>l',struct.calcsize('d') + struct.calcsize('l') + len(FIFO[0])) + struct.pack('>d',FIFO[1]) + struct.pack('>l',len(FIFO[0])) + struct.pack(str(len(FIFO[0]))+'s',FIFO[0])
#     pFIFO = (struct.pack('>l',struct.calcsize('d')+struct.calcsize('l')
#                          + len(FIFO[0])
#                          + struct.pack('>d',FIFO[1]) + struct.pack('>l',len(FIFO[0]))
#                          + struct.pack(str(len(FIFO[0]))+'s',FIFO[0])))

def set_checksum(stream):
    return stream+"{:2X}\r".format(sum(stream))[-3:]

def keep_awake(timer):
    serial.write(set_checksum(SET+DAT))
    
what=0
def ask(timer):
    W=DAT, TXT, DAT, ALR, DAT, STG
    global what
    what = what +1
    if what > 5:
        what = 0        
    serial.write(set_checksum(SET+W[what]))
    return what

global W
W = DAT, DAT, DAT, DAT, STG
def wask(timer):
    global what
    what = what +1
    if what > len(W)-1:
        what = 0        
    serial.write(set_checksum(SET+W[what]))
    return what

import struct

#def wrt(timer):
    #with open('str.txt','a') as file:
#        t = (struct.pack('>l',struct.calcsize('d')+struct.calcsize('l')+len(FIFO[0]))
#            + struct.pack('>d',FIFO[1]) + struct.pack('>l',len(FIFO[0])) + struct.pack(str(len(FIFO[0]))+'s',FIFO[0]))
#        file.write(t)

import os
import struct
from machine import Timer

file=open('str.txt','a')
file.seek(0)

def wrt(timer):
    FIFO=L.FIFO
    t = (struct.pack('>l',struct.calcsize('d')+struct.calcsize('l')
                     +len(FIFO[0]))
         + struct.pack('>d',FIFO[1]) + struct.pack('>l',len(FIFO[0]))
         + struct.pack(str(len(FIFO[0]))+'s',FIFO[0]))
    file.write(t)

import usocket #as socket
import socket
def connect(addrss):
    global SOCK
    addr_info = socket.getaddrinfo(addrss,5000)
    addr = addr_info[0][-1]
    SOCK=usocket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SOCK.connect(addr)

def socks(timer):
    global SOCK
    try :
        SOCK.send(pFIFO)
    except  OSError as e:
        print('.')

from machine import Timer
def activate():
    timer0 = Timer(0)
    timer0.init(period = 1000, mode = Timer.PERIODIC, callback = wask)
    timer1 = Timer(1)
    timer1.init(period = 100, mode = Timer.PERIODIC, callback = push)
    timer2 = Timer(2)
    timer2.init(period = 1000, mode = Timer.PERIODIC, callback = socks)

#for i in range(3):
# serial.write(set_checksum(SET+ICC))
# time.sleep_ms(200)
# serial.write(set_checksum(SET+ID))
# time.sleep_ms(200)
# serial.write(set_checksum(GET+ICC))
# time.sleep_ms(200)
# serial.write(set_checksum(GET+ID+WHO))
# time.sleep_ms(200)


# def main():
#     serial.write(set_checksum(SET+ICC))
#     serial.write(set_checksum(SET+ID))
#     serial.write(set_checksum(GET+ICC))
#     serial.write(set_checksum(GET+ID+WHO))

#def fast_start():
#    serial.write(set_checksum(SET+ICC))
#    serial.write(set_checksum(SET+ID))
#    serial.write(set_checksum(GET+ICC))
#    serial.write(set_checksum(GET+ID+WHO))
