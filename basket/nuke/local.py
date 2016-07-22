#!/usr/bin/python
# -'''- coding: utf-8 -'''-

# Run script in NUKE

# set the project to the local directory

import sys, os
import nuke

from PySide.QtCore import *
from PySide.QtGui import *

class LocalizeFiles:
    def __init__(self):
        # self.nukeroot = nuke.root()

        self.server_seq = 'Z:\\Users\\Ian\\Desktop\\PROJ_server\\Working\\xyz\\010\\d_Render\\seq\\'
        self.local_seq = 'Z:/Users/Ian/Desktop/PROJ_local/Working/xyz/010/d_Render/seq/ubercam.%04d.png'

        localexists = self.checkforlocalproject()
        if localexists[0] == True:
            if os.path.isdir(localexists[1] + 'Working\\xyz\\010') == False:
                dircreate = FolderBuilder()
                dircreate.createdir(localexists[1], 'xyz', '010')
                nuke.scriptSaveAs(filename=localexists[1] + '\\Working\\xyz\\010\\' + 'HelloWorld.nk')
        else:
            os.makedirs(localexists[1])
            dircreate = FolderBuilder()
            dircreate.createdir(localexists[1], 'xyz', '010')
            nuke.scriptSaveAs(filename=localexists[1] + '\\Working\\xyz\\010\\' + 'HelloWorld.nk')

    def proxylocal(self):
        self.nukeroot.knob('proxy').setValue(True)
        self.nukeroot.knob('proxy_type').setValue('format')
        self.nukeroot.knob('proxy_format').setValue(self.nukeroot.format().name())
        self.nukeroot.knob('proxySetting').setValue('always')

        self.n_read = nuke.toNode('Read1')
        print(self.n_read.knob('file').getValue())

        self.n_read.knob('proxy').setValue(self.local_seq)

    def getlocaldesktop(self):
        basedrive = 'Z:\\Users\\Ian\\Desktop\\'
        return basedrive

    def checkforlocalproject(self):
        desktop = self.getlocaldesktop()
        localdir = desktop + 'PROJ_local'

        if os.path.isdir(localdir) == True:
            return [True, localdir]
        else:
            return [False, localdir]

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.label = QLabel('hello world')
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)


# ---
# PORTED FOLDER BUILDER
# ---

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

# ---
#
# ---

if __name__ == '__main__':
    # form = Form()
    # form.setWindowTitle('Test')
    # form.show()

    test = LocalizeFiles()