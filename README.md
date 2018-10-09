# SHM-Client

Un utilitaire de gestion de machine tel que WIndows / Linux / Mac OSX mais optimisé pour TinkerBoard et Raspberry Pi

# Installation automatique

Pour installer le coté client il suffit d'éxécuter cette commande en linux :
```bash
curl https://raw.githubusercontent.com/MinePlugins/SHM-Client/master/install.sh | sudo bash
```

# Dependence

- curl
- git
- Python 3
  - Requests
  - Flask
  - Psutil
  - Hashlib

# Installation manuel

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