from flask import Flask
import pip._vendor.requests as requests
from flask_socketio import SocketIO, emit
from PySide6.QtWidgets import QMenu,QComboBox, QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget,QGroupBox, QHBoxLayout, QTextEdit, QPushButton, QScrollArea, QSizePolicy, QFrame
from PySide6.QtCore import Slot, Signal, QThread
from PySide6.QtGui import QTextOption, QGuiApplication, QCursor
from PySide6.QtCore import Qt
import sys
from socketio import Client


class MainWindow(QMainWindow):
    def __init__(self, menu, parent=None):
        super().__init__(parent)

        self.menu = menu
        self.set_menu_style()

    def set_menu_style(self):
        self.menu.setStyleSheet("""
            QMenu {
                color: #000000;
            }
            QMenu::item {
                color: #000000;
            }
            QMenu::item:hover {
                color: #FFFFFF;
                border: 1px solid #000000;
                background-color: #000000;
            }
        """)

# ...

def main():
    # Create the application
    app = QApplication(sys.argv)

    # Create the menu
    menu = QMenu()

    # Create and show the main window
    window = MainWindow(menu)
    window.show()

    # Execute the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()