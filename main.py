import sys
import sqlite3
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox

class GoldenTransportApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Golden Transport")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Add Vehicle button
        btn = QPushButton("Add Vehicle")
        btn.clicked.connect(self.add_vehicle)
        layout.addWidget(btn)

        self.setLayout(layout)

    def add_vehicle(self):
        try:
            conn = sqlite3.connect('golden_transport.db')
            cursor = conn.cursor()

            # Generate a random registration number each time
            reg_no = f"MH12AB{random.randint(1000,9999)}"

            cursor.execute("""
                INSERT INTO vehicles (vehicle_number, capacity, status)
                VALUES (?, ?, ?)
            """, (reg_no, 5000, "Available"))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", f"Vehicle added with reg no: {reg_no}")

        except sqlite3.IntegrityError as e:
            QMessageBox.warning(self, "Error", f"Database error: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GoldenTransportApp()
    window.show()
    sys.exit(app.exec_())