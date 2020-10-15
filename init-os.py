#! /usr/bin/python python3

import os


# update
os.system('sudo apt update && sudo apt upgrade -y')

os.system('sudo apt install curl make unrar gnome-tweaks wget -y')

# google-chrome
os.system('wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb')
os.system('sudo dpkg -i --force-depends google-chrome-stable_current_amd64.deb')


os.system('sudo apt-get install guake -y')
os.system('sudo apt-get install mc -y')

# shutter
os.system('sudo add-apt-repository ppa:linuxuprising/shutter -y')
os.system('sudo apt-get update')
os.system('sudo apt install shutter -y')
os.system('wget https://launchpad.net/ubuntu/+archive/primary/+files/libgoocanvas-common_1.0.0-1_all.deb')
os.system('wget https://launchpad.net/ubuntu/+archive/primary/+files/libgoocanvas3_1.0.0-1_amd64.deb')
os.system('wget https://launchpad.net/ubuntu/+archive/primary/+files/libgoo-canvas-perl_0.06-2ubuntu3_amd64.deb')
os.system('sudo dpkg -i libgoocanvas-common_1.0.0-1_all.deb')
os.system('sudo dpkg -i libgoocanvas3_1.0.0-1_amd64.deb')
os.system('sudo dpkg -i libgoo-canvas-perl_0.06-2ubuntu3_amd64.deb')
os.system('sudo apt -f install -y')
os.system('sudo snap install shutter')

# git
os.system('sudo apt-get install git -y')
os.system('git config --global user.name "name"(roman)')
os.system('git config --global user.email "email"(romaxa83@ukr.net)') 
os.system('git config --list')

# php
os.system('sudo apt install python-software-properties -y')
os.system('sudo add-apt-repository ppa:ondrej/php')
os.system('sudo apt update')
os.system('sudo apt install php7.4 -y')
os.system('sudo apt install php7.4-cli -y')
os.system('sudo apt install php7.4-xml -y')
os.system('sudo apt install php7.4-common -y')
os.system('sudo apt install php7.4-zip -y')
os.system('sudo apt install php7.4-mysql -y')
os.system('sudo apt install php7.4-fpm -y')
os.system('sudo apt install php7.4-curl -y')
os.system('sudo apt install php7.4-mbstring -y')
os.system('sudo apt install php7.4-json -y')
os.system('sudo apt install php7.4-cgi -y')
os.system('sudo apt install php7.4-gd -y')
os.system('sudo apt install libapache2-mod-php7.4 -y')
os.system('sudo apt install php7.4-xdebug -y')

# db-client
os.system('sudo apt install mysql-client postgresql-client')

# openvpn
os.system('sudo apt update')
os.system('sudo apt install openvpn -y')
os.system('sudo apt-get install network-manager-openvpn -y')
os.system('sudo apt-get install network-manager-openvpn-gnome -y')


# install docker
os.system('curl https://get.docker.com > /tmp/install.sh')
os.system('chmod +x /tmp/install.sh')
os.system('/tmp/install.sh')
os.system('docker version')
os.system('sudo groupadd docker')
os.system('sudo gpasswd -a ${USER} docker')
os.system('sudo service docker restart')

# install docker-compose
os.system('sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose')
os.system('sudo chmod +x /usr/local/bin/docker-compose')
os.system('docker-compose -v')

# install ctop for docker
os.system('sudo wget https://github.com/bcicen/ctop/releases/download/v0.7.2/ctop-0.7.2-linux-amd64 -O /usr/local/bin/ctop')
os.system('sudo chmod +x /usr/local/bin/ctop')

# sublime
os.system('wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -')
os.system('sudo apt-add-repository "deb https://download.sublimetext.com/ apt/stable/"')
os.system('sudo apt install sublime-text -y')


# return_code = subprocess.call("docker -v", shell=True) 
# print(return_code)
# https://overcoder.net/q/3228/%D0%B2%D1%8B%D0%B7%D0%BE%D0%B2-%D0%B2%D0%BD%D0%B5%D1%88%D0%BD%D0%B5%D0%B9-%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B-%D0%B2-python
