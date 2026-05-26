import sqlite3

conn = sqlite3.connect('golden_transport.db')
cursor = conn.cursor()

# Admin table
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Insert default admin
cursor.execute("INSERT OR IGNORE INTO admin (username, password) VALUES (?, ?)", ("admin", "admin123"))

conn.commit()
conn.close()