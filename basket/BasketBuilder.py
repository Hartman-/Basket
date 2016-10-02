#!/usr/bin/env python

import argparse
import os

import BasketGlobals as config


# SET THE BASE LOCATION
SERVER = os.path.join(config.serverDir(), os.getenv('SHOW'))
LOCAL = os.path.join(config.rootDir(), os.getenv('SHOW'))


# Basic 'Safe' Server Directory make
def make_dir(indir, loc=SERVER):
    baseDir = os.path.join(loc, indir)
    try:
        if not os.path.isdir(baseDir):
            os.makedirs(baseDir)
    except IOError as e:
        print e
        pass


# Return subdirectories
def sub_dirs(indir):
    return config.BASE_DIRS[indir]


# Iterate through sub dirs in the given top dir
def make_sub(top, loc=SERVER):
    # If the sub directory isn't empty
    if sub_dirs(top) is not []:
        for sub in sub_dirs(top):
            subdir = os.path.join(top, sub)
            make_dir(subdir, loc=loc)


# Iterate through and make the top level directories
# Then create the sub directories
def make_top(top, loc=SERVER):
    for key, dirname in top.iteritems():
        make_dir(key, loc=loc)
        make_sub(key, loc=loc)


# --- SHOT SPECIFIC DIRECTORY CREATION ---

# Make a Working/Publish Shot directory
def make_prod_dir(scene, shot, loc=SERVER):
    for prod_dir in config.PROD_DIRS:
        pdir = os.path.join(prod_dir, scene, shot)
        for stage in config.STAGE_DIRS:
            sdir = os.path.join(pdir, stage)
            make_dir(sdir, loc=loc)


# Make a Frame Shot directory
def make_frame_dir(scene, shot, loc=SERVER):
    fdir = os.path.join('frames', scene, shot)
    for sub in config.FRAME_DIRS:
        sdir = os.path.join(fdir, sub)
        make_dir(sdir, loc=loc)


# One stop Function to initialize the server directories
def build_base_server():
    make_dir(SERVER)
    make_top(config.BASE_DIRS)


# Creates Base local directories
def build_base_local():
    make_dir(LOCAL)
    make_top(config.BASE_DIRS, loc=LOCAL)


if __name__ == "__main__":
    #build_base_server()
    build_base_local()
    # parser = argparse.ArgumentParser(
    #     prog="BasketBuilder",
    #     description="BUILD ALL THE DIRECTORIES!"
    # )
    #
    #
    # parser.add_argument("-sc",
    #                     help="Scene",
    #                     type=str)
    # parser.add_argument("-sh",
    #                     help="Shot",
    #                     type=str)