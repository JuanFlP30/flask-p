from flask import Flask, jsonify
from dotenv import load_dotenv
from app.config.database import init_mongodb
from app.routes.mongo_routes import mongo_bp
from app.routes.mysql_routes import mysql_bp

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Inicializar bases de datos
init_mongodb(app)

# Registrar Blueprints (rutas)
app.register_blueprint(mongo_bp)
app.register_blueprint(mysql_bp)

# Rutas principales
@app.route('/')
def index():
    return jsonify({
        'message': 'API funcionando correctamente',
        'status': 'success',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'mongodb': '/mongo/users',
            'mariadb': '/mysql/users'
        }
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
