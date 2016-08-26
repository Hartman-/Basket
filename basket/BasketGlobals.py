#!/usr/bin/env python

import os
import platform
from glob import glob

# Configure Necessary Global Variables for Basket

def setupSession():
    # DEFINE EXAMPLE ENVIRONMENT
    os.environ['SHOW'] = 'PROJ_local'
    os.environ['SEQ'] = 'xyz'
    os.environ['SHOT'] = '010'


def curOS():
    currentOS = platform.system()
    return currentOS


def rootDir():
    return os.path.expanduser('~') + '\\Desktop\\LAW\\'


def serverDir():
    return os.path.expanduser('~') + '\\Desktop\\LAW_server'


def getNukeScripts():
    nkFiles = glob(os.path.join(nukeDir(), '*.nk'))
    return nkFiles


def nukeDir():
    curDir = os.path.join(serverDir(), os.getenv('SHOW'), 'Working', os.getenv('SEQ'), os.getenv('SHOT'), '07. Comp')
    if not os.path.isdir(curDir):
        raise ValueError, 'NUKE Directory does not exist'
    return curDir


def stageDir(stage):
    stages = ['01. PreVis', '02. Layout', '03. Anim', '04. FX', '05. Lighting', '06. Render', '07. Comp', '08. Edit']
    baseDir = os.path.join(serverDir(), os.getenv('SHOW'), 'Working', os.getenv('SEQ'), os.getenv('SHOT'))
    # Thanks for starting at Zero lists!
    curDir = os.path.join(baseDir, stages[stage - 1])
    if not os.path.isdir(curDir):
        raise ValueError, 'File Directory does not exist'
    return curDir


def seqDir():
    curDir = os.path.join(serverDir(), os.getenv('SHOW'), 'Frames', os.getenv('SEQ'), os.getenv('SHOT'), 'src')
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
    print 'hello'