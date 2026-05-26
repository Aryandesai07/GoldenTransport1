# tracking_form.py
from asyncio import subprocess
import os
import webbrowser

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

class TrackingForm(QWidget):
    def __init__(self, dashboard_window=None):
        super().__init__()
        self.dashboard_window = dashboard_window
        self.setWindowTitle("Golden Transport - Tracking")
        self.resize(1000, 600)
        self.setMinimumSize(800, 500)

        # --- Main Layout ---
        layout = QVBoxLayout()

        # --- Title ---
        title = QLabel("📍 Tracking Service")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # --- Placeholder Message ---
        msg = QLabel("🚧 Tracking service is not available right now.\n"
                     "This feature will be enabled in future updates.")
        msg.setFont(QFont("Segoe UI", 14))
        msg.setAlignment(Qt.AlignCenter)
        layout.addWidget(msg)
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
        # --- Back to Dashboard Button ---
        back_btn = QPushButton("⬅ Back to Dashboard")
        back_btn.setFont(QFont("Segoe UI", 12))
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """)
        back_btn.clicked.connect(self.go_back_dashboard)
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)
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
    def go_back_dashboard(self):
        """Close tracking form and show dashboard again"""
        self.close()
        if self.dashboard_window:
            self.dashboard_window.show()