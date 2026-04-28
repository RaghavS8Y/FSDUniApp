from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class EnrolmentWindow(QMainWindow):
    def __init__(self, student_name="Student", subjects=None):
        super().__init__()
        self.student_name = student_name
        self.subjects = subjects or []
        self.setWindowTitle("GUIUniApp - Enrolment")
        self.setFixedSize(500, 420)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel(f"Welcome, {self.student_name}")
        title.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.count_label = QLabel(f"Enrolled: {len(self.subjects)} / 4")
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.count_label.setStyleSheet("color: gray; font-size: 12px;")
        layout.addWidget(self.count_label)

        self.subject_list = QListWidget()
        self.subject_list.setFixedHeight(180)
        self._refresh_list()
        layout.addWidget(self.subject_list)

        btn_row = QHBoxLayout()

        self.enrol_btn = QPushButton("Enrol in Subject")
        self.enrol_btn.setFixedHeight(36)
        self.enrol_btn.clicked.connect(self._on_enrol)
        btn_row.addWidget(self.enrol_btn)

        view_btn = QPushButton("View Subjects")
        view_btn.setFixedHeight(36)
        view_btn.clicked.connect(self._on_view)
        btn_row.addWidget(view_btn)

        layout.addLayout(btn_row)

        logout_btn = QPushButton("Logout")
        logout_btn.setFixedHeight(36)
        logout_btn.setStyleSheet("color: red;")
        logout_btn.clicked.connect(self._on_logout)
        layout.addWidget(logout_btn)

    def _refresh_list(self):
        self.subject_list.clear()
        if not self.subjects:
            item = self.subject_list.addItem("No subjects enrolled yet.")
        else:
            for s in self.subjects:
                self.subject_list.addItem(
                    f"[ Subject::{s.subject_id} -- mark = {s.mark} -- grade = {s.grade} ]"
                )
        self.count_label.setText(f"Enrolled: {len(self.subjects)} / 4")

    def _on_enrol(self):
        if len(self.subjects) >= 4:
            from gui.exception_window import ExceptionWindow
            ExceptionWindow("Students are allowed to enrol in 4 subjects only.", self).exec()
            return
        # Will be wired to SubjectController.enrol_subject() later

    def _on_view(self):
        from gui.subject_window import SubjectWindow
        self.subject_window = SubjectWindow(self.subjects, parent=self)
        self.subject_window.show()

    def _on_logout(self):
        from gui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
