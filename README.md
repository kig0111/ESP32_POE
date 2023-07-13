## ESP32_POE
data transfert from an ESP32-POE-ISO to a DB over MQTT protocol

# Projet NEONAT : stocker les données de l'incubateur dans une base de données 

Les données de l'incubateur sont envoyées via le port série RS232 vers l'ESP32. Au démarrage, l'incubateur veut communiqer avec l'ESP32 ; c'est la phase d'initialisation, elle est nécéssaire pour pouvoir récupérer les données de l'incubateur. Par l 'ESP32 envoie alors la trame qu'il recoit sur un serveur mqtt, voici la trame envoyée : ID_ESP32 | horodatage | données reçues. Un webrepl est également mis en place pour gérer à distance l'ESP32 si besoin. Le serveur analyse et stocke les données sur une base de données grâce à un programme en Python.

# Détails techniques 

Le micropython inséré dans l'ESP32 est la version V1.14, le lien pour le télécharger est dans le dossier dos_projet_marion, le fichier nommé esptool_doc.txt avec la marche à suivre pour l'injecter dans l'ESP32.
Le logiciel utilisé est Visual Studio Code avec l'extension Pymakr pour écrire en micropython. 

# Dossiers

Tous les programmes en micropython se trouvent dans le dossier "projet-marion", les programmes en python se trouvent dans le dossier "python". Le dossier "dos_projet_marion" contient des programmes de tests, les trames envoyées par l'incubateur, le schéma de l'ESP32-POE-ISO. Enfin, le dossier "BDD" contient la base de données créée avec les trames reçues par l'incubateur. 

# Programmes utilisés

1. Micropython
    - main.py : initialisation de la communication entre l'incub et l'esp32, lecture des données sur rs232 + envoi de la trame complète sur le serveur mqtt - boot.py : se connecte à l'Ethernet et commence un        webrepl, appel de la fonction ntpchu, connection au serveur (appel de publisher.py)
    - publisher.py : envoie un message précis au serveur mqtt
    - ntpchu.py : mise à l'heure de l'ESP32 pour l'horodatage correct (date + heure)
  
2.  Python
    - envoi_bdd.py : créé une base de données 
    - reception_mosquitto.py : analyse les trames du serveur et rempli la base de données 

# Initialisation communication 

1. TN500 :  b'x1bQ6C' : ICC : 1ere commande envoyée par l'incubateur pour démarrer la communication 
2. ESP32 :  b'\x01Q52' : l'ESP32 lui répond qu'il est prêt à communiquer 
3. TN500 :  b'\x1bR6D' : demande d'identfication 
4. ESP32 :  l'appareil s'id, si on ne connait pas l'id : b'\x01R53'
5. ESP32 :  b'\x1bR6D' : demande d'identfication
6. TN500 :  l'incubateur s'identfie

Après cet échange, l'ESP32 peut demander des données spécifiques (T°, humidité, niveau de lumière, paramètrage,...).  

Lorsque l'incubateur envoie un NOP : b'\x1b04B cela signifie que l'incubateur attend, il envoie cette trame pour préciser que ca fait 2 secondes qu'il n'a rien reçu.
