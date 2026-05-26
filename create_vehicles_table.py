import sqlite3

conn = sqlite3.connect("golden_transport.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS vehicles")

cursor.execute("""
CREATE TABLE vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_number TEXT NOT NULL,
    capacity REAL,
    status TEXT
)
""")

conn.commit()
conn.close()
print("Vehicles table recreated successfully.")