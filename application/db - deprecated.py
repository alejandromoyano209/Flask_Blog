import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO login_usuario (usuario, password) VALUES (?, ?)",
            ('lucia@lucia.com', 'aaaa'))

cur.execute("INSERT INTO login_usuario (usuario, password) VALUES (?, ?)",
            ('juan@juan.com', 'bbbb'))


connection.commit()
connection.close()
