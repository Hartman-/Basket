#!/usr/bin/env python

'''
POST RENDER SCRIPT TO KICK OUT ARCHIVAL MOV OF LAST COMP RENDER
nuke -t imageconvertwithargs.py myimage.####.tif myimage.####.jpg
nuke -t imageconvertwithargs.py xyz 010 cg Ravine
'''

import time
from glob import glob
import os
import re
import sys

inputPath = sys.argv[1]
# inputPath = '//awexpress.westphal.drexel.edu/digm_anfx/SRPJ_LAW/renderman/HeroShipTurntable_v003_imh29_0/images/frame_v001/frame_v001.0001.exr'.replace('//', '\\\\').replace('/', '\\')
# inputPath = 'C:/Users/imh29/Desktop/HoudiniProjects/LAW/render/Flipbook/161012/rocketTest_v007.1.jpg'.replace('//', '\\\\').replace('/', '\\')
# inputPath = '\\\\awexpress.westphal.drexel.edu\\digm_anfx\\SRPJ_LAW\\frames\\lpo\\010\\cg\\frame.0001.exr'
dirPath = os.path.dirname(inputPath)
dirName = re.split(r'\.(\d+)\.', os.path.basename(inputPath))

def getSequence():
    files = sorted(glob(os.path.join(dirPath, '*.*.*')), key=os.path.getmtime)
    return files

seqFiles = getSequence()

# GRAB THE RIGHT MOST DIGIT IN THE FIRST FRAME'S FILE NAME
firstString = re.findall( r'\d+', seqFiles[0] )[-1]
print seqFiles
print 'first: %s' % seqFiles[0]
# GET THE PADDING FROM THE AMOUNT OF DIGITS
padding = len( firstString )
# CREATE PADDING STRING FRO SEQUENCE NOTATION
paddingString = '%02s' % padding
# CONVERT TO INTEGER
firstFrame = int( firstString )
# GET LAST FRAME
lastFrame = int( re.findall(r'\d+', seqFiles[-1] )[-1] )
# GET EXTENSION
# ext = os.path.splitext( seqFiles[0] )[-1]
ext = dirName[2]
fileName = '%s.%s.%s' % (dirName[0], ('#'*padding), ext)
filePath = os.path.join(dirPath, fileName).replace('\\', '/')

date = time.strftime("%y%m%d")
writeName = '%s_%s.%s' % (date, dirName[0], 'mov')
writePath = os.path.join(dirPath, writeName).replace('\\', '/')

# DEBUGGING
print 'First Frame: %s' % firstFrame
print 'Last Frame: %s' % lastFrame

# print 'Read: %s' % filePath
# print 'Write: %s' % writePath


# NUKE Nodes
r = nuke.nodes.Read(file=filePath)
r.knob('first').setValue(int(firstFrame))
r.knob('last').setValue(int(lastFrame))
w = nuke.nodes.Write(file=writePath)

# Gotta make sure the quality is gud
w.knob('file_type').setValue('mov')
w.knob('mov64_fps').setValue(30)
w.knob('meta_codec').setValue('jpeg')
w.knob('mov64_units').setValue('Frames')
w.knob('mov64_write_timecode').setValue(True)
w.knob('mov64_bitrate').setValue(115000)
w.knob('mov64_bitrate_tolerance').setValue(40000)

# Nuke with the reverse logic? ... Lower = Better
w.knob('mov64_quality_min').setValue(2)
w.knob('mov64_quality_max').setValue(4)

w.setInput(0, r)
nuke.execute("Write1", firstFrame, lastFrame)

