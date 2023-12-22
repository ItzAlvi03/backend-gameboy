#region Libraries imports
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
#endregion

#region settings
app = Flask(__name__)
CORS(app)

db_path = './mysite/usuarios.db'
connection = sqlite3.connect(db_path)
#endregion

#region API Endpoints

#   SUMMARY: Endpoint to get insert users to usuarios.db
#   RETURN: response 200(succsefully insert into usuarios.db) or response 500(cannot insert into usuarios.db)
#   POST /insertarUsuario
#   VALUES: data(user info)
@app.route('/insertarUsuario', methods=['POST'])
def insertar_usuario():
    data = request.json
    correo = data['correo']
    nombre = data['nombre']
    contrasena = data['contraseña']

    try:
        cursor = connection.cursor()
        query = 'INSERT INTO usuarios (correo, nombre, contraseña) VALUES (?, ?, ?)'
        cursor.execute(query, (correo, nombre, contrasena))
        connection.commit()
        return jsonify({'mensaje': 'Usuario insertado correctamente'}), 200
    except Exception as e:
        print(f'Error al insertar usuario: {e}')
        return jsonify({'mensaje': 'Error al insertar usuario'}), 500


#   SUMMARY: Endpoint to see if exists users in usuarios.db
#   RETURN: response 200(with the user or empty) or response 500
#   POST /comprobarUsuario
#   VALUES: data(user info)
@app.route('/comprobarUsuario', methods=['POST'])
def comprobar_usuario():
    data = request.json
    nombre = data['nombre']

    try:
        cursor = connection.cursor()
        query = 'SELECT * FROM usuarios WHERE nombre = ?'
        cursor.execute(query, (nombre,))
        result = cursor.fetchall()
        return jsonify(usuario=result), 200
    except Exception as e:
        print(f'Error al buscar usuario: {e}')
        return jsonify({'mensaje': 'Error al buscar usuario'}), 500

#   SUMMARY: Endpoint to see if exists users in usuarios.db
#   RETURN: response 200(with the user or empty) or response 500
#   POST /comprobarLogIn
#   VALUES: data(user info)
@app.route('/comprobarLogIn', methods=['POST'])
def comprobar_log_in():
    data = request.json
    nombre = data['nombre']
    contrasenia = data['contraseña']

    try:
        cursor = connection.cursor()
        query = 'SELECT * FROM usuarios WHERE nombre = ? AND contraseña = ?'
        cursor.execute(query, (nombre, contrasenia))
        result = cursor.fetchone()
        return jsonify(usuario=result), 200
    except Exception as e:
        print(f'Error al buscar usuario: {e}')
        return jsonify({'mensaje': 'Error al buscar usuario'}), 500

#method setting cors
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

#endregion

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        connection.close()
