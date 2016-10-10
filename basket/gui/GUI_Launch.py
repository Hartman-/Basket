#!/usr/bin/python
# -'''- coding: utf-8 -'''-

from glob import glob
import os

from PySide.QtCore import *
from PySide.QtGui import *

import BasketBuilder
import BasketGlobals as config


class WindowLayout(QTabWidget):

    # Define Emitter Signals
    launch = Signal(int, str)
    createnew = Signal(int)
    openasset = Signal(str)

    def __init__(self, parent=None):
        super(WindowLayout, self).__init__(parent)

        # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
        #  TABS
        # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

        self.tabAssets = QWidget()
        self.tabShots = QWidget()

        self.addTab(self.tabShots, "tabShots")
        self.addTab(self.tabAssets, "tabAssets")

        self.setTabText(0, "Shots")
        self.setTabText(1, "Assets")

        # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
        #  SHOTS
        # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

        # S3 INPUTS
        self.label_scene = QLabel('Scene')
        self.label_scene.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_shot = QLabel('Shot')
        self.label_shot.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.dropdown_scene = QComboBox()
        self.dropdown_scene.setMinimumWidth(100)
        self.dropdown_shot = QComboBox()
        self.dropdown_shot.setMinimumWidth(100)

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

        for i_stage, t_stage in enumerate(config.STAGE_DIRS):
            self.dropdown_stage.addItem(t_stage)

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
        self.updateDB()
        self.dropdown_scene.currentIndexChanged.connect(self.updateShotList)

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

        self.tabShots.setLayout(appWrapper)

        # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
        #  ASSETS
        # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

        self.btn_browse = QPushButton("Browse Assets")
        self.btn_AssetLaunch = QPushButton("Launch")
        self.label_Directory = QLabel("Directory:")
        self.label_Directory.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.text_Directory = QLineEdit()

        self.btn_browse.clicked.connect(self.browseAssets)
        self.btn_AssetLaunch.clicked.connect(self.launchAsset)

        assetLayout = QVBoxLayout()

        inputLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()

        inputLayout.addWidget(self.label_Directory)
        inputLayout.addWidget(self.text_Directory)
        buttonLayout.addWidget(self.btn_browse)
        buttonLayout.addWidget(self.btn_AssetLaunch)
        inputLayout.addLayout(buttonLayout)
        inputLayout.addStretch(3)

        assetLayout.addLayout(inputLayout)

        self.tabAssets.setLayout(assetLayout)

    def browseAssets(self):
        assetFile = QFileDialog.getOpenFileName(self,
                                                "Open Asset",
                                                os.path.join(config.serverDir(), 'working', 'assets'),
                                                )
        correctedPath = assetFile[0].replace('//', '\\\\').replace('/', '\\')
        self.text_Directory.setText(correctedPath)

    def launchAsset(self):
        print 'And I grabbed her by the cat'
        if self.text_Directory.text() != '':
            self.openasset.emit(self.text_Directory.text())

    def updateDB(self):
        self.updateSceneList()
        self.updateShotList()

    def updateSceneList(self):
        BAD_DIRS = ['assets', 'animatic']
        self.dropdown_scene.clear()
        for i_scene, t_scene in enumerate(next(os.walk(os.path.join(config.serverDir(), 'working', 'scenes')))[1]):
            if t_scene not in BAD_DIRS:
                self.dropdown_scene.addItem(t_scene)
        config.setSeq(self.dropdown_scene.currentText())

    def updateShotList(self):
        config.setSeq(self.dropdown_scene.currentText())
        self.dropdown_shot.clear()
        if os.getenv('SEQ') != '':
            for i_shot, t_shot in enumerate(next(os.walk(os.path.join(config.serverDir(), 'working', 'scenes', os.getenv('SEQ'))))[1]):
                self.dropdown_shot.addItem(t_shot)
            config.setShot(self.dropdown_shot.currentText())
            self.updateTags()
        else:
            self.canLaunch()

    def emitlaunch(self):
        # Return the stage index to the launcher, add one to compensate for zero-based index
        config.setStage(self.getStageIndex())
        self.launch.emit(self.getStageIndex(), self.dropdown_tag.currentText())

    def emitcreate(self):
        config.setStage(self.getStageIndex())
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
        if self.dropdown_tag.count() >= 1:
            self.btn_launch.setEnabled(True)
        else:
            self.btn_launch.setDisabled(True)


class QDialog_FolderCreate(QDialog):

    sendirs = Signal(str, str)

    def __init__(self, parent=None):
        super(QDialog_FolderCreate, self).__init__(parent)

        self.sceneLabel = QLabel("Scene: ")
        self.sceneLabel.setMinimumWidth(40)
        self.sceneName = QLineEdit()
        self.sceneName.setMaximumWidth(150)
        self.sceneName.setPlaceholderText("Type Scene Here...")

        self.shotLabel = QLabel("Shot: ")
        self.shotLabel.setMinimumWidth(40)
        self.shotName = QLineEdit()
        self.shotName.setMaximumWidth(150)
        self.shotName.setPlaceholderText("Type Shot Here...")

        self.submitbtn = QPushButton("Create")
        self.quitbtn = QPushButton("Quit")
        self.quitbtn.clicked.connect(self.close)

        hbox_Scene = QHBoxLayout()
        hbox_Scene.addWidget(self.sceneLabel)
        hbox_Scene.addWidget(self.sceneName)
        hbox_Scene.addStretch(1)

        hbox_Shot = QHBoxLayout()
        hbox_Shot.addWidget(self.shotLabel)
        hbox_Shot.addWidget(self.shotName)
        hbox_Shot.addStretch(1)

        hbox_Cmd = QHBoxLayout()
        hbox_Cmd.addStretch(1)
        hbox_Cmd.addWidget(self.submitbtn)
        hbox_Cmd.addWidget(self.quitbtn)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addLayout(hbox_Scene)
        layout.addLayout(hbox_Shot)
        layout.addLayout(hbox_Cmd)

        # Set dialog layout
        self.setLayout(layout)

        # Add submitbtn signal
        self.submitbtn.clicked.connect(self.pressbtn)

    def pressbtn(self):
        self.sendirs.emit(self.sceneName.text(), self.shotName.text())
        self.sceneName.clear()
        self.shotName.clear()


class Launcher(QMainWindow):
    def __init__(self, parent=None):
        super(Launcher, self).__init__(parent)
        self.mainlayout = WindowLayout()
        self.initUI()

    def initUI(self):

        # CREATE MENU BAR
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        shotAction = QAction('&Create Shot', self)
        shotAction.setStatusTip('Build out folder structure for a new shot')
        shotAction.triggered.connect(self.create_dir)

        syncAction = QAction('&Sync Project', self)
        syncAction.setStatusTip('Sync Local Project with Server')
        syncAction.triggered.connect(self.synclocal)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        buildMenu = menubar.addMenu('&Build')

        fileMenu.addAction(exitAction)
        buildMenu.addAction(shotAction)
        buildMenu.addAction(syncAction)

        self.setCentralWidget(self.mainlayout)
        self.show()

    def create_dir(self):
        modalFolder = QDialog_FolderCreate()
        modalFolder.setWindowTitle('Create')
        modalFolder.show()
        modalFolder.sendirs.connect(self.send_to_make)

    def synclocal(self):
        BasketBuilder.rep_prod_dir()

    @Slot(str, str)
    def send_to_make(self, scene, shot):
        BasketBuilder.make_prod_dir(scene, shot)
        self.mainlayout.updateDB()