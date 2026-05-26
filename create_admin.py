import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QFrame, QInputDialog
)
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.QtGui import QFont
from twilio.rest import Client
import os
from db_helper import create_admin


class CreateAdmin(QWidget):
    def __init__(self, login_window=None):
        super().__init__()
        self.login_window = login_window
        self.setWindowTitle("Golden Transport - Create Admin")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(900, 600)
        self.setMinimumSize(800, 500)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                stop:0 #0078d7, stop:1 #f0f0f0);
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        box = QFrame()
        box.setStyleSheet("background-color: white; border-radius: 20px;")
        box.setFixedSize(600, 400)

        box_layout = QVBoxLayout()
        box_layout.setSpacing(20)

        # Top bar buttons
        self.btn_minimize = QPushButton("–")
        self.btn_minimize.setFixedSize(40, 30)
        self.btn_minimize.setStyleSheet("background-color: #0078d7; color: white; border-radius: 5px;")
        self.btn_minimize.clicked.connect(self.smooth_minimize)

        self.btn_maximize = QPushButton("□")
        self.btn_maximize.setFixedSize(40, 30)
        self.btn_maximize.setStyleSheet("background-color: gray; color: white; border-radius: 5px;")
        self.btn_maximize.clicked.connect(self.smooth_maximize_restore)

        self.btn_close = QPushButton("X")
        self.btn_close.setFixedSize(40, 30)
        self.btn_close.setStyleSheet("background-color: red; color: white; border-radius: 5px;")
        self.btn_close.clicked.connect(self.smooth_close)

        top_bar = QHBoxLayout()
        top_bar.addStretch()
        top_bar.addWidget(self.btn_minimize)
        top_bar.addWidget(self.btn_maximize)
        top_bar.addWidget(self.btn_close)
        box_layout.addLayout(top_bar)

        # Title
        title = QLabel("Create Admin Account")
        title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(title)

        # Username input
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Enter New Username")
        self.input_user.setFont(QFont("Segoe UI", 18))
        self.input_user.setFixedHeight(50)
        box_layout.addWidget(self.input_user)

        # Password input
        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Enter New Password")
        self.input_pass.setFont(QFont("Segoe UI", 18))
        self.input_pass.setFixedHeight(50)
        self.input_pass.setEchoMode(QLineEdit.Password)
        box_layout.addWidget(self.input_pass)

        # Contact number input
        self.input_contact = QLineEdit()
        self.input_contact.setPlaceholderText("Enter Contact Number")
        self.input_contact.setFont(QFont("Segoe UI", 18))
        self.input_contact.setFixedHeight(50)
        box_layout.addWidget(self.input_contact)

        # Create button
        self.btn_create = QPushButton("Create Admin")
        self.btn_create.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.btn_create.setStyleSheet("background-color: #0078d7; color: white; padding: 12px; border-radius: 10px;")
        self.btn_create.clicked.connect(self.handle_create_admin)
        box_layout.addWidget(self.btn_create)

        # Back button
        self.btn_back = QPushButton("Back to Login")
        self.btn_back.setFont(QFont("Segoe UI", 14))
        self.btn_back.setStyleSheet("color: #0078d7; background: none; border: none;")
        self.btn_back.clicked.connect(self.go_back)
        box_layout.addWidget(self.btn_back)

        box.setLayout(box_layout)
        main_layout.addWidget(box)
        self.setLayout(main_layout)

    # --- OTP Sending ---
    def send_otp(self, contact_no, otp):
        account_sid = "AC71bfe9588c06d7e79df10b00b2de1bec"
        auth_token = "ac48e5d1808dcfc269f256bf2779ae1c"
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f"Your Golden Transport OTP is {otp}",
            from_="+14782106758",   # your Twilio number
            to=f"+91{9284926533}"  # Indian format
        )
        return message.sid

    # --- Create Admin with OTP ---
    def handle_create_admin(self):
        username = self.input_user.text()
        password = self.input_pass.text()
        contact_no = self.input_contact.text()

        if not username or not password or not contact_no:
            QMessageBox.warning(self, "Error", "Please enter username, password, and contact number.")
            return

        otp = str(random.randint(100000, 999999))
        self.send_otp(contact_no, otp)

        entered_otp, ok = QInputDialog.getText(self, "OTP Verification", "Enter the OTP sent to your mobile:")

        if ok and entered_otp == otp:
            if create_admin(username, password, contact_no):
                QMessageBox.information(self, "Success", f"Admin '{username}' created successfully!")
            else:
                QMessageBox.warning(self, "Error", "Username already exists.")
        else:
            QMessageBox.warning(self, "Error", "Invalid OTP. Please try again.")

    # --- Smooth Controls ---
    def smooth_close(self):
        reply = QMessageBox.question(
            self,
            "Exit Confirmation",
            "Do you really want to exit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.animation = QPropertyAnimation(self, b"windowOpacity")
            self.animation.setDuration(300)
            self.animation.setStartValue(1)
            self.animation.setEndValue(0)
            self.animation.finished.connect(self.close)
            self.animation.start()
        else:
            self.setWindowOpacity(1)

    def closeEvent(self, event):
        event.accept()

    def smooth_minimize(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0.3)
        self.animation.finished.connect(self.showMinimized)
        self.animation.start()

    def showEvent(self, event):
        self.setWindowOpacity(1)
        super().showEvent(event)

    def smooth_maximize_restore(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(250)
        self.animation.setStartValue(0.8)
        self.animation.setEndValue(1)
        self.animation.start()

        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def go_back(self):
        if self.login_window:
            self.login_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CreateAdmin()
    window.show()
    sys.exit(app.exec_())