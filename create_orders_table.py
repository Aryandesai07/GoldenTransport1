import sqlite3

conn = sqlite3.connect("golden_transport.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS orders;")

cursor.execute("""
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    lorry_no_name TEXT,
    driver_no TEXT,
    from_place TEXT,
    to_place TEXT,
    freight REAL,
    ton_age REAsL,
    advance REAL,
    balance REAL,
    load TEXT,
    commission REAL
);
""")

conn.commit()
conn.close()

print("Orders table recreated successfully.")