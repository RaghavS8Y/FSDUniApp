import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("My First PyQt App")
window.resize(300, 100)

label = QLabel("Hello, PyQt!", parent=window)
label.move(90, 40)

window.show()
sys.exit(app.exec())