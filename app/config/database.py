"""
Configuración de conexiones a bases de datos
"""
from flask_pymongo import PyMongo
import mysql.connector
import os

# Instancia global de MongoDB
mongo = None

def init_mongodb(app):
    """Inicializa la conexión a MongoDB"""
    global mongo
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    mongo = PyMongo(app)
    return mongo

def get_mongodb():
    """Obtiene la instancia de MongoDB"""
    return mongo

def get_mariadb_connection():
    """Crea y retorna una conexión a MariaDB"""
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )
