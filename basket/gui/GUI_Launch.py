#!/usr/bin/python
# -'''- coding: utf-8 -'''-

from glob import glob
import os

from PySide.QtCore import *
from PySide.QtGui import *

import BasketGlobals as config


class WindowLayout(QWidget):

    # Define Emitter Signals
    launch = Signal(int, str)
    createnew = Signal(int)

    def __init__(self, parent=None):
        super(WindowLayout, self).__init__(parent)

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
        for i_scene, t_scene in enumerate(
                next(os.walk(os.path.join(config.serverDir(), os.getenv('SHOW'), 'Working')))[1]):
            self.dropdown_scene.addItem(t_scene)

        # Set the Scene to a default (First one in the directory)
        config.setSeq(self.dropdown_scene.currentText())

        for i_shot, t_shot in enumerate(
                next(os.walk(os.path.join(config.serverDir(), os.getenv('SHOW'), 'Working', os.getenv('SEQ'))))[1]):
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
        self.dropdown_tag = QComboBox()

        self.label_stage = QLabel('Stage')
        self.dropdown_stage = QComboBox()
        self.dropdown_stage.setMinimumWidth(100)

        for i_stage, t_stage in enumerate(next(os.walk(
                os.path.join(config.serverDir(), os.getenv('SHOW'), 'Working', os.getenv('SEQ'), os.getenv('SHOT'))))[
                                              1]):
            self.dropdown_stage.addItem(t_stage)

        self.dropdown_stage.currentIndexChanged.connect(self.updateTags)

        # MISC LAYOUT
        vbox_tag = QVBoxLayout()
        vbox_tag.addWidget(self.label_tag)
        vbox_tag.addWidget(self.dropdown_tag)

        vbox_stage = QVBoxLayout()
        vbox_stage.addWidget(self.label_stage)
        vbox_stage.addWidget(self.dropdown_stage)

        # LAUNCH BUTTONS
        self.btn_launch = QPushButton('Launch Existing...')
        self.btn_create = QPushButton('Create New...')

        # Check if there is an existing file
        self.canLaunch()

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
        leftLower.addWidget(self.btn_create)

        leftLower.setContentsMargins(20, 0, 20, 0)

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
                next(os.walk(os.path.join(config.serverDir(), os.getenv('SHOW'), 'Working', os.getenv('SEQ'))))[1]):
            self.dropdown_shot.addItem(t_shot)

        self.updateTags()

    def emitlaunch(self):
        # Return the stage index to the launcher, add one to compensate for zero-based index
        self.launch.emit(self.getStageIndex(), self.dropdown_tag.currentText())

    def emitcreate(self):
        self.createnew.emit(self.getStageIndex())

    def getTags(self):
        # Grab all the files in given stage directory, unbiased of file type
        files = glob(os.path.join(config.serverStageDir(self.dropdown_stage.currentText()), '*.*'))
        sort = []
        for i, n in enumerate(files):
            # Add all found file variables to a list
            splt = os.path.basename(n).split('_')
            if len(splt) >= 2:
                sort.append(splt[2])

        # Sets are DISTINCT objects, no repeats, removes duplicate names
        distinct = set(sort)
        return distinct

    def updateTags(self):
        self.dropdown_tag.clear()
        for i_tag, t_tag in enumerate(self.getTags()):
            self.dropdown_tag.addItem(t_tag)
        # Whenever tags update, we need to update whether or not there is existing file
        self.canLaunch()

    def getStageIndex(self):
        return int(self.dropdown_stage.currentIndex() + 1)

    def canLaunch(self):
        if self.dropdown_tag.count() > 0:
            self.btn_launch.setEnabled(True)
        else:
            self.btn_launch.setDisabled(True)


class Launcher(QMainWindow):
    def __init__(self, parent=None):
        super(Launcher, self).__init__(parent)

        self.initUI()

    def initUI(self):

        # CREATE MENU BAR
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        shotAction = QAction('&Create Shot', self)
        shotAction.setStatusTip('Build out folder structure for a new shot')
        shotAction.triggered.connect(self.test)

        syncAction = QAction('&Sync Project', self)
        syncAction.setStatusTip('Sync Local Project with Server')
        syncAction.triggered.connect(self.test)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        buildMenu = menubar.addMenu('&Build')

        fileMenu.addAction(exitAction)
        buildMenu.addAction(shotAction)
        buildMenu.addAction(syncAction)

        mainlayout = WindowLayout()

        self.setCentralWidget(mainlayout)
        self.show()

    def test(self):
        print 'Hello World'