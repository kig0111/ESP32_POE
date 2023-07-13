#
# This file is part of the BIOM_AID distribution (https://bitbucket.org/kig13/dem/).
# Copyright (c) 2023 Romuald Kliglich, Marion Normand, Loic Degrugilliers.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#


from machine import UART 

#uart1 = UART(2,baudrate=9600,bits=8,parity=0,stop=1,tx=4,rx=36)

"""while True: 
    cpt = 0
    data = [] 
    data[cpt] = uart1.read() 
    while data[cpt] != 0x0D: 
        cpt = cpt + 1
        data[cpt] = uart1.read() 
        print(data[cpt]) 
        cpt + 1 
    print("FIN")"""


from machine import UART
import time
import _thread

ser = UART(2,baudrate=38400,bits=8,parity=0,stop=1,tx=4,rx=36)
def reception_rs232():
    line = str()
    #char = b' '
    CR = b'\n'  #retour a la ligne 
    vide = None
    nbre = 1
    #char = ser.read()
    while nbre: 
        #print(type(CR))
        char = ser.read() # copie d’une ligne entiere jusqu’a \n dans « line »
        #print(type(line))
        #if char == vide:   #char == CR | 
        while char == vide:
            char = ser.read()
        #print(type(char))
        #print(char)
        #else: 
        if char == CR:
            line = ''
            continue
        line = line + char.decode()
        print(line)

while True: 
    reception_rs232()
    time.sleep(0.02)

"""
#création et démarrage des thread 
thread1 = threading.Thread(target=envoi_rs232(ser)) 
thread2 = threading.Thread(target=reception_rs232(ser))
thread1.start()
thread2.start()
#attends que thread soint excécutés 
thread1.join()
thread2.join()"""


#_thread.start_new_thread(envoi_rs232) 
#_thread.start_new_thread(reception_rs232) 

