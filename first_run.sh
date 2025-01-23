
--- dependencias

sudo apt-get install sudo wget curl software-properties-common dirmngr gnupg2 pkg-config build-essential libaspell-dev python3-dev python3-venv python3-pip libapache2-mod-wsgi-py3 git redis libmariadb-dev

wget https://dev.mysql.com/get/mysql-apt-config_0.8.30-1_all.deb
sudo dpkg -i mysql-apt-config_0.8.30-1_all.deb
a
sudo apt update
sudo apt install mysql-client aspell aspell-es pkg-config libmariadb-dev mysql-community-server mysql-server python3-dev libmysqlclient-dev -y
sudo apt-get install mariadb-server mariadb-client -y

--- creacion del usuario
sudo useradd -m -s /bin/bash -G sudo moonlite

-- crear entorno

git clone https://github.com/vinxenx0/moonlite

cd moonline
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -r requirements.mysql.txt

-- arrancar

python3 run.py