import sqlite3

conn = sqlite3.connect("golden_transport.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE admin ADD COLUMN contact_no TEXT;")
    print("Column contact_no added successfully.")
except sqlite3.OperationalError as e:
    print("Error:", e)

# Show table structure
cursor.execute("PRAGMA table_info(admin);")
print(cursor.fetchall())

conn.commit()
conn.close()

cursor.execute("PRAGMA table_info(admin);")
columns = [col[1] for col in cursor.fetchall()]
if "contact_no" not in columns:
    cursor.execute("ALTER TABLE admin ADD COLUMN contact_no TEXT;")
