import codecs

fichier = open("C:/Users/drbstag/Desktop/dos_projet_marion/data_incubateur.txt", "r")
fichierW = open("C:/Users/drbstag/Desktop/dos_projet_marion/data_incubateur.bin", "wb")
res = fichier.read()
print("res   " + res)

res = codecs.decode(res, "hex")
print(str(res,'utf-8'))
print("ascii :   " + str(res))

fichierW.write(res)

fichier.close() 
fichierW.close() 
