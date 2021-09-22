#!/usr/bin/python3
from main import connect_and_getfile, load_cache, save_cache, play
import os
from os.path import exists
import sys
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog, QLabel, QCheckBox)

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setGeometry(500, 500, 500, 500)
        self.p = None
        # Create widgets
        url, user, password, filename, remove_file = load_cache()
        self.text = QLabel("Play audio files through ftp")
        # self.text_status = QLabel("Status:\n")
        self.edit_user = QLineEdit(user)
        self.edit_password = QLineEdit(password)
        self.edit_url = QLineEdit(url)
        self.edit_filename = QLineEdit(filename)
        self.remove_file = QCheckBox("Remove file afterwards")
        self.button_connect = QPushButton("Connect and get file")
        self.button_stop = QPushButton("Stop audio")
        # Create layout and add widgets

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        # self.layout.addWidget(self.text_status)
        self.layout.addWidget(self.edit_url)
        self.layout.addWidget(self.edit_user)
        self.layout.addWidget(self.edit_password)
        self.layout.addWidget(self.edit_filename)
        self.layout.addWidget(self.remove_file)
        self.layout.addWidget(self.button_connect)

        self.edit_url.setPlaceholderText("url")
        self.edit_user.setPlaceholderText("user")
        self.edit_password.setPlaceholderText("password")
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.edit_filename.setPlaceholderText("filename")
        self.remove_file.setChecked(remove_file)
        self.button_connect.clicked.connect(self.connect)
        self.button_stop.clicked.connect(self.stop)
        self.setLayout(self.layout)


    def closeEvent(self, event):
        if self.remove_file.isChecked():
            if exists("audio"):
                os.remove("audio")
        event.accept()
        print(event)
        try:
            self.p.terminate()
        except Exception:
            pass


    # Greets the user
    def connect(self):
        url = self.edit_url.text()
        user = self.edit_user.text()
        password = self.edit_password.text()
        filename = self.edit_filename.text()
        remove_file = self.remove_file.isChecked()
        response = connect_and_getfile(url, user, password, filename, remove_file)
        if isinstance(response, Exception):
            self.close()
            return

        self.p = play()
        self.layout.addWidget(self.button_stop)

    def stop(self):
        if self.p is not None:
            self.p.terminate()



if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())

