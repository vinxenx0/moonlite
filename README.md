
Requisitos

# apt install python3-venv libapache2-mod-wsgi-py3 git redis  libmariadb-dev 
# pip install email_validator sqlalchemy_utils flask_wtf flask_login mysqlclient 
# pip install flask_migrate flask_mail whois ipwhois  pyasn requests
# pip install aspell-python-py3 langid textstat PyJWT
# pip install python-whois


Lanzar
# pip install gunicorn
# gunicorn -w 4 --bind unix:/tmp/gunicorn.sock wsgi:app
# gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app

Proxy

# sudo a2enmod proxy
# sudo a2enmod proxy_http

# install



