import os
import sqlite3
import datetime
import webbrowser
import subprocess
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QMessageBox, QTableWidget, QTableWidgetItem, QLabel, QComboBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QTimer, Qt

from whatsapp.whatsapp_menu import WhatsAppMenu


class VehicleForm(QWidget):
    def __init__(self, parent=None, dashboard_callback=None):
        super().__init__(parent)
        self.setWindowTitle("Vehicle Management")
        self.resize(1000, 600)

        self.dashboard_callback = dashboard_callback

        layout = QVBoxLayout()

        # --- Header Bar ---
        header_layout = QHBoxLayout()

        # Date & Time
        self.datetime_label = QLabel()
        self.datetime_label.setFont(QFont("Segoe UI", 11))
        header_layout.addWidget(self.datetime_label)

        # Dashboard button
        dashboard_btn = QPushButton("🏠 Dashboard")
        dashboard_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        dashboard_btn.setStyleSheet("""
            QPushButton {
                color: #FFFFFF;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        dashboard_btn.clicked.connect(self.go_dashboard)   # ✅ ab ye method class ke andar hoga
        header_layout.addStretch()
        header_layout.addWidget(dashboard_btn)

        # Window control buttons
        for text, slot in [("➖", self.showMinimized), ("⬜", self.showMaximized), ("❌", self.close)]:
            btn = QPushButton(text)
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: qlineargradient(
                        spread:pad, x1:0, y1:0, x2:1, y2:0,
                        stop:0 #041426, stop:1 #0b3a66
                    );
                    color: white;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #005A9E;
                }
            """)
            btn.clicked.connect(slot)
            header_layout.addWidget(btn)

        layout.addLayout(header_layout)

        # WhatsApp button
        self.whatsapp_btn = QPushButton(" WhatsApp")
        self.whatsapp_btn.setIcon(QIcon("whatsapp/icons/whatsapp.png"))
        self.whatsapp_btn.setStyleSheet("""
            QPushButton {
                background-color: #25D366;
                color: white;
                font-weight: bold;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #128C7E;
            }
        """)
        self.whatsapp_btn.clicked.connect(self.open_whatsapp_menu)
        layout.addWidget(self.whatsapp_btn, alignment=Qt.AlignCenter)

        # --- Title ---
        title = QLabel("🚚 Vehicle Management")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #0b3a66;")
        layout.addWidget(title)

        # --- Vehicle Table ---
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Vehicle Number", "Capacity", "Status"])
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                font-size: 13px;
                background-color: #fafafa;
                border: 1px solid #ccc;
            }
            QHeaderView::section {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #041426, stop:1 #0b3a66
                );
                color: white;
                padding: 6px;
                border: none;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.table)

        # --- Form Fields ---
        form_layout = QHBoxLayout()
        self.vehicle_number = QLineEdit(); self.vehicle_number.setPlaceholderText("Vehicle Number (MH07 AB1234)")
        self.capacity = QLineEdit(); self.capacity.setPlaceholderText("Capacity (tons)")
        self.status = QComboBox(); self.status.addItems(["Available", "In Use", "Maintenance"])
        self.edit_id = QLineEdit(); self.edit_id.setPlaceholderText("Enter ID to Edit/Delete")

        form_layout.addWidget(self.vehicle_number)
        form_layout.addWidget(self.capacity)
        form_layout.addWidget(self.status)
        form_layout.addWidget(self.edit_id)
        layout.addLayout(form_layout)

        # --- Action Buttons ---
        btn_layout = QHBoxLayout()

        btn_add = QPushButton("➕ Add"); btn_add.clicked.connect(self.add_vehicle)
        btn_edit = QPushButton("✏️ Edit"); btn_edit.clicked.connect(self.edit_vehicle)
        btn_delete = QPushButton("🗑 Delete"); btn_delete.clicked.connect(self.delete_vehicle)

        for btn, color in [(btn_add, "#0078D7"), (btn_edit, "#0078D7"), (btn_delete, "#dc3545")]:
            btn.setFont(QFont("Segoe UI", 12))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    padding: 8px 20px;
                    border-radius: 6px;
                }}
                QPushButton:hover {{
                    background-color: #005A9E;
                }}
            """)
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # Load vehicles
        self.load_vehicles()

        # Real-time clock
        timer = QTimer(self)
        timer.timeout.connect(self.update_datetime)
        timer.start(1000)
        self.update_datetime()



    def update_datetime(self):
        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.datetime_label.setText(f"📅 {now}")

    def get_connection(self):
        return sqlite3.connect("golden_transport.db")

    def go_dashboard(self):
        try:
            if self.dashboard_callback:
                self.dashboard_callback()
            else:
                self.close()
        except Exception as e:
            print("Error in go_dashboard:", e)
            self.close()

    def load_vehicles(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_number TEXT,
                capacity TEXT,
                status TEXT
            )
        """)
        cursor.execute("SELECT id, vehicle_number, capacity, status FROM vehicles ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(0)
        for row in rows:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for col, value in enumerate(row):
                self.table.setItem(row_position, col, QTableWidgetItem(str(value)))

    def add_vehicle(self):
        if not self.vehicle_number.text().strip() or not self.capacity.text().strip():
            QMessageBox.warning(self, "Error", "Please fill all fields.")
            return
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vehicles (vehicle_number, capacity, status) VALUES (?, ?, ?)",
                       (self.vehicle_number.text().strip(),
                        self.capacity.text().strip(),
                        self.status.currentText()))
        conn.commit(); conn.close()
        QMessageBox.information(self, "Added", "Vehicle added successfully.")
        self.load_vehicles()

    def open_whatsapp_menu(self):
        try:
            exe_path = r"C:\Users\{}\AppData\Local\WhatsApp\WhatsApp.exe".format(os.getlogin())
            if os.path.exists(exe_path):
                subprocess.Popen([exe_path])
                return
            result = os.system("start whatsapp://")
            if result == 0:
                return
            webbrowser.open("https://web.whatsapp.com/")
        except Exception as e:
            print("Error opening WhatsApp:", e)
            webbrowser.open("https://web.whatsapp.com/")

    def edit_vehicle(self):
        if not self.edit_id.text().strip():
            QMessageBox.warning(self, "Error", "Enter ID to edit.")
            return
        reply = QMessageBox.question(self, "Confirm Edit",
                                     "Are you sure you want to edit this vehicle?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE vehicles SET vehicle_number=?, capacity=?, status=? WHERE id=?",
                           (self.vehicle_number.text().strip(),
                            self.capacity.text().strip(),
                            self.status.currentText(),
                            self.edit_id.text().strip()))
            conn.commit(); conn.close()
            QMessageBox.information(self, "Edited", "Vehicle updated successfully.")
            self.load_vehicles()

    def delete_vehicle(self):
        if not self.edit_id.text().strip():
            QMessageBox.warning(self, "Error", "Enter ID to delete.")
            return
        reply = QMessageBox.question(self, "Confirm Delete",
                                     "Are you sure you want to delete this vehicle?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vehicles WHERE id=?", (self.edit_id.text().strip(),))
            conn.commit(); conn.close()
            QMessageBox.information(self, "Deleted", "Vehicle deleted successfully.")
            self.load_vehicles()
