sudo apt-get install wget curl software-properties-common dirmngr gnupg2 pkg-config build-essential libaspell-dev python3-dev python3-venv libapache2-mod-wsgi-py3 git redis libmariadb-dev

wget https://dev.mysql.com/get/mysql-apt-config_0.8.30-1_all.deb
sudo dpkg -i mysql-apt-config_0.8.30-1_all.deb

sudo apt update
sudo apt install mysql-client mysql-community-server mysql-server -y
sudo apt-get install mariadb-server mariadb-client -y

git clone -b log-user-activity https://github.com/vinxenx0/moonlite

cd moonline
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -r requirements.mysql.txt