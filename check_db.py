import sqlite3

conn = sqlite3.connect("golden_transport.db")
cursor = conn.cursor()

# Show all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

# Show all vehicles
cursor.execute("SELECT * FROM vehicles;")
print("Vehicles:", cursor.fetchall())

conn.close()
