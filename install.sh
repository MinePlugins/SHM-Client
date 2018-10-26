#!/bin/bash
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`
_end=100
function ProgressBar {
# Process data
	let _progress=(${1}*100/${2}*100)/100
	let _done=(${_progress}*4)/10
	let _left=40-$_done
# Build progressbar string lengths
	_done=$(printf "%${_done}s")
	_left=$(printf "%${_left}s")

# 1.2 Build progressbar strings and print the ProgressBar line
# 1.2.1 Output example:
# 1.2.1.1 Progress : [########################################] 100%
printf "\rProgress : [${_done// /#}${_left// /-}] ${_progress}%%"

}

echo "${green}Mise à jour des paquets${reset}"

sudo apt-get update > /dev/null
ProgressBar 10 ${_end}
echo "${green}Installation des dépendances python${reset}"

sudo apt-get install git cron python3 python3-pip python3-setuptools python3-numpy python3-dev -y > /dev/null
ProgressBar 20 ${_end}
echo "${green}Clone du repository SHM${reset}"
sudo mkdir /home/SHM
cd /home/SHM
rm -rf SHM-Client
ProgressBar 25 ${_end}
sudo git clone https://github.com/MinePlugins/SHM-Client.git > /dev/null
ProgressBar 40 ${_end}
echo "${green}Ajout au crontab reboot${reset}"
sudo chmod +x /home/SHM/SHM-Client/start.sh
line="@reboot /home/SHM/SHM-Client/start.sh"
crontab -l | grep -q '@reboot /home/SHM/SHM-Client/start.sh'  && (crontab -l; echo "$line" ) | crontab - || echo "${red}Le cron existe déjà${reset}"
ProgressBar 60 ${_end}

echo "${green}Installation des paquet python${reset}"


sudo pip3 install requests > /dev/null
sudo pip3 install simplejson > /dev/null
sudo pip3 install hashlib > /dev/null
sudo pip3 install flask > /dev/null
sudo pip3 install psutil > /dev/null
sudo pip3 install requests > /dev/null

ProgressBar 90 ${_end}
echo "${green}Lancement du script${reset}"
echo "${green} Ecoute sur l'ip :"
sudo hostname -I | cut -d' ' -f1
echo "${reset}"
ProgressBar 100 ${_end}
cd /home/SHM/SHM-Client/hyperviseur-client/
sudo python3 hyperviseur.py > /dev/null

echo "${green}FIN${reset}"