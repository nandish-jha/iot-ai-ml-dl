from PyQt5               import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets     import QMessageBox
from subscribe           import subscribe
from publish             import publish
from cryptography.fernet import Fernet

import parking_1
import time
import sys

spots = [16, 18, 22, 36, 38]    # List of parking spots (board GPIOs)
status = ['occupied', 'empty']  # List of parking status

class MainWindow(QtWidgets.QMainWindow, parking_1.Ui_MainWindow):
    
    publish_inst_1 = publish()
    subscribe_inst_1 = subscribe()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.warn_on_button.clicked.connect(self.warn_on)
        self.warn_off_button.clicked.connect(self.warn_off)
        self.send_button.clicked.connect(self.send)
    
    def send(self):
        text_to_be_sent = self.send_message_text_field.toPlainText()
        self.publish_inst_1.main_loop(text_to_be_sent, "messages")
        self.publish_inst_1.client.loop_stop()
        self.send_message_text_field.clear()

    def warn_on(self):
        warning = "warning on"
        self.publish_inst_1.main_loop(warning, "warnings")
        self.publish_inst_1.client.loop_stop()

    def warn_off(self):
        warning = "warning off"
        self.publish_inst_1.main_loop(warning, "warnings")
        self.publish_inst_1.client.loop_stop()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    subscribe_inst_1 = subscribe()
    subscribe_inst_1.main_loop(mainWindow)

    sys.exit(app.exec_())
