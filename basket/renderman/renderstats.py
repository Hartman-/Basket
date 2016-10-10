#!/usr/bin/env python

import datetime
import os
from glob import glob
import xml.etree.cElementTree as xml

directory = '\\\\awexpress.westphal.drexel.edu\\digm_anfx\\SRPJ_LAW\\renderman\\HeroShipTurntable_v003_imh29_0\\rib'
dirlist = []


def includesXML(ribdir):
    for fname in os.listdir(ribdir):
        if fname.endswith('.xml'):
            return True
    else:
        return False


def folderList():
    riblist = sorted(glob(os.path.join(directory, '*')), key=os.path.getmtime)
    for index, ribfolder in enumerate(riblist):
        if not includesXML(ribfolder):
            riblist.pop(index)
    riblist.pop(len(riblist)-1)
    return riblist


def getRenderTime(ribdir):
    for fname in os.listdir(ribdir):
        if fname.endswith('.xml'):
            xmltree = xml.parse(os.path.join(ribdir,fname))
            root = xmltree.getroot()
            # Get to the timers in the xml file
            pureseconds = root[1][1][0][1][0][0].text
            # m, s = divmod(float(pureseconds), 60)
            # h, m = divmod(m, 60)
            # trunctime = "%d:%02d:%02d" % (h, m, s)
            # formattime = str(datetime.timedelta(seconds=float(pureseconds)))
            return pureseconds


def getAllTimes():
    alltimes = []
    for index, fname in enumerate(folderList()):
        alltimes.append(getRenderTime(fname))
    return alltimes


def getAverageTime(times):
    total = 0.0
    for time in times:
        print time
        total += float(time)
    print total
    print str(datetime.timedelta(seconds=total))

if __name__ == '__main__':
    # print folderList()[0]
    # getRenderTime(folderList()[0])
    getAverageTime(getAllTimes())