#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import os

class FolderBuilder:
    def __init__(self):
        self.newdir = 'C:\\Users\\Ian\\Desktop\\PROJ-proj\\'

        self.publish_dir = 'C:\\Users\\Ian\\Desktop\\PROJ-proj\\Publish\\'
        self.working_dir = 'C:\\Users\\Ian\\Desktop\\PROJ-proj\\Working\\'

        self.alldirs = [self.publish_dir, self.working_dir]

        self.scene = ''
        self.shot = ''

    def builddir(self, base_dir):
        newdir = base_dir + self.scene + '\\' + self.shot
        self.newdir = newdir

    def createdir(self, sc, sh):
        self.scene = sc
        self.shot = sh

        for d in self.alldirs:
            self.builddir(d)
            if not os.path.exists(self.newdir):
                os.makedirs(self.newdir)
