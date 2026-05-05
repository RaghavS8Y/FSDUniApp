from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame,
    QLabel, QPushButton, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class EnrolmentWindow(QMainWindow):
    def __init__(self, student):
        super().__init__()
        self.student = student
        self.setWindowTitle("GUIUniApp - Enrolment")
        self.setFixedSize(560, 560)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Header bar
        header = QFrame()
        header.setFixedHeight(64)
        header.setStyleSheet("QFrame { background-color: #4f46e5; }")
        header_row = QHBoxLayout(header)
        header_row.setContentsMargins(24, 0, 24, 0)

        app_label = QLabel("GUIUniApp")
        app_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        app_label.setStyleSheet("color: white; background: transparent;")
        header_row.addWidget(app_label)

        header_row.addStretch()

        logout_btn = QPushButton("Logout")
        logout_btn.setFixedSize(84, 36)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: 2px solid rgba(255,255,255,0.55);
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                min-height: 0px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.15);
                border-color: white;
            }
            QPushButton:pressed {
                background-color: rgba(255,255,255,0.25);
            }
        """)
        logout_btn.clicked.connect(self._on_logout)
        header_row.addWidget(logout_btn)

        outer.addWidget(header)

        # Content area
        content = QWidget()
        content.setStyleSheet("QWidget { background-color: #f1f5f9; }")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(32, 28, 32, 28)
        content_layout.setSpacing(14)

        welcome_label = QLabel(f"Welcome, {self.student.name}")
        welcome_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        welcome_label.setStyleSheet("color: #0f172a; background: transparent;")
        content_layout.addWidget(welcome_label)

        self.count_label = QLabel()
        self.count_label.setStyleSheet("color: #64748b; font-size: 13px; background: transparent;")
        content_layout.addWidget(self.count_label)

        content_layout.addSpacing(4)

        self.subject_list = QListWidget()
        self.subject_list.setAlternatingRowColors(True)
        self.subject_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._refresh_list()
        content_layout.addWidget(self.subject_list)

        content_layout.addSpacing(4)

        self.enrol_btn = QPushButton("+ Enrol in Subject")
        self.enrol_btn.setFixedHeight(46)
        self.enrol_btn.clicked.connect(self._on_enrol)
        content_layout.addWidget(self.enrol_btn)

        view_btn = QPushButton("View Subject Details")
        view_btn.setFixedHeight(46)
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: #e2e8f0;
                color: #1e293b;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                min-height: 0px;
            }
            QPushButton:hover { background-color: #cbd5e1; }
            QPushButton:pressed { background-color: #94a3b8; }
        """)
        view_btn.clicked.connect(self._on_view)
        content_layout.addWidget(view_btn)

        outer.addWidget(content, 1)

    def _refresh_list(self):
        self.subject_list.clear()
        if not self.student.subjects:
            item = QListWidgetItem("No subjects enrolled yet.")
            item.setForeground(Qt.GlobalColor.gray)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.subject_list.addItem(item)
        else:
            for s in self.student.subjects:
                self.subject_list.addItem(
                    f"  Subject {s.subject_id}    ·    Mark: {s.mark}    ·    Grade: {s.grade}"
                )
        self.count_label.setText(
            f"Enrolled in {len(self.student.subjects)} of 4 subjects"
        )

    def _on_enrol(self):
        from gui.exception_window import ExceptionWindow
        from models.subject import Subject
        from models.database import Database

        # check enrolment limit
        if len(self.student.subjects) >= 4:
            ExceptionWindow("Students are allowed to enrol in 4 subjects only.", self).exec()
            return

        # create new subject and add to student
        new_subject = Subject()
        self.student.subjects.append(new_subject)

        # save updated student back to database
        db = Database()
        all_students = db.read_all()

        for i in range(len(all_students)):
            if all_students[i].student_id == self.student.student_id:
                all_students[i] = self.student

        db.write_all(all_students)

        self._refresh_list()

    def _on_view(self):
        from gui.subject_window import SubjectWindow
        self.subject_window = SubjectWindow(self.student.subjects, parent=self)
        self.subject_window.show()

    def _on_logout(self):
        from gui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
