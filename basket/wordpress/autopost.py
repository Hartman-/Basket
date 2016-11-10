import sys

from PySide.QtCore import *
from PySide.QtGui import *

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo


# Setup Basic Dialog window for user
class QDialog_Wordpress(QDialog):
    def __init__(self, parent=None):
        super(QDialog_Wordpress, self).__init__(parent)

        # Initialize the User
        self.wp = Client('http://lobstersare.online/xmlrpc.php', 'WordpressBob', 'B04OidJ)T&^WcnLz5FM0O70W')

        post_content = '<iframe src="https://www.youtube.com/embed/DleMS0c7Ka8?&amp;autoplay=1&amp;loop=1&amp;playlist=DleMS0c7Ka8" width="853" height="480" frameborder="0" allowfullscreen="allowfullscreen"></iframe>'
        # Initialize new post
        self.newpost = WordPressPost()
        self.newpost.title = 'Title'

        self.newpost.content = post_content

        self.newpost.terms_names = {
            'post_tag': ['test'],
            'category': ['Tests']
        }

        self.setupUI()

    def makePost(self):
        self.wp.call(NewPost(self.newpost))

    def convertYoutubeLink(self):
        youtubeURL = self.in_youtube.text()
        print youtubeURL
        youtubeSplit = youtubeURL.split('/')
        print youtubeSplit
        youtubeID = youtubeSplit[len(youtubeSplit) - 1]

        loopString = '?&amp;autoplay=1&amp;loop=1&amp;playlist=%s' % youtubeID
        url = '%s%s' % (youtubeURL, loopString)
        iframe = '<iframe src="%s" width="853" height="480" frameborder="0" allowfullscreen="allowfullscreen"></iframe>' % url
        print iframe

        self.in_youtube.clear()

    def setupUI(self):
        windowLayout = QVBoxLayout()

        btn = QPushButton("Fuck with Ducks")
        btn.pressed.connect(self.makePost)

        youtubeLabel = QLabel("Youtube URL")
        self.in_youtube = QLineEdit()
        btn_youtube = QPushButton("Add")
        btn_youtube.pressed.connect(self.convertYoutubeLink)

        windowLayout.addWidget(btn)
        windowLayout.addWidget(youtubeLabel)
        windowLayout.addWidget(self.in_youtube)
        windowLayout.addWidget(btn_youtube)

        self.setLayout(windowLayout)



type = 'ppj'
if (type == 'ppj'):
    # Make it a ppj tag
    print 'suck dick'

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = QDialog_Wordpress()
    form.setWindowTitle('Project Transfer')
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
