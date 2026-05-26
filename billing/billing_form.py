import os
import subprocess
import sys
import sqlite3
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QTimer, QDateTime
from datetime import datetime

from whatsapp.whatsapp_menu import WhatsAppMenu

class BillingForm(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Golden Transport - Billing")
        self.setGeometry(250, 120, 950, 600)

        ## --- Central Widget ---
        central_widget = QWidget()
        main_layout = QVBoxLayout()          # layout without parent
        central_widget.setLayout(main_layout)  # attach layout to widget
        self.setCentralWidget(central_widget)

        # --- Header with Title + Live Time + Dashboard Button ---
        header_layout = QHBoxLayout()

        title = QLabel("💰 Billing Page")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header_layout.addWidget(title)

        # Live Time
        self.time_label = QLabel()
        self.time_label.setFont(QFont("Segoe UI", 12))
        header_layout.addWidget(self.time_label)

        # Update time every second
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time()

        # Dashboard Button
        btn_dashboard = QPushButton("⬅ Back to Dashboard")
        btn_dashboard.setStyleSheet("background-color:#2980b9; color:white; padding:6px; border-radius:6px;")
        btn_dashboard.clicked.connect(self.back_to_dashboard)
        header_layout.addWidget(btn_dashboard)

        main_layout.addLayout(header_layout)

        # --- Invoice Section ---
        form_layout = QHBoxLayout()

        left_layout = QVBoxLayout()

        self.invoice_date = QLineEdit()
        self.invoice_date.setPlaceholderText("Invoice Date (YYYY-MM-DD)")
        left_layout.addWidget(self.invoice_date)

        self.due_date = QLineEdit()
        self.due_date.setPlaceholderText("Due Date (YYYY-MM-DD)")
        left_layout.addWidget(self.due_date)

        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Customer Name")
        left_layout.addWidget(self.customer_name)

        self.broker_commission = QLineEdit()
        self.broker_commission.setPlaceholderText("Broker Commission")
        left_layout.addWidget(self.broker_commission)

        self.transport_charges = QLineEdit()
        self.transport_charges.setPlaceholderText("Transport Charges")
        left_layout.addWidget(self.transport_charges)

        self.taxes = QLineEdit()
        self.taxes.setPlaceholderText("Taxes")
        left_layout.addWidget(self.taxes)

        form_layout.addLayout(left_layout)

        right_layout = QVBoxLayout()
        self.payment_status = QComboBox()
        self.payment_status.addItems(["Paid", "Pending", "Overdue"])
        right_layout.addWidget(self.payment_status)

        self.payment_mode = QComboBox()
        self.payment_mode.addItems(["Cash", "Bank Transfer", "UPI"])
        right_layout.addWidget(self.payment_mode)

        btn_save = QPushButton("💾 Save Invoice")
        btn_save.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_save.setStyleSheet("background-color:#27ae60; color:white; padding:8px; border-radius:6px;")
        btn_save.clicked.connect(self.save_invoice)
        right_layout.addWidget(btn_save)

        form_layout.addLayout(right_layout)
        main_layout.addLayout(form_layout)
        #Whatsapp button in top bar
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
        header_layout.addWidget(self.whatsapp_btn)
        # --- Ledger Table ---
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels([
            "Invoice No", "Customer", "Broker", "Transport", "Taxes",
            "Total", "Status", "Mode"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)

        # --- Export + Email Buttons ---
        export_layout = QHBoxLayout()

        btn_pdf = QPushButton("📄 Export PDF")
        btn_pdf.setStyleSheet("background-color:#2980b9; color:white; padding:6px; border-radius:6px;")
        btn_pdf.clicked.connect(self.export_pdf)
        export_layout.addWidget(btn_pdf)

        btn_excel = QPushButton("📊 Export Excel")
        btn_excel.setStyleSheet("background-color:#f39c12; color:white; padding:6px; border-radius:6px;")
        btn_excel.clicked.connect(self.export_excel)
        export_layout.addWidget(btn_excel)

        btn_email = QPushButton("✉ Email Invoice")
        btn_email.setStyleSheet("background-color:#8e44ad; color:white; padding:6px; border-radius:6px;")
        btn_email.clicked.connect(self.email_invoice)
        export_layout.addWidget(btn_email)

        main_layout.addLayout(export_layout)

        self.load_invoices()

    # --- Live Time Update ---
    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("dd-MM-yyyy hh:mm:ss")
        self.time_label.setText(f"🕒 {current_time}")

    # --- Back to Dashboard ---
    def back_to_dashboard(self):
        self.close()
        if self.parent:
            self.parent.show()

    def generate_invoice_no(self):
        year = datetime.now().strftime("%Y")
        conn = sqlite3.connect("golden_transport.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM billing")
        count = cursor.fetchone()[0] + 1
        conn.close()
        return f"INV{year}-{count:03d}"

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
    # --- Save Invoice ---
    def save_invoice(self):
        # Validate required fields
        if not self.customer_name.text().strip():
            QMessageBox.warning(self, "Validation", "Customer Name is required.")
            return
        if not self.broker_commission.text().strip():
            QMessageBox.warning(self, "Validation", "Broker Commission is required.")
            return
        if not self.transport_charges.text().strip():
            QMessageBox.warning(self, "Validation", "Transport Charges are required.")
            return
        if not self.taxes.text().strip():
            QMessageBox.warning(self, "Validation", "Taxes are required.")
            return
        if not self.invoice_date.text().strip():
            QMessageBox.warning(self, "Validation", "Invoice Date is required.")
            return
        if not self.due_date.text().strip():
            QMessageBox.warning(self, "Validation", "Due Date is required.")
            return
        
        # Generate invoice number
        invoice_no = self.generate_invoice_no()
        customer = self.customer_name.text().strip()
        broker = float(self.broker_commission.text())
        transport = float(self.transport_charges.text())
        taxes = float(self.taxes.text())
        total = broker + transport + taxes
        status = self.payment_status.currentText()
        mode = self.payment_mode.currentText()
        invoice_date = self.invoice_date.text().strip()
        due_date = self.due_date.text().strip()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save to DB
        conn = sqlite3.connect("golden_transport.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO billing (invoice_no, customer_name, broker_commission,
            transport_charges, taxes, total_amount, payment_status, payment_mode,
            invoice_date, due_date, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (invoice_no, customer, broker, transport, taxes, total,
            status, mode, invoice_date, due_date, created_at))
        conn.commit()
        conn.close()

        # Success message
        QMessageBox.information(self, "Success", f"Invoice {invoice_no} saved!")
        self.load_invoices()

        # --- Clear fields after save ---
        self.customer_name.clear()
        self.broker_commission.clear()
        self.transport_charges.clear()
        self.taxes.clear()
        self.invoice_date.clear()
        self.due_date.clear()
        self.payment_status.setCurrentIndex(0)
        self.payment_mode.setCurrentIndex(0)

    # --- Load Invoices ---
    def load_invoices(self):
        conn = sqlite3.connect("golden_transport.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT invoice_no, customer_name, broker_commission, transport_charges,
                   taxes, total_amount, payment_status, payment_mode
            FROM billing ORDER BY id DESC LIMIT 10
        """)
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(0)
        for row in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))

    # --- Export PDF ---
    def export_pdf(self):
        QMessageBox.information(self, "Export", "PDF export feature will be added here.")

    # --- Export Excel ---
    def export_excel(self):
        QMessageBox.information(self, "Export", "Excel export feature will be added here.")

    # --- Email Invoice ---
    def email_invoice(self):
        QMessageBox.information(self, "Email", "Email sending feature will be added here.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BillingForm()
    window.show()
    sys.exit(app.exec_())