import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QFrame, QInputDialog
)
from PyQt5.QtCore import QPropertyAnimation, Qt
from PyQt5.QtGui import QFont, QCursor
from db_helper import check_admin, reset_password
from dashboard import Dashboard


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Golden Transport - Admin Login")
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
        box.setFixedSize(700, 550)

        box_layout = QVBoxLayout()
        box_layout.setSpacing(25)

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

        # Banner
        banner = QLabel("Golden TamilNadu Transport")
        banner.setFont(QFont("Segoe UI", 28, QFont.Bold))
        banner.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 10px;")
        banner.setAlignment(Qt.AlignCenter)
        banner.setMinimumWidth(600)
        banner.setWordWrap(True)
        box_layout.addWidget(banner, stretch=1)

        # Title
        title = QLabel("Admin Login")
        title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(title)

        # Username input
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Enter Username")
        self.input_user.setFont(QFont("Segoe UI", 18))
        self.input_user.setFixedHeight(50)
        self.input_user.returnPressed.connect(self.focus_password)
        box_layout.addWidget(self.input_user)

        # Password input
        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Enter Password")
        self.input_pass.setFont(QFont("Segoe UI", 18))
        self.input_pass.setFixedHeight(50)
        self.input_pass.setEchoMode(QLineEdit.Password)
        self.input_pass.returnPressed.connect(self.check_login)
        box_layout.addWidget(self.input_pass)

        # Login button
        self.btn_login = QPushButton("Login")
        self.btn_login.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.btn_login.setStyleSheet("background-color: #0078d7; color: white; padding: 15px; border-radius: 10px;")
        self.btn_login.clicked.connect(self.check_login)
        box_layout.addWidget(self.btn_login)

        # Links layout
        links_layout = QHBoxLayout()

        self.btn_create = QPushButton("Create Admin")
        self.btn_create.setFont(QFont("Segoe UI", 14))
        self.btn_create.setStyleSheet("color: #0078d7; background: none; border: none;")
        self.btn_create.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_create.clicked.connect(self.open_create_admin)
        links_layout.addWidget(self.btn_create)

        # If you want to disable Forgot Password for security, remove this block
        self.btn_forgot_pass = QPushButton("Forgot Password?")
        self.btn_forgot_pass.setFont(QFont("Segoe UI", 14))
        self.btn_forgot_pass.setStyleSheet("color: #0078d7; background: none; border: none;")
        self.btn_forgot_pass.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_forgot_pass.clicked.connect(self.forgot_password)
        links_layout.addWidget(self.btn_forgot_pass)

        box_layout.addLayout(links_layout)

        box.setLayout(box_layout)
        main_layout.addWidget(box)
        self.setLayout(main_layout)

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

    # --- Login Logic ---
    def focus_password(self):
        self.input_pass.setFocus()

    from dashboard import Dashboard

    def check_login(self):
        username = self.input_user.text()
        password = self.input_pass.text()

        if check_admin(username, password):
            self.dashboard = Dashboard(self)   # pass login window reference
            self.dashboard.show()
            self.hide()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")

    def open_create_admin(self):
        from create_admin import CreateAdmin
        self.create_window = CreateAdmin(self)
        self.create_window.show()
        self.hide()

    def forgot_password(self):
        username, ok = QInputDialog.getText(self, "Reset Password", "Enter your username:")
        if ok and username:
            new_pass, ok2 = QInputDialog.getText(self, "Reset Password", "Enter new password:")
            if ok2 and new_pass:
                if reset_password(username, new_pass):
                    QMessageBox.information(self, "Success", "Password reset successfully!")
                else:
                    QMessageBox.warning(self, "Error", "Username not found.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginForm()
    window.show()
    sys.exit(app.exec_())