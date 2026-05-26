# tracking_form.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
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

    def go_back_dashboard(self):
        """Close tracking form and show dashboard again"""
        self.close()
        if self.dashboard_window:
            self.dashboard_window.show()