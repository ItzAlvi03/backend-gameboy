import sqlite3

db_path = './Databases/usuarios.db'
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

query = '''
CREATE TABLE IF NOT EXISTS usuarios (
    nombre VARCHAR(18) PRIMARY KEY,
    correo VARCHAR(30),
    contraseña VARCHAR(16)
);
'''
cursor.execute(query)

connection.commit()
connection.close()
print("end")