from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


GRADE_COLOURS = {
    "HD": "#2e7d32",
    "D":  "#1565c0",
    "C":  "#6a1e9a",
    "P":  "#e65100",
    "Z":  "#b71c1c",
}


class SubjectWindow(QMainWindow):
    def __init__(self, subjects=None, parent=None):
        super().__init__(parent)
        self.subjects = subjects or []
        self.setWindowTitle("GUIUniApp - Enrolled Subjects")
        self.setFixedSize(460, 360)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel(f"Showing {len(self.subjects)} subject{'s' if len(self.subjects) != 1 else ''}")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Subject ID", "Mark", "Grade"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self._populate_table()
        layout.addWidget(self.table)

        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(36)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

    def _populate_table(self):
        self.table.setRowCount(len(self.subjects))
        for row, subject in enumerate(self.subjects):
            id_item = QTableWidgetItem(str(subject.subject_id))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            mark_item = QTableWidgetItem(str(subject.mark))
            mark_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            grade_item = QTableWidgetItem(subject.grade)
            grade_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            colour = GRADE_COLOURS.get(subject.grade, "#000000")
            grade_item.setForeground(__import__("PyQt6.QtGui", fromlist=["QColor"]).QColor(colour))

            self.table.setItem(row, 0, id_item)
            self.table.setItem(row, 1, mark_item)
            self.table.setItem(row, 2, grade_item)
