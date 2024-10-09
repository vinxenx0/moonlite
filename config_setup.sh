#!/bin/bash

# Función para instalar el cliente MySQL
install_mysqlclient() {
    sudo apt-get update
    sudo apt-get install -y libmysqlclient-dev libmariadb-dev
}

create_db() {
        
        # Comprobamos si la base de datos ya existe
        mysql -h "$db_host" -u "$db_user" -p"$db_pwd" -e "USE $db_name" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "La base de datos $db_name ya existe. No es necesario crearla."
        else
            # Creamos la base de datos
            mysql -h "$db_host" -u "$db_user" -p"$db_pwd" -e "CREATE DATABASE $db_name"
            if [ $? -eq 0 ]; then
                echo "La base de datos $db_name se ha creado correctamente."
            else
                echo "Error al crear la base de datos $db_name."
                exit 1
            fi
        fi

        # Ejecutamos el script SQL para crear las tablas
        mysql -h "$db_host" -u "$db_user" -p"$db_pwd" "$db_name" < install/create_tables.sql

        if [ $? -eq 0 ]; then
            echo "Tablas creadas correctamente."
        else
            echo "Error al crear las tablas."
            exit 1
        fi

}

# Función para preguntar al usuario y guardar las respuestas en config.py
ask_and_save_config() {
    echo "Introduce los detalles de configuración de la base de datos:"
    read -p "DB_HOST: " db_host
    read -p "DB_NAME: " db_name
    read -p "DB_USER: " db_user
    read -s -p "DB_PWD: " db_pwd
    echo ""
    read -p "Elige el tipo de base de datos (0 SQLITE / 1 MYSQL): " db_type
    read -p "Introduce la clave secreta: " secret_key

    echo "DB_HOST = '$db_host'" > instance/install.log
    echo "DB_NAME = '$db_name'" >> instance/install.log
    echo "DB_USER = '$db_user'" >> instance/install.log
    echo "DB_PWD = '$db_pwd'" >> instance/install.log
    echo "DB_TYPE = '$db_type'" >> instance/install.log
    echo "SECRET_KEY = '$secret_key'" > instance/config.py


    # añadir app.run(debug=True, port='8000', host='0.0.0.0')
    # añadir SMTP

    #app.config['MAIL_SERVER'] = 'localhost'
    #app.config['MAIL_PORT'] = 8025  # Puerto SMTP de Mailhog
    #app.config['MAIL_USE_TLS'] = False
    #app.config['MAIL_USE_SSL'] = False
    #app.config['MAIL_USERNAME'] = None
    #app.config['MAIL_PASSWORD'] = None

     if [[ "$db_type" == "1" ]]; then
        echo "SQLALCHEMY_DATABASE_URI = 'mysql://$db_user:$db_pwd@$db_host/$db_name'" >> instance/config.py
        install_mysqlclient
        create_db
    else
        echo "SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/database.db'" >> instance/config.py
    fi

    echo "Configuración base de datos en instance/config.py."

    echo "Introduce los colores iniciales"
    read -p "PRIMARIO: " color_primario
    read -p "SECUNDARIO: " color_secundario
    read -p "ENLACES: " color_enlaces
    read -p "SITIO: " nombre_sitio
    read -p "LOGO URL: " logo_url
    echo ""

    echo "COLOR_PRIMARY = '$color_primario'" >> instance/config.py
    echo "COLOR_SECONDARY  = '$color_secundario'" >> instance/config.py
    echo "COLOR_TERTIARY = '$color_enlaces'" >> instance/config.py
    echo "WEB_NAME = '$nombre_sitio'" >> instance/config.py
    echo "LOGO_URL = '$logo_url'" >> instance/config.py


    # Escribe la configuración en config.py
    echo "COLOR_PRIMARY = '$color_primario'" >> instance/install.log
    echo "COLOR_SECONDARY  = '$color_secundario'" >> instance/install.log
    echo "COLOR_TERTIARY = '$color_enlaces'" >> instance/install.log
    echo "WEB_NAME = '$nombre_sitio'" >> instance/install.log
    echo "LOGO_URL = '$logo_url'" >> instance/install.log

    echo "Configuración guardada en instance/config.py."
}

# Comprobar si instance directory existe
if [ ! -d "instance" ]; then
    mkdir instance
fi

# Preguntar al usuario y guardar la configuración
ask_and_save_config
