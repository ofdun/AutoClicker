import sys
import os
from PyQt5.QtCore import QSize, QEvent, Qt
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QWidget,
    QLineEdit,
    QVBoxLayout)
import configparser
import keyboard
import mouse
from math import inf
from time import sleep
from threading import Thread

EXCEPTION_KEYS = {
    16777248: "SHIFT",
    16777249: "CTRL",
    16777250: "WIN",
    16777251: "ALT",
}
MOUSE_KEYS = {
    Qt.RightButton: "RMB",
    Qt.LeftButton: "LMB"
}
REVERSE_MOUSE_KEYS = {
    "LMB": Qt.LeftButton,
    "RMB": Qt.RightButton
}

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        if 'config.cfg' not in os.listdir():
            self.create_config()

        self.setWindowTitle("AutoClicker")
        self.setWindowIcon(QIcon('icon.ico'))
        self.setFixedSize(QSize(400, 250))

        press_label = QLabel("Press")
        press_label.adjustSize()
        press_label.setMaximumWidth(50)

        self.button_to_click = QPushButton()
        self.button_to_click.last = ""
        self.button_to_click.adjustSize()
        self.button_to_click.setMaximumWidth(150)
        self.button_to_click.clicked.connect(self.choose_button_to_click)
        self.ready_to_change_key = False

        every_label = QLabel("every")
        every_label.adjustSize()

        self.every_time_click = QLineEdit()
        self.every_time_click.adjustSize()
        self.every_time_click.setMaximumWidth(50)

        mills_for_label = QLabel("milliseconds for")
        mills_for_label.adjustSize()

        self.click_time = QLineEdit()
        self.click_time.adjustSize()
        self.click_time.setMaximumWidth(50)

        seconds_label = QLabel("seconds.")
        seconds_label.adjustSize()

        hbox1 = QHBoxLayout()
        hbox1.addWidget(press_label)
        hbox1.addWidget(self.button_to_click)
        hbox1.addWidget(every_label)
        hbox1.addWidget(self.every_time_click)
        hbox1.addWidget(mills_for_label)
        hbox1.addWidget(self.click_time)
        hbox1.addWidget(seconds_label)

        self.started = False

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_pressing)
        self.start_button.adjustSize()
        self.start_button.setMaximumWidth(100)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_pressing)
        self.stop_button.adjustSize()
        self.stop_button.setMaximumWidth(100)

        self.rebind_start_button = QPushButton()
        self.rebind_start_button.clicked.connect(self.choose_button_to_start)
        self.rebind_start_button.adjustSize()
        self.rebind_start_button.setMaximumWidth(100)
        self.ready_to_change_start_key = False

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.start_button)
        hbox2.addWidget(self.stop_button)
        hbox2.addWidget(self.rebind_start_button)

        reset_button = QPushButton("Reset Config")
        reset_button.adjustSize()
        reset_button.clicked.connect(self.reset_config)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(reset_button)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)
        self.render_config()

        self.detect_key_presses()

        self.show()

    @staticmethod
    def get_key_from_value(dictionary, value) -> str:
        for key, val in dictionary.items():
            if val == value:
                return key
        raise ValueError("Value not found in dictionary")
    
    @staticmethod
    def create_config() -> None:
        cfg = configparser.ConfigParser()
        cfg["DEFAULT"] = {
            "button_to_press": "LMB",
            "click_every": "1000",
            "for_seconds": "0",
            "start_button": "F6"
        }
        with open("config.cfg", "w") as configfile:
            cfg.write(configfile)

    def update_start_stop_buttons(self):
        self.start_button.setEnabled(not self.started)
        self.stop_button.setEnabled(self.started)

    def start_pressing(self):
        for_seconds_time = int(self.click_time.text())
        key_to_click = self.button_to_click.last

        if for_seconds_time <= 0:
            for_seconds_time = inf
        time_to_wait = int(self.every_time_click.text())
        self.started = True
        self.update_start_stop_buttons()

        Thread(
            target=self.clicker, args=[for_seconds_time, time_to_wait, key_to_click]
        ).start()

    def clicker(self, for_seconds_time, time_to_wait, key_to_click):
        if key_to_click not in REVERSE_MOUSE_KEYS:
            while for_seconds_time >= 0 and self.started:
                keyboard.send(key_to_click)
                sleep(time_to_wait / 1000)
                for_seconds_time -= time_to_wait / 1000
        else:
            key_to_click = REVERSE_MOUSE_KEYS[key_to_click]
            while for_seconds_time >= 0 and self.started:
                if key_to_click == Qt.LeftButton:
                    mouse.click()
                elif key_to_click == Qt.RightButton:
                    mouse.right_click()
                sleep(time_to_wait / 1000)
                for_seconds_time -= time_to_wait / 1000

    def stop_pressing(self):
        self.started = False
        self.update_start_stop_buttons()

    @staticmethod
    def load_config() -> configparser.ConfigParser:
        cfg = configparser.ConfigParser()
        cfg.read_file(open("config.cfg"))
        return cfg

    def render_config(self) -> None:
        cfg = self.load_config()
        default_button = cfg.get("DEFAULT", "button_to_press")
        click_every = cfg.get("DEFAULT", "click_every")
        for_seconds = cfg.get("DEFAULT", "for_seconds")
        start_button_label = cfg.get('DEFAULT', "start_button")
        self.button_to_click.setText(default_button)
        if default_button in MOUSE_KEYS:
            self.button_to_click.last = self.get_key_from_value(
                MOUSE_KEYS, default_button
            )
        else:
            self.button_to_click.last = default_button
        self.every_time_click.setText(click_every)
        self.click_time.setText(for_seconds)
        self.start_button.setText(f"Start ({start_button_label})")
        self.start_button.bind = start_button_label
        self.rebind_start_button.setText(start_button_label)
        self.update_start_stop_buttons()

    def reset_config(self) -> None:
        cfg = self.load_config()
        cfg["DEFAULT"] = {
            "button_to_press": "LMB",
            "click_every": "1000",
            "for_seconds": "0",
            "start_button": "F6"
        }
        with open("config.cfg", "w") as configfile:
            cfg.write(configfile)
        self.render_config()

    def choose_button_to_click(self) -> None:
        self.ready_to_change_key = True
        self.button_to_click.setText("...")

    def choose_button_to_start(self) -> None:
        self.ready_to_change_start_key = True
        self.rebind_start_button.setText("...")

    def on_key_pressed(self, event) -> None:
        key = event.name

        if self.ready_to_change_start_key:
            self.rebind_start_button.setText(key.upper())
            self.start_button.bind = key
            self.start_button.setText(f"Start ({self.start_button.bind.upper()})")
            self.ready_to_change_start_key = False

        if self.ready_to_change_key:
            self.button_to_click.setText(key.upper())
            self.button_to_click.last = key
            self.ready_to_change_key = False

    def on_mouse_key_pressed(self, event) -> None:
        key = event.button()

        symbol = MOUSE_KEYS.get(key, "ERROR")

        if self.ready_to_change_key:
            self.button_to_click.setText(symbol)
            self.button_to_click.last = symbol
            self.ready_to_change_key = False

    def on_keyboard_press(self, event) -> None:
        key = event.name
        if key == self.start_button.bind:
            if self.started:
                self.stop_pressing()
            else:
                self.start_pressing()
        else:
            self.on_key_pressed(event)

    # Using PyQt5 event handler only for detecting mouse presses
    def event(self, event) -> bool:
        if isinstance(event, QEvent):
            if event.type() == QEvent.MouseButtonPress:
                self.on_mouse_key_pressed(event)
            return QMainWindow.event(self, event)

    def detect_key_presses(self):
        keyboard.on_press(self.on_keyboard_press)

    def closeEvent(self, a0) -> None:
        cfg = self.load_config()
        cfg["DEFAULT"] = {
            "button_to_press": self.button_to_click.last,
            "click_every": self.every_time_click.text(),
            "for_seconds": self.click_time.text(),
            "start_button": self.start_button.bind
        }
        with open("config.cfg", "w") as configfile:
            cfg.write(configfile)
        return super().closeEvent(a0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec())
