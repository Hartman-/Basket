#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import sys, os
from PySide.QtCore import *
from PySide.QtGui import *

from basket import config

class Form(QDialog):

    launch = Signal(str)

    def __init__(self, nkScripts, parent=None):
        super(Form, self).__init__(parent)

        self.nkScripts = nkScripts

        self.label = QLabel('Directory...')
        self.selector = QComboBox()
        self.launchbtn = QPushButton('Launch')

        self.label_shot = QLabel('Shot')
        self.label_scene = QLabel('Scene')
        self.text_shot = QLineEdit()
        self.text_scene = QLineEdit()

        self.select_scene = QComboBox()
        self.select_shot = QComboBox()

        hbox_scene = QHBoxLayout()
        hbox_scene.addWidget(self.label_scene)
        hbox_scene.addWidget(self.select_scene)

        hbox_shot = QHBoxLayout()
        hbox_shot.addWidget(self.label_shot)
        hbox_shot.addWidget(self.select_shot)

        vbox_select = QVBoxLayout()
        vbox_select.addWidget(self.label)
        vbox_select.addWidget(self.selector)
        vbox_select.addWidget(self.launchbtn)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_scene)
        vbox.addLayout(hbox_shot)
        vbox.addLayout(vbox_select)

        self.setLayout(vbox)

        self.select_scene.currentIndexChanged.connect(self.updateShotList)

        for i, n in enumerate (self.nkScripts):
            print('nk_%s' % i, os.path.basename(n))
            self.label.setText(os.path.dirname(n))
            self.selector.addItem(os.path.basename(n))

        for i_scene, d_scene in enumerate (next(os.walk(os.path.join(config.rootDir(), os.getenv('SHOW'), 'Working')))[1]):
            print(os.path.join(config.rootDir(), os.getenv('SHOW'), 'Working'))
            self.select_scene.addItem(d_scene)

        for i_shot, d_shot in enumerate (next(os.walk(os.path.join(config.rootDir(), os.getenv('SHOW'), 'Working', os.getenv('SEQ'))))[1]):
            self.select_shot.addItem(d_shot)

        self.launchbtn.clicked.connect(self.emitlaunch)

    def emitlaunch(self):
        self.launch.emit(os.path.join(self.label.text(), self.selector.itemText(self.selector.currentIndex())))

    def updateShotList(self):
        print('Text Edited')
        self.select_shot.clear()
        config.setSeq(self.select_scene.itemText(self.select_scene.currentIndex()))
        for i_shot, d_shot in enumerate (next(os.walk(os.path.join(config.rootDir(), os.getenv('SHOW'), 'Working', os.getenv('SEQ'))))[1]):
            self.select_shot.addItem(d_shot)

