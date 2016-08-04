#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import os
import sys
from glob import glob

from PySide.QtCore import *
from PySide.QtGui import *

from basket.gui import FolderBuild_ui


# DEFINE EXAMPLE ENVIRONMENT
os.environ['SHOW'] = 'PROJ_local'
os.environ['SEQ'] = 'xyz'
os.environ['SHOT'] = '010'


def rootDir(user):
    return 'C:\\Users\\' + str(user) + '\\Desktop\\LAW\\'


def getNukeScripts():
    nkFiles = glob(os.path.join(nukeDir(), '*.nk'))
    return nkFiles


def nukeDir():
    curDir = os.path.join(rootDir('IanHartman'), os.getenv('SHOW'), 'Working', os.getenv('SEQ'), os.getenv('SHOT'), '07. Comp')
    if not os.path.isdir(curDir):
        raise ValueError, 'NUKE Directory does not exist'
    return curDir


class FolderBuilder:
    def __init__(self):
        self.newdir = 'C:\\Users\\jszot.BKLYNDIGI\\Desktop\\PROJ-proj\\'

        self.project_directory = 'C:\\Users\\Ian\\Desktop\\PROJ-proj\\'

        self.publish_dir = self.project_directory + 'Publish\\'
        self.working_dir = self.project_directory + 'Working\\'

        self.subdirs = ['a_Layout', 'b_Animation', 'c_Lighting', 'd_Render']

        self.alldirs = [self.publish_dir, self.working_dir]

        self.scene = ''
        self.shot = ''

    def updatedirectories(self):
        self.publish_dir = self.project_directory + '\\Publish\\'
        self.working_dir = self.project_directory + '\\Working\\'
        self.alldirs = [self.publish_dir, self.working_dir]

    def builddir(self, base_dir, sub_dir):
        newdir = base_dir + self.scene + '\\' + self.shot + '\\' + sub_dir
        self.newdir = newdir

    @Slot(str, str, str)
    def createdir(self, path, sc, sh):
        self.setdirectory(path)
        self.scene = sc
        self.shot = sh

        for d in self.alldirs:
            for sub in self.subdirs:
                self.builddir(d, sub)
                if not os.path.exists(self.newdir):
                    os.makedirs(self.newdir)

    @Slot(str)
    def setdirectory(self, path):
        self.project_directory = path
        self.updatedirectories()

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = FolderBuild_ui.Form()
    form.setWindowTitle('Folder Creator')
    form.show()

    a = FolderBuilder()

    form.btnpressed.connect(a.createdir)
    form.dirselected.connect(a.setdirectory)
    # Run the main Qt loop
    sys.exit(app.exec_())
