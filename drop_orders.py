import sqlite3

conn = sqlite3.connect("golden_transport.db")
cursor = conn.cursor()

# Drop the orders table
cursor.execute("DROP TABLE IF EXISTS orders")

conn.commit()
conn.close()

print("Orders table deleted successfully.")