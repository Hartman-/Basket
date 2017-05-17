#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import os, re
import getpass
from glob import glob
import nuke
import nukescripts
import BasketGlobals as config
from PySide.QtCore import *
from PySide.QtGui import *


def pluginPaths():
    paths = []

    user = str(getpass.getuser())
    userPath = os.path.join("W:\\SRPJ_LAW\\nuke\\users\\", user)
    if os.path.isdir(userPath):
        paths.append(userPath)

    showPath = "W:\\SRPJ_LAW\\nuke\\show\\HONU"
    if os.path.isdir(showPath):
        paths.append(showPath)

    return paths


def getFrameRange(title, frameRange):
    ret = nuke.getFramesAndViews(title, frameRange)
    newRange = ret[0]
    return newRange


def buildBatchScripts():
    exePath = "C:/Program Files/Nuke10.5v2/Nuke10.5.exe"
    nukeX = "--nukex"
    frameRange = '%s-%s' % (int(nuke.root().knob("first_frame").value()), int(nuke.root().knob("last_frame").value()))
    filePath = nuke.root().knob('name').value()
    fileName = os.path.splitext(os.path.basename(filePath))[0]

    selectedNodes = nuke.selectedNodes()
    writeNodes = []

    for n in selectedNodes:
        if n.Class() == 'Write':
            writeNodes.append(n)

    for i, n in enumerate(writeNodes):
        title = '[%s] Frame Range' % n.name()
        newRange = getFrameRange(title, frameRange)
        numInstances = nuke.getInput("[%s] Number of Instances:" % n.name(), "1")

        for index in range(0, int(numInstances)):
            firstFrame = int(newRange.split('-')[0])
            lastFrame = int(newRange.split('-')[1])
            adjustedRange = '%s-%s' % ((firstFrame + index), lastFrame)

            envpaths = pluginPaths()
            print  envpaths
            envstr = 'SET NUKE_PATH=%s;%s;' % (envpaths[0], envpaths[1])

            cmd = '"%s" %s -F %sx%s -X %s "%s"' % (exePath, nukeX, adjustedRange, numInstances, n.name(), filePath)
            userPath = os.path.expanduser('~')
            batPath = os.path.join(userPath, 'Desktop', '%s_%s_%s.bat' % (fileName, n.name(), index + 1))

            open(batPath, 'w').close()

            batstr = "%s\n%s" % (envstr, cmd)

            if os.path.isfile(batPath):
                if batstr != '':
                    f = open(batPath, 'a')
                    f.write(batstr)
                    f.close()

if nuke.env['gui']:
    class BatchSetup( nukescripts.PythonPanel ):
        def __init__(self):
            nukescripts.PythonPanel.__init__(self, 'Frame Range')

            firstframe = int(nuke.root()['first_frame'].value())
            lastframe = int(nuke.root()['last_frame'].value())

            self.frame_start = nuke.Int_Knob("start", "Start:")
            self.frame_end = nuke.Int_Knob("end", "End:")
            self.addKnob(self.frame_start)
            self.addKnob(self.frame_end)
            self.frame_start.setValue(firstframe)
            self.frame_end.setValue(lastframe)

            self.instances = nuke.Int_Knob('instances', 'Instances:')
            self.addKnob(self.instances)
            self.instances.setValue(1)

        def showModalDialog(self):
            result = nukescripts.PythonPanel.showModalDialog(self)
            if result:
                ret_str = '%s-%sx%s' % (self.frame_start.value(), self.frame_end.value(), self.instances.value())
                nuke.tprint(ret_str)
                return [self.frame_start.value(),
                        self.frame_end.value(),
                        self.instances.value()]


