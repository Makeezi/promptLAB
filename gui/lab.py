from flask import Flask
import pip._vendor.requests as requests
from flask_socketio import SocketIO, emit
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget,QGroupBox, QHBoxLayout, QTextEdit, QPushButton, QScrollArea, QSizePolicy, QFrame
from PySide6.QtCore import Slot, Signal, QThread
from PySide6.QtGui import QTextOption, QGuiApplication
from PySide6.QtCore import Qt
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

class SharedCondition:
    def __init__(self, id, condition, connect=False):
        self.id = id
        self.condition = condition
        self.connect = connect



class InputField(QTextEdit):
    textChangedWithText = Signal(str, int)
    def __init__(self, placeholder_text, signal_connection, sharedCondition, parent=None):
        super().__init__(parent)
        self.id = id
        self.setPlaceholderText(str(sharedCondition.id) + " " + placeholder_text)
        if(sharedCondition.connect):
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
    def __init__(self, sio_thread, sharedCondition, parent=None):
        super().__init__(parent)
        if(sharedCondition.condition == "pos"):
            self.positive_input = InputField("Enter positive text here...", sio_thread.send_positive, sharedCondition)
        elif(sharedCondition.condition == "neg"):
            self.positive_input = InputField("Enter negative text here...", sio_thread.send_negative, sharedCondition)
        # self.negative_input = InputField("Enter negative text here...", sio_thread.send_negative, id)
        # Create a group box and set a background color
        self.group_box = QGroupBox()
        self.group_box.setMinimumSize(500, 200)
        self.group_box.setStyleSheet("""
            background-color: #1B1A55;
            border: 1px solid black;
            padding: 10px;
            border-radius: 5px;
            height: 100px;
            max-width: 800px;
                                     padding: 10px;
        """)


        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.group_box.setSizePolicy(sizePolicy)

        self.addWidget(self.positive_input)
        # self.addWidget(self.negative_input)
        self.group_box.setLayout(self)

buttonStyle = """
    QPushButton {
        background-color: #1B1A55;
        border: 1px solid black;
        color: #9290C3;
        padding: 10px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #535C91;
    }
    QPushButton:pressed {
        background-color: #9290C3;
        color: #1B1A55;
    }
"""


# https://colorhunt.co/palette/070f2b1b1a55535c919290c3
class MainWindow(QMainWindow):
    def __init__(self, sio_thread):
        super().__init__()

        screen = QGuiApplication.screens()[0]
        screen_size = screen.size()

        # Set window size to be 75% of the screen size
        self.resize(screen_size.width() * 0.75, screen_size.height() * 0.75)
        # Set window size to be 75% of the screen size
        
        self.sio_thread = sio_thread
        # Set window title
        self.setWindowTitle("Input App")

        self.setStyleSheet("background-color: #070F2B;")  # Black background

        self.layout = QVBoxLayout()

        self.addRow()

        # Create a button for adding new rows
        add_row_button = QPushButton("Add Row")
        add_row_button.clicked.connect(self.addRow)
        add_row_button.setStyleSheet(buttonStyle)
        

        # Create a scroll area and set its widget resizable property to True
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        # Create a widget for the scroll area and set its layout
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.layout)
        scroll_area.setWidget(scroll_widget)
        

        # Set central widget
        self.column = QVBoxLayout()
        self.column.addWidget(scroll_area)
        self.column.addWidget(add_row_button)
        central_widget = QWidget()
        central_widget.setLayout(self.column)
        self.setCentralWidget(central_widget)

    def addRow(self):
        # Create a new QHBoxLayout for this row
        row_layout = QHBoxLayout()
        row_layout.setSpacing(0)
        plus_button = QPushButton("+")
        plus_button.clicked.connect(lambda: self.add_conditioning(row_layout))
        plus_button.setStyleSheet(buttonStyle)

        # Create a scroll area and set its widget resizable property to True
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        # Create a widget for the scroll area and set its layout
        scroll_widget = QWidget()
        scroll_widget.setLayout(row_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setMinimumHeight(300)
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.row = QHBoxLayout()
        self.row.addWidget(scroll_area)
        self.row.addWidget(plus_button)

        self.layout.addLayout(self.row)

    def add_conditioning(self, row_layout):
        sharedCondition = SharedCondition(0, "pos", True)
        conditioning = Conditioning(self.sio_thread, sharedCondition)
        # Add the Conditioning widget to the last row's layout
        row_layout.addWidget(conditioning.group_box)

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