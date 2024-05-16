from flask import Flask
import pip._vendor.requests as requests
from flask_socketio import SocketIO, emit
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget
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

class MainWindow(QMainWindow):
    def __init__(self, sio_thread):
        super().__init__()

        # Set window title
        self.setWindowTitle("Input App")

        # Create input fields
        self.positive_input_field = QLineEdit()
        self.positive_input_field.setPlaceholderText("Enter positive text here...")
        self.positive_input_field.textChanged.connect(sio_thread.send_positive)

        self.negative_input_field = QLineEdit()
        self.negative_input_field.setPlaceholderText("Enter negative text here...")
        self.negative_input_field.textChanged.connect(sio_thread.send_negative)

        # Set central widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.positive_input_field)
        layout.addWidget(self.negative_input_field)
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