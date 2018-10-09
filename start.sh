#!/bin/bash

echo "${green}Lancement du script${reset}"

cd /home/linaro/SHM-Client/hyperviseur-client/
echo "${green} Ecoute sur l'ip :"
ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'
echo "${reset}"

python3 hyperviseur.py


echo "${green}FIN${reset}"