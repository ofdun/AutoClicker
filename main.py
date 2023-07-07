import sys

from PyQt5.QtCore import QSize, QEvent, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                            QLabel, QHBoxLayout, QWidget, QLineEdit,
                            QVBoxLayout)
import configparser

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
        
        self.button_to_click = QPushButton('')
        self.button_to_click.last = ''
        self.button_to_click.adjustSize()
        self.button_to_click.setMaximumWidth(150)
        self.button_to_click.clicked.connect(self.choose_button_to_click)
        self.ready_to_change_key = False
        
        every_label = QLabel("every")
        every_label.adjustSize()
        
        self.every_time_click = QLineEdit('')
        self.every_time_click.adjustSize()

        mills_for_label = QLabel("mills for")
        mills_for_label.adjustSize()

        self.click_time = QLineEdit('')
        self.click_time.adjustSize()

        seconds_label = QLabel('seconds.')
        seconds_label.adjustSize()
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(press_label)
        hbox1.addWidget(self.button_to_click)
        hbox1.addWidget(every_label)
        hbox1.addWidget(self.every_time_click)
        hbox1.addWidget(mills_for_label)
        hbox1.addWidget(self.click_time)
        hbox1.addWidget(seconds_label)

        reset_button = QPushButton("Reset Config")
        reset_button.adjustSize()
        reset_button.clicked.connect(self.reset_config)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(reset_button)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        
        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)
        self.render_config_updates()

        self.show()

    @staticmethod
    def get_key_from_value(dictionary, value) -> str:
        for key, val in dictionary.items():
            if val == value:
                return key
        raise ValueError("Value not found in dictionary")
    
    @staticmethod
    def load_config() -> configparser.ConfigParser:
        cfg = configparser.ConfigParser()
        cfg.read_file(open('config.cfg'))
        return cfg
    
    def render_config_updates(self):
        cfg = self.load_config()
        default_button = cfg.get('DEFAULT', 'button_to_press')
        click_every = cfg.get('DEFAULT', 'click_every')
        for_seconds = cfg.get('DEFAULT', 'for_seconds')
        self.button_to_click.setText(default_button)
        self.button_to_click.last = default_button
        self.every_time_click.setText(click_every)
        self.click_time.setText(for_seconds)
    
    def reset_config(self):
        cfg = self.load_config()
        cfg['DEFAULT'] = {
            'button_to_press': "LMB",
            'click_every': "1000",
            'for_seconds': "0"
        }
        with open('config.cfg', 'w') as configfile:
            cfg.write(configfile)
        self.render_config_updates()

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
            self.button_to_click.last = symbol
            self.ready_to_change_key = False
    
    def on_mouse_key_pressed(self, event) -> None:
        key = event.button()

        symbol = EXCEPTION_KEYS.get(key, 'ERROR')

        if self.ready_to_change_key:
            self.button_to_click.setText(symbol)
            self.ready_to_change_key = False
    
    def event(self,event):
        if event.type() == QEvent.KeyPress:
            self.on_key_pressed(event)
        elif event.type() == QEvent.MouseButtonPress:
            self.on_mouse_key_pressed(event)
        return QMainWindow.event(self, event)
    
    def closeEvent(self, a0) -> None:
        cfg = self.load_config()
        cfg['DEFAULT'] = {
            'button_to_press': self.button_to_click.last,
            'click_every': self.every_time_click.text(),
            'for_seconds': self.click_time.text()
        }
        with open('config.cfg', 'w') as configfile:
            cfg.write(configfile)
        return super().closeEvent(a0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec())