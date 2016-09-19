#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import os
from PySide.QtCore import *
from PySide.QtGui import *

import BasketGlobals as config

class Form(QDialog):

    launch = Signal(str)
    nuke_go = Signal()
    maya_go = Signal()

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.nkScripts = config.getNukeScripts()

        # SCENE/SHOT GUI INITIALIZATION
        self.label = QLabel('Directory...')
        self.select_script = QComboBox()
        self.launchbtn = QPushButton('Launch')

        self.label_shot = QLabel('Shot')
        self.label_scene = QLabel('Scene')
        self.text_shot = QLineEdit()
        self.text_scene = QLineEdit()

        self.select_scene = QComboBox()
        self.select_shot = QComboBox()

        # LAUNCH BUTTONS
        self.nukebtn = QPushButton("Nuke")
        self.mayabtn = QPushButton("Maya")

        hbox_scene = QHBoxLayout()
        hbox_scene.addWidget(self.label_scene)
        hbox_scene.addWidget(self.select_scene)

        hbox_shot = QHBoxLayout()
        hbox_shot.addWidget(self.label_shot)
        hbox_shot.addWidget(self.select_shot)

        vbox_select = QVBoxLayout()
        # vbox_select.addWidget(self.label)
        vbox_select.addWidget(self.select_script)
        vbox_select.addWidget(self.launchbtn)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_scene)
        vbox.addLayout(hbox_shot)
        vbox.addLayout(vbox_select)

        self.setLayout(vbox)

        for i, n in enumerate (self.nkScripts):
            self.label.setText(os.path.dirname(n))
            self.select_script.addItem(os.path.basename(n))

        for i_scene, d_scene in enumerate (next(os.walk(os.path.join(config.serverDir(), os.getenv('SHOW'), 'Working')))[1]):
            self.select_scene.addItem(d_scene)
            if d_scene == os.getenv('SEQ'):
                self.select_scene.setCurrentIndex(i_scene)

        for i_shot, d_shot in enumerate (next(os.walk(os.path.join(config.serverDir(), os.getenv('SHOW'), 'Working', os.getenv('SEQ'))))[1]):
            self.select_shot.addItem(d_shot)

        self.select_scene.currentIndexChanged.connect(self.updateShotList)
        self.select_shot.currentIndexChanged.connect(self.updateEnv)
        self.launchbtn.clicked.connect(self.emitlaunch)

        # Define Signals
        self.nukebtn.clicked.connect(self.emitnuke)
        self.mayabtn.clicked.connect(self.emitmaya)

    def emitlaunch(self):
        self.launch.emit(os.path.join(self.label.text(), self.select_script.currentText()))

    def updateEnv(self):
        config.setShot(self.select_shot.currentText())

    def updateShotList(self):
        self.select_shot.clear()
        config.setSeq(self.select_scene.currentText())
        for i_shot, d_shot in enumerate (next(os.walk(os.path.join(config.rootDir(), os.getenv('SHOW'), 'Working', os.getenv('SEQ'))))[1]):
            self.select_shot.addItem(d_shot)

        self.updateScriptList()

    def updateScriptList(self):
        self.select_script.clear()
        for i, n in enumerate (config.getNukeScripts()):
            self.label.setText(os.path.dirname(n))
            self.select_script.addItem(os.path.basename(n))

    def emitnuke(self):
        self.nuke_go.emit()

    def emitmaya(self):
        self.maya_go.emit()
