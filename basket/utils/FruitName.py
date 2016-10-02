#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import sys, os, time
import subprocess
import shutil
from PySide.QtCore import *
from PySide.QtGui import *

import BasketGlobals as config

from gui import Launcher_ui
from gui import FileSelector


class FruitName:
    def __init__(self):
        localize = LocalProject()
        localize.buildlocal()

    @Slot(str)
    def launchnuke(self, filepath):
        path = self.buildpath('\\Program Files\\Nuke9.0v8\\Nuke9.0.exe')
        subprocess.Popen([path, '--nukex', filepath])

    def launchmaya(self):
        path = self.buildpath('\\Program Files\\Autodesk\\Maya2016\\bin\\maya.exe')
        subprocess.Popen(path)

    def buildpath(self, exe):
        basedrive = os.path.abspath(os.sep)

        if basedrive[2:] == "\\":
            basedrive = basedrive[:2]

        exepath = basedrive + exe
        return exepath


class LocalProject:
    def __init__(self):
        self.structure = {
            'source': ['plates', 'reference'],
            'library': ['models', 'templates', 'sound', 'texture'],
            'delivery': ['dailies'],
            'docs': []
        }

    def firstlevel(self):
        folders = []
        for key, value in self.structure.iteritems():
            folders.append(key)
        return folders

    def subdirs(self, dir):
        return self.structure[dir]

    def buildlocal(self):
        for root_index, root_dir in enumerate (self.firstlevel()):
            r_directory = os.path.join(config.rootDir(), os.getenv('SHOW'), root_dir)
            if not os.path.exists(r_directory):
                os.makedirs(r_directory)

            # Create any subdirectories
            for sub_index, sub_dir in enumerate (self.subdirs(root_dir)):
                # Only execute if there is anything
                s_directory = os.path.join(config.rootDir(), os.getenv('SHOW'), root_dir, sub_dir)
                if not os.path.exists(s_directory):
                    os.makedirs(s_directory)

        # Copy the remaining (working, publish, frames) folders down
        self.replicateserver()

    ''' Constructor that returns all files in the current directory
        These files are then ignored in the shutil.copytree '''
    def ignore_files(self, dir, files):
        return [f for f in files if os.path.isfile(os.path.join(dir, f))]

    def replicateserver(self):
        server_root = os.path.join(config.serverDir(), os.getenv('SHOW'))
        local_root = os.path.join(config.rootDir(), os.getenv('SHOW'))

        # Replicate the WORKING folder structure
        if not os.path.exists(os.path.join(local_root, 'working')):
            shutil.copytree(
                os.path.join(server_root, 'working'),
                os.path.join(local_root, 'working'),
                ignore=self.ignore_files)

        # Replicate the PUBLISH folder structure
        if not os.path.exists(os.path.join(local_root, 'publish')):
            shutil.copytree(
                os.path.join(server_root, 'publish'),
                os.path.join(local_root, 'publish'),
                ignore=self.ignore_files)

        # Replicate the FRAMES folder structure
        if not os.path.exists(os.path.join(local_root, 'frames')):
            shutil.copytree(
                os.path.join(server_root, 'frames'),
                os.path.join(local_root, 'frames'),
                ignore=self.ignore_files)


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    config.setupSession()

    gui = Launcher_ui.Launcher()
    gui.setWindowTitle('LAW Launcher')
    gui.show()

    nukeFile_gui = FileSelector.Form()
    nukeFile_gui.setWindowTitle('NUKE Shot Launcher')

    program = FruitName()

    gui.nukepressed.connect(nukeFile_gui.show)
    gui.mayapressed.connect(program.launchmaya)
    nukeFile_gui.launch.connect(program.launchnuke)

    sys.exit(app.exec_())
