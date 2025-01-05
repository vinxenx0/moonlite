# Usar una imagen base de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos
COPY requirements.txt requirements.txt
COPY requirements.mysql.txt requirements.mysql.txt

# Instalar las dependencias necesarias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -r requirements.mysql.txt

# Copiar todo el código de la aplicación
COPY . .

# Crear el entorno virtual y activarlo (opcional, ya que Docker ya proporciona un entorno aislado)
RUN python3 -m venv .venv

# Activar el entorno virtual
RUN . .venv/bin/activate

# Exponer el puerto que la aplicación usará
EXPOSE 8080

# Establecer la variable de entorno para usar producción (de ser necesario)
ENV FLASK_ENV=production

# Ejecutar la aplicación usando Gunicorn (el servidor de producción)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "run:app"]

# Comando para ejecutar la aplicación Flask en development
#CMD ["/bin/bash", "-c", "source .venv/bin/activate && python3 run.py"]
