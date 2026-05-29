from datetime import time
import subprocess
import sys
from turtle import st

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QFrame,
    QInputDialog,
)

from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation
from PyQt5.QtGui import QFont, QCursor

from db_helper import check_admin, reset_password
from dashboard import Dashboard


class LoginForm(QWidget):

    def __init__(self):
        super().__init__()

        self.oldPos = self.pos()

        self.setWindowTitle("Golden Transport - Admin Login")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(950, 600)

        # =====================================================
        # MAIN WINDOW STYLE
        # =====================================================

        self.setStyleSheet("""
            QWidget{
                background:qlineargradient(
                    spread:pad,
                    x1:0,
                    y1:0,
                    x2:1,
                    y2:1,
                    stop:0 #0f2027,
                    stop:0.5 #203a43,
                    stop:1 #2c5364
                );
            }
        """)

        # =====================================================
        # MAIN LAYOUT
        # =====================================================

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)

        # =====================================================
        # LOGIN BOX
        # =====================================================

        self.box = QFrame()

        self.box.setFixedSize(720, 520)

        self.box.setStyleSheet("""
            QFrame{
                background:rgba(255,255,255,0.96);
                border-radius:25px;
                border:2px solid rgba(255,215,0,0.3);
            }
        """)

        box_layout = QVBoxLayout()
        box_layout.setSpacing(20)

        # =====================================================
        # TOP BAR
        # =====================================================

        top_bar = QHBoxLayout()

        title_bar = QLabel("🚛 Golden TamilNadu Transport")
        title_bar.setFont(QFont("Segoe UI", 15, QFont.Bold))
        title_bar.setStyleSheet("""
            color:#222;
            background:transparent;
        """)

        top_bar.addWidget(title_bar)
        top_bar.addStretch()

        # Minimize Button
        self.btn_min = QPushButton("—")
        self.btn_min.setFixedSize(40, 30)
        self.btn_min.clicked.connect(self.showMinimized)

        # Maximize Button
        self.btn_max = QPushButton("□")
        self.btn_max.setFixedSize(40, 30)
        self.btn_max.clicked.connect(self.toggle_max_restore)

        # Close Button
        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(40, 30)
        self.btn_close.clicked.connect(self.close)

        for btn, color in [
            (self.btn_min, "#0078d7"),
            (self.btn_max, "#555"),
            (self.btn_close, "#ff4d4d")
        ]:

            btn.setStyleSheet(f"""
                QPushButton{{
                    background:{color};
                    color:white;
                    border:none;
                    border-radius:8px;
                    font-size:16px;
                    font-weight:bold;
                }}

                QPushButton:hover{{
                    background:white;
                    color:black;
                }}
            """)

        top_bar.addWidget(self.btn_min)
        top_bar.addWidget(self.btn_max)
        top_bar.addWidget(self.btn_close)

        box_layout.addLayout(top_bar)

        # =====================================================
        # HEADER
        # =====================================================

        banner = QLabel("ADMIN LOGIN")

        banner.setAlignment(Qt.AlignCenter)

        banner.setFont(QFont("Segoe UI", 30, QFont.Bold))

        banner.setStyleSheet("""
            color:#111;
            padding:15px;
            background:#FFD700;
            border-radius:15px;
        """)

        box_layout.addWidget(banner)

        # =====================================================
        # DESCRIPTION
        # =====================================================

        desc = QLabel(
            "Secure access to Golden TamilNadu Transport Management System"
        )

        desc.setAlignment(Qt.AlignCenter)

        desc.setFont(QFont("Segoe UI", 13))

        desc.setStyleSheet("""
            color:#444;
            background:transparent;
        """)

        box_layout.addWidget(desc)

        # =====================================================
        # USERNAME
        # =====================================================

        self.input_user = QLineEdit()

        self.input_user.setPlaceholderText("Enter Username")

        self.input_user.setFixedHeight(55)

        self.input_user.setFont(QFont("Segoe UI", 14))

        self.input_user.returnPressed.connect(self.focus_password)

        # =====================================================
        # PASSWORD
        # =====================================================

        self.input_pass = QLineEdit()

        self.input_pass.setPlaceholderText("Enter Password")

        self.input_pass.setEchoMode(QLineEdit.Password)

        self.input_pass.setFixedHeight(55)

        self.input_pass.setFont(QFont("Segoe UI", 14))

        self.input_pass.returnPressed.connect(self.check_login)

        input_style = """
            QLineEdit{
                border:2px solid #ddd;
                border-radius:12px;
                padding-left:18px;
                background:white;
                color:#222;
            }

            QLineEdit:focus{
                border:2px solid #FFD700;
            }
        """

        self.input_user.setStyleSheet(input_style)
        self.input_pass.setStyleSheet(input_style)

        box_layout.addWidget(self.input_user)
        box_layout.addWidget(self.input_pass)

        # =====================================================
        # SHOW PASSWORD BUTTON
        # =====================================================

        self.show_pass = QPushButton("👁 Show Password")

        self.show_pass.setCursor(QCursor(Qt.PointingHandCursor))

        self.show_pass.setStyleSheet("""
            QPushButton{
                background:transparent;
                color:#0078d7;
                border:none;
                text-align:left;
                font-size:13px;
            }
        """)

        self.show_pass.clicked.connect(self.toggle_password)

        box_layout.addWidget(self.show_pass)

        # =========================================================
    # LOGIN BUTTON
    # =========================================================

        st.markdown("<br><br><br>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1,1,1])

        with c2:

            if st.button("🔐 ENTER ADMIN PANEL"):

                with st.spinner("Launching Secure Admin Panel..."):

                    time.sleep(1)

                    try:

                        subprocess.Popen(
                            [sys.executable, "login.py"],
                            shell=True
                        )

                        st.success("Admin Panel Started Successfully")

                    except Exception as e:

                        st.error(f"Unable to launch login window: {e}")

                # =====================================================
                # LINKS
                # =====================================================

                links_layout = QHBoxLayout()

                self.btn_create = QPushButton("Create Admin")
                self.btn_forgot = QPushButton("Forgot Password?")

                for btn in [self.btn_create, self.btn_forgot]:

                    btn.setCursor(QCursor(Qt.PointingHandCursor))

                    btn.setStyleSheet("""
                        QPushButton{
                            background:transparent;
                            color:#0078d7;
                            border:none;
                            font-size:13px;
                        }

                        QPushButton:hover{
                            color:#FFD700;
                        }
                    """)

                self.btn_create.clicked.connect(self.open_create_admin)
                self.btn_forgot.clicked.connect(self.forgot_password)

                links_layout.addWidget(self.btn_create)
                links_layout.addStretch()
                links_layout.addWidget(self.btn_forgot)

                box_layout.addLayout(links_layout)

                self.box.setLayout(box_layout)

                # =====================================================
                # CENTER BOX
                # =====================================================

                main_layout.addStretch()

                row = QHBoxLayout()
                row.addStretch()
                row.addWidget(self.box)
                row.addStretch()

                main_layout.addLayout(row)

                main_layout.addStretch()

                self.setLayout(main_layout)

                # =====================================================
                # OPENING ANIMATION
                # =====================================================

                self.setWindowOpacity(0)

                self.fade = QPropertyAnimation(self, b"windowOpacity")
                self.fade.setDuration(800)
                self.fade.setStartValue(0)
                self.fade.setEndValue(1)
                self.fade.start()

    # =====================================================
    # DRAG WINDOW
    # =====================================================

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):

        delta = QPoint(event.globalPos() - self.oldPos)

        self.move(self.x() + delta.x(), self.y() + delta.y())

        self.oldPos = event.globalPos()

    # =====================================================
    # WINDOW CONTROLS
    # =====================================================

    def toggle_max_restore(self):

        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # =====================================================
    # PASSWORD TOGGLE
    # =====================================================

    def toggle_password(self):

        if self.input_pass.echoMode() == QLineEdit.Password:

            self.input_pass.setEchoMode(QLineEdit.Normal)
            self.show_pass.setText("🙈 Hide Password")

        else:

            self.input_pass.setEchoMode(QLineEdit.Password)
            self.show_pass.setText("👁 Show Password")

    # =====================================================
    # LOGIN FUNCTIONS
    # =====================================================

    def focus_password(self):
        self.input_pass.setFocus()

    def check_login(self):

        username = self.input_user.text().strip()
        password = self.input_pass.text().strip()

        if not username or not password:

            QMessageBox.warning(
                self,
                "Missing Fields",
                "Please enter username and password."
            )

            return

        if check_admin(username, password):

            QMessageBox.information(
                self,
                "Login Success",
                "Welcome Admin!"
            )

            self.dashboard = Dashboard(self)

            self.dashboard.show()

            self.hide()

        else:

            QMessageBox.warning(
                self,
                "Login Failed",
                "Invalid username or password."
            )

    # =====================================================
    # CREATE ADMIN
    # =====================================================

    def open_create_admin(self):

        from create_admin import CreateAdmin

        self.create_window = CreateAdmin(self)

        self.create_window.show()

        self.hide()

    # =====================================================
    # RESET PASSWORD
    # =====================================================

    def forgot_password(self):

        username, ok = QInputDialog.getText(
            self,
            "Reset Password",
            "Enter Username:"
        )

        if ok and username:

            new_pass, ok2 = QInputDialog.getText(
                self,
                "Reset Password",
                "Enter New Password:"
            )

            if ok2 and new_pass:

                if reset_password(username, new_pass):

                    QMessageBox.information(
                        self,
                        "Success",
                        "Password reset successful!"
                    )

                else:

                    QMessageBox.warning(
                        self,
                        "Error",
                        "Username not found."
                    )


# =====================================================
# RUN APP
# =====================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = LoginForm()

    window.show()

    sys.exit(app.exec_())
