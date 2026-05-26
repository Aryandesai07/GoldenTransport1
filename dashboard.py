import sys
import sqlite3
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QApplication, QFrame, QLineEdit, QMessageBox, QGroupBox,QDateEdit,
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from datetime import datetime
from PyQt5.QtCore import QDate

# Import forms from separate modules
from vehicles.vehicle_form import VehicleForm
from billing.billing_form import BillingForm
from reports.report_form import ReportForm
from tracking.tracking_form import TrackingForm


class Dashboard(QWidget):
    def __init__(self, login_window=None):
        super().__init__()
        self.login_window = login_window
        self.setWindowTitle("Golden Logistics - Dashboard")   # ✅ updated title
        self.resize(1200, 700)
        self.setMinimumSize(1000, 600)

        # --- Master Layout (Vertical) ---
        master_layout = QVBoxLayout()

        # --- Top Bar Frame ---
        top_frame = QFrame()
        top_frame.setFixedHeight(55)   # ✅ compact height
        top_frame.setStyleSheet("""
            background-color: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:0,
                stop:0 #1c1c1c, stop:1 #3a3a3a
            );   /* Black-gray gradient */
            border-bottom: 2px solid #444;
            padding: 6px;
        """)
        top_bar = QHBoxLayout(top_frame)
        top_bar.setContentsMargins(10, 0, 10, 0)

        # --- Logo + Branding ---
        logo_label = QLabel()
        logo_pixmap = QPixmap("assets/logo.png")   # place logo file in project folder
        logo_pixmap = logo_pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignVCenter)

        brand_label = QLabel("Golden Transport")   # ✅ clear name
        brand_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        brand_label.setStyleSheet("color: #FFD700; letter-spacing: 2px;")  # gold text

        sub_label = QLabel("Reliable Logistics")   # ✅ tagline
        sub_label.setFont(QFont("Segoe UI", 11))
        sub_label.setStyleSheet("color: white;")

        brand_layout = QVBoxLayout()
        brand_layout.addWidget(brand_label)
        brand_layout.addWidget(sub_label)
        brand_layout.setContentsMargins(10, 0, 20, 0)   # ✅ spacing
        brand_layout.setAlignment(Qt.AlignVCenter)

        logo_layout = QHBoxLayout()
        logo_layout.addWidget(logo_label)
        logo_layout.addLayout(brand_layout)
        logo_layout.setSpacing(15)   # ✅ gap between logo and text
        logo_layout.setAlignment(Qt.AlignVCenter)

        top_bar.addLayout(logo_layout)


        # --- Digital Calendar ---
        calendar = QDateEdit()
        calendar.setDisplayFormat("dd-MM-yyyy")
        calendar.setDate(QDate.currentDate())
        calendar.setCalendarPopup(True)
        calendar.setStyleSheet("""
            QDateEdit {
                background-color: #2c2c2c;
                color: white;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px 8px;
            }
        """)
        top_bar.addWidget(calendar)

        # --- Notification Icon ---
        notif_btn = QPushButton("🔔")
        notif_btn.setFixedSize(32, 32)
        notif_btn.setStyleSheet("""
            QPushButton {
                background-color: #2c2c2c;
                color: #FFD700;
                border-radius: 16px;
                border: 1px solid #555;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)
        top_bar.addWidget(notif_btn)

        # --- User Info + Logout ---
        user_label = QLabel("Aryan")
        user_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        user_label.setStyleSheet("color: #f0f0f0;")

        logout_btn = QPushButton("Logout")
        logout_btn.setFont(QFont("Segoe UI", 12))
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border-radius: 6px;
                padding: 4px 10px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        logout_btn.clicked.connect(self.logout)

        user_layout = QHBoxLayout()
        user_layout.addWidget(user_label)
        user_layout.addWidget(logout_btn)
        top_bar.addLayout(user_layout)

        # ✅ Add top bar to master layout
        master_layout.addWidget(top_frame)

        # --- Main Area (Sidebar + Content) ---
        main_area = QHBoxLayout()

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
            background-color: #2C3E50;
            color: white;
            border-right: 2px solid #1ABC9C;
        """)
        side_layout = QVBoxLayout()

        btn_dashboard = QPushButton("🏠 Dashboard")
        btn_dashboard.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_dashboard.setFixedHeight(40)
        btn_dashboard.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 6px;
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
            btn.setStyleSheet(self.sidebar_button_style())
            btn.clicked.connect(handler)
            side_layout.addWidget(btn)

        side_layout.addStretch()

        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.setFont(QFont("Segoe UI", 9))
        settings_btn.setFixedSize(100, 28)
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

        title = QLabel("Admin Dashboard")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        content.addWidget(title)

        # Date + Search Bar
        search_bar = QHBoxLayout()
        date_label = QLabel("Date: " + datetime.now().strftime("%d-%m-%Y"))
        date_label.setFont(QFont("Segoe UI", 14))
        search_bar.addWidget(date_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Date (dd-mm-yyyy)")
        self.search_input.setFixedWidth(200)
        search_bar.addWidget(self.search_input)

        btn_search = QPushButton("Search")
        btn_search.setFont(QFont("Segoe UI", 12))
        btn_search.clicked.connect(self.search_orders)
        search_bar.addWidget(btn_search)

        search_bar.addStretch()
        content.addLayout(search_bar)

        # Stats Row
        stats_layout = QHBoxLayout()
        for stat in ["Total Vehicles", "Active Trips", "Completed Deliveries", "Pending Orders", "Total Revenue"]:
            box = QLabel(stat + "\n0")
            box.setFont(QFont("Segoe UI", 14))
            box.setStyleSheet("background-color: #f0f0f0; border-radius: 10px; padding: 20px;")
            box.setAlignment(Qt.AlignCenter)
            stats_layout.addWidget(box)
        content.addLayout(stats_layout)

        # Entry Fields + Save Order
        self.entry_layout = QHBoxLayout()
        self.entry_fields = {}
        self.columns = ["Date", "Lorry No", "Lorry Name", "Driver Name", "From", "To",
                        "Freight", "Ton Age", "Advance", "Balance", "Load", "Commission"]
        form_box = QGroupBox("Add New Order")
        form_box.setLayout(self.entry_layout)
        content.addWidget(form_box)

        for col in self.columns:
            field = QLineEdit()
            field.setPlaceholderText(col)
            field.setFixedWidth(110)
            self.entry_fields[col] = field
            self.entry_layout.addWidget(field)

        btn_save_order = QPushButton("Save Order")
        btn_save_order.setFont(QFont("Segoe UI", 12))
        btn_save_order.clicked.connect(self.save_order)
        self.entry_layout.addWidget(btn_save_order)

        # Orders Table
        self.table = QTableWidget(0, len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        content.addWidget(self.table)

        self.load_recent_orders()

        # More Records Button
        btn_more_records = QPushButton("More Records")
        btn_more_records.setFont(QFont("Segoe UI", 12))
        btn_more_records.clicked.connect(self.load_all_orders)
        content.addWidget(btn_more_records)

        # --- Logout Button (bottom center) ---
        logout_layout = QHBoxLayout()
        btn_logout = QPushButton("Logout")
        btn_logout.setFont(QFont("Segoe UI", 14, QFont.Bold))
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
        logout_layout.addWidget(btn_logout, alignment=Qt.AlignCenter)
        content.addLayout(logout_layout)

        # ✅ Add content to main area
        main_area.addLayout(content)

        # ✅ Add main area to master layout
        master_layout.addLayout(main_area)

        # ✅ Apply layout to the widget
        self.setLayout(master_layout)



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
                    lorry_no TEXT,
                    driver_name TEXT,
                    from_place TEXT,
                    to_place TEXT,
                    freight TEXT,
                    ton_age TEXT,
                    advance TEXT,
                    balance TEXT,
                    load TEXT,
                    commission TEXT
                )
            """)

            # ✅ Fetch ALL records
            cursor.execute("""
                SELECT date, lorry_no, lorry_no, driver_name,
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

    # --- Save Order ---
    def save_order(self):
        try:
            values = [self.entry_fields[field].text().strip() for field in self.columns]

            if not values[0] or not values[1]:
                QMessageBox.warning(self, "Input Error", "Date and Lorry No. are required.")
                return

            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    lorry_no TEXT,
                    driver_name TEXT,
                    from_place TEXT,
                    to_place TEXT,
                    freight TEXT,
                    ton_age TEXT,
                    advance TEXT,
                    balance TEXT,
                    load TEXT,
                    commission TEXT
                )
            """)

            cursor.execute("""
                INSERT INTO orders (
                    date, lorry_no, lorry_no, driver_name,
                    from_place, to_place, freight, ton_age,
                    advance, balance, load, commission
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, values)

            conn.commit()
            self.load_recent_orders()

            for field in self.entry_fields.values():
                field.clear()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save order:\n{e}")
        finally:
            if 'conn' in locals():
                conn.close()

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
                    lorry_no TEXT,
                    driver_name TEXT,
                    from_place TEXT,
                    to_place TEXT,
                    freight TEXT,
                    ton_age TEXT,
                    advance TEXT,
                    balance TEXT,
                    load TEXT,
                    commission TEXT
                )
            """)

            # ✅ Fetch latest 10 records
            cursor.execute("""
                SELECT date, lorry_no, lorry_no, driver_name,
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
        search_date = self.search_input.text().strip()
        if not search_date:
            QMessageBox.warning(self, "Error", "Enter a date to search.")
            return

        conn = self.get_connection()
        cursor = conn.cursor()

        # Case 1: Full date (dd-mm-yyyy)
        if "-" in search_date and len(search_date.split("-")) == 3:
            cursor.execute("""
                SELECT date, lorry_no, lorry_no, driver_name,
                    from_place, to_place, freight, ton_age,
                    advance, balance, load, commission
                FROM orders WHERE date = ?
            """, (search_date,))

        # Case 2: Only day (e.g. "29")
        elif search_date.isdigit() and len(search_date) <= 2:
            cursor.execute("""
                SELECT date, lorry_no, lorry_no, driver_name,
                    from_place, to_place, freight, ton_age,
                    advance, balance, load, commission
                FROM orders
                WHERE CAST(substr(date, 1, instr(date, '-')-1) AS INTEGER) = ?
            """, (int(search_date),))

        # Case 3: Only year (e.g. "2026")
        elif search_date.isdigit() and len(search_date) == 4:
            cursor.execute("""
                SELECT date, lorry_no, lorry_no, driver_name,
                    from_place, to_place, freight, ton_age,
                    advance, balance, load, commission
                FROM orders
                WHERE CAST(substr(date, -4) AS INTEGER) = ?
            """, (int(search_date),))

        else:
            QMessageBox.warning(self, "Error", f"Invalid date format: {search_date}")
            conn.close()
            return

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            QMessageBox.information(self, "No Records Found",
                                    f"No orders found for '{search_date}'.")
            return

        self.table.setRowCount(0)

        for row in rows:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for col, value in enumerate(row):
                self.table.setItem(row_position, col, QTableWidgetItem(str(value)))

    # --- Open Vehicles Form ---
    def open_vehicle_form(self):
        self.vehicle_window = VehicleForm(dashboard_callback=self.show_dashboard)
        self.vehicle_window.show()
        self.hide()

    # --- Open Tracking Form ---
    def open_tracking_form(self):
        if not hasattr(self, "tracking_window"):
            self.tracking_window = TrackingForm(self)
        self.tracking_window.show()

    # --- Open Billing Form ---
    def open_billing_form(self):
        self.billing_window = BillingForm(self)   # parent pass karna optional hai
        self.billing_window.show()                # ✅ new page open hoga

    # --- Open Reports Form ---
    def open_report_form(self):
        from reports.report_form import ReportForm
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