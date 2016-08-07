#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import os
import sys
from glob import glob

from PySide.QtCore import *
from PySide.QtGui import *

from basket import config

from basket.gui import FolderBuild_ui


class FolderBuilder:
    def __init__(self):
        self.newdir = 'C:\\Users\\jszot.BKLYNDIGI\\Desktop\\PROJ-proj\\'

        self.project_directory = config.rootDir() + 'PROJ_local\\'

        self.publish_dir = self.project_directory + 'Publish\\'
        self.working_dir = self.project_directory + 'Working\\'

        self.subdirs = ['01. PreVis', '02. Layout', '03. Anim', '04. FX', '05. Lighting', '06. Render', '07. Comp', '08. Edit']

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