class HManager:
    def __init__(self):
        pass

    def easySave(self):
        description = nuke.getInput('Script Variable', 'bashComp').replace(' ', '')
        self.s_easySave(description)

    def s_easySave(self, description, server=config.nukeDir(), ver=1):
        fileSaved = False
        version = ver
        while not fileSaved:
            nkName = '%s_%s_%s_v%02d_%s_%s.nk' % (os.getenv('SEQ'), os.getenv('SHOT'), description, version, 'comp', getpass.getuser())
            nkPath = os.path.join(server, nkName)
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

    def createBatchScripts(self):
        exePath = nuke.env['ExecutablePath']
        nukeX = "--nukex"
        filePath = nuke.root().knob('name').value()
        fileName = os.path.splitext(os.path.basename(filePath))[0]

        selectedNodes = nuke.selectedNodes()
        writeNodes = []

        for n in selectedNodes:
            if n.Class() == 'Write':
                writeNodes.append(n)

        if len(writeNodes) == 0:
            nuke.message('No Write nodes selected!')
            return 1

        batch_setup = BatchSetup()

        for i, n in enumerate(writeNodes):
            title = '[%s] Frame Range' % n.name()
            newRange = batch_setup.showModalDialog()
            numInstances = int(newRange[2])

            for index in range(0, int(numInstances)):
                firstFrame = newRange[0]
                lastFrame = newRange[1]
                adjustedRange = '%s-%s' % ((firstFrame + index), lastFrame)

                envpaths = pluginPaths()
                print envpaths
                envstr = 'SET NUKE_PATH=%s;%s;' % (envpaths[0], envpaths[1])

                cmd = '"%s" %s -F %sx%s -X %s "%s"' % (exePath, nukeX, adjustedRange, numInstances, n.name(), filePath)
                userPath = os.path.expanduser('~')
                batPath = os.path.join(userPath, 'Desktop', '%s_%s_%s.bat' % (fileName, n.name(), index + 1))

                open(batPath, 'w').close()

                batstr = "%s\n%s" % (envstr, cmd)

                if os.path.isfile(batPath):
                    if batstr != '':
                        f = open(batPath, 'a')
                        f.write(batstr)
                        f.close()

    def refreshUI(self):
        nuke.updateUI()


def createWriteDirs():
    tgtDir = os.path.dirname(nuke.filename(nuke.thisNode()))
    osdir = nuke.callbacks.filenameFilter(tgtDir)
    if not os.path.isdir(osdir):
        os.makedirs(osdir)


def localizeRead():
    nukeroot = nuke.root()

    # Set the global variables to enable reading a proxy file
    # Set setting to 'always' to ensure tha the proxy files get read
    nukeroot.knob('proxy').setValue(True)
    nukeroot.knob('proxy_type').setValue('format')
    nukeroot.knob('proxy_format').setValue(nukeroot.format().name())
    nukeroot.knob('proxySetting').setValue('always')

    # Grab selected nodes in DAG
    selectedNodes = nuke.selectedNodes()

    # Double check that only read nodes were selected
    # Pop/Remove them if they aren't
    for i, node in enumerate (selectedNodes):
        if not node.Class().lower() == 'read':
            selectedNodes.pop(i)

    # Set each read node to the appropriate local directory
    for index, readnode in enumerate (selectedNodes):
        filename = readnode.knob('file').value()
        filepath = filename.replace(config.serverDir(), config.rootDir())
        readnode.knob('proxy').setValue(filepath)

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


# Foundry File Loader
# =====

def seqSubDirs(i):
    base = [ 'plates', 'cg', 'elements' ]
    set = {
        0: base,
        1: base
    }
    return set[i]


def getVersions():
    '''Return a dictionary of rendered versions per type'''
    # DEFINE THE DIRECTORIES YOU WANT TO INCLUDE
    types = seqSubDirs(0)
    # INITIALISE THE DICTIONARY WE WILL RETURN AT THE END OF THE FUNCTION
    versionDict = {}
    # GET THE DIRECTORY BASED ON THE CURRENT SHOT ENVIRONMENT
    shotDir = os.path.join( config.framesDir(), os.getenv('SEQ'), os.getenv('SHOT') )
    print shotDir
    # LOOP THROUGH THE FOLDERS INSIDE THE SHOT DIRECTORY AND COLLECT THE IMAGE SEQUENCES THEY CONTAIN
    for t in types:
        print t
        versionDict[t] = [] # THIS WILL HOLD THE FOUND SEQUENCES
        typeDir = os.path.join( shotDir, t ) # GET THE CURRENT DIRECTORY PATH
        for d in os.listdir( typeDir ): # LOOP THROUGH IT'S CONTENTS
            path = os.path.join( typeDir, d)
            print path
            # if os.path.isdir( path ): # LOOP THROUGH SUB DIRECTORIES
            versionDict[t].append( getFileSeq( path ) ) # RUN THE getFileSeq() FUNCTION AND APPEND IT'S OUTPUT TO THE LIST
    return versionDict


