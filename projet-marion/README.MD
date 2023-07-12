Projet NEONAT : stocker les données de l'incubateur dans une base de données 

Les données de l'incubateur sont envoyées via le port série RS232 vers l'ESP32. L'ESP32 envoie alors une trame sur un serveur mqtt, voici la trame envoyée : ID_ESP32 | horodatage | données reçues. Un webrepl est également mis en place pour gérer à distance l'ESP32 si besoin. 

Programmes utilisés : 
    - main.py : fonction princiale qui va appeler toutes les autres (démarrage avec la communication entre l'incub et l'esp32, lecture des données sur rs232 + envoi de a trame sur le serveur mqtt)
    - boot.py : se connecte à l'Ethernet et commence un webrepl, appel de la fonction ntpchu, connection au serveur (appel de publisher.py)
    - publisher.py : envoie un message au serveur mqtt 
    - ntpchu.py : mise à l'heure de l'ESP32 pour l'horodatage correct 
    - webrepl_cfg.py : mot de passe du webrepl 

La mise à l'heure de l'ESP32 peut mettre du temps, c'est normal

La base de donnée est créée en python dans C:\Users\drbstag\Desktop\python 