#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import os, sys
from PySide.QtCore import *
from PySide.QtGui import *

from basket import Pinapple


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

    @Slot(str, str)
    def createdir(self, sc, sh):
        self.scene = sc
        self.shot = sh

        for d in self.alldirs:
            for sub in self.subdirs:
                self.builddir(d, sub)
                if not os.path.exists(self.newdir):
                    os.makedirs(self.newdir)

    @Slot(str)
    def setdirectory(self, string):
        self.project_directory = string
        self.updatedirectories()

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Pinapple.Form()
    form.setWindowTitle('Folder Creator')
    form.show()

    a = FolderBuilder()

    form.btnpressed.connect(a.createdir)
    form.dirselected.connect(a.setdirectory)
    # Run the main Qt loop
    sys.exit(app.exec_())
