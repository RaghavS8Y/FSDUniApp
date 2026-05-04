import sys
from PyQt6.QtWidgets import QApplication
from gui.login_window import LoginWindow

APP_STYLE = """
    QWidget {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
        color: #0f172a;
    }
    QLineEdit {
        background-color: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 14px;
        color: #0f172a;
        selection-background-color: #c7d2fe;
    }
    QLineEdit:focus {
        border-color: #6366f1;
    }
    QPushButton {
        background-color: #6366f1;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 11px 20px;
        font-size: 14px;
        font-weight: bold;
        min-height: 40px;
    }
    QPushButton:hover {
        background-color: #4f46e5;
    }
    QPushButton:pressed {
        background-color: #4338ca;
    }
    QListWidget {
        background-color: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 4px;
        outline: none;
        font-size: 13px;
        color: #0f172a;
    }
    QListWidget::item {
        padding: 10px 14px;
        border-radius: 6px;
        color: #1e293b;
    }
    QListWidget::item:alternate {
        background-color: #f8fafc;
    }
    QListWidget::item:hover {
        background-color: #f1f5f9;
    }
    QListWidget::item:selected {
        background-color: #ede9fe;
        color: #4f46e5;
    }
    QTableWidget {
        background-color: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        gridline-color: #f1f5f9;
        outline: none;
        selection-background-color: #ede9fe;
        selection-color: #4f46e5;
    }
    QTableWidget::item {
        padding: 10px 16px;
    }
    QHeaderView::section {
        background-color: #6366f1;
        color: white;
        padding: 10px 16px;
        border: none;
        font-weight: bold;
        font-size: 13px;
    }
    QScrollBar:vertical {
        width: 6px;
        background: transparent;
        margin: 0;
    }
    QScrollBar::handle:vertical {
        background: #cbd5e1;
        border-radius: 3px;
        min-height: 20px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0;
    }
"""


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
