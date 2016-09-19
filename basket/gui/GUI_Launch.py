#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import os
from PySide.QtCore import *
from PySide.QtGui import *

import BasketGlobals as config


class Launcher(QDialog):

    def __init__(self, parent=None):
        super(Launcher, self).__init__(parent)

        # S/S INPUTS
        self.label_scene = QLabel('Scene')
        self.label_shot = QLabel('Shot')
        self.dropdown_scene = QComboBox()
        self.dropdown_shot = QComboBox()

        # POPULATE S/S INPUTS
        for i_scene, t_scene in enumerate(next(os.walk(os.path.join(config.serverDir(), os.getenv('SHOW'), 'Working')))[1]):
            self.dropdown_scene.addItem(t_scene)

        # Set the Scene to a default (First one in the directory)
        config.setSeq(self.dropdown_scene.currentText())

        for i_shot, t_shot in enumerate(next(os.walk(os.path.join(config.serverDir(), os.getenv('SHOW'), 'Working', os.getenv('SEQ'))))[1]):
            self.dropdown_shot.addItem(t_shot)

        self.dropdown_scene.currentIndexChanged.connect(self.updateShotList)
        self.dropdown_shot.currentIndexChanged.connect(self.updateEnv)

        # S/S LAYOUT
        hbox_scene = QHBoxLayout()
        hbox_scene.addWidget(self.label_scene)
        hbox_scene.addWidget(self.dropdown_scene)

        hbox_shot = QHBoxLayout()
        hbox_shot.addWidget(self.label_shot)
        hbox_shot.addWidget(self.dropdown_shot)

        # APP LAYOUT
        appBox = QVBoxLayout()
        appBox.addLayout(hbox_scene)
        appBox.addLayout(hbox_shot)

        self.setLayout(appBox)

    def updateEnv(self):
        config.setShot(self.dropdown_shot.currentText())

    def updateShotList(self):
        self.dropdown_shot.clear()
        config.setSeq(self.dropdown_scene.currentText())
        for i_shot, t_shot in enumerate(
                next(os.walk(os.path.join(config.rootDir(), os.getenv('SHOW'), 'Working', os.getenv('SEQ'))))[1]):
            self.dropdown_shot.addItem(t_shot)