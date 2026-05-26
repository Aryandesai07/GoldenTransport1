import sqlite3

conn = sqlite3.connect("golden_transport.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM admin")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()