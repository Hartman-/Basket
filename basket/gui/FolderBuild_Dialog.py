#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import sys, os
from PySide.QtCore import *
from PySide.QtGui import *


class Form(QDialog):

    btnpressed = Signal(str, str, str)
    dirselected = Signal(str)

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        # Create widgets
        self.browseLabel = QLabel('Project Directory: ')
        self.browsebtn = QPushButton("Browse")
        self.pathName = QLineEdit()
        self.pathName.setMinimumWidth(250)

        self.sceneLabel = QLabel("Scene: ")
        self.sceneLabel.setMinimumWidth(40)
        self.sceneName = QLineEdit()
        self.sceneName.setMaximumWidth(150)
        self.sceneName.setPlaceholderText("Type Scene Here...")

        self.shotLabel = QLabel("Shot: ")
        self.shotLabel.setMinimumWidth(40)
        self.shotName = QLineEdit()
        self.shotName.setMaximumWidth(150)
        self.shotName.setPlaceholderText("Type Shot Here...")

        self.submitbtn = QPushButton("Create")
        self.quitbtn = QPushButton("Quit")

        hbox_Path = QHBoxLayout()
        hbox_Path.addWidget(self.browseLabel)
        hbox_Path.addWidget(self.pathName)
        hbox_Path.addWidget(self.browsebtn)

        hbox_Scene = QHBoxLayout()
        hbox_Scene.addWidget(self.sceneLabel)
        hbox_Scene.addWidget(self.sceneName)
        hbox_Scene.addStretch(1)

        hbox_Shot = QHBoxLayout()
        hbox_Shot.addWidget(self.shotLabel)
        hbox_Shot.addWidget(self.shotName)
        hbox_Shot.addStretch(1)

        hbox_Cmd = QHBoxLayout()
        hbox_Cmd.addStretch(1)
        hbox_Cmd.addWidget(self.submitbtn)
        hbox_Cmd.addWidget(self.quitbtn)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addLayout(hbox_Path)
        layout.addLayout(hbox_Scene)
        layout.addLayout(hbox_Shot)
        layout.addLayout(hbox_Cmd)

        # Set dialog layout
        self.setLayout(layout)

        # Add submitbtn signal
        self.browsebtn.clicked.connect(self.selectdirectory)
        self.submitbtn.clicked.connect(self.pressbtn)
        self.quitbtn.clicked.connect(QCoreApplication.instance().quit)

    def pressbtn(self):
        self.btnpressed.emit(self.pathName.text(), self.sceneName.text(), self.shotName.text())
        self.sceneName.clear()
        self.shotName.clear()

    def selectdirectory(self):
        selected_directory = QFileDialog.getExistingDirectory()
        self.dirselected.emit(selected_directory)
        self.pathName.setText(selected_directory)
