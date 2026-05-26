import os
import sqlite3
import subprocess
import webbrowser
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QFileDialog
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import pandas as pd

from whatsapp.whatsapp_menu import WhatsAppMenu

class ReportForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Golden Transport - Reports")
        self.resize(1000, 600)

        layout = QVBoxLayout()

        # Title
        title = QLabel("Reports Overview")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Date (dd-mm-yyyy)")
        self.search_input.setFixedWidth(200)
        search_layout.addWidget(self.search_input)

        btn_search = QPushButton("Search")
        btn_search.setFont(QFont("Segoe UI", 12))
        btn_search.clicked.connect(self.search_reports)
        search_layout.addWidget(btn_search)

        layout.addLayout(search_layout)

        # Table
        self.columns = ["Date", "Lorry No", "Add Name", "Driver No", "From", "To",
                        "Freight", "Ton Age", "Advance", "Balance", "Load", "Commission", "Remarks"]
        self.table = QTableWidget(0, len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        layout.addWidget(self.table)
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
        layout.addWidget(self.whatsapp_btn, alignment=Qt.AlignRight)
        # Export buttons
        export_layout = QHBoxLayout()
        btn_csv = QPushButton("Export CSV")
        btn_csv.clicked.connect(self.export_csv)
        export_layout.addWidget(btn_csv)

        btn_excel = QPushButton("Export Excel")
        btn_excel.clicked.connect(self.export_excel)
        export_layout.addWidget(btn_excel)

        layout.addLayout(export_layout)

        self.setLayout(layout)

        # in __init__ top bar
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
    # --- Search reports by date ---
    def search_reports(self):
        date = self.search_input.text().strip()
        conn = sqlite3.connect("golden_transport.db")
        cursor = conn.cursor()

        query = f"""
        SELECT report_date, lorry_no, add_name, driver_no, from_place, to_place,
               freight, ton_age, advance, balance, load, commission, remarks
        FROM reports
        WHERE report_date = ?
        """
        cursor.execute(query, (date,))
        rows = cursor.fetchall()

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

        conn.close()
    def open_whatsapp_menu(self):
        try:
            # 1. Check if standalone WhatsApp.exe exists
            exe_path = r"C:\Users\{}\AppData\Local\WhatsApp\WhatsApp.exe".format(os.getlogin())
            if os.path.exists(exe_path):
                subprocess.Popen([exe_path])
                return

            # 2. Try Microsoft Store version (URI scheme)
            result = os.system("start whatsapp://")
            if result == 0:
                return

            # 3. Fallback → WhatsApp Web
            webbrowser.open("https://web.whatsapp.com/")
        except Exception as e:
            print("Error opening WhatsApp:", e)
            # Always fallback to Web if anything fails
            webbrowser.open("https://web.whatsapp.com/")
    # --- Export to CSV ---
    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "reports.csv", "CSV Files (*.csv)")
        if path:
            conn = sqlite3.connect("golden_transport.db")
            df = pd.read_sql_query("SELECT * FROM reports", conn)
            df.to_csv(path, index=False)
            conn.close()

    # --- Export to Excel ---
    def export_excel(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Excel", "reports.xlsx", "Excel Files (*.xlsx)")
        if path:
            conn = sqlite3.connect("golden_transport.db")
            df = pd.read_sql_query("SELECT * FROM reports", conn)
            df.to_excel(path, index=False)
            conn.close()
