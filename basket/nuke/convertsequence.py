#!/usr/bin/env python

'''
POST RENDER SCRIPT TO KICK OUT ARCHIVAL MOV OF LAST COMP RENDER
nuke -t imageconvertwithargs.py myimage.####.tif myimage.####.jpg
nuke -t imageconvertwithargs.py xyz 010 cg Ravine
'''

from glob import glob
import os
import re
import sys

# import BasketGlobals as config
#
# # Set Seq / Shot
# os.environ['SEQ'] = str(sys.argv[1])
# os.environ['SHOT'] = str(sys.argv[2])
#
# dirPath = os.path.join(config.framesDir(), str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]))

inputPath = sys.argv[1].replace('//', '\\\\').replace('/', '\\')
# inputPath = '//awexpress.westphal.drexel.edu/digm_anfx/SRPJ_LAW/ALAW/renderman/HeroShipTurntable_v002_imh29_0/images/Turntable1_cam_010Shape/Turntable1_cam_010Shape.0001.exr'.replace('//', '\\\\').replace('/', '\\')
dirPath = os.path.dirname(inputPath)

def getSequence():
    files = sorted(glob(os.path.join(dirPath, '*.*.*')), key=os.path.getmtime)
    return files

seqFiles = getSequence()
print seqFiles[0]

dirName = os.path.basename(dirPath)

# GRAB THE RIGHT MOST DIGIT IN THE FIRST FRAME'S FILE NAME
firstString = re.findall( r'\d+', seqFiles[0] )[-1]
# GET THE PADDING FROM THE AMOUNT OF DIGITS
padding = len( firstString )
# CREATE PADDING STRING FRO SEQUENCE NOTATION
paddingString = '%02s' % padding
# CONVERT TO INTEGER
firstFrame = int( firstString )
# GET LAST FRAME
lastFrame = int( re.findall( r'\d+', seqFiles[-1] )[-1] )
# GET EXTENSION
ext = os.path.splitext( seqFiles[0] )[-1]

fileName = '%s.%s%s' % (dirName, ('#'*padding), ext)
filePath = os.path.join(dirPath, fileName).replace('\\', '/')

writeName = '%s.%s' % (dirName, 'mov')
writePath = os.path.join(dirPath, writeName).replace('\\', '/')

# print 'First Frame: %s' % firstFrame
# print 'Last Frame: %s' % lastFrame
#
# print 'Read: %s' % filePath
# print 'Write: %s' % writePath


# # NUKE Nodes
r = nuke.nodes.Read(file=filePath)
r.knob('first').setValue(int(firstFrame))
r.knob('last').setValue(int(lastFrame))
w = nuke.nodes.Write(file=writePath)
w.setInput(0, r)
nuke.execute("Write1", firstFrame, lastFrame)

