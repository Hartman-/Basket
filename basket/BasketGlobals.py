#!/usr/bin/env python

import os
import platform
from glob import glob


# GLOBAL CONSTANTS

# --- File Structure Constants ---
BASE_DIRS = {
             'delivery': [
                 'CritiqueArchive'
             ],
             'docs': [],
             'frames': [],
             'library': [
                 'models',
                 'templates',
                 'sound',
                 'texture'
             ],
             'publish': [],
             'source': [
                 'plates',
                 'reference'
             ],
             'working': [
                 'scenes',
                 'assets'
             ]}

PROD_DIRS = [
    'scenes',
    'publish'
]

STAGE_DIRS = [
    '01. PreVis',
    '02. Layout',
    '03. Anim',
    '04. FX',
    '05. Lighting',
    '06. Render',
    '07. Comp'
]

FRAME_DIRS = [
    'cg',
    'comp',
    'edit',
    'elements',
    'plates'
]

# GLOBAL FUNCTIONS


def curOS():
    currentOS = platform.system()
    return currentOS


def rootDir():
    curDir = os.path.expanduser('~') + '\\Desktop\\LAW_local\\'
    # MAYA LOVES TO MAKE MY LIFE DIFFICULT
    # THROWING \DOCUMENTS INTO SHIT
    if 'Documents' in curDir:
        curDir = curDir.replace('/', '\\').replace('\\Documents', '')
    return curDir


def serverDir():
    # \\awexpress.westphal.drexel.edu\digm_anfx\SRPJ_LAW\ALAW\renderman\HeroShipTurntable_v002_imh29_0\images
    # curDir = os.path.expanduser('~') + '\\Desktop\\LAW_s\\'
    curDir = '\\\\awexpress.westphal.drexel.edu\\digm_anfx\\SRPJ_LAW'
    # MAYA LOVES TO MAKE MY LIFE DIFFICULT
    # THROWING \DOCUMENTS INTO SHIT
    if 'Documents' in curDir:
        curDir = curDir.replace('/', '\\').replace('\\Documents', '')
    return curDir


def getNukeScripts():
    nkFiles = glob(os.path.join(nukeDir(), '*.nk'))
    return nkFiles


def nukeDir():
    curDir = os.path.join(rootDir(), 'working', 'scenes', os.getenv('SEQ'), os.getenv('SHOT'), '07. Comp')
    if not os.path.isdir(curDir):
        raise ValueError, 'NUKE Directory does not exist'
    return curDir


def serverStageDir(stage):
    curDir = os.path.join(serverDir(), 'working', 'scenes', os.getenv('SEQ'), os.getenv('SHOT'), stage)
    if not os.path.isdir(curDir):
        raise ValueError, 'Stage Directory does not exist'
    return curDir


def localFramesDir():
    curDir = os.path.join(rootDir(), 'frames', os.getenv('SEQ'), os.getenv('SHOT'), 'plates')
    if not os.path.isdir(curDir):
        raise ValueError, 'Frames Directory does not exist'
    return curDir


def stageDir(stage):
    stages = ['01. PreVis', '02. Layout', '03. Anim', '04. FX', '05. Lighting', '06. Render', '07. Comp', '08. Edit']
    baseDir = os.path.join(serverDir(), 'working', 'scenes', os.getenv('SEQ'), os.getenv('SHOT'))
    # Thanks for starting at Zero lists!
    curDir = os.path.join(baseDir, stages[stage - 1])

    if not os.path.isdir(curDir):
        raise ValueError, 'File Directory does not exist: ' + curDir
    return curDir


def publishDir(stage):
    stages = ['01. PreVis', '02. Layout', '03. Anim', '04. FX', '05. Lighting', '06. Render', '07. Comp', '08. Edit']
    baseDir = os.path.join(serverDir(), 'publish', os.getenv('SEQ'), os.getenv('SHOT'))
    # Thanks for starting at Zero lists!
    curDir = os.path.join(baseDir, stages[stage])
    if not os.path.isdir(curDir):
        raise ValueError, 'File Directory does not exist: ' + curDir
    return curDir


def seqDir():
    curDir = os.path.join(serverDir(), 'Frames', os.getenv('SEQ'), os.getenv('SHOT'), 'plates')
    if not os.path.isdir(curDir):
        raise ValueError, 'Frames Directory does not exist'
    return curDir


def libraryDir(sub):
    curDir = os.path.join(serverDir(), 'library', str(sub))
    if not os.path.isdir(curDir):
        raise ValueError, 'Frames Directory does not exist'
    return curDir


def framesDir():
    curDir = os.path.join(serverDir(), 'Frames')
    print curDir
    if not os.path.isdir(curDir):
        raise ValueError, 'Frames Directory does not exist'
    return curDir


# SET SHOW ENV VARIABLE
def setShow(show):
    os.environ['SHOW'] = str(show)


# SET SEQ ENV VARIABLE
def setSeq(seq):
    os.environ['SEQ'] = str(seq)


# SET SHOT ENV VARIABLE
def setShot(shot):
    os.environ['SHOT'] = str(shot)


def setStage(stage):
    os.environ['STAGE'] = str(stage)


def stageNum():
    return int(os.getenv('STAGE')) - 1


def applicationPath(ext):
    if type(ext) is not int:
        paths = {
            '.ma': 'C:\\Program Files\\Autodesk\\Maya2016.5\\bin\\maya.exe',
            '.mb': 'C:\\Program Files\\Autodesk\\Maya2016.5\\bin\\maya.exe',
            '.nk': 'C:\\Program Files\\Nuke10.0v4\\Nuke10.0.exe',
            '.hip': 'C:\\Program Files\\Side Effects Software\\Houdini 15.5.565\\bin\\houdinifx.exe',
            '.hipnc': 'C:\\Program Files\\Side Effects Software\\Houdini 15.5.565\\bin\\houdinifx.exe'
        }
        return paths[ext]
    else:
        paths = {
            1: 'C:\\Program Files\\Autodesk\\Maya2016.5\\bin\\maya.exe',
            2: 'C:\\Program Files\\Autodesk\\Maya2016.5\\bin\\maya.exe',
            3: 'C:\\Program Files\\Autodesk\\Maya2016.5\\bin\\maya.exe',
            4: 'C:\\Program Files\\Side Effects Software\\Houdini 15.5.565\\bin\\houdinifx.exe',
            5: 'C:\\Program Files\\Autodesk\\Maya2016.5\\bin\\maya.exe',
            6: 'C:\\Program Files\\Autodesk\\Maya2016.5\\bin\\maya.exe',
            7: 'C:\\Program Files\\Nuke10.0v4\\Nuke10.0.exe',
            8: 'C:\\Program Files\\Adobe\\Adobe Premiere Pro CC 2015\\Adobe Premiere Pro.exe'
        }
        return paths[ext]


if __name__ == '__main__':
    print applicationPath('.ma')
