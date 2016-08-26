#!/usr/bin/env python

# IMPORT python base modules
import argparse
import glob
import re
import shutil
import subprocess
import sys
import os

# IMPORT custom modules
import BasketGlobals as config


class Launcher:
    def __init__(self):
        localize = LocalizeProject()
        localize.buildlocal()

    def launchnuke(self, filepath):
        # Set the path to a default of Windows
        path = 'C:\\Program Files\\Nuke9.0v8\\Nuke9.0.exe'
        if config.curOS().lower() is not 'windows':
            path = 'MacOSPath'
        p = Popen([path, '--nukex', filepath], stdout=PIPE)

    def launchmaya(self, filepath):
        pass

    def launch(self, appPath, filePath):
        p = subprocess.Popen([appPath, '--nukex', filePath], creationflags=subprocess.CREATE_NEW_CONSOLE)

    def applicationpath(self, stage):
        paths = {
            0: '',
            1: '',
            2: '',
            3: '',
            4: '',
            5: '',
            6: '',
            7: 'C:\\Program Files\\Nuke9.0v8\\Nuke9.0.exe',
            8: ''
        }
        return paths[stage]

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
            newest = max(glob.iglob(os.path.join(config.stageDir(stage), filetypes[stage])),key=os.path.getctime)
        return newest

class LocalizeProject:
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


''' BEGIN FUNCTION
	Run the command line program, parse incoming arguments '''
def initialize():
    config.setupSession()
    hehe = Launcher()

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
    # parser.add_argument("-a", "--app",
    # 	required=True,
    # 	help="Define the application to launch into",
    # 	type=str,
    # 	choices=["NUKE", "MAYA"])

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

    hehe.launch(hehe.applicationpath(args.stage), hehe.latestfile(args.stage, args.tag))


    # Runs if the file is run directly... NOT imported
if __name__ == "__main__":
    initialize()

# NOTES

'''
- Use 'choices' option on the parser.add_argument to limit the user to the currently established seq/shots in the server directory
'''
