import os
import subprocess
import sys
import sqlite3
import webbrowser
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QApplication, QFrame, QLineEdit, QMessageBox, QGroupBox,QDateEdit,QCalendarWidget
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt
from datetime import datetime
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QLineEdit
from sqlalchemy import values


# Import forms from separate modules
from orders.orders_form import OrdersForm
from vehicles.vehicle_form import VehicleForm
from billing.billing_form import BillingForm
from reports.report_form import ReportForm
from tracking.tracking_form import TrackingForm

from whatsapp.whatsapp_menu import WhatsAppMenu
class Dashboard(QWidget):
    def __init__(self, login_window=None):
        super().__init__()
        self.login_window = login_window
        self.setWindowTitle("Golden Transport - Dashboard")
        self.resize(1200, 700)
        self.setMinimumSize(1000, 600)

        # --- Master Layout (Vertical) ---
        master_layout = QVBoxLayout()
        master_layout.setContentsMargins(0, 0, 0, 0)
        master_layout.setSpacing(0)

        # --- Top Bar Frame (professional, muted midnight-blue) ---
        top_frame = QFrame()
        top_frame.setFixedHeight(85)
        top_frame.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #041426, stop:1 #0b3a66
                );
                border-bottom: 1px solid rgba(255,255,255,0.06);
                padding: 10px;
            }
        """)

        top_bar = QHBoxLayout(top_frame)
        top_bar.setContentsMargins(20, 0, 20, 0)
        top_bar.setSpacing(12)

        # --- Left Side: Branding ---
        logo_label = QLabel()
        logo_path = "assets/golden.jpeg"
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path)
            if not pix.isNull():
                logo_label.setPixmap(pix.scaled(56, 56, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                logo_label.setText("GT")
                logo_label.setStyleSheet("color: white; font-weight: bold; font-size: 18px;")
                logo_label.setFixedSize(56, 56)
                logo_label.setAlignment(Qt.AlignCenter)
        else:
            logo_label.setText("GT")
            logo_label.setStyleSheet("color: white; font-weight: bold; font-size: 18px;")
            logo_label.setFixedSize(56, 56)
            logo_label.setAlignment(Qt.AlignCenter)

        brand_label = QLabel("GOLDEN TRANSPORT")
        brand_label.setFont(QFont("Segoe UI", 26, QFont.Bold))
        brand_label.setStyleSheet("color: #FFFFFF; letter-spacing: 1px;")

        branding_layout = QHBoxLayout()
        branding_layout.addWidget(logo_label)
        branding_layout.addWidget(brand_label)
        branding_layout.setSpacing(12)
        branding_layout.setAlignment(Qt.AlignVCenter)

        top_bar.addLayout(branding_layout)
        top_bar.addStretch()

        # --- Right Side: Profile + Calendar Icon + Notifications ---
        right_layout = QHBoxLayout()
        right_layout.setSpacing(10)

        # Avatar
        avatar = QLabel()
        avatar_path = "assets/avatar.png"
        if os.path.exists(avatar_path):
            pix = QPixmap(avatar_path)
            if not pix.isNull():
                avatar.setPixmap(pix.scaled(44, 44, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                avatar.setFixedSize(44, 44)
            else:
                avatar.setText("A")
                avatar.setFixedSize(44, 44)
                avatar.setStyleSheet("color: white; font-weight: bold;")
        else:
            avatar.setText("A")
            avatar.setFixedSize(44, 44)
            avatar.setStyleSheet("color: white; font-weight: bold;")

        avatar.setStyleSheet("border-radius: 22px; border: 1px solid rgba(255,255,255,0.08); background-color: transparent;")
        avatar.setAlignment(Qt.AlignCenter)

        profile_container = QHBoxLayout()
        profile_container.setSpacing(8)
        profile_container.addWidget(avatar)
        profile_container.setAlignment(Qt.AlignVCenter)

        right_layout.addLayout(profile_container)

        # Calendar icon button
        self.calendar_btn = QPushButton()
        self.calendar_btn.setFixedSize(36, 36)
        self.calendar_btn.setCursor(Qt.PointingHandCursor)
        self.calendar_btn.setToolTip("Open calendar")
        self.calendar_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #FFFFFF;
                border-radius: 18px;
                border: 1px solid rgba(255,255,255,0.06);
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.04);
            }
        """)
        self.calendar_btn.setText("📅")
        right_layout.addWidget(self.calendar_btn)

        # Notification Bell + Badge
        notif_btn = QPushButton("🔔")
        notif_btn.setFixedSize(36, 36)
        notif_btn.setCursor(Qt.PointingHandCursor)
        notif_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #FFFFFF;
                border-radius: 18px;
                border: 1px solid rgba(255,255,255,0.06);
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.04);
            }
        """)

        badge = QLabel("5")
        badge.setFont(QFont("Segoe UI", 10, QFont.Bold))
        badge.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            border-radius: 8px;
            padding: 2px 6px;
        """)
        badge.setAlignment(Qt.AlignCenter)

        notif_layout = QHBoxLayout()
        notif_layout.setSpacing(6)
        notif_layout.addWidget(notif_btn)
        notif_layout.addWidget(badge)
        right_layout.addLayout(notif_layout)

        top_bar.addLayout(right_layout)

        # Add top bar to master layout
        master_layout.addWidget(top_frame)

        # WhatsApp button
        self.whatsapp_btn = QPushButton(" WhatsApp")
        whatsapp_icon_path = "whatsapp/icons/whatsapp.png"
        if os.path.exists(whatsapp_icon_path):
            self.whatsapp_btn.setIcon(QIcon(whatsapp_icon_path))
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
        if hasattr(self, "open_whatsapp_menu"):
            self.whatsapp_btn.clicked.connect(self.open_whatsapp_menu)
        top_bar.addWidget(self.whatsapp_btn)

        # Calendar popup setup
        self._calendar_popup = QCalendarWidget()
        self._calendar_popup.setWindowFlags(Qt.Popup)
        self._calendar_popup.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self._calendar_popup.setGridVisible(False)
        self._calendar_popup.setFirstDayOfWeek(Qt.Monday)
        self._calendar_popup.setStyleSheet("""
            QCalendarWidget {
                background-color: #0b3a66;
                color: #ffffff;
                border: 1px solid rgba(255,255,255,0.08);
            }
            QCalendarWidget QToolButton {
                background: transparent;
                color: #ffffff;
                height: 28px;
                qproperty-iconSize: 18px;
                font: 10pt "Segoe UI";
            }
            QCalendarWidget QSpinBox {
                color: #ffffff;
                background: transparent;
                border: none;
            }
            QCalendarWidget QAbstractItemView {
                background-color: transparent;
                color: #ffffff;
                selection-background-color: #e6c200;
                selection-color: #0b3a66;
            }
            QCalendarWidget QWidget { color: #ffffff; }
        """)

        # Connect popup signals
        self._calendar_popup.clicked.connect(self._on_calendar_selected)
        self.calendar_btn.clicked.connect(self._show_calendar)

        # --- Main Area (Sidebar + Content) ---
        main_area = QHBoxLayout()
        main_area.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            background-color: #2C3E50;
            color: white;
            border-right: 1px solid rgba(255,215,0,0.06);
        """)
        side_layout = QVBoxLayout()

        btn_dashboard = QPushButton("🏠 Dashboard")
        btn_dashboard.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_dashboard.setFixedHeight(40)
        btn_dashboard.setCursor(Qt.PointingHandCursor)
        btn_dashboard.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 6px;
                text-align: left;
                padding-left: 12px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """)
        side_layout.addWidget(btn_dashboard)

        for text, handler in [
            ("Vehicles", self.open_vehicle_form),
            ("Tracking", self.open_tracking_form),
            ("Billing", self.open_billing_form),
            ("Reports", self.open_report_form),
        ]:
            btn = QPushButton(text)
            btn.setFont(QFont("Segoe UI", 14))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(self.sidebar_button_style())
            btn.clicked.connect(handler)
            side_layout.addWidget(btn)

        # Orders button (placed before stretch + consistent font)
        btn_orders = QPushButton("Orders")
        btn_orders.setFont(QFont("Segoe UI", 14))
        btn_orders.setCursor(Qt.PointingHandCursor)
        btn_orders.setStyleSheet(self.sidebar_button_style())
        btn_orders.clicked.connect(self.open_orders_form)
        side_layout.addWidget(btn_orders)

        side_layout.addStretch()

        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.setFont(QFont("Segoe UI", 9))
        settings_btn.setFixedSize(100, 28)
        settings_btn.setCursor(Qt.PointingHandCursor)
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        settings_btn.clicked.connect(self.open_settings)
        side_layout.addWidget(settings_btn)

        sidebar.setLayout(side_layout)
        main_area.addWidget(sidebar)

        # --- Content Area ---
        content = QVBoxLayout()
        content.setContentsMargins(18, 18, 18, 18)
        content.setSpacing(12)

        title = QLabel("Admin Dashboard")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2f2f2f;")
        content.addWidget(title)

        # Date + Search Bar
        search_bar = QHBoxLayout()
        date_label2 = QLabel("Date: " + datetime.now().strftime("%d-%m-%Y"))
        date_label2.setFont(QFont("Segoe UI", 14))
        date_label2.setStyleSheet("color: #3b3b3b;")
        search_bar.addWidget(date_label2)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Date (dd-mm-yyyy)")
        self.search_input.setFixedWidth(200)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 6px;
                border: 1px solid rgba(0,0,0,0.06);
                border-radius: 6px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 1px solid rgba(230,194,0,0.6);
            }
        """)
        search_bar.addWidget(self.search_input)

        btn_search = QPushButton("Search")
        btn_search.setFont(QFont("Segoe UI", 12))
        btn_search.setCursor(Qt.PointingHandCursor)
        btn_search.setStyleSheet("""
            QPushButton {
                background-color: #e6c200;
                color: #222;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #d4b000;
            }
        """)
        btn_search.clicked.connect(self.search_orders)
        search_bar.addWidget(btn_search)

        search_bar.addStretch()
        content.addLayout(search_bar)

        # --- Stats Row ---
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(10)
        for stat in ["Total Vehicles", "Active Trips", "Completed Deliveries", "Pending Orders", "Total Revenue"]:
            box = QLabel(stat + "\n0")
            box.setFont(QFont("Segoe UI", 14))
            box.setStyleSheet("background-color: #f7f7f7; border-radius: 10px; padding: 18px; color: #333;")
            box.setAlignment(Qt.AlignCenter)
            stats_layout.addWidget(box)
        content.addLayout(stats_layout)

        # --- Entry Fields + Save Order ---
        self.entry_layout = QHBoxLayout()
        self.entry_fields = {}
        self.columns = [
            "date", "lorry_no", "lorry_name", "driver_name", "driver_no",
            "from_place", "to_place", "freight", "ton_age",
            "advance", "balance", "load", "commission"
        ]

        form_box = QGroupBox("Add New Order")
        form_box.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                border: 1px solid rgba(0,0,0,0.06);
                border-radius: 8px;
                padding: 10px;
                background-color: #ffffff;
            }
        """)
        form_box.setLayout(self.entry_layout)
        content.addWidget(form_box)

        for col in self.columns:
            field = QLineEdit()
            field.setPlaceholderText(col)
            field.setFixedWidth(110)
            field.setStyleSheet("padding:6px; border:1px solid rgba(0,0,0,0.06); border-radius:6px;")
            self.entry_fields[col] = field
            self.entry_layout.addWidget(field)

        btn_save_order = QPushButton("Save Order")
        btn_save_order.setFont(QFont("Segoe UI", 12))
        btn_save_order.setCursor(Qt.PointingHandCursor)
        btn_save_order.setStyleSheet("""
            QPushButton {
                background-color: #2f80ed;
                color: white;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #1f6fd6;
            }
        """)
        btn_save_order.clicked.connect(self.save_order)
        self.entry_layout.addWidget(btn_save_order)

        # --- Orders Table ---
        self.table = QTableWidget(0, len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid rgba(0,0,0,0.04);
            }
            QHeaderView::section {
                background-color: #fafafa;
                border: none;
                padding: 8px;
            }
        """)
        content.addWidget(self.table)

        # Load recent orders
        self.load_recent_orders()

        # --- More Records Button ---
        btn_more_records = QPushButton("More Records")
        btn_more_records.setFont(QFont("Segoe UI", 12))
        btn_more_records.setCursor(Qt.PointingHandCursor)
        btn_more_records.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #e8e8e8;
            }
        """)
        btn_more_records.clicked.connect(self.load_all_orders)
        content.addWidget(btn_more_records)

        # --- Logout Button (bottom center) ---
        logout_layout = QHBoxLayout()
        btn_logout = QPushButton("Logout")
        btn_logout.setFont(QFont("Segoe UI", 14, QFont.Bold))
        btn_logout.setCursor(Qt.PointingHandCursor)
        btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border-radius: 8px;
                padding: 10px 25px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        btn_logout.clicked.connect(self.logout)

        logout_layout.addStretch()
        logout_layout.addWidget(btn_logout)
        logout_layout.addStretch()
        content.addLayout(logout_layout)

        # Add content to main area
        main_area.addLayout(content)

        # Add main area to master layout
        master_layout.addLayout(main_area)

        # Apply layout
        self.setLayout(master_layout)


    def _show_calendar(self):
        """
        Show the calendar popup positioned under the calendar button.
        """
        btn_pos = self.calendar_btn.mapToGlobal(self.calendar_btn.rect().bottomLeft())
        # Position the popup so it appears below the button
        self._calendar_popup.move(btn_pos)
        self._calendar_popup.show()

    def _on_calendar_selected(self, qdate):
        """
        Handle date selection from the popup calendar.
        Updates search_input (if present) and hides the popup.
        """
        if hasattr(self, "search_input"):
            self.search_input.setText(qdate.toString("dd-MM-yyyy"))
        self._calendar_popup.hide()

    def load_all_orders(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # ✅ Ensure table exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    lorry_no TEXT,
                    lorry_name TEXT,
                    driver_name TEXT,
                    driver_no TEXT,
                    from_place TEXT,
                    to_place TEXT,
                    freight REAL,
                    ton_age REAL,
                    advance REAL,
                    balance REAL,
                    load TEXT,
                    commission REAL
                )
            """)

            # ✅ Fetch ALL records
            cursor.execute("""
                SELECT date, lorry_no, lorry_name, driver_name, driver_no,
                    from_place, to_place, freight, ton_age,
                    advance, balance, load, commission
                FROM orders
                ORDER BY id DESC
            """)

            rows = cursor.fetchall()
            self.table.setRowCount(0)

            for row_data in rows:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                for col, value in enumerate(row_data):
                    self.table.setItem(row_position, col, QTableWidgetItem(str(value)))

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load all orders:\n{e}")

        finally:
            if 'conn' in locals():
                conn.close()

    def sidebar_button_style(self):
        return """
            QPushButton {
                background-color: #34495E;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #1ABC9C;
            }
        """


    def open_settings(self):
        QMessageBox.information(self, "Settings", "Here you can configure Golden Transport preferences.")

    # --- Database connection ---
    def get_connection(self):
        return sqlite3.connect("golden_transport.db")

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

    # --- Save Order ---
    def save_order(self):
        try:
            values = [self.entry_fields[field].text().strip() for field in self.columns]

            # Basic validation
            if not values[0] or not values[1]:
                QMessageBox.warning(self, "Input Error", "Date and Lorry No. are required.")
                return

            conn = self.get_connection()
            cursor = conn.cursor()

            # Ensure table exists (optional safety)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    lorry_no TEXT,
                    lorry_name TEXT,
                    driver_name TEXT,
                    driver_no TEXT,
                    from_place TEXT,
                    to_place TEXT,
                    freight REAL,
                    ton_age REAL,
                    advance REAL,
                    balance REAL,
                    load TEXT,
                    commission REAL
                )
            """)

            # Confirm DB schema count matches UI
            cursor.execute("PRAGMA table_info(orders)")
            db_cols = [r[1] for r in cursor.fetchall() if r[1] != 'id']
            if len(db_cols) != len(self.columns):
                QMessageBox.critical(
                    self, "Schema Mismatch",
                    f"DB has {len(db_cols)} columns, UI has {len(self.columns)}. Fix schema or UI."
                )
                conn.close()
                return

            placeholders = ", ".join(["?"] * len(self.columns))
            columns_sql = ", ".join(self.columns)
            sql = f"INSERT INTO orders ({columns_sql}) VALUES ({placeholders})"
            cursor.execute(sql, values)

            conn.commit()
            self.load_recent_orders()

            for field in self.entry_fields.values():
                field.clear()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save order:\n{e}")
        finally:
            if 'conn' in locals():
                conn.close()

        # Debug prints
        print("DEBUG db_cols =", db_cols)
        print("DEBUG ui_cols =", self.columns)
        print("DEBUG values =", values)

    def open_orders_form(self):
        self.orders_form = OrdersForm()
        self.orders_form.show()

    # --- Load recent orders ---
    def load_recent_orders(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # ✅ Ensure table exists (prevents first-run crash)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    lorry_no TEXT,
                    lorry_name TEXT,
                    driver_name TEXT,
                    driver_no TEXT,
                    from_place TEXT,
                    to_place TEXT,
                    freight REAL,
                    ton_age REAL,
                    advance REAL,
                    balance REAL,
                    load TEXT,
                    commission REAL
                )
            """)

            # ✅ Fetch latest 10 records
            cursor.execute("""
                SELECT date, lorry_no, lorry_name, driver_name, driver_no,
                    from_place, to_place, freight, ton_age,
                    advance, balance, load, commission
                FROM orders
                ORDER BY id DESC
                LIMIT 10
            """)

            rows = cursor.fetchall()

            # ✅ Clear table before loading new data
            self.table.setRowCount(0)

            # ✅ Insert data into table
            for row_data in rows:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                for col, value in enumerate(row_data):
                    self.table.setItem(row_position, col, QTableWidgetItem(str(value)))

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load orders:\n{e}")

        finally:
            if 'conn' in locals():
                conn.close()



    def search_orders(self):
        search_text = self.search_input.text().strip()
        if not search_text:
            QMessageBox.warning(self, "Error", "Enter a date or lorry number to search.")
            return

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Case 1: Full date (dd-mm-yyyy)
            if "-" in search_text and len(search_text.split("-")) == 3:
                cursor.execute("""
                    SELECT date, lorry_no, lorry_name, driver_name, driver_no,
                        from_place, to_place, freight, ton_age,
                        advance, balance, load, commission
                    FROM orders WHERE date = ?
                """, (search_text,))

            # Case 2: Only day (e.g. "29")
            elif search_text.isdigit() and len(search_text) <= 2:
                cursor.execute("""
                    SELECT date, lorry_no, lorry_name, driver_name, driver_no,
                        from_place, to_place, freight, ton_age,
                        advance, balance, load, commission
                    FROM orders
                    WHERE CAST(substr(date, 1, instr(date, '-')-1) AS INTEGER) = ?
                """, (int(search_text),))

            # Case 3: Only year (e.g. "2026")
            elif search_text.isdigit() and len(search_text) == 4:
                cursor.execute("""
                    SELECT date, lorry_no, lorry_name, driver_name, driver_no,
                        from_place, to_place, freight, ton_age,
                        advance, balance, load, commission
                    FROM orders
                    WHERE CAST(substr(date, -4) AS INTEGER) = ?
                """, (int(search_text),))

            # Case 4: Lorry number (full or partial, e.g. "MH09FL1858" or "1858")
            else:
                cursor.execute("""
                    SELECT date, lorry_no, lorry_name, driver_name, driver_no,
                        from_place, to_place, freight, ton_age,
                        advance, balance, load, commission
                    FROM orders
                    WHERE lorry_no LIKE ?
                """, (f"%{search_text}%",))


            rows = cursor.fetchall()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to search orders:\n{e}")
            return
        finally:
            conn.close()

        if not rows:
            QMessageBox.information(self, "No Records Found",
                                    f"No orders found for '{search_text}'.")
            return

        self.table.setRowCount(0)
        for row in rows:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for col, value in enumerate(row):
                self.table.setItem(row_position, col, QTableWidgetItem(str(value)))



    def open_vehicle_form(self):
        # callback ke liye self.show pass karo
        self.vehicle_window = VehicleForm(dashboard_callback=self.show)
        self.vehicle_window.showMaximized()   # full screen khulega
        # ❌ self.hide() mat likho

    # --- Open Tracking Form ---
    def open_tracking_form(self):
        if not hasattr(self, "tracking_window"):
            self.tracking_window = TrackingForm(self)
        self.tracking_window.show()

    # --- Open Billing Form ---
    def open_billing_form(self):
        self.billing_window = BillingForm(self)   # parent pass optional
        self.billing_window.show()                # ✅ new page opens

    # --- Open Reports Form ---
    def open_report_form(self):
        self.report_window = ReportForm()
        self.report_window.show()

    def show_dashboard(self):
        self.vehicle_window.close()
        self.show()

    def logout(self):
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # ✅ Close dashboard and show login window again
            self.close()
            if self.login_window:
                self.login_window.show()

