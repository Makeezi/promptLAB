from flask import Flask
import pip._vendor.requests as requests
from flask_socketio import SocketIO, emit
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget,QGroupBox, QHBoxLayout
from PySide6.QtCore import Slot, Signal, QThread
import sys
from socketio import Client

class SocketIOThread(QThread):
    message_received = Signal(str)

    def __init__(self):
        super().__init__()
        self.sio = Client()

    def run(self):
        self.sio.connect('http://127.0.0.1:5000', wait_timeout = 10)
        self.sio.wait()

    def send_positive(self, message):
        self.sio.emit('positive', message)

    def send_negative(self, message):
        self.sio.emit('negative', message)

class InputField(QLineEdit):
    def __init__(self, placeholder_text, signal_connection, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder_text)
        self.textChanged.connect(signal_connection)
        self.setStyleSheet("""
            border: none;
            color: #9290C3;
        """)

# https://colorhunt.co/palette/070f2b1b1a55535c919290c3
class MainWindow(QMainWindow):
    def __init__(self, sio_thread):
        super().__init__()

        # Set window title
        self.setWindowTitle("Input App")
        self.setStyleSheet("background-color: #070F2B;")  # Black background


        # Create input fields
        positive_input = InputField("Enter positive text here...", sio_thread.send_positive)
        negative_input = InputField("Enter negative text here...", sio_thread.send_negative)

         # Create a group box and set a background color
        group_box = QGroupBox()
        group_box.setStyleSheet("""
            background-color: #1B1A55;
            border: 1px solid black;
            padding: 10px;
            border-radius: 5px;
        """)
        # Add input fields to the group box
        layout = QHBoxLayout()
        layout.addWidget(positive_input)
        layout.addWidget(negative_input)
        group_box.setLayout(layout)

        # Set central widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(group_box)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


def main():
    # Create the application
    app = QApplication(sys.argv)

    # Create and start the SocketIO thread
    sio_thread = SocketIOThread()
    sio_thread.start()

    # Create and show the main window
    window = MainWindow(sio_thread)
    window.show()

    # Execute the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()