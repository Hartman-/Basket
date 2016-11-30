#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import os
import sys

import qb

from PySide.QtCore import *
from PySide.QtGui import *

#
# GUI CLASSES
#


class FileDrop(QListWidget):

    fileDropped = Signal(list)

    def __init__(self, type, parent=None):
        super(FileDrop, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setIconSize(QSize(72, 72))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.fileDropped.emit(links)
        else:
            event.ignore()


class SubLayout(QWidget):
    def __init__(self, parent=None):
        super(SubLayout, self).__init__(parent)

        self.label = QLabel('Hello World')

        self.view = FileDrop(self)
        self.view.fileDropped.connect(self.pictureDropped)

        layout = QHBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def pictureDropped(self, l):
        for url in l:
            if os.path.exists(url):
                print(url)
                self.frameRange(url)
                icon = QIcon(url)
                pixmap = icon.pixmap(72, 72)
                icon = QIcon(pixmap)
                item = QListWidgetItem(url, self.view)
                item.setIcon(icon)
                item.setStatusTip(url)

    def frameRange(self, filepath):
        # fp = open(filepath)
        # while True:
        #     line = fp.next()
        #     if line.startswith("select -ne :defaultRenderGlobals;"):
        #         break
        # while line.find('".fs"') == -1:
        #     line = fp.next()
        # start = int(line.split(" ")[2].split(";")[0])
        # while line.find('".ef"') == -1:
        #     line = fp.next()
        # end = int(line.split(" ")[2].split(";")[0])
        # frames = end - start + 1
        # print 'frames: %s-%s (%s)' % (start, end, frames)

        numcams = 0
        with open(filepath) as fileobj:
            for line in fileobj:
                if line.startswith("createNode camera -n"):
                    numcams += 1
        print numcams

        fp = open(filepath)

        index = 0
        while index < numcams:
            line = fp.next()
            if line.startswith("createNode camera -n"):
                while len(line.rstrip().expandtabs(4)) - len(line.rstrip().lstrip()) != 4:
                    line = fp.next()
                    # if line.startswith('setAttr ".rnd" no;"'):
                    #     break
                    # else:
                    #     print(line)
                    #     break
                    print(line)
                index += 1




        # Base Line Length
        # print(line.rstrip().expandtabs(4))
        # print(line.rstrip().lstrip())
        # print(len(line.rstrip().expandtabs(4)) - len(line.rstrip().lstrip()))
        # fp.close()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mainlayout = SubLayout()
        self.initUI()

    def initUI(self):

        self.setCentralWidget(self.mainlayout)
        self.show()


#
# MAIN RUN FUNCTIONS
#

def main():
    # Create the Qt Application
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.setWindowTitle('Qube Submit')

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
