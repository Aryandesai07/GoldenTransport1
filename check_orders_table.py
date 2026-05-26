import sqlite3

conn = sqlite3.connect("golden_transport.db")
cursor = conn.cursor()

# Show all columns in the orders table
cursor.execute("PRAGMA table_info(orders);")
columns = cursor.fetchall()

for col in columns:
    print(col)

conn.close()