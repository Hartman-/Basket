#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import os, sys
from PySide.QtCore import *
from PySide.QtGui import *

import Pinapple


class FolderBuilder:
    def __init__(self):
        self.newdir = 'C:\\Users\\Ian\\Desktop\\PROJ-proj\\'

        self.publish_dir = 'C:\\Users\\Ian\\Desktop\\PROJ-proj\\Publish\\'
        self.working_dir = 'C:\\Users\\Ian\\Desktop\\PROJ-proj\\Working\\'

        self.alldirs = [self.publish_dir, self.working_dir]

        self.scene = ''
        self.shot = ''

    def builddir(self, base_dir):
        newdir = base_dir + self.scene + '\\' + self.shot
        self.newdir = newdir

    @Slot(str, str)
    def createdir(self, sc, sh):
        self.scene = sc
        self.shot = sh

        for d in self.alldirs:
            self.builddir(d)
            if not os.path.exists(self.newdir):
                os.makedirs(self.newdir)

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Pinapple.Form()
    form.setWindowTitle('Folder Creator')
    form.show()

    a = FolderBuilder()

    form.btnpressed.connect(a.createdir)
    # Run the main Qt loop
    sys.exit(app.exec_())