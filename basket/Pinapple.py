#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import sys, os
from PySide.QtCore import *
from PySide.QtGui import *


class Form(QDialog):

    btnpressed = Signal(str, str)

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        # Create widgets
        self.sceneLabel = QLabel("Scene: ")
        self.sceneName = QLineEdit()
        self.sceneName.setPlaceholderText("Type Scene Here...")

        self.shotLabel = QLabel("Shot: ")
        self.shotName = QLineEdit()
        self.shotName.setPlaceholderText("Type Shot Here...")

        self.submitbtn = QPushButton("Create Folders")

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.sceneLabel)
        layout.addWidget(self.sceneName)
        layout.addWidget(self.shotLabel)
        layout.addWidget(self.shotName)
        layout.addWidget(self.submitbtn)

        # Set dialog layout
        self.setLayout(layout)

        # Add submitbtn signal
        self.submitbtn.clicked.connect(self.pressbtn)

    def pressbtn(self):
        self.btnpressed.emit(self.sceneName.text(), self.shotName.text())
        self.sceneName.clear()
        self.shotName.clear()
