import sqlite3

def insert_sample_reports():
    conn = sqlite3.connect("golden_transport.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO reports (
        report_date, lorry_no, add_name, driver_no, from_place, to_place,
        freight, ton_age, advance, balance, load, commission, remarks
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "18-04-2026", "MH12AB1234", "Aryan Transport", "DRV001",
        "Kolhapur", "Pune", 15000, 20, 5000, 10000,
        "Cement", 500, "On time"
    ))

    conn.commit()
    conn.close()
    print("Sample report inserted successfully.")

if __name__ == "__main__":
    insert_sample_reports()
