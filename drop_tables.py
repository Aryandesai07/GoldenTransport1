import sqlite3

conn = sqlite3.connect("golden_transport.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS reports;")
cursor.execute("DROP TABLE IF EXISTS orders;")

conn.commit()
conn.close()
print("Old tables dropped.")
