import time 

def traitement(donnee):
    print("donnees : ",donnee)
    for i in range(60):
        if donnee[i:i+2] == '6C': 
            print("ok, humidité") 
        elif donnee[i:i+2] == '6D': 
            print("ok, T°C air") 
        elif donnee[i:i+2] == '6E': 
            print("ok, RWP") 
        elif donnee[i:i+2] == 'C2': 
            print("ok, delta skin") 
        elif donnee[i:i+2] == 'E4': 
            print("ok, niveau lumière") 
        elif donnee[i:i+2] == 'EC': 
            print("ok, NL") 
        elif donnee[i:i+2] == 'F1': 
            print("ok, CHP") 
        elif donnee[i:i+2] == 'F3': 
            print("ok, weight date") 
        else:
            print("rien") 