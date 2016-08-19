# !/usr/bin/env python

import os
from glob import glob


# Configure Necessary Global Variables for Basket


__project_name__ = 'Basket Project'
__project_acr__ = 'BSKP'
__project_dir__ = 'Z:\\Users\\Ian\\Desktop\\PROJ_server'
__local_dir__ = 'Z:\\Users\\Ian\\Desktop\\PROJ_local'
__shot_num__ = '010'
__shot_str__ = 'Shot 010'
__shot_version__ = 1
__cur_user__ = 'imh29'


def setupSession():
    # DEFINE EXAMPLE ENVIRONMENT
    os.environ['SHOW'] = 'PROJ_local'
    os.environ['SEQ'] = 'xyz'
    os.environ['SHOT'] = '010'


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