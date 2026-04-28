from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUIUniApp")
        self.setFixedSize(420, 320)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(12)
        layout.setContentsMargins(50, 40, 50, 40)

        title = QLabel("Student Sign In")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        layout.addSpacing(10)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setFixedHeight(36)
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(36)
        layout.addWidget(self.password_input)

        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setStyleSheet("color: red; font-size: 12px;")
        layout.addWidget(self.error_label)

        login_btn = QPushButton("Login")
        login_btn.setFixedHeight(38)
        login_btn.setStyleSheet("font-size: 14px;")
        login_btn.clicked.connect(self._on_login)
        layout.addWidget(login_btn)

    def _on_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            from gui.exception_window import ExceptionWindow
            ExceptionWindow("Email and password fields cannot be empty.", self).exec()
            return

        # Placeholder until StudentController is wired in
        from gui.enrolment_window import EnrolmentWindow
        self.enrolment_window = EnrolmentWindow(student_name="Test Student")
        self.enrolment_window.show()
        self.close()
