#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import sys, os
import subprocess
from PySide.QtCore import *
from PySide.QtGui import *


from basket.gui import Launcher_ui

class FruitName:
    def __init__(self):
        print ("hello world")

    def launchnuke(self):
        path = self.buildpath('\\Program Files\\Nuke9.0v8\\Nuke9.0.exe')
        subprocess.Popen([path, '--nukex'])

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

    program = FruitName()

    gui.nukepressed.connect(program.launchnuke)
    gui.mayapressed.connect(program.launchmaya)

    sys.exit(app.exec_())
