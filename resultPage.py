from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel

class ResultPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Result Page")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Simulation Result")
        label.setStyleSheet("font-size: 24px; font-weight: bold; color: #414360;")
        layout.addWidget(label)

        result_label = QLabel("Simulation completed successfully!")
        result_label.setStyleSheet("font-size: 18px; color: #414360;")
        layout.addWidget(result_label)

        self.setGeometry(100, 100, 400, 200)  # Adjust the size as needed
