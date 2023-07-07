import sys

from PyQt5.QtCore import QSize, QEvent, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                            QLabel, QHBoxLayout, QWidget, QLineEdit,
                            QVBoxLayout)

EXCEPTION_KEYS = {
            16777248: 'SHIFT',
            16777249: 'CTRL',
            16777250: "WIN",
            16777251: 'ALT',
            Qt.RightButton: "RMB",
            Qt.LeftButton: "LMB",
            Qt.MiddleButton: "MMB",
            Qt.ExtraButton1: "M4",
            Qt.ExtraButton2: "M5",
            Qt.ExtraButton3: "M6",
            Qt.ExtraButton4: "M7",
            Qt.ExtraButton5: "M8",
            Qt.ExtraButton6: "M9",
            Qt.ExtraButton7: "M10",
            Qt.ExtraButton8: "M11",
            Qt.ExtraButton9: "M12",
            Qt.ExtraButton10: "M13",
            Qt.ExtraButton11: "M14",
            Qt.ExtraButton12: "M15",
            Qt.ExtraButton13: "M16",
            Qt.ExtraButton14: "M17",
            Qt.ExtraButton15: "M18"
        }

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("AutoClicker")
        self.setFixedSize(QSize(400, 250))
        
        press_label = QLabel("Press")
        press_label.adjustSize()
        press_label.setMaximumWidth(50)
        
        self.button_to_click = QPushButton("btn")
        self.button_to_click.adjustSize()
        self.button_to_click.setMaximumWidth(150)
        self.button_to_click.clicked.connect(self.choose_button_to_click)
        self.ready_to_change_key = False
        
        every_label = QLabel("every")
        every_label.adjustSize()
        
        every_time_click = QLineEdit('1000')
        every_time_click.adjustSize()

        mills_for_label = QLabel("mills for")
        mills_for_label.adjustSize()

        click_time = QLineEdit('0')
        click_time.adjustSize()

        seconds_label = QLabel('seconds.')
        seconds_label.adjustSize()
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(press_label)
        hbox1.addWidget(self.button_to_click)
        hbox1.addWidget(every_label)
        hbox1.addWidget(every_time_click)
        hbox1.addWidget(mills_for_label)
        hbox1.addWidget(click_time)
        hbox1.addWidget(seconds_label)

        hbox2 = QHBoxLayout()

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        
        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)
        
        self.show()

    @staticmethod
    def get_key_from_value(dictionary, value) -> str:
        for key, val in dictionary.items():
            if val == value:
                return key
        raise ValueError("Value not found in dictionary")

    def choose_button_to_click(self) -> None:
        self.ready_to_change_key = True
        self.button_to_click.setText("...")
    
    def on_key_pressed(self, event) -> None:
        key = event.key()

        try:
            symbol = QKeySequence(key).toString()
            print(f"Key pressed: {symbol}")
        except UnicodeEncodeError:
            symbol = EXCEPTION_KEYS.get(key, "ERROR")
            print(f"Key pressed: {symbol}")

        if self.ready_to_change_key:
            self.button_to_click.setText(symbol)
            self.button_to_click.last_pressed_button = key
            self.ready_to_change_key = False
    
    def on_mouse_key_pressed(self, event) -> None:
        key = event.button()

        symbol = EXCEPTION_KEYS.get(key, 'ERROR')

        if self.ready_to_change_key:
            self.button_to_click.setText(symbol)
            self.button_to_click.last_pressed_button = key
            self.ready_to_change_key = False
    
    def event(self,event):
        if event.type() == QEvent.KeyPress:
            self.on_key_pressed(event)
        elif event.type() == QEvent.MouseButtonPress:
            self.on_mouse_key_pressed(event)
        return QMainWindow.event(self, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec())