import sqlite3

db_path = './Databases/usuarios.db'
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

query = '''INSERT INTO usuarios (correo, nombre, contraseña)
           SELECT ?, ?, ? 
           WHERE NOT EXISTS (
               SELECT 1 
               FROM usuarios 
               WHERE correo = ? AND nombre = ? AND contraseña = ?
           )'''
cursor.execute(query, ('admin@admin.com', 'admin', '010203', 'admin@admin.com', 'admin', '010203'))

connection.commit()
connection.close()
print("end")