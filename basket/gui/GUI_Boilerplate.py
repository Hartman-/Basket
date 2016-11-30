#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import os
import sys

from PySide.QtCore import *
from PySide.QtGui import *


class SubLayout(QWidget):
    def __init__(self, parent=None):
        super(SubLayout, self).__init__(parent)

        self.label = QLabel('Hello World')

        layout = QHBoxLayout()
        layout.addWidget(self.label)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mainlayout = SubLayout()
        self.initUI()

    def initUI(self):

        self.setCentralWidget(self.mainlayout)
        self.show()


if __name__ == "__main__":

    # Create the Qt Application
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.setWindowTitle('Main Window')

    sys.exit(app.exec_())