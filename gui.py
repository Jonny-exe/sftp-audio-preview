#!/usr/bin/python3
from main import connect_sftp, load_cache, save_cache, play, get_file
import os
from os.path import exists
from copy import deepcopy
from functools import partial
import sys
from PySide2.QtWidgets import (
    QLineEdit,
    QPushButton,
    QApplication,
    QVBoxLayout,
    QDialog,
    QLabel,
    QCheckBox,
    QScrollArea,
    QWidget,
    QMainWindow,
    QButtonGroup,
    QGroupBox
)
from PySide2.QtCore import Qt, QSize


class Form(QMainWindow):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setGeometry(500, 500, 500, 500)
        self.p = None

        self.scroll = QScrollArea()
        self.widget = QWidget()

        # Create widgets
        url, user, password, remove_file = load_cache()
        self.text = QLabel("Play audio files through ftp")
        # self.text_status = QLabel("Status:\n")
        self.edit_user = QLineEdit(user)
        self.edit_password = QLineEdit(password)
        self.edit_url = QLineEdit(url)
        self.remove_file = QCheckBox("Remove file afterwards")
        self.button_connect = QPushButton("Connect and get file")
        self.button_stop = QPushButton("Stop audio")
        self.path = QLabel("path")
        self.files_container = QGroupBox()
        self.files = QVBoxLayout()
        self.files_container.setLayout(self.files)
        # Create layout and add widgets

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)

        # self.layout.addWidget(self.text_status)
        self.layout.addWidget(self.edit_url)
        self.layout.addWidget(self.edit_user)
        self.layout.addWidget(self.edit_password)
        self.layout.addWidget(self.remove_file)
        self.layout.addWidget(self.button_connect)
        self.layout.addWidget(self.path)
        self.layout.addWidget(self.files_container)

        self.edit_url.setPlaceholderText("url")
        self.edit_user.setPlaceholderText("user")
        self.edit_password.setPlaceholderText("password")
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.remove_file.setChecked(remove_file)
        self.button_connect.clicked.connect(self.connect)
        self.button_stop.clicked.connect(self.stop)
        self.setLayout(self.layout)

        # Scroll Area Properties
        self.widget.setLayout(self.layout)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)

    def closeEvent(self, event):
        if self.remove_file.isChecked():
            if exists("audio"):
                os.remove("audio")
        try:
            self.p.terminate()
        except Exception:
            pass
        event.accept()

    # Greets the user
    def connect(self):
        url = self.edit_url.text()
        user = self.edit_user.text()
        password = self.edit_password.text()
        remove_file = self.remove_file.isChecked()
        conn = connect_sftp(url, user, password, remove_file)
        if isinstance(conn, Exception):
            self.close()
            return
        dirs = self.add_dirs(conn)

    def get_and_play(self, conn, filename):
        get_file(conn, filename)
        self.p = play()
        self.layout.addWidget(self.button_stop)
    
    def add_dirs(self, conn, path=None):
        if path is not None:
            conn.chdir(path)
        self.path.setText(conn.pwd)
        dirs = conn.listdir(conn.pwd)

        while self.files.count() != 0:
            widget = self.files.takeAt(0)
            widget.widget().hide()
        self.button_back = QPushButton("..")
        self.files.addWidget(self.button_back)
        self.button_back.clicked.connect(partial(self.add_dirs, conn, path=".."))

        for folder_name in dirs:
            isdir = conn.isdir(folder_name)
            label = QPushButton(folder_name + " * " * int(isdir))
            if isdir:
                func = partial(self.add_dirs, conn, path=conn.pwd+"/"+folder_name)
            else:
                func = partial(self.get_and_play, conn, conn.pwd+"/"+folder_name)
            label.clicked.connect(func)
                
            self.files.addWidget(label)
            
        return dirs

    def stop(self):
        if self.p is not None:
            self.p.terminate()


if __name__ == "__main__":
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    try:
        form = Form()
        form.show()
        # Run the main Qt loop
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("Bye")
