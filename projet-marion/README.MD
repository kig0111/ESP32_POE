Projet NEONAT : stocker les données de l'incubateur dans une base d
                                                      <--------------- b'\x1bR6D' : demande d'identfication 

Le micropython inséré dans l'ESP32 est la version V1.14, le lien pour le télécharger est dans le fichier esptool_doc.txt avec la marche à suivre pour l'injecter dans l'ESP32. 

Les données de l'incubateur sont envoyées via le port série RS232 vers l'ESP32. Au démarrage, l'incubateur veut communiqer avec l'ESP32 ; c'est la phase d'initialisation, elle est nécéssaire pour pouvoir récupérer les données de l'incubateur. Par l 'ESP32 envoie alors la trame qu'il recoit sur un serveur mqtt, voici la trame envoyée : ID_ESP32 | horodatage | données reçues. Un webrepl est également mis en place pour gérer à distance l'ESP32 si besoin. Le serveur analyse et stocke les données sur une base de données grâce à un programme en Python. 

Programmes utilisés : 
    - main.py : initialisation de la communication entre l'incub et l'esp32, lecture des données sur rs232 + envoi de la trame complète sur le serveur mqtt 
    - boot.py : se connecte à l'Ethernet et commence un webrepl, appel de la fonction ntpchu, connection au serveur (appel de publisher.py)
    - publisher.py : envoie un message précis au serveur mqtt 
    - ntpchu.py : mise à l'heure de l'ESP32 pour l'horodatage correct (date + heure)

La mise à l'heure de l'ESP32 peut mettre du temps, c'est normal, la connection au serveur aussi

La base de donnée est créée en python. Elle est d'abord analysée, puis envoyée sur la base de donnée. Les programmes se trouvent dans le dossier Python : envoi_bdd.py et reception_mosquitto.py sont utilisés et analyse_donnees est un programme de test. 

                                                    INITIALISATION COMMUNICATION : 
                                                ESP32                            TN500
                                                      <---------------  b'x1bQ6C' : ICC : 1ere commande envoyée par l'incubateur pour démarrer la communication 
b'\x01Q52' : l'ESP32 lui répond qu'il est prêt à communiquer ---------------------->
                                                      <--------------- b'\x1bR6D' : demande d'identfication 
l'appareil s'id, si on ne connait pas l'id  : b'\x01R53'     ---------------------->
                   demande d'identification : b'\x1bR6D'     ---------------------->
                                                      <--------------- l'incubateur s'identfie
                                                      
Lorsque l'incubateur envoie un NOP : b'\x1b04B cela signifie que l'incubateur attend, il envoie cette trame pour préciser que ca fait 2 secondes qu'il n'a rien reçu. 