from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ExceptionWindow(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Error")
        self.setFixedSize(360, 160)
        self._build_ui(message)

    def _build_ui(self, message):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        icon_label = QLabel("⚠")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setFont(QFont("Arial", 24))
        layout.addWidget(icon_label)

        msg_label = QLabel(message)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setWordWrap(True)
        msg_label.setStyleSheet("color: red; font-size: 13px;")
        layout.addWidget(msg_label)

        ok_btn = QPushButton("OK")
        ok_btn.setFixedHeight(34)
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)
