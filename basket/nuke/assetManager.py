#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import os, re
import getpass
import nuke
import nukescripts

import BasketGlobals as config

from PySide.QtCore import *
from PySide.QtGui import *

class HManager:
    def __init__(self):
        print('helpme')

    def easySave(self):
        description = nuke.getInput('Script Variable', 'bashComp').replace(' ', '')
        self.s_easySave(description)

    def s_easySave(self, description, ver=1):
        fileSaved = False
        version = ver
        while not fileSaved:
            nkName = '%s_%s_%s_v%02d_%s_%s.nk' % (os.getenv('SEQ'), os.getenv('SHOT'), description, version, 'comp', getpass.getuser())
            nkPath = os.path.join(config.nukeDir(), nkName)
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

    def localizeRead(self):
        selectedNodes = nuke.SelectedNodes()

        # Double check that only write nodes were selected
        for i, node in enumerate (selectedNodes):
            if not node.Class() == 'write':
                selectedNodes.pop(i)

        # Set each write node to the appropriate local directory
        node.knob('proxy').setValue(self.local_seq)


# class LoaderPanel( nukescripts.PythonPanel ):
#     def __init__(self, nkScripts):
#         nukescripts.PythonPanel.__init__( self, 'Open Nuke Script')
#         self.checkboxes = []
#         self.nkScripts = nkScripts
#
#         for i, n in enumerate (self.nkScripts):
#             k = nuke.Boolean_Knob('nk_%s' % i, os.path.basename(n))
#             self.addKnob(k)
#             k.setFlag(nuke.STARTLINE)
#             self.checkboxes.append(k)
#
#     def knobChanged(self,knob):
#         if knob in self.checkboxes:
#             for cb in self.checkboxes:
#                 if knob == cb:
#                     index = int( knob.name().split('_')[-1])
#                     self.selectedScript = self.nkScripts[index]
#                     continue
#                 cb.setValue(False)








class LocalizeFiles:
    def __init__(self):
        # self.nukeroot = nuke.root()

        self.server_seq = 'Z:\\Users\\Ian\\Desktop\\PROJ_server\\Working\\xyz\\010\\d_Render\\seq\\'
        self.local_seq = 'Z:/Users/Ian/Desktop/PROJ_local/Working/xyz/010/d_Render/seq/ubercam.%04d.png'

        localexists = self.checkforlocalproject()
        if localexists[0] == True:
            if os.path.isdir(localexists[1] + 'Working\\xyz\\010') == False:
                nuke.scriptSaveAs(filename=localexists[1] + '\\Working\\xyz\\010\\' + 'HelloWorld.nk')
        else:
            os.makedirs(localexists[1])
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
