#!/usr/bin/env python

import sys
import subprocess

from PySide.QtCore import *
from PySide.QtGui import *

import BasketGlobals as config


class ArchiveDialog(QDialog):
    def __init__(self, parent=None):
        super(ArchiveDialog, self).__init__(parent)

        # Create widgets
        self.browseLabel = QLabel('Image Sequence: ')
        self.browsebtn = QPushButton("Browse")
        self.pathName = QLineEdit()
        self.pathName.setMinimumWidth(250)

        self.submitbtn = QPushButton("Archive")
        self.quitbtn = QPushButton("Quit")

        hbox_Path = QHBoxLayout()
        hbox_Path.addWidget(self.browseLabel)
        hbox_Path.addWidget(self.pathName)
        hbox_Path.addWidget(self.browsebtn)

        hbox_Cmd = QHBoxLayout()
        hbox_Cmd.addStretch(1)
        hbox_Cmd.addWidget(self.submitbtn)
        hbox_Cmd.addWidget(self.quitbtn)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addLayout(hbox_Path)
        layout.addLayout(hbox_Cmd)

        self.setLayout(layout)

        # Add submitbtn signal
        self.browsebtn.clicked.connect(self.selectdirectory)
        self.submitbtn.clicked.connect(self.goArchive)
        self.quitbtn.clicked.connect(QCoreApplication.instance().quit)

    def selectdirectory(self):
        fname = QFileDialog.getOpenFileName(None, "Select Image", config.framesDir())
        self.pathName.setText(fname[0])

    def goArchive(self):
        if self.pathName.text() is not None:
            path = self.pathName.text().replace('//', '\\\\').replace('/', '\\')
            print path
            subprocess.Popen(['C:\Program Files\Nuke10.0v4\Nuke10.0.exe',
                   '--nukex',
                   '-ti',
                   'X:/Classof2017/LobstersAreWeird/basket/nuke/convertsequence.py',
                   path])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = ArchiveDialog()
    gui.setWindowTitle('LAW Archiver')
    gui.show()
    sys.exit(app.exec_())
