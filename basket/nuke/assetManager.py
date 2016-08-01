#!/usr/bin/python
# -'''- coding: utf-8 -'''-

# Run script in NUKE

# set the project to the local directory

import sys, os, re
import nuke

from PySide.QtCore import *
from PySide.QtGui import *

class Environment:
    def __init__(self):

        # DEFINE EXAMPLE ENVIRONMENT
        os.environ['SHOW'] = 'PROJ_local'
        os.environ['SEQ'] = 'xyz'
        os.environ['SHOT'] = '010'

    def rootDir(self, user):
        return 'C:\\Users\\' + str(user) + '\\Desktop\\LAW\\'

    def nukeDir(self):
        curDir = os.path.join(self.rootDir('IanHartman'), os.getenv('SHOW'), 'Working', os.getenv('SEQ'), os.getenv('SHOT'), '07. Comp')
        if not os.path.isdir( curDir ):
            raise ValueError, 'NUKE Directory does not exist'
        return curDir

    # SET SHOW ENV VARIABLE
    def setShow(self, show):
        os.environ['SHOW'] = str(show)

    # SET SEQ ENV VARIABLE
    def setSeq(self, seq):
        os.environ['SEQ'] = str(seq)

    # SET SHOT ENV VARIABLE
    def setShot(self, shot):
        os.environ['SHOT'] = str(shot)


class HManager:
    def __init__(self):
        self.env = Environment()
        self.nkDir = self.env.nukeDir()

    def easySave(self):
        description = nuke.getInput( 'Script Variable', 'bashComp' ).replace(' ','')

        fileSaved = False
        version = 1
        while not fileSaved:
            nkName = '%s_%s_%s_%s_v%02d.nk' % ( os.getenv('SHOW'), os.getenv('SEQ'), os.getenv('SHOT'), description, version)
            nkPath = os.path.join(self.nkDir, nkName)
            if os.path.isfile(nkPath):
                version += 1
                continue
            nuke.scriptSaveAs(nkPath)
            fileSaved = True
        return nkPath

    # CHECK FOR VERSION IN SCRIPT NAME
    def checkScriptName(self):
        if not re.search(r'[vV]\d+', nuke.root().name()):
            raise NameError, 'Please include a version number and save script again.'

    def refreshUI(self):
        nuke.updateUI()


class HGui:
    def __init__(self):



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