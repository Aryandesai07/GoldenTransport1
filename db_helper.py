import sqlite3

DB_NAME = "golden_transport.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def check_admin(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM admin WHERE username=? AND password=?",
        (username, password)
    )
    result = cursor.fetchone()
    conn.close()
    print("Database check_admin result:", result)   # Debug line
    return result

def create_admin(username, password, contact_no):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO admin (username, password, contact_no) VALUES (?, ?, ?)",
            (username, password, contact_no)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def list_admins():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM admin")
    admins = cursor.fetchall()
    conn.close()
    return [a[0] for a in admins]

def reset_password(username, new_password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE admin SET password=? WHERE username=?",
        (new_password, username)
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated > 0   # True if a row was updated
def create_reports_table():
    conn = connect_db()
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()

    import sqlite3

def get_total_bookings():
    conn = sqlite3.connect("golden_transport.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM orders")
    result = cursor.fetchone()[0]
    conn.close()
    return result

def get_completed_trips():
    conn = sqlite3.connect("golden_transport.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM orders WHERE status='Completed'")
    result = cursor.fetchone()[0]
    conn.close()
    return result

def get_total_revenue():
    conn = sqlite3.connect("golden_transport.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(freight) FROM orders WHERE status='Completed'")
    result = cursor.fetchone()[0] or 0
    conn.close()
    return result
