#region Libraries imports
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
from PIL import Image
import os
import base64
from YoloV8.model import predict
from YoloV8.contour import contorno
from YoloV8.boxes import box
#endregion

#region settings
app = Flask(__name__)
CORS(app)

db_path = './Databases/usuarios.db'
#endregion
#region ENCRYPT METHODS

def hash_password(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    hash_password = key.hex()
    salt = salt.hex()
    return hash_password, salt

def verify_password(stored_hash, stored_salt, provided_password):
    salt = bytes.fromhex(stored_salt)
    key = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return key.hex() == stored_hash

#endregion
#region API Endpoints

#   SUMMARY: Endpoint to check if server is OK
#   RETURN: Hello message
#   GET /hello
@app.route('/hello', methods=['GET'])
def hello():
    return "Hello"

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
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        query = 'INSERT INTO usuarios (correo, nombre, contraseña) VALUES (?, ?, ?)'
        cursor.execute(query, (correo, nombre, contrasena))
        connection.commit()
        return jsonify({'mensaje': 'Usuario insertado correctamente'}), 200
    except Exception as e:
        print(f'Error al insertar usuario: {e}')
        return jsonify({'mensaje': 'Error al insertar usuario'}), 500


#   SUMMARY: Endpoint to see if exists users in usuarios.db
#   RETURN: response 200(existe o no existe) or response 500
#   POST /comprobarUsuario
#   VALUES: data(user info)
@app.route('/comprobarUsuario', methods=['POST'])
def comprobar_usuario():
    data = request.json
    nombre = data['nombre']

    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        query = 'SELECT * FROM usuarios WHERE nombre = ?'
        cursor.execute(query, (nombre,))
        result = cursor.fetchall()
        if result:
            return jsonify('existe'), 200
        else:
            return jsonify('no existe'), 200

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
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        query = 'SELECT * FROM usuarios WHERE nombre = ? AND contraseña = ?'
        cursor.execute(query, (nombre, contrasenia))
        result = cursor.fetchone()
        return jsonify(usuario=result), 200
    except Exception as e:
        print(f'Error al buscar usuario: {e}')
        return jsonify({'mensaje': 'Error al buscar usuario'}), 500

@app.route('/predict', methods=['POST'])
def predecir():
    try:
        img = request.files['img']
        img.save('./YoloV8/temp.jpg')
    except Exception as e:
        return str("La imagen es corrupta"), 500
    
    prediction_value = float(request.form.get('predict'))
    absolute_path = os.path.abspath("./YoloV8/temp.jpg")
    result = predict(absolute_path, prediction_value)
    return jsonify({'result': result}), 200


@app.route('/contorno', methods=['POST'])
def contour():
    try:
        img = request.files.get('img')
        if img is None:
            raise ValueError("'img' key not found in the request data")

        img.save('./YoloV8/temp.jpg')

        result_data_base64 = request.form.get('result')
        if result_data_base64 is None:
            raise ValueError("'result' key not found in the request data")

        # Decodificar result_data_base64 antes de escribir en el archivo
        result_data = base64.b64decode(result_data_base64)
        result_file_path = './YoloV8/result.pkl'

        with open(result_file_path, 'wb') as result_file:
            result_file.write(result_data)

        # Procesar la imagen y la lista result
        annotated_img_path = contorno('./YoloV8/temp.jpg', result_file_path)

        return jsonify({'annotated_img': annotated_img_path}), 200
    except Exception as e:
        return str(e), 400

@app.route('/boxes', methods=['POST'])
def boxes():
    try:
        img = request.files.get('img')
        if img is None:
            raise ValueError("'img' key not found in the request data")

        img.save('./YoloV8/temp.jpg')

        result_data_base64 = request.form.get('result')
        if result_data_base64 is None:
            raise ValueError("'result' key not found in the request data")

        # Decodificar result_data_base64 antes de escribir en el archivo
        result_data = base64.b64decode(result_data_base64)
        result_file_path = './YoloV8/result.pkl'

        with open(result_file_path, 'wb') as result_file:
            result_file.write(result_data)

        # Procesar la imagen y la lista result
        annotated_img_path = box('./YoloV8/temp.jpg', result_file_path)
        return jsonify({'annotated_img': annotated_img_path}), 200

    except Exception as e:
        return str(e), 400

#method setting cors
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

#endregion

# SERVER START URL => https://alviapi.ddns.net/api
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)