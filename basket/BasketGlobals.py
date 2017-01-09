#!/usr/bin/env python

import os
import platform
from glob import glob

import utils.appconfig as appconfig


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

STAGE_DIRS = appconfig.get_config_value('law', 'stages')

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
    curDir = '%s' % appconfig.get_config_value('project', 'projdir')
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
        raise ValueError, '%s NUKE Directory does not exist' % curDir
    return curDir


def serverStageDir(stage):
    curDir = os.path.join(serverDir(), 'working', 'scenes', os.getenv('SEQ'), os.getenv('SHOT'), STAGE_DIRS[stage])
    if not os.path.isdir(curDir):
        raise ValueError, 'Stage Directory does not exist'
    return curDir


def localFramesDir():
    curDir = os.path.join(rootDir(), 'frames', os.getenv('SEQ'), os.getenv('SHOT'), 'plates')
    if not os.path.isdir(curDir):
        raise ValueError, 'Frames Directory does not exist'
    return curDir


def stageDir(stage):
    baseDir = os.path.join(serverDir(), 'working', 'scenes', os.getenv('SEQ'), os.getenv('SHOT'))
    # Thanks for starting at Zero lists!
    curDir = os.path.join(baseDir, STAGE_DIRS[stage])

    if not os.path.isdir(curDir):
        raise ValueError, 'File Directory does not exist: ' + curDir
    return curDir


def publishDir(stage):
    baseDir = os.path.join(serverDir(), 'publish', os.getenv('SEQ'), os.getenv('SHOT'))
    # Thanks for starting at Zero lists!
    curDir = os.path.join(baseDir, STAGE_DIRS[stage])
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
        raise ValueError, 'Library Directory does not exist'
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
    os.environ['LAWSTAGE'] = str(stage)


def stageNum():
    return int(os.getenv('LAWSTAGE'))


def applicationPath(ext):
    if type(ext) is not int:
        paths = {
            '.ma': appconfig.get_config_value('app', 'mayaexe'),
            '.mb': appconfig.get_config_value('app', 'mayaexe'),
            '.nk': appconfig.get_config_value('app', 'nukeexe'),
            '.hip': appconfig.get_config_value('app', 'houdiniexe'),
            '.hipnc': appconfig.get_config_value('app', 'houdiniexe'),
            '.hiplc': appconfig.get_config_value('app', 'houdiniexe')
        }
        return paths[ext]
    else:
        paths = {
            0: appconfig.get_config_value('app', 'mayaexe'),
            1: appconfig.get_config_value('app', 'mayaexe'),
            2: appconfig.get_config_value('app', 'mayaexe'),
            3: appconfig.get_config_value('app', 'houdiniexe'),
            4: appconfig.get_config_value('app', 'mayaexe'),
            5: appconfig.get_config_value('app', 'mayaexe'),
            6: appconfig.get_config_value('app', 'nukeexe'),
            7: appconfig.get_config_value('app', 'premiereexe')
        }
        return paths[ext]


if __name__ == '__main__':
    print serverDir()
