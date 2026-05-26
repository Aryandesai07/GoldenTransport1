from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon

class WhatsAppMenu(QGroupBox):
    def __init__(self, parent=None):
        # remove or change the title text
        super().__init__("", parent)   # no title shown
        layout = QVBoxLayout()

        chat_btn = QPushButton("💬 New Chat")
        status_btn = QPushButton("📸 Status")
        calls_btn = QPushButton("📞 Calls")

        for btn in [chat_btn, status_btn, calls_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    color: #333;
                    padding: 6px 10px;
                    border-radius: 4px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            layout.addWidget(btn)

        self.setLayout(layout)

