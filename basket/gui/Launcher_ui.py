#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import sys, os
from PySide.QtCore import *
from PySide.QtGui import *

class Launcher(QDialog):

    nukepressed = Signal()
    mayapressed = Signal()

    def __init__(self, parent=None):
        super(Launcher, self).__init__(parent)

        # Define Widgets

        # --- BUTTONS ---
        self.nukebtn = QPushButton("Nuke")
        self.mayabtn = QPushButton("Maya")

        # --- LAYOUTS ---
        hbox_Nuke = QHBoxLayout()
        hbox_Nuke.addStretch(1)
        hbox_Nuke.addWidget(self.nukebtn)
        hbox_Nuke.addStretch(1)

        hbox_Maya = QHBoxLayout()
        hbox_Maya.addStretch(1)
        hbox_Maya.addWidget(self.mayabtn)
        hbox_Maya.addStretch(1)

        layout = QVBoxLayout()
        layout.addLayout(hbox_Nuke)
        layout.addLayout(hbox_Maya)

        self.setLayout(layout)

        # Define Signals
        self.nukebtn.clicked.connect(self.emitnuke)
        self.mayabtn.clicked.connect(self.emitmaya)

    def emitnuke(self):
        self.nukepressed.emit()

    def emitmaya(self):
        self.mayapressed.emit()
