#!/usr/bin/env python

# IMPORT python base modules
import argparse
import glob
import subprocess
import sys
import os

from PySide.QtCore import *
from PySide.QtGui import *

# IMPORT custom modules
import BasketGlobals as config
import BasketBuilder
import gui.GUI_Launch as LauncherGUI


class Launcher:
    def __init__(self):
        localize = LocalizeProject()
        localize.buildlocal()

    def launch(self, appPath, filePath):
        if appPath is config.applicationPath('.nk'):
            subprocess.Popen([appPath, '--nukex', filePath], creationflags=subprocess.CREATE_NEW_CONSOLE)
            return
        if appPath is config.applicationPath('.ma'):
            subprocess.Popen([appPath, '-file', filePath, '-script', 'X:\\Classof2017\\LobstersAreWeird\\basket\\maya\\mayaLaunchCall.mel'])
            return
        else:
            subprocess.Popen([appPath, filePath])
            return

    def createNewFile(self, appPath):
        # NUKE is a Special Snowflake
        if appPath is config.applicationPath('.nk'):
            subprocess.Popen([appPath, '--nukex'], creationflags=subprocess.CREATE_NEW_CONSOLE)
            return
        # Maya Needs its special little MEL file
        if appPath is config.applicationPath('.ma'):
            subprocess.Popen([appPath, '-script', 'X:\\Classof2017\\LobstersAreWeird\\basket\\maya\\mayaLaunchCall.mel'])
            return
        # Houdini and Premiere are Chill AF
        else:
            subprocess.Popen(appPath)
            return

    # Get the latest nuke file
    def latestfile(self, stage, tag):
        filetypes = ['', '*.ma', '*.ma', '*.ma', '*.hip', '*.ma', '*.ma', '*.nk', '*.pproj']
        newest = ''

        # If the user passes a tag filter
        # sadly glob doesn't seem to have a way to filter
        if tag is not None:
            matchedfiles = []

            # Build list of files that match the tag substring
            for file in os.listdir(config.stageDir(stage)):
                if os.path.basename(file).find(tag) > -1:
                    matchedfiles.append(file)
            newest = ''

            # Filter the matched list to get the newest file
            for f in matchedfiles:
                lasttime = os.path.getctime(os.path.join(config.stageDir(stage), newest))
                newtime = os.path.getctime(os.path.join(config.stageDir(stage), f))
                if newtime >= lasttime:
                    newest = f

            # rebuild the files path before returning to the launcher
            newest = os.path.join(config.stageDir(stage), newest)
            # if the tag exists in the file name, it returns a number
            # if it doesnt' exist, returns -1
        else:
            newest = max(glob.iglob(os.path.join(config.stageDir(stage), filetypes[stage])), key=os.path.getctime)
        return newest

    @Slot(int, str)
    def goLaunch(self, stage, tag):
        self.launch(config.applicationPath(stage), self.latestfile(stage, tag))

    @Slot(int)
    def goNewFile(self, stage):
        self.createNewFile(
            config.applicationPath(stage)
        )

    @Slot(str)
    def goAsset(self, path):
        config.setSeq('assets')
        psuedoShot = os.path.dirname(path.strip(str(os.path.join(config.serverDir(), 'working', 'assets'))))
        config.setShot(psuedoShot)
        filename, file_extension = os.path.splitext(path)
        self.launch(config.applicationPath(file_extension), path)

    @Slot(str)
    def goNewAsset(self, name):
        config.setSeq('assets')
        config.setShot(str(name))

        BasketBuilder.make_dir(os.path.join('working', os.getenv('SEQ'), os.getenv('SHOT')))
        self.createNewFile(config.applicationPath('.ma'))

    @Slot(int, str, str)
    def renderScene(self, stage, tag, cam):
        cmd = '"C:\\Program Files\\Autodesk\\Maya2016.5\\bin\\render.exe" -r rman'
        project = ' -proj "\\\\awexpress.westphal.drexel.edu\digm_anfx\SRPJ_LAW"'
        shadingRate = ' -setAttr ShadingRate 16'

        if cam != '':
            camera = ' -cam %s' % cam
        else:
            camera = ''

        file = ' "%s"' % self.latestfile(stage, tag)

        render_cmd = '%s%s%s%s%s' % (cmd, project, shadingRate, camera, file)
        print render_cmd
        # subprocess.Popen(render_cmd)
        # return

class LocalizeProject:
    def __init__(self):
        print 'Setting up Local Project Structure'

    def buildlocal(self):
        BasketBuilder.build_base_local()
        # Copy the remaining (working, publish, frames) folders down
        BasketBuilder.rep_prod_dir()

''' BEGIN FUNCTION
	Run the command line program, parse incoming arguments '''

# Catch the initial input
# User can choose to enter commandline mode if they want
def catch():
    initParse = argparse.ArgumentParser()
    initParse.add_argument("-c", "--cmd",
                           help="Enter CommandLine Mode",
                           action="store_true")
    args = initParse.parse_args()

    if args.cmd is True:
        initialize()
    else:
        goUI()


def initialize():
    basketLaunch = Launcher()

    # Initialize the command line argument parser
    parser = argparse.ArgumentParser(
        prog="BasketLauncher",
        description="Application launcher to keep Ian's head on straight through Senior Project")

    # Add Arguments to the parser
    parser.add_argument("--show",
                        help="Define the show",
                        type=str)
    parser.add_argument("-s", "--seq",
                        required=True,
                        help="Define the sequence",
                        type=str)
    parser.add_argument("-sh", "--shot",
                        required=True,
                        help="Define the shot",
                        type=str)
    parser.add_argument("-st", "--stage",
                        required=True,
                        help="Define the step of the process",
                        type=int)
    parser.add_argument("-t", "--tag",
                        help="Define a specific tag to open the most recent file",
                        type=str)

    # store_true means to receive no arguments, provide callback of TRUE when flag is used
    parser.add_argument("-r", "--render",
                        help="# # # NO ACTION # # #",
                        action="store_true")

    # Parse the arguments passed into the command line
    args = parser.parse_args()

    # print the value of a parsed arg
    # print("sequence: %s | shot: %s" % (args.seq, args.shot))
    config.setSeq(args.seq)
    config.setShot(args.shot)

    basketLaunch.launch(
        config.applicationPath(args.stage),
        basketLaunch.latestfile(args.stage, args.tag)
    )


def goUI():
    appLaunch = Launcher()

    app = QApplication(sys.argv)
    gui = LauncherGUI.Launcher()
    gui.setWindowTitle('LAWncher')

    emitter = gui.centralWidget()

    emitter.launch.connect(appLaunch.goLaunch)
    emitter.createnew.connect(appLaunch.goNewFile)
    emitter.openasset.connect(appLaunch.goAsset)
    emitter.newasset.connect(appLaunch.goNewAsset)
    # emitter.renderscene.connect(appLaunch.renderScene)

    os.environ['RMS_SCRIPT_PATHS'] = "%RMS_SCRIPT_PATHS%;X:/Classof2017/LobstersAreWeird/basket/renderman"

    sys.exit(app.exec_())


# Runs if the file is run directly... NOT imported
if __name__ == "__main__":
    catch()
