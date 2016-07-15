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
        self.srcpathlabel = QLabel('Server Directory: ')
        self.srcpathbtn = QPushButton("Src")
        self.srcpathname = QLineEdit()
        self.srcpathname.setMinimumWidth(250)

        self.localpathlabel = QLabel('Local Directory: ')
        self.localpathbtn = QPushButton("Local")
        self.localpathname = QLineEdit()
        self.localpathname.setMinimumWidth(250)

        self.submitbtn = QPushButton("Create")
        self.quitbtn = QPushButton("Quit")

        hbox_SrcPath = QHBoxLayout()
        hbox_SrcPath.addWidget(self.srcpathlabel)
        hbox_SrcPath.addWidget(self.srcpathname)
        hbox_SrcPath.addWidget(self.srcpathbtn)

        hbox_LocalPath = QHBoxLayout()
        hbox_LocalPath.addWidget(self.localpathlabel)
        hbox_LocalPath.addWidget(self.localpathname)
        hbox_LocalPath.addWidget(self.localpathbtn)

        hbox_Cmd = QHBoxLayout()
        hbox_Cmd.addStretch(1)
        hbox_Cmd.addWidget(self.submitbtn)
        hbox_Cmd.addWidget(self.quitbtn)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addLayout(hbox_SrcPath)
        layout.addLayout(hbox_LocalPath)
        layout.addLayout(hbox_Cmd)

        # Set dialog layout
        self.setLayout(layout)

        # Add submitbtn signal
        self.srcpathbtn.clicked.connect(self.selectsourcedir)
        self.localpathbtn.clicked.connect(self.selectlocaldir)
        self.submitbtn.clicked.connect(self.pressbtn)
        self.quitbtn.clicked.connect(QCoreApplication.instance().quit)

    def pressbtn(self):
        self.btnpressed.emit(self.pathName.text(), self.sceneName.text(), self.shotName.text())
        self.sceneName.clear()
        self.shotName.clear()

    def selectsourcedir(self):
        selected_directory = QFileDialog.getExistingDirectory()
        self.dirselected.emit(selected_directory)
        self.srcpathname.setText(selected_directory)

    def selectlocaldir(self):
        selected_directory = QFileDialog.getExistingDirectory()
        self.dirselected.emit(selected_directory)
        self.localpathname.setText(selected_directory)

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.setWindowTitle('Project Transfer')
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
