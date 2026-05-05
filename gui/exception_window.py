from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFrame, QWidget, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ExceptionWindow(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ERROR")
        self.setFixedSize(380, 230)
        self.setStyleSheet("QDialog { background-color: #ffffff; }")
        self._build_ui(message)

    def _build_ui(self, message):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Red accent strip at top
        strip = QFrame()
        strip.setFixedHeight(5)
        strip.setStyleSheet("QFrame { background-color: #dc2626; }")
        outer.addWidget(strip)

        # Content
        content = QWidget()
        content.setStyleSheet("QWidget { background-color: #ffffff; }")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(36, 20, 36, 28)
        content_layout.setSpacing(10)

        icon_label = QLabel("ERROR")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 34px; color: #dc2626; background: transparent;")


        title_label = QLabel("Something went wrong")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #0f172a; background: transparent;")
        content_layout.addWidget(title_label)

        msg_label = QLabel(message)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setWordWrap(True)
        msg_label.setStyleSheet("color: #64748b; font-size: 13px; background: transparent;")
        content_layout.addWidget(msg_label)

        content_layout.addSpacing(6)

        ok_btn = QPushButton("OK")
        ok_btn.setFixedHeight(42)
        ok_btn.clicked.connect(self.accept)
        content_layout.addWidget(ok_btn)

        outer.addWidget(content, 1)
