#instance/config.example.py


SECRET_KEY = 'tu_clave_secreta'
#SQLALCHEMY_DATABASE_URI = 'mysql://user:password@host/db' # requiere mysqlclient
SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/database.db'  
SQLALCHEMY_TRACK_MODIFICATIONS = False


#SEND_FILE_MAX_AGE_DEFAULT = 0

#app.config['MAIL_SERVER'] = 'localhost'
#app.config['MAIL_PORT'] = 8025  # Puerto SMTP de Mailhog
#app.config['MAIL_USE_TLS'] = False
#app.config['MAIL_USE_SSL'] = False
#app.config['MAIL_USERNAME'] = None
#app.config['MAIL_PASSWORD'] = None


COLOR_PRIMARY = "#ffffff"
COLOR_SECONDARY = "#000000"
COLOR_TERTIARY= "#0066cc"
WEB_NAME = "FLASKAPP"
LOGO_URL = "logo.png"

# Colores corporativos
CORPORATE_COLORS = {
    'primary': '#007bff',   # Azul
    'secondary': '#6c757d', # Gris
    'success': '#28a745',   # Verde
    'info': '#17a2b8',      # Azul claro
    'warning': '#ffc107',   # Amarillo
    'danger': '#dc3545',    # Rojo
    'light': '#f8f9fa',     # Gris claro
    'dark': '#343a40'       # Negro
}
