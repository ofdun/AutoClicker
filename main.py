import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                            QLabel, QHBoxLayout, QWidget, QLineEdit,
                            QSizePolicy)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AutoClicker")
        self.setFixedSize(QSize(600, 400))
        
        press_label = QLabel("Press")
        press_label.adjustSize()
        press_label.setMaximumWidth(50)
        
        button_to_click = QPushButton("btn")
        button_to_click.adjustSize()
        button_to_click.setMaximumWidth(150)
        
        every_label = QLabel("every")
        every_label.adjustSize()
        
        number_of_mills_to_click = QLineEdit('1000')
        number_of_mills_to_click.adjustSize()
        
        layout = QHBoxLayout()
        layout.addWidget(press_label)
        layout.addWidget(button_to_click)
        layout.addWidget(every_label)
        layout.addWidget(number_of_mills_to_click)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec())