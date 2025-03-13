import sqlite3

db_path = './Databases/usuarios.db'
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

query = 'SELECT * FROM usuarios'
cursor.execute(query)
result = cursor.fetchall()
print(result)

connection.commit()
connection.close()