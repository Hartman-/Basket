import getpass
import os
import re
from time import strftime

from shiboken import wrapInstance

import maya.cmds as cmds
from maya.mel import eval
import maya.OpenMayaUI as omui

from PySide import QtCore
from PySide import QtGui

import BasketGlobals as config


L_COLUMN_WIDTH = 100
R_COLUMN_WIDTH = 160


def setProjectDirectory():
    cmds.workspace('\\\\awexpress.westphal.drexel.edu\\digm_anfx\\SRPJ_LAW', o=True)


def setupRenderEnvironment():
    if not cmds.pluginInfo('RenderMan_for_Maya.mll', query=True, loaded=True):
        cmds.loadPlugin('RenderMan_for_Maya.mll', quiet=True)
        cmds.pluginInfo('RenderMan_for_Maya.mll', edit=True, autoload=True)
    if not cmds.pluginInfo('gpuCache.mll', query=True, loaded=True):
        cmds.loadPlugin('gpuCache.mll', quiet=True)
        cmds.pluginInfo('gpuCache.mll', edit=True, autoload=True)
    if cmds.pluginInfo('Mayatomr.mll', query=True, loaded=True):
        cmds.unloadPlugin('Mayatomr.mll', force=True)
    cmds.setAttr("defaultRenderGlobals.imageFilePrefix", "frame", type='string')


def createDirs(input):
    tgtDir = os.path.dirname(input)
    if not os.path.isdir(tgtDir):
        os.makedirs(tgtDir)


def writeLocalLog(path, message):
    txtpath = os.path.join(path, '_publishLog.txt')
    file = open(txtpath, 'a')
    file.write(str(strftime("%d %B %Y %H:%M:%S")) + ' | ' + str(message) + ' | ' + getpass.getuser() + '\n')
    file.close()


def easy_save(*args):
    variable = cmds.promptDialog(
        title='Easy Save',
        message='Enter Variable:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel').replace(' ', '')
    if variable == 'OK':
        text = cmds.promptDialog(query=True, text=True)
        f_easySave(text)



# Adding the file incrementation functionality that Maya should have
def easy_iterate(*args):
    filePath = cmds.file(query=True, sceneName=True)
    fileName = os.path.basename(filePath)
    fileDir = os.path.dirname(filePath)

    # Make sure there is a version in the file name
    if re.search(r'[vV]\d+', fileName):
        fileSaved = False
        # Regex split the filename around version delimiter
        # Get the number
        split = re.split(r'([vV]\d+)', fileName)
        version = int(split[1][1:])
        while not fileSaved:
            newName = '%sv%02d%s' % (split[0], version, split[2])
            newPath = os.path.join(fileDir, newName)
            if os.path.isfile(newPath):
                version += 1
                continue
            cmds.file(rename=newPath)
            cmds.file(save=True, type='mayaAscii')
            fileSaved = True
        return newPath


# Functional EasySave
# Defines the backbone of EasySave allowing for separate Variables to be defined
# Automatically builds the correct filename
def f_easySave(desc, ver=1):
    fileSaved = False
    version = ver

    if os.getenv('SEQ') != 'assets':
        while not fileSaved:
            stageName = config.STAGE_DIRS[config.stageNum()].split(' ')[1]
            mayaName = '%s_%s_%s_v%02d_%s_%s.ma' % (os.getenv('SEQ'), os.getenv('SHOT'), desc, version, stageName, getpass.getuser())
            mayaPath = os.path.join(config.stageDir(config.stageNum()), mayaName)
            if os.path.isfile(mayaPath):
                version += 1
                continue
            cmds.file(rename=mayaPath)
            cmds.file(save=True, type='mayaAscii')
            fileSaved = True
        return mayaPath
    else:
        while not fileSaved:
            mayaName = '%s_v%02d_%s.ma' % (desc, version, getpass.getuser())
            mayaPath = os.path.join(config.serverDir(), 'working', os.getenv('SEQ'), os.getenv('SHOT'), mayaName)
            if os.path.isfile(mayaPath):
                version += 1
                continue
            cmds.file(rename=mayaPath)
            cmds.file(save=True, type='mayaAscii')
            fileSaved = True
        return mayaPath


