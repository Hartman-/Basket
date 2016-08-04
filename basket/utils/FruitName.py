#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import sys, os
import subprocess
from PySide.QtCore import *
from PySide.QtGui import *

from basket.gui import Launcher_ui
from basket.utils import Pinapple
from basket.gui import FileSelector

class FruitName:
    def __init__(self):
        print ("hello world")

    @Slot(str)
    def launchnuke(self, filepath):
        path = self.buildpath('\\Program Files\\Nuke9.0v8\\Nuke9.0.exe')
        subprocess.Popen([path, '--nukex', filepath])

    def launchmaya(self):
        path = self.buildpath('\\Program Files\\Autodesk\\Maya2016\\bin\\maya.exe')
        subprocess.Popen(path)

    def buildpath(self, exe):
        basedrive = os.path.abspath(os.sep)

        if basedrive[2:] == "\\":
            basedrive = basedrive[:2]

        exepath = basedrive + exe
        return exepath

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form

    gui = Launcher_ui.Launcher()
    gui.setWindowTitle('VFX Launcher')
    gui.show()

    nukeFile_gui = FileSelector.Form(Pinapple.getNukeScripts())
    nukeFile_gui.setWindowTitle('Test')

    program = FruitName()

    gui.nukepressed.connect(nukeFile_gui.show)
    gui.mayapressed.connect(program.launchmaya)
    nukeFile_gui.launch.connect(program.launchnuke)

    sys.exit(app.exec_())
