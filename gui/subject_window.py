from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFrame,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor


GRADE_STYLES = {
    "HD": ("#166534", "#dcfce7"),
    "D":  ("#1e40af", "#dbeafe"),
    "C":  ("#6b21a8", "#f3e8ff"),
    "P":  ("#9a3412", "#ffedd5"),
    "Z":  ("#991b1b", "#fee2e2"),
}


class SubjectWindow(QMainWindow):
    def __init__(self, subjects=None, parent=None):
        super().__init__(parent)
        self.subjects = subjects or []
        self.setWindowTitle("GUIUniApp - Subjects")
        self.setFixedSize(500, 420)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Header
        header = QFrame()
        header.setFixedHeight(64)
        header.setStyleSheet("QFrame { background-color: #4f46e5; }")
        header_layout = QVBoxLayout(header)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.setContentsMargins(24, 0, 24, 0)

        count = len(self.subjects)
        header_label = QLabel(f"Enrolled Subjects  ({count} / 4)")
        header_label.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        header_label.setStyleSheet("color: white; background: transparent;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(header_label)

        outer.addWidget(header)

        # Content
        content = QWidget()
        content.setStyleSheet("QWidget { background-color: #f1f5f9; }")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(28, 24, 28, 24)
        content_layout.setSpacing(14)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Subject ID", "Mark", "Grade"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setColumnWidth(0, 160)
        self.table.setColumnWidth(1, 100)
        self._populate_table()
        content_layout.addWidget(self.table)

        if self.subjects:
            avg = sum(s.mark for s in self.subjects) / len(self.subjects)
            avg_label = QLabel(f"Average mark: {avg:.1f}")
            avg_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            avg_label.setStyleSheet("color: #64748b; font-size: 12px; background: transparent;")
            content_layout.addWidget(avg_label)

        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(46)
        close_btn.setStyleSheet("""
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
        close_btn.clicked.connect(self.close)
        content_layout.addWidget(close_btn)

        outer.addWidget(content, 1)

    def _populate_table(self):
        self.table.setRowCount(len(self.subjects))
        for row, subject in enumerate(self.subjects):
            self.table.setRowHeight(row, 46)

            id_item = QTableWidgetItem(f"Subject {subject.subject_id}")
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            mark_item = QTableWidgetItem(str(subject.mark))
            mark_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            grade_item = QTableWidgetItem(subject.grade)
            grade_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            fg, bg = GRADE_STYLES.get(subject.grade, ("#374151", "#f3f4f6"))
            grade_item.setForeground(QColor(fg))
            grade_item.setBackground(QColor(bg))

            self.table.setItem(row, 0, id_item)
            self.table.setItem(row, 1, mark_item)
            self.table.setItem(row, 2, grade_item)
