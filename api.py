#region Libraries imports
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
#endregion

#region settings
app = Flask(__name__)
CORS(app)

db_path = 'usuarios.db'
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
    contraseña = data['contraseña']

    try:
        cursor = connection.cursor()
        query = 'INSERT INTO usuarios (correo, nombre, contraseña) VALUES (?, ?, ?)'
        cursor.execute(query, (correo, nombre, contraseña))
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
    contraseña = data['contraseña']

    try:
        cursor = connection.cursor()
        query = 'SELECT * FROM usuarios WHERE nombre = ?'
        cursor.execute(query, (nombre,))
        result = cursor.fetchall()
        return jsonify(result), 200
    except Exception as e:
        print(f'Error al buscar usuario: {e}')
        return jsonify({'mensaje': 'Error al buscar usuario'}), 500

#endregion

if __name__ == '__main__':
    try:
        app.run(debug=True, port=8000)
    finally:
        connection.close()