def getFileSeq( dirPath ):
    '''Return file sequence with same name as the parent directory. Very loose example!!'''
    path = os.path.dirname( dirPath )
    dirName = re.split(r'\.(\d+)\.', os.path.basename(dirPath))
    # COLLECT ALL FILES IN THE DIRECTORY THAT HVE THE SAME NAME AS THE DIRECTORY
    files = sorted(glob( os.path.join( path, '*.*.*' ) ), key=os.path.getmtime)
    print files
    # GRAB THE RIGHT MOST DIGIT IN THE FIRST FRAME'S FILE NAME
    firstString = re.findall( r'\d+', files[0] )[-1]
    # GET THE PADDING FROM THE AMOUNT OF DIGITS
    padding = len( firstString )
    # CREATE PADDING STRING FRO SEQUENCE NOTATION
    paddingString = '%02s' % padding
    # CONVERT TO INTEGER
    first = int( firstString )
    # GET LAST FRAME
    last = int( re.findall( r'\d+', files[-1] )[-1] )
    # GET EXTENSION
    ext = os.path.splitext( files[0] )[-1]
    # BUILD SEQUENCE NOTATION
    fileName = '%s.%%%sd%s %s-%s' % ( dirName[0], str(padding).zfill(2), ext, first, last )
    # RETURN FULL PATH AS SEQUENCE NOTATION
    return os.path.join( dirPath, fileName )


def createDbKnob():
    # CREATE USER KNOBS
    node = nuke.thisNode()
    tabKnob = nuke.Tab_Knob( 'DB', 'DB' )
    typeKnob = nuke.Enumeration_Knob( 'versionType', 'type', seqSubDirs(0) )
    updateKnob = nuke.PyScript_Knob( 'update', 'update' )
    updateKnob.setValue( 'assetManager.updateDbKnob()' )
    versionKnob = nuke.Enumeration_Knob( '_version', 'version', [] ) # DO NOT USE "VERSION" AS THE KNOB NAME AS THE READ NODE ALREADY HAS A "VERSION" KNOB
    loadKnob = nuke.PyScript_Knob( 'load', 'load' )

    # ASSIGN PYTHON SCRIPT AS ONE LARGE STRING
    loadScript = '''#THIS ASSUMES NO WHITE SPACES IN FILE PATH
node = nuke.thisNode()
path, range = node['_version'].value().split()
first, last = range.split('-')
node['file'].setValue( path )
node['first'].setValue( int(first) )
node['last'].setValue( int(last) )'''

    loadKnob.setValue( loadScript )

    # ADD NEW KNOBS TO NODE
    for k in ( tabKnob, typeKnob, updateKnob, versionKnob, loadKnob ):
        node.addKnob( k )
    # UPDATE THE VERSION KNOB SO IT SHOWS WHAT'S ON DISK / IN THE DATABASE
    updateDbKnob()


def updateDbKnob():
    node = nuke.thisNode()
    knob = nuke.thisKnob()

    # RUN ONLY IF THE TYPE KNOB CHANGES OR IF THE NODE PANEL IS OPENED
    if not knob or knob.name() in [ 'versionType', 'showPanel' ]:
        # GET THE VERSION DICTIONARY
        versionDict = getVersions()
        # POPULATE THE VERSION KNOB WITH THE VERSIONS REQUESTED THROUGH THE TYPE KNOB
        node['_version'].setValues( versionDict[ node['versionType'].value() ] )
        # SET THE A VALUE TO THE FIRST ITEM IN THE LIST
        # node['_version'].setValue(0)


# =====


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.label = QLabel('hello world')
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
