import sqlite3

def create_tables():
    conn = sqlite3.connect("golden_transport.db")
    cursor = conn.cursor()

    # Vehicles table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_number TEXT NOT NULL,
        capacity REAL,
        status TEXT
    )
    """)

    # Orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        lorry_no TEXT,
        add_name TEXT,
        driver_name TEXT,
        from_place TEXT,
        to_place TEXT,
        freight REAL,
        ton_age REAL,
        advance REAL,
        balance REAL,
        load TEXT,
        commission REAL
    )
    """)

    # Billing table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS billing (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        amount REAL,
        status TEXT
    )
    """)

    # Tracking table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        location TEXT,
        status TEXT
    )
    """)

    # Reports table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_date TEXT,
        lorry_no TEXT,
        add_name TEXT,
        driver_no TEXT,
        from_place TEXT,
        to_place TEXT,
        freight REAL,
        ton_age REAL,
        advance REAL,
        balance REAL,
        load TEXT,
        commission REAL,
        remarks TEXT
    )
    """)


if __name__ == "__main__":
    create_tables()