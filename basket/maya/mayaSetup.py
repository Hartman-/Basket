import getpass
import os
import re

import maya.cmds as cmds

import BasketGlobals as config


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
#
def easy_iterate(*args):
    filePath = cmds.file(query=True, sceneName=True)
    fileName = os.path.basename(filePath)
    fileDir = os.path.dirname(filePath)

    # Make sure there is a version in the file name
    if re.search(r'[vV]\d+', fileName):
        fileSaved = False
        # Regex split the filename around version delimiter
        # Get the number
        split = re.split(r'([vV]\d+)', 'xyz_010_cubeTest_v01_imh29.ma')
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

def main():
    cmds.menu(label='Manage', tearOff=True, parent='MayaWindow')
    cmds.menuItem(divider=True, dividerLabel='Save')
    cmds.menuItem(label='Easy Save', command=easy_save)
    cmds.menuItem(label='Easy Iterate', command=easy_iterate)
    cmds.menuItem(divider=True, dividerLabel='Export')
    cmds.menuItem(label='Publish Asset')
    cmds.menuItem(divider=True, dividerLabel='Submit')
    cmds.menuItem(label='Submit to Qube')