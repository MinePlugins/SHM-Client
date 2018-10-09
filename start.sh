#!/bin/bash

echo "${green}Lancement du script${reset}"

echo "${green} Ecoute sur l'ip :"
hostname -I | cut -d' ' -f1
echo "${reset}"

cd /home/SHM/SHM-Client/hyperviseur-client

sudo python3 hyperviseur.py


echo "${green}FIN${reset}"