#!/bin/bash
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

echo "${green}Mise à jour des paquets${reset}"

sudo apt-get update

echo "${green}Installation des dépendances python${reset}"

sudo apt-get install git cron python3 python3-pip python3-setuptools python3-numpy python3-dev -y

echo "${green}Clone du repository SHM${reset}"
sudo mkdir /home/SHM
cd /home/SHM
rm -rf SHM-Client
sudo git clone https://github.com/MinePlugins/SHM-Client.git

echo "${green}Ajout au crontab reboot${reset}"
sudo chmod +x /home/SHM/SHM-Client/start.sh
line="@reboot ./home/SHM/SHM-Client/start.sh"
(crontab -l; echo "$line" ) | crontab -
(crontab -l; echo "$line" ) | crontab -

echo "${green}Installation des paquet python${reset}"


sudo pip3 install requests
sudo pip3 install hashlib
sudo pip3 install flask
sudo pip3 install psutil
sudo pip3 install requests

echo "${green}Lancement du script${reset}"
echo "${green} Ecoute sur l'ip :"
sudo hostname -I | cut -d' ' -f1
echo "${reset}"

cd /home/SHM/SHM-Client/hyperviseur-client/
sudo python3 hyperviseur.py

echo "${green}FIN${reset}"