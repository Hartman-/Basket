import sys

from PySide.QtCore import *
from PySide.QtGui import *


# Setup Basic Dialog window for user
class QDialog_youtube(QDialog):
    def __init__(self, parent=None):
        super(QDialog_youtube, self).__init__(parent)

        self.setupUI()

    def convertYoutubeLink(self):
        youtubeURL = self.in_youtube.text()
        print youtubeURL
        youtubeSplit = youtubeURL.split('=')
        print youtubeSplit
        youtubeID = youtubeSplit[len(youtubeSplit) - 1]
        basestr = 'https://www.youtube.com/embed/'
        loopString = '?&amp;autoplay=1&amp;loop=1&amp;playlist=%s' % youtubeID
        url = '%s%s%s' % (basestr, youtubeID, loopString)
        iframe = '<iframe src="%s" width="853" height="480" frameborder="0" allowfullscreen="allowfullscreen"></iframe>' % url
        print iframe

        self.text_LoopEmbed.setText(iframe)
        self.in_youtube.clear()

    def exportDescription(self):
        base_desc = "Lobsters Are Weird is a six-person animation team from Drexel University. We're currently working on a short film about space travel. Please subscribe to our channel for the latest developments towards our project.\n We're always looking for feedback! If you have any thoughts, ideas, or ways that we can improve, please leave your feedback in a comment."
        desc = self.in_desc.text()
        full_desc = '%s%s%s' % (desc, '\n', base_desc)

        self.text_desc.setText(full_desc)
        self.in_desc.clear()

    def setupUI(self):
        windowLayout = QVBoxLayout()

        youtubeLabel = QLabel("Youtube URL")
        self.in_youtube = QLineEdit()
        btn_youtube = QPushButton("Add")
        btn_youtube.pressed.connect(self.convertYoutubeLink)
        self.text_LoopEmbed = QTextEdit()

        label_desc = QLabel("Youtube Description")
        self.in_desc = QLineEdit()
        btn_desc = QPushButton("Create")
        btn_desc.pressed.connect(self.exportDescription)
        self.text_desc = QTextEdit()

        windowLayout.addWidget(youtubeLabel)
        windowLayout.addWidget(self.in_youtube)
        windowLayout.addWidget(btn_youtube)
        windowLayout.addWidget(self.text_LoopEmbed)

        windowLayout.addWidget(label_desc)
        windowLayout.addWidget(self.in_desc)
        windowLayout.addWidget(btn_desc)
        windowLayout.addWidget(self.text_desc)

        self.setLayout(windowLayout)

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = QDialog_youtube()
    form.setWindowTitle('Youtube Generator')
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())



