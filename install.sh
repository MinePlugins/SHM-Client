#!/bin/bash
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

echo "${green}Mise à jour des paquets${reset}"

sudo apt-get update

echo "${green}Installation des dépendances python${reset}"

sudo apt-get install git cron python3 python3-pip python3-setuptools python3-numpy python3-dev -y

echo "${green}Clone du repository SHM${reset}"

cd /home/linaro
rm -rf SHM-Client
git clone http://git.estiam.com/quentin.cournut/SHM-Client.git

echo "${green}Ajout au crontab reboot${reset}"

line="@reboot ./home/linaro/SHM-Client/start.sh"
(crontab -u linaro -l; echo "$line" ) | crontab -u linaro -

echo "${green}Installation des paquet python${reset}"

sudo pip3 install requests
sudo pip3 install hashlib
sudo pip3 install flask
sudo pip3 install psutil
sudo pip3 install requests

echo "${green}Lancement du script${reset}"
echo "${green} Ecoute sur l'ip :"
ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'
echo "${reset}"

cd /home/linaro/SHM-Client/hyperviseur-client/
python3 hyperviseur.py

echo "${green}FIN${reset}"