from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFrame,
    QLabel, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUIUniApp")
        self.setFixedSize(440, 500)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Coloured header
        header = QFrame()
        header.setFixedHeight(150)
        header.setStyleSheet("QFrame { background-color: #4f46e5; }")
        header_layout = QVBoxLayout(header)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.setSpacing(6)

        app_label = QLabel("GUIUniApp")
        app_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_label.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        app_label.setStyleSheet("color: white; background: transparent;")
        header_layout.addWidget(app_label)

        subtitle = QLabel("University Student Portal")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #c7d2fe; font-size: 13px; background: transparent;")
        header_layout.addWidget(subtitle)

        outer.addWidget(header)

        # White form area
        form_widget = QWidget()
        form_widget.setStyleSheet("QWidget { background-color: #ffffff; }")
        form = QVBoxLayout(form_widget)
        form.setContentsMargins(48, 36, 48, 36)
        form.setSpacing(14)

        title = QLabel("Sign In")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #0f172a; background: transparent;")
        form.addWidget(title)

        form.addSpacing(6)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email address")
        self.email_input.setFixedHeight(46)
        form.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(46)
        self.password_input.returnPressed.connect(self._on_login)
        form.addWidget(self.password_input)

        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setWordWrap(True)
        self.error_label.setFixedHeight(20)
        self.error_label.setStyleSheet("color: #dc2626; font-size: 12px; background: transparent;")
        form.addWidget(self.error_label)

        login_btn = QPushButton("Sign In")
        login_btn.setFixedHeight(46)
        login_btn.clicked.connect(self._on_login)
        form.addWidget(login_btn)

        form.addStretch()
        outer.addWidget(form_widget, 1)

    def _on_login(self):
        from gui.exception_window import ExceptionWindow
        from models.database import Database
        from gui.enrolment_window import EnrolmentWindow

        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        # check fields are not empty
        if email == "" or password == "":
            ExceptionWindow("Email and password fields cannot be empty.", self).exec()
            return

        # check email and password format separately for specific feedback
        import re
        from controllers.student_controller import EMAIL_PATTERN, PASSWORD_PATTERN
        if not re.match(EMAIL_PATTERN, email):
            ExceptionWindow("Incorrect email format.", self).exec()
            return
        if not re.match(PASSWORD_PATTERN, password):
            ExceptionWindow("Incorrect password format.", self).exec()
            return

        # search for student in database
        db = Database()
        all_students = db.read_all()
        logged_in_student = None
        email_match = None

        for student in all_students:
            if student.email == email:
                email_match = student
            if student.email == email and student.password == password:
                logged_in_student = student

        # check if student was found
        if logged_in_student is None:
            if email_match is None:
                ExceptionWindow("No account found with that email address.", self).exec()
            else:
                ExceptionWindow("Incorrect password. Please try again.", self).exec()
            return

        # open enrolment window
        self.enrolment_window = EnrolmentWindow(logged_in_student)
        self.enrolment_window.show()
        self.close()
