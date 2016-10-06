#!/usr/bin/env python

import os
import platform
from glob import glob


# GLOBAL CONSTANTS

# --- File Structure Constants ---
BASE_DIRS = {
             'delivery': [
                 'dailies'
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
             'working': []}

PROD_DIRS = [
    'working',
    'publish'
]

STAGE_DIRS = [
    '01. PreVis',
    '02. Layout',
    '03. Anim',
    '04. FX',
    '05. Lighting',
    '06. Render',
    '07. Comp',
    '08. Edit'
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
    curDir = os.path.join(rootDir(), 'Working', os.getenv('SEQ'), os.getenv('SHOT'), '07. Comp')
    if not os.path.isdir(curDir):
        raise ValueError, 'NUKE Directory does not exist'
    return curDir


def serverStageDir(stage):
    curDir = os.path.join(serverDir(), 'Working', os.getenv('SEQ'), os.getenv('SHOT'), stage)
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
    baseDir = os.path.join(serverDir(), 'Working', os.getenv('SEQ'), os.getenv('SHOT'))
    # Thanks for starting at Zero lists!
    curDir = os.path.join(baseDir, stages[stage - 1])

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


if __name__ == '__main__':
    print framesDir(None)
