import sqlite3


import billing

# Connect to your existing database
conn = sqlite3.connect("golden_transport.db")
cursor = conn.cursor()

# Create billing table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS billing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_no TEXT UNIQUE,
    customer_name TEXT,
    order_id INTEGER,
    broker_commission REAL,
    transport_charges REAL,
    taxes REAL,
    total_amount REAL,
    payment_status TEXT,   -- Paid, Pending, Overdue
    payment_mode TEXT,      -- Cash, Bank Transfer, UPI
    invoice_date TEXT,
    due_date TEXT,
    created_at TEXT
);
""")

conn.commit()
conn.close()

print("Billing table created successfully in golden_transport.db")
    