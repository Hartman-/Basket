#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import os
from PySide.QtCore import *
from PySide.QtGui import *

import BasketGlobals as config


class Launcher(QDialog):

    launch = Signal(int, str)

    def __init__(self, parent=None):
        super(Launcher, self).__init__(parent)

        # S3 INPUTS
        self.label_scene = QLabel('Scene')
        self.label_scene.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_shot = QLabel('Shot')
        self.label_shot.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.dropdown_scene = QComboBox()
        self.dropdown_scene.setMinimumWidth(100)
        self.dropdown_shot = QComboBox()
        self.dropdown_shot.setMinimumWidth(100)

        # POPULATE S3 INPUTS
        for i_scene, t_scene in enumerate(next(os.walk(os.path.join(config.serverDir(), os.getenv('SHOW'), 'Working')))[1]):
            self.dropdown_scene.addItem(t_scene)

        # Set the Scene to a default (First one in the directory)
        config.setSeq(self.dropdown_scene.currentText())

        for i_shot, t_shot in enumerate(next(os.walk(os.path.join(config.serverDir(), os.getenv('SHOW'), 'Working', os.getenv('SEQ'))))[1]):
            self.dropdown_shot.addItem(t_shot)

        # Set the Shot to a default (First in directory)
        config.setShot(self.dropdown_shot.currentText())

        self.dropdown_scene.currentIndexChanged.connect(self.updateShotList)
        self.dropdown_shot.currentIndexChanged.connect(self.updateEnv)

        # S3 LAYOUT
        hbox_scene = QHBoxLayout()
        hbox_scene.addWidget(self.label_scene)
        hbox_scene.addWidget(self.dropdown_scene)

        hbox_shot = QHBoxLayout()
        hbox_shot.addWidget(self.label_shot)
        hbox_shot.addWidget(self.dropdown_shot)

        # MISC WIDGETS
        self.label_options = QLabel('Options')
        self.label_tag = QLabel('Tag')
        self.input_tag = QLineEdit()

        self.label_stage = QLabel('Stage')
        self.dropdown_stage = QComboBox()
        self.dropdown_stage.setMinimumWidth(100)

        for i_stage, t_stage in enumerate(next(os.walk(os.path.join(config.serverDir(), os.getenv('SHOW'), 'Working', os.getenv('SEQ'), os.getenv('SHOT'))))[1]):
            self.dropdown_stage.addItem(t_stage)

        # MISC LAYOUT
        vbox_tag = QVBoxLayout()
        vbox_tag.addWidget(self.label_tag)
        vbox_tag.addWidget(self.input_tag)

        vbox_stage = QVBoxLayout()
        vbox_stage.addWidget(self.label_stage)
        vbox_stage.addWidget(self.dropdown_stage)

        # LAUNCH BUTTONS
        self.btn_launch = QPushButton('Launch')

        # LAUNCH SIGNALS
        self.btn_launch.clicked.connect(self.emitlaunch)
        self.btn_launch.clicked.connect(QCoreApplication.instance().quit)

        # APP LAYOUT
        appWrapper = QHBoxLayout()

        leftColumn = QVBoxLayout()

        leftUpper = QVBoxLayout()
        leftUpper.addLayout(hbox_scene)
        leftUpper.addLayout(hbox_shot)
        leftUpper.addStretch(3)

        leftUpper.setContentsMargins(20, 20, 20, 20)

        leftLower = QVBoxLayout()
        leftLower.addWidget(self.btn_launch)

        leftLower.setContentsMargins(20,0,20,0)

        leftColumn.addLayout(leftUpper)
        leftColumn.addLayout(leftLower)

        rightColumn = QVBoxLayout()
        rightColumn.addWidget(self.label_options)
        rightColumn.addLayout(vbox_tag)
        rightColumn.addLayout(vbox_stage)
        rightColumn.addStretch(3)

        appWrapper.addLayout(leftColumn)
        appWrapper.addLayout(rightColumn)


        self.setLayout(appWrapper)

    def updateEnv(self):
        config.setShot(self.dropdown_shot.currentText())

    def updateShotList(self):
        self.dropdown_shot.clear()
        config.setSeq(self.dropdown_scene.currentText())
        for i_shot, t_shot in enumerate(
                next(os.walk(os.path.join(config.rootDir(), os.getenv('SHOW'), 'Working', os.getenv('SEQ'))))[1]):
            self.dropdown_shot.addItem(t_shot)

    def emitlaunch(self):
        # Return the stage index to the launcher, add one to compensate for zero-based index
        self.launch.emit(int(self.dropdown_stage.currentIndex() + 1), self.input_tag.text())
