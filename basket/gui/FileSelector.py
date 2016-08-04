#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import sys, os
from PySide.QtCore import *
from PySide.QtGui import *

from basket.utils import Pinapple

class Form(QDialog):

    launch = Signal(str)

    def __init__(self, nkScripts, parent=None):
        super(Form, self).__init__(parent)

        self.nkScripts = nkScripts

        self.label = QLabel('Directory...')
        self.selector = QComboBox()
        self.launchbtn = QPushButton('Launch')

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.selector)
        vbox.addWidget(self.launchbtn)
        self.setLayout(vbox)

        for i, n in enumerate (self.nkScripts):
            print('nk_%s' % i, os.path.basename(n))
            self.label.setText(os.path.dirname(n))
            self.selector.addItem(os.path.basename(n))

        self.launchbtn.clicked.connect(self.emitlaunch)

    def emitlaunch(self):
        self.launch.emit(os.path.join(self.label.text(), self.selector.itemText(self.selector.currentIndex())))