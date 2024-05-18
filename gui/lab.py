from flask import Flask
import pip._vendor.requests as requests
from flask_socketio import SocketIO, emit
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget,QGroupBox, QHBoxLayout, QTextEdit
from PySide6.QtCore import Slot, Signal, QThread
from PySide6.QtGui import QTextOption
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

    def send_positive(self, msg, id):
        print(id)
        self.sio.emit('positive',  {'msg': msg, 'id': id})

    def send_negative(self, msg, id):
        print(id)
        self.sio.emit('negative',  {'msg': msg, 'id': id})

class InputField(QTextEdit):
    textChangedWithText = Signal(str, int)
    def __init__(self, placeholder_text, signal_connection, id, parent=None):
        super().__init__(parent)
        self.id = id
        self.setPlaceholderText(str(self.id) + " " + placeholder_text)
        self.textChanged.connect(self.emitTextChangedWithText)
        self.textChangedWithText.connect(signal_connection)
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        
        self.setStyleSheet("""
            QTextEdit {
                border: none;
                color: #9290C3;
                background-color: #070F2B;
                height: 100%;
                min-width: 300px;
            }
            QTextEdit:focus {
                border: 1px solid #9290C3;
            }
        """)
    @Slot()
    def emitTextChangedWithText(self):
        self.textChangedWithText.emit(self.toPlainText(), self.id)
class Conditioning(QHBoxLayout):
    def __init__(self, sio_thread, id, parent=None):
        super().__init__(parent)
        self.positive_input = InputField("Enter positive text here...", sio_thread.send_positive, id)

        self.negative_input = InputField("Enter negative text here...", sio_thread.send_negative, id)
        # Create a group box and set a background color
        self.group_box = QGroupBox()
        self.group_box.setStyleSheet("""
            background-color: #1B1A55;
            border: 1px solid black;
            padding: 10px;
            border-radius: 5px;
            min-height: 200px;
            max-width: 1000px; 
                                     padding: 10px;
        """)

        self.addWidget(self.positive_input)
        self.addWidget(self.negative_input)
        self.group_box.setLayout(self)


# https://colorhunt.co/palette/070f2b1b1a55535c919290c3
class MainWindow(QMainWindow):
    def __init__(self, sio_thread):
        super().__init__()

        # Set window title
        self.setWindowTitle("Input App")
        self.setStyleSheet("background-color: #070F2B;")  # Black background


        conditioning = Conditioning(sio_thread, 0)
        conditioning2 = Conditioning(sio_thread, 1)

        # Set central widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(conditioning.group_box)
        layout.addWidget(conditioning2.group_box)


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