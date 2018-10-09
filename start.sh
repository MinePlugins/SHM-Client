#!/bin/bash

echo "${green}Lancement du script${reset}"

cd /home/linaro/SHM-Client/hyperviseur-client/
echo "${green} Ecoute sur l'ip :"
hostname -I | cut -d' ' -f1
echo "${reset}"

python3 hyperviseur.py


echo "${green}FIN${reset}"