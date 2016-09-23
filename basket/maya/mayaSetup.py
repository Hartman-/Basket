import getpass
import os
import re
from time import strftime

import maya.cmds as cmds
from maya.mel import eval

import BasketGlobals as config


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
    while not fileSaved:
        mayaName = '%s_%s_%s_v%02d_%s_%s.ma' % (os.getenv('SEQ'), os.getenv('SHOT'), desc, version, 'preVis', getpass.getuser())
        mayaPath = os.path.join(config.stageDir(1), mayaName)
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
        abcName = '%s_%s_%s.abc' % ('asset', desc, getpass.getuser())
        fbxName = '%s_%s_%s.fbx' % ('asset', desc, getpass.getuser())

        fileAbc = os.path.join(config.libraryDir('models'), desc, abcName).replace('\\', '/')
        fileFbx = os.path.join(config.libraryDir('models'), desc, fbxName).replace('\\', '/')
        createDirs(fileAbc)
        selected = cmds.ls(selection=True)
        liststring = ''
        for i, o in enumerate(selected):
            liststring += '-root |'+str(o)+' '
        eval('AbcExport -j "-frameRange 1 1 -uvWrite -dataFormat ogawa %s -file %s";' % (liststring, fileAbc))
        cmds.file(fileFbx, exportSelected=True, type='FBX export')
        writeLocalLog(os.path.dirname(fileAbc), os.path.basename(cmds.file(query=True, sceneName=True)))


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
    abc = cmds.file(abcFile, i=True, returnNewNodes=True)
    fbx = cmds.file(fbxFile, r=True, returnNewNodes=True, namespace='fbxImport')
    refs = cmds.ls(type='reference')
    for i in refs:
        rFile = cmds.referenceQuery(i, f=True)
        cmds.file(rFile, importReference=True)

    print abc
    print fbx

    # objSel = cmds.ls(sl=True, s=1, dag=1)
    # for object in objSel:
    #     SgNodes = cmds.listConnections(object, type='shadingEngine')
    #     matMaya = cmds.listConnections(SgNodes[0] + '.surfaceShader')
    #     objectName = object.replace('Shape', '')
    #     print 'OBJECT: ' + objectName + ' | ' + 'MAYA SHADER: ' + matMaya[0]


def main():
    cmds.menu(label='LAW', tearOff=True, parent='MayaWindow')

    cmds.menuItem(divider=True, dividerLabel='Save')
    cmds.menuItem(label='Easy Save', command=easy_save)
    cmds.menuItem(label='Easy Iterate', command=easy_iterate)

    cmds.menuItem(divider=True, dividerLabel='Import')
    cmds.menuItem(label='Import Asset', command=asset_Import)

    cmds.menuItem(divider=True, dividerLabel='Export')
    cmds.menuItem(label='Publish Asset', command=asset_Publish)

    cmds.menuItem(divider=True, dividerLabel='Submit')
    cmds.menuItem(label='Submit to Qube')