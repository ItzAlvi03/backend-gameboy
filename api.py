from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

db_path = 'usuarios.db'

@app.route('/insertarUsuario', methods=['POST'])
def insertar_usuario():
    data = request.json
    correo = data['correo']
    nombre = data['nombre']
    contraseña = data['contraseña']

    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        query = 'INSERT INTO usuarios (correo, nombre, contraseña) VALUES (?, ?, ?)'
        cursor.execute(query, (correo, nombre, contraseña))
        connection.commit()
        return jsonify({'mensaje': 'Usuario insertado correctamente'}), 200
    except Exception as e:
        print(f'Error al insertar usuario: {e}')
        return jsonify({'mensaje': 'Error al insertar usuario'}), 500
    finally:
        connection.close()

@app.route('/comprobarUsuario', methods=['POST'])
def comprobar_usuario():
    data = request.json
    nombre = data['nombre']
    contraseña = data['contraseña']

    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        query = 'SELECT * FROM usuarios WHERE nombre = ?'
        cursor.execute(query, (nombre,))
        result = cursor.fetchall()
        return jsonify(result), 200
    except Exception as e:
        print(f'Error al buscar usuario: {e}')
        return jsonify({'mensaje': 'Error al buscar usuario'}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