def asset_Publish(*args):
    var = cmds.promptDialog(
        title='Publish Asset',
        message='Asset Name:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel').replace(' ', '')
    if var == 'OK':
        desc = cmds.promptDialog(query=True, text=True)
        # abcName = '%s_%s_%s.abc' % ('asset', desc, getpass.getuser())
        fbxName = '%s_%s_%s.fbx' % ('asset', desc, getpass.getuser())

        # fileAbc = os.path.join(config.libraryDir('models'), desc, abcName).replace('\\', '/')
        fileFbx = os.path.join(config.libraryDir('models'), desc, fbxName).replace('\\', '/')
        createDirs(fileFbx)
        selected = cmds.ls(selection=True)
        liststring = ''
        for i, o in enumerate(selected):
            liststring += '-root |'+str(o)+' '
        # eval('AbcExport -j "-frameRange 1 1 -uvWrite -writeFaceSets -writeUVSets -dataFormat ogawa %s -file %s";' % (liststring, fileAbc))
        cmds.file(fileFbx, exportSelected=True, type='FBX export')
        writeLocalLog(os.path.dirname(fileFbx), os.path.basename(cmds.file(query=True, sceneName=True)))


def asset_Import(*args):
    basicFilter = "*.abc"
    # print config.libraryDir('models')
    ifile = cmds.fileDialog2(
        dialogStyle=2,
        fileMode=1,
        dir=config.libraryDir('models'),
        fileFilter=basicFilter)
    abcFile = ifile[0]
    fbxFile = os.path.splitext(abcFile)[0] + '.fbx'
    print fbxFile

    fbx = cmds.file(fbxFile, r=True, returnNewNodes=True, namespace='ifbx')

    # Get all references in the scene
    # Make the references imported
    refs = cmds.ls(type='reference')
    for i in refs:
        rFile = cmds.referenceQuery(i, f=True)
        cmds.file(rFile, importReference=True)

    abc = cmds.file(abcFile, i=True, returnNewNodes=True)

    abcList = abc

    for i_shape, n_shape in enumerate(abcList):
        if not cmds.objectType(n_shape, isType='shape'):
            abcList.pop(i_shape)

    for i_abc, n_abc in enumerate(abcList):
        for n_fbx in fbx:
            print 'abc: ' + n_abc
            print 'fbx: ' + n_fbx.replace('ifbx:', '')
            if n_abc in n_fbx.replace('ifbx:', ''):
                print 'hit me baby one more time'
                # cmds.connectAttr(n_abc.outPolyMesh[0], n_fbx.inMesh, f=True)
                # eval('connectAttr -f %s.outPolyMesh[0] %s.inMesh;' % (n_abc, n_fbx))

                sgNode = cmds.listConnections(n_fbx, type='shadingEngine')
                matMaya = cmds.listConnections(sgNode[0] + '.surfaceShader')
                objectName = n_fbx.replace('Shape', '')
                print 'OBJECT: ' + objectName + ' | ' + 'MAYA SHADER: ' + matMaya[0]
                cmds.select(n_abc)
                cmds.hyperShade(assign=matMaya[0])
                cmds.select(cl=True)
                cmds.select(n_fbx)
                cmds.delete()
                cmds.select(cl=True)


def scene_Publish(*args):
    fileSaved = False
    filePath = cmds.file(query=True, sceneName=True)
    fileName = os.path.basename(filePath)
    split = fileName.split('_')
    newName = '%s_%s_%s_%s.ma' % (split[0], split[1], split[4], split[5])
    while not fileSaved:
        mayaPath = os.path.join(config.publishDir(config.stageNum()), newName)
        cmds.file(rename=mayaPath)
        cmds.file(save=True, type='mayaAscii')
        writeLocalLog(os.path.dirname(mayaPath), fileName)
        fileSaved = True
    return mayaPath


def scene_Reference(*args):
    basicFilter = "*.ma"
    ifile = cmds.fileDialog2(
        caption='Reference Published Scene',
        okCaption='Reference',
        dialogStyle=2,
        fileMode=1,
        dir=config.publishDir(config.stageNum()),
        fileFilter=basicFilter)
    maFile = ifile[0]
    print maFile
    namespace = os.path.basename(maFile)[:-3]
    publishRef = cmds.file(maFile, r=True, returnNewNodes=True, namespace=namespace)


def maya_main_window():
    maya_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(maya_ptr), QtGui.QWidget)


class Label(QtGui.QLabel):
    def __init__(self, text, parent=None):
        super(Label, self).__init__(parent)
        self.setFixedWidth(L_COLUMN_WIDTH)
        self.setContentsMargins(0, 0, 5, 0)
        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.setText(text)


class Input(QtGui.QLineEdit):
    def __init__(self, text, width=R_COLUMN_WIDTH, parent=None):
        super(Input, self).__init__(parent)
        self.setText(text)
        self.setMaximumWidth(width)


class RenderDialog(QtGui.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(RenderDialog, self).__init__(parent)

        # Default Values
        self.cmd = '"C:\\Program Files\\Autodesk\\Maya2016.5\\bin\\render.exe" -r rman'
        self.project = ' -proj "\\\\awexpress.westphal.drexel.edu\digm_anfx\SRPJ_LAW"'
        self.camera = 'persp'
        self.startFrame = cmds.getAttr('defaultRenderGlobals.startFrame')
        self.endFrame = cmds.getAttr('defaultRenderGlobals.endFrame')
        # rlayer = 'master'
        self.numChunks = 1
        self.namePrefix = cmds.getAttr('defaultRenderGlobals.imageFilePrefix')
        self.shadingRate = 16
        self.resWidth = cmds.getAttr('defaultResolution.width')
        self.resHeight = cmds.getAttr('defaultResolution.height')

        lprefix = Label('Image Prefix')
        self.opprefix = Input(str(self.namePrefix))
        prefixLayout = QtGui.QHBoxLayout()
        prefixLayout.addWidget(lprefix)
        prefixLayout.addWidget(self.opprefix)

        lcamera = Label('Camera')
        self.opcamera = QtGui.QComboBox()

        cameras = cmds.listCameras()
        for index, cam in enumerate(cameras):
            self.opcamera.addItem(cam)
            if cmds.getAttr(cam + '.renderable'):
                self.opcamera.setCurrentIndex(index)

        camLayout = QtGui.QHBoxLayout()
        camLayout.addWidget(lcamera)
        camLayout.addWidget(self.opcamera)

        lstartf = Label('Start Frame')
        self.opstartf = Input(str(int(self.startFrame)))
        startfLayout = QtGui.QHBoxLayout()
        startfLayout.addWidget(lstartf)
        startfLayout.addWidget(self.opstartf)

        lendf = Label('End Frame')
        self.opendf = Input(str(int(self.endFrame)))
        endfLayout = QtGui.QHBoxLayout()
        endfLayout.addWidget(lendf)
        endfLayout.addWidget(self.opendf)

        lchunk = Label('# of Chunks')
        self.opchunks = Input(str(self.numChunks))
        chunkLayout = QtGui.QHBoxLayout()
        chunkLayout.addWidget(lchunk)
        chunkLayout.addWidget(self.opchunks)

        inputWidth = (R_COLUMN_WIDTH/2) - 9

        lres = Label('Resolution')
        self.opresw = Input(str(self.resWidth), width=inputWidth)
        self.opresh = Input(str(self.resHeight), width=inputWidth)
        resLayout = QtGui.QHBoxLayout()
        resLayout.addWidget(lres)
        resLayout.addWidget(self.opresw)
        resLayout.addWidget(self.opresh)

        lshading = Label('Shading Rate')
        self.opshading = Input(str(self.shadingRate))
        shadingLayout = QtGui.QHBoxLayout()
        shadingLayout.addWidget(lshading)
        shadingLayout.addWidget(self.opshading)

        btn_generate = QtGui.QPushButton('Generate')
        btn_generate.clicked.connect(self.generate_scripts)
        btn_clear = QtGui.QPushButton('Clear')
        btn_clear.clicked.connect(self.clear_scripts)
        cmdLayout = QtGui.QHBoxLayout()
        cmdLayout.addWidget(btn_generate)
        cmdLayout.addWidget(btn_clear)

        self.cmd_text = QtGui.QTextEdit()

        windowLayout = QtGui.QVBoxLayout()
        windowLayout.addLayout(prefixLayout)
        windowLayout.addLayout(camLayout)
        windowLayout.addLayout(startfLayout)
        windowLayout.addLayout(endfLayout)
        windowLayout.addLayout(chunkLayout)
        windowLayout.addLayout(resLayout)
        windowLayout.addLayout(shadingLayout)
        windowLayout.addLayout(cmdLayout)
        windowLayout.addWidget(self.cmd_text)

        self.setLayout(windowLayout)

    def batch_frame_ranges(self, startf, endf, numchunks):
        ranges = []

        # Start a while loop to construct each flag string
        i = startf
        while i <= numchunks:
            frange = ' -s %s -e %s -b %s' % (i, endf, numchunks)
            ranges.append(frange)
            i += 1

        # return list of flag strings
        return ranges

    def generate_scripts(self):
        self.clear_scripts()
        filePath = cmds.file(query=True, sceneName=True)

        chunks = self.batch_frame_ranges(
            int(self.opstartf.text()),
            int(self.opendf.text()),
            int(self.opchunks.text())
        )

        scripts = []

        for index, chunk in enumerate(chunks):
            imageDir = '{frames/%s/%s/cg}' % (os.getenv('SEQ'), os.getenv('SHOT'))
            script = '@set SEQ=%s\n@set SHOT=%s\n@set %s\n%s%s -im %s -fnc name.#.ext -of OpenEXR -pad 4 -cam %s -res %s %s%s -setAttr ShadingRate %s "%s"' % (
                os.getenv('SEQ'),
                os.getenv('SHOT'),
                'RMS_SCRIPT_PATHS=X:\\Classof2017\\LobstersAreWeird\\basket\\renderman',
                self.cmd,
                self.project,
                self.opprefix.text(),
                self.opcamera.currentText(),
                self.opresw.text(),
                self.opresh.text(),
                chunk,
                self.opshading.text(),
                filePath
            )
            scripts.append(script)
            self.cmd_text.append(script + ' \n')

            if ':' in self.opcamera.currentText():
                cleanCam = self.opcamera.currentText().split(':')[1]
            else:
                cleanCam = self.opcamera.currentText()

            noDocuments = os.path.expanduser('~').replace('/', '\\').replace('\\Documents', '')
            batpath = os.path.join(noDocuments, 'Desktop', '%s_%s_%s_RenderBat.bat' % (os.getenv('SEQ'), cleanCam, index))
            file = open(batpath, 'a')
            file.write(script + ' \n')
            file.close()


        print scripts

    def clear_scripts(self):
        self.cmd_text.clear()


def render_Batch(*args):
    ui = RenderDialog()
    ui.setWindowTitle('Generate Batch Script')
    ui.show()


def main():
    cmds.menu(label='LAW', tearOff=True, parent='MayaWindow')

    # cmds.menuItem(divider=True, dividerLabel='Manage')
    # cmds.menuItem(label='Change Shot', command=switch_shot)

    cmds.menuItem(divider=True, dividerLabel='Save')
    cmds.menuItem(label='Easy Save', command=easy_save)
    cmds.menuItem(label='Easy Iterate', command=easy_iterate)

    cmds.menuItem(divider=True, dividerLabel='Import')
    # cmds.menuItem(label='Import Asset', command=asset_Import)
    cmds.menuItem(label='Reference Stage', command=scene_Reference)

    cmds.menuItem(divider=True, dividerLabel='Export')
    cmds.menuItem(label='Publish Scene', command=scene_Publish)
    cmds.menuItem(label='Publish Asset', command=asset_Publish)

    # cmds.menuItem(divider=True, dividerLabel='Submit')
    # cmds.menuItem(label='Submit to Qube')

    cmds.menuItem(divider=True, dividerLabel='Render')
    cmds.menuItem(label='Generate Batch Script', command=render_Batch)

    setProjectDirectory()
    setupRenderEnvironment()
