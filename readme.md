## kochkorAd
ad project for kochkor
sudo apt-get install python3 python-dev python3-dev
sudo apt-get install python python3-dev python3-setuptools python3-pip
sudo apt-get install libjpeg8-dev # for pillow
sudo apt-get install postgresql

CREATE ROLE intellect_user WITH LOGIN PASSWORD 'root';
create database "kochkor" with owner "intellect_user" ENCODING 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';
sudo pip3 install virtualenv
virtualenv --no-site-packages --distribute -p /usr/bin/python3.6 venv