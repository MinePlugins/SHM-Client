# SHM-Client  :computer:
<a><img src="https://img.shields.io/badge/python-3.x-blue.svg"></a>
<a href="https://github.com/batteurMDR/shm-server/tree/dev" target="_blank"><img src="https://img.shields.io/badge/server-nodejs-brightgreen.svg"></a><br>
Un utilitaire de gestion de machine tel que WIndows / Linux / Mac OSX mais optimisé pour TinkerBoard et Raspberry Pi

# Installation automatique (Linux Only)

Pour installer le coté client il suffit d'éxécuter cette commande en linux :
```bash
curl https://raw.githubusercontent.com/MinePlugins/SHM-Client/master/install.sh | sudo bash
```

# Dépendences  :package:

- curl
- git
- Python 3
  - Requests
  - Flask
  - Psutil
  - Hashlib

# Installation manuelle (Linux Only)

```bash
sudo apt-get update
sudo apt-get install git cron python3 python3-pip python3-setuptools python3-numpy python3-dev -y
mkdir /home/SHM
cd /home/SHM
rm -rf SHM-Client
git clone http://git.estiam.com/quentin.cournut/SHM-Client.git
(crontab -l; echo "@reboot ./home/SHM/SHM-Client/start.sh" ) | crontab -
sudo pip3 install requests
sudo pip3 install hashlib
sudo pip3 install flask
sudo pip3 install psutil
cd /home/SHM/SHM-Client/hyperviseur-client/
python3 hyperviseur.py
```

Puis connectez-vous à l'adresse de votre machine avec le port 5000

# Installation Windows

- Cloner le git
- Installer Python3 et les dépendances
- Lancer le script python

# Configuration

Connectez-vous grâce à l'adresse IP:5000 de la machine [http://localhost:5000](http://localhost:5000) et suivez l'utilitaire d'installation

## Etape 1 (Identifiant)

Le mot de passe doit être d'au moins 8 caractères

![Etape 1](https://raw.githubusercontent.com/MinePlugins/SHM-Client/master/images/install_etape_1.png)

## Etape 2 (Configuration)

Le mot de passe doit être d'au moins 8 caractères

![Etape 2](https://raw.githubusercontent.com/MinePlugins/SHM-Client/master/images/install_etape_2.png)

## Etape 3 (Finalisation)

Cette étapes mets du temps, alors soyez patient, a la fin de cette étapes cliquer sur le bouton vert

![Etape 3](https://raw.githubusercontent.com/MinePlugins/SHM-Client/master/images/install_etape_3.png)

# Les pages

## Status

Page qui renseigne sur l'utilisation de la machine

![Status](https://raw.githubusercontent.com/MinePlugins/SHM-Client/master/images/status.png)

## Log

Page qui renseigne sur les log du panel

![Status](https://raw.githubusercontent.com/MinePlugins/SHM-Client/master/images/log.png)

## Processus

Page qui renseigne sur les processus de la machine
