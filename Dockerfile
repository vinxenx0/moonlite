FROM python:3.10-slim

# Instalar las dependencias necesarias
RUN apt-get update && apt-get install -y \
    sudo \
    wget \
    curl \
    software-properties-common \
    dirmngr \
    gnupg2 \
    pkg-config \
    build-essential \
    libaspell-dev \
    python3-dev \
    python3-venv \
    libapache2-mod-wsgi-py3 \
    git \
    redis \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar los archivos necesarios
COPY requirements.txt requirements.txt

# Crear un entorno virtual y activarlo
#RUN python3 -m venv /app/.venv

# Instalar las dependencias en el entorno virtual directamente
RUN pip install --upgrade pip
# RUN pip install email_validator sqlalchemy_utils flask_wtf flask_login mysqlclient flask_migrate flask_mail whois ipwhois  pyasn requests aspell-python-py3 langid textstat PyJWT python-whois
RUN pip install -r requirements.txt
#RUN /app/.venv/bin/pip install -r requirements.mysql.txt

# Copiar el código de la aplicación
COPY . .

# Establecer las variables de entorno
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Ejecutar la aplicación usando Gunicorn (el servidor de producción)
# CMD ["gunicorn", "-b", "0.0.0.0:8080", "run:app"]

# Comando para ejecutar la aplicación Flask en development
CMD ["/bin/bash", "-c", "python3 run.py"]
