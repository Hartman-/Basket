# ===

# === Burn-In Builder
# === By: Ian Hartman 

# ===

# Import Modules 
import nuke
import os


def normframerange(inbegin, inend):
    # We always want the counter to start at 1
    startframe = 1
    # Need to compensate for the end of the frame range, add 1
    endframe = (inend - inbegin) + 1

    return [startframe, endframe]

def curnormframe(inbegin):
    return (nuke.frame() - inbegin + 1)


# Setup Node Classes
class RectNode:
    def __init__(self, Name, Area, Color, Opacity, Ramp, Input):
        self.Name = Name
        self.Area = Area
        self.Color = Color
        self.Opacity = Opacity
        self.Ramp = Ramp
        self.Input = Input

        self.rectNode = nuke.createNode('Rectangle', inpanel=False)
        self.rectNode['name'].setValue(self.Name)

        self.rectNode['area'].setExpression(str(self.Area[0]), 0)
        self.rectNode['area'].setExpression(str(self.Area[1]), 1)
        self.rectNode['area'].setExpression(str(self.Area[2]), 2)
        self.rectNode['area'].setExpression(str(self.Area[3]), 3)

        self.rectNode['color'].setValue(self.Color)
        self.rectNode['opacity'].setValue(self.Opacity)

        if (self.Ramp == True):
            self.rectNode['ramp'].setValue('linear')
            self.rectNode['color'].setValue(0)
            self.rectNode['color0'].setValue(1)
            self.rectNode['p1'].setValue([0, 50])
            self.rectNode['p0'].setValue([500, 50])

        self.rectNode.setInput(0, self.Input)


class TextNode:
    def __init__(self, Name, Message, Alt, Size, Box, Resize, xJustify, Input):
        self.Name = Name
        self.Message = Message
        self.Size = Size
        self.Box = Box
        self.Resize = Resize
        self.xJustify = xJustify
        self.Input = Input

        textString = str(Name) + '_text'

        k_String = nuke.EvalString_Knob(textString, str(Name) + '_text')

        self.textNode = nuke.createNode('Text', inpanel=False)
        self.textNode['name'].setValue(self.Name)
        self.textNode['size'].setValue(self.Size)

        self.textNode['box'].setExpression(str(self.Box[0]), 0)
        self.textNode['box'].setExpression(str(self.Box[1]), 1)
        self.textNode['box'].setExpression(str(self.Box[2]), 2)
        self.textNode['box'].setExpression(str(self.Box[3]), 3)

        self.textNode['xjustify'].setValue(self.xJustify)
        self.textNode.setInput(0, self.Input)
        self.textNode.addKnob(k_String)

        self.height = int(nuke.root().height())

        if (Alt == True):
            self.textNode[textString].setValue(self.Message)
            self.textNode['message'].setValue('[python {nuke.thisNode()["' + textString + '"].getValue()}]')
        else:
            self.textNode['message'].setValue(self.Message)

        # Determine Correct Font upon creation
        fontKnob = 'font'
        winDrive = 'C:'
        SSPPath = ''

        SSPMacPath = '/Library/Fonts/SourceSansPro-Regular.otf'
        SSPWinPath = '{}/Windows/Fonts/SourceSansPro-Regular.otf'.format(winDrive)
        if (nuke.env["WIN32"] == True):
            OS = 'Win'
            winDrive = os.environ['SYSTEMDRIVE']
            SSPPath = SSPWinPath
        if (nuke.env["MACOS"] == True):
            OS = 'Mac'
            SSPPath = SSPMacPath

        self.textNode['font'].setValue(SSPPath)

        # Make sure the comments don't push up into the rest of the slate
        if (self.Name == 'SlateComment'):
            self.textNode['yjustify'].setValue('top')

        # if (self.Resize == True):
        #     print self.Box[0]
        #     # [0, 980, (rootWidth/2), 1080]
        #     self.textNode['box'].setExpression(
        #         '[python {nuke.toNode("pRect").knob("area").value()[0] + ' + str(self.Box[0]) + '}]', 0)
        #     self.textNode['box'].setExpression(
        #         '[python {nuke.toNode("pRect").knob("area").value()[1] + ' + str(self.Box[1]) + '}]', 1)
        #     self.textNode['box'].setExpression(
        #         '[python {nuke.toNode("pRect").knob("area").value()[3] - ' + str(self.height - self.Box[3]) + '}]',
        #         3)


def dropBurnIn():
    # Define Variables
    nukeRoot = nuke.root()

    rootWidth = 'root.width'
    rootHeight = 'root.height'

    zeroWidth = 'root.width - root.width'
    zeroHeight = 'root.height - root.height'

    halfWidth = 'root.width / 2'

    proj_Format = nukeRoot.format()
    proj_Comments = nukeRoot['label'].getValue()

    origFrameRange = nuke.FrameRange()
    origFrameRange.setLast(int(nukeRoot['last_frame'].getValue()))
    origFrameRange.setFirst(int(nukeRoot['first_frame'].getValue()))

    # Clear Selection in Node Graph
    nuke.selectAll()
    nuke.invertSelection()

    # Create Group
    # Populate Following script in the group node
    n_burnInGroup = nuke.makeGroup()
    n_burnInGroup['name'].setValue('BurnIn')

    # Create / Format Knobs on BurnIn Group

    k_InputTab = nuke.Tab_Knob('User Information')
    k_CtrlTab = nuke.Tab_Knob('Controls')

    k_Author = nuke.Link_Knob('author', 'author')
    k_Author.setLink('root.BurnIn.AuthorName.AuthorName_text')
    k_ShotName = nuke.Link_Knob('shot', 'shot name')
    k_ShotName.setLink('root.BurnIn.ShotName.ShotName_text')
    k_Notes = nuke.Multiline_Eval_String_Knob('notes', 'notes')

    k_ShowFileName = nuke.Link_Knob('disable_filename', 'disable filename')
    k_ShowFileName.setLink('root.BurnIn.Filename.disable')
    k_ShowShotName = nuke.Link_Knob('disable_shot', 'disable shot name')
    k_ShowShotName.setLink('root.BurnIn.ShotName.disable')
    k_ShowAuthorName = nuke.Link_Knob('disable_author', 'disable authorname')
    k_ShowAuthorName.setLink('root.BurnIn.AuthorName.disable')
    k_ShowFrameCounter = nuke.Link_Knob('disable_frame', 'disable counter')
    k_ShowFrameCounter.setLink('root.BurnIn.FrameCounter.disable')

    refreshCode = """
nuke.toNode("BurnIn").knob("disable").setValue(True)
nuke.toNode("BurnIn").knob("disable").setValue(False)
"""

    k_refreshBurnIn = nuke.PyScript_Knob('refresh', 'refresh', refreshCode)
    k_refreshBurnIn.setFlag(nuke.STARTLINE)

    n_burnInGroup.addKnob(k_InputTab)
    n_burnInGroup.addKnob(k_Author)
    n_burnInGroup.addKnob(k_ShotName)
    n_burnInGroup.addKnob(k_Notes)

    n_burnInGroup.addKnob(k_CtrlTab)
    n_burnInGroup.addKnob(k_ShowFileName)
    n_burnInGroup.addKnob(k_ShowShotName)
    n_burnInGroup.addKnob(k_ShowAuthorName)
    n_burnInGroup.addKnob(k_ShowFrameCounter)
    n_burnInGroup.addKnob(k_refreshBurnIn)

    n_burnInGroup.begin()

    k_CtrlTab = nuke.Tab_Knob('Controls')
    k_CtrlAuthor = nuke.String_Knob('author', 'author')
    k_CtrlAuthor.setValue('Ian Hartman')
    k_CtrlShotName = nuke.String_Knob('shot', 'shot name')
    k_CtrlShotName.setValue('Shot01')

    # Add Timecode
    n_timecode = nuke.createNode('AddTimeCode', inpanel=False)
    n_timecode['metafps'].setValue(False)
    n_timecode['fps'].setExpression("[python {nuke.root()['fps'].getValue()}]")
    n_timecode['useFrame'].setValue(True)
    n_timecode['frame'].setValue(2)

    # Build Rectangle Overlays
    n_topRect = RectNode('TopOverlay',
                         [zeroWidth, 'root.height - 100', rootWidth, rootHeight],
                         0,
                         0.5,
                         False,
                         n_timecode)
    n_botRect = RectNode('BotOverlay',
                         [zeroWidth, zeroHeight, rootWidth, 100], 0, 0.5,
                         False,
                         n_topRect.rectNode)

    # Build Text Nodes
    # python int(nuke.frame())]/[python {int(nuke.toNode("BurnIn").knob("last_frame").getValue())}
    # n_Drexel = TextNode('Drexel',
    #                     'Drexel University',
    #                     False,
    #                     30,
    #                     [25, 'root.height- 100,' rootWidth, 'root.height,
    ''#                     False,
    #                     'left',
    #                     n_botRect.rectNode)

    n_frameCounter = TextNode('FrameCounter',
                              '[python {int(burnin.curnormframe(nuke.root().knob("first_frame").value()))}]/[python {int(burnin.normframerange(nuke.root().knob("first_frame").value(),nuke.root().knob("last_frame").value())[1])}] ([python {nuke.frame()}])',
                              False,
                              30,
                              ['root.width - 200', zeroHeight, rootWidth, 100],
                              False,
                              'center',
                              n_botRect.rectNode)

    n_shotName = TextNode('ShotName',
                          'Hello World',
                          True,
                          30,
                          [25, zeroHeight, rootWidth, 100],
                          False,
                          'left',
                          n_frameCounter.textNode)

    n_fileName = TextNode('Filename',
                          "[python {os.path.splitext(os.path.basename(nuke.root().knob('name').value()))[0]}]",
                          False,
                          30,
                          [0, 'root.height - 100', rootWidth, rootHeight],
                          False,
                          'center',
                          n_shotName.textNode)

    n_authorName = TextNode('AuthorName',
                            'YOUR NAME HERE',
                            True,
                            30,
                            [zeroWidth, zeroHeight, rootWidth, 100],
                            False,
                            'center',
                            n_fileName.textNode)

    n_Rect = RectNode('pRect',
                      [25, zeroHeight, rootWidth, 'root.height - 100'],
                      0,
                      0,
                      False,
                      None)

    # n_DrexelBanner = TextNode('DrexelBanner',
    #                           'Drexel University',
    #                           False,
    #                           50,
    #                           [0, 'root.height- 100,' rootWidth, 'root.height,
    ''#                           False,
    #                           'center',
    #                           None)

    n_localTime = TextNode('LocalTime',
                           'Date: [date %D] [date %T]',
                           False,
                           50,
                           [zeroWidth, 'root.height - 100', halfWidth, rootHeight],
                           True,
                           'left',
                           None)

    n_slateAuthor_t = TextNode('SlateAuthor_Title',
                               'Author: ',
                               False,
                               50,
                               [zeroWidth, 'root.height - 200', halfWidth, 'root.height - 100'],
                               True,
                               'left',
                               n_localTime.textNode)

    n_slateAuthor = TextNode('SlateAuthor',
                             '[python {nuke.toNode("BurnIn").knob("author").getValue()}]',
                             True,
                             50,
                             [175, 'root.height - 200', halfWidth, 'root.height - 100'],
                             True,
                             'left',
                             n_slateAuthor_t.textNode)

    n_slateFormat = TextNode('SlateFormat',
                             'Format: [python {nuke.root().format().name()}]',
                             True,
                             50,
                             [zeroWidth, 'root.height - 300', halfWidth, 'root.height - 200'],
                             True,
                             'left',
                             n_slateAuthor.textNode)

    n_slateShot = TextNode('SlateShot',
                           'Shot: [python {nuke.toNode("BurnIn").knob("shot").getValue()}]',
                           False,
                           50,
                           [zeroWidth, 'root.height - 400', halfWidth, 'root.height - 300'],
                           True,
                           'left',
                           n_slateFormat.textNode)

    n_slateRange = TextNode('SlateRange',
                            '[python {int(nuke.root().knob("first_frame").value())}] - [python {int(nuke.root().knob("last_frame").value())}]',
                            True,
                            50,
                            [zeroWidth, 'root.height - 500', halfWidth, 'root.height - 400'],
                            True,
                            'left',
                            n_slateShot.textNode)

    n_slateCommentTitle = TextNode('SlateCommentTitle',
                                   'Comments: ',
                                   False,
                                   50,
                                   [halfWidth, 'root.height - 150', rootWidth, 'root.height - 50'],
                                   False,
                                   'left',
                                   n_slateRange.textNode)

    n_slateComment = TextNode('SlateComment',
                              '[python {nuke.toNode("BurnIn").knob("notes").getValue()}]',
                              False,
                              50,
                              [halfWidth, 'root.height - 150', rootWidth, 'root.height - 250'],
                              False,
                              'left',
                              n_slateCommentTitle.textNode)

    n_slateGrey = RectNode('greyTest', [0, 0, 50, 50], [0.5, 0.5, 0.5, 1], 1, False, n_slateComment.textNode)
    n_slateYellow = RectNode('yellowTest', [50, 0, 100, 50], [0.5, 0.5, 0, 1], 1, False, n_slateGrey.rectNode)
    n_slateCyan = RectNode('cyanTest', [100, 0, 150, 50], [0, 0.5, 0.5, 1], 1, False, n_slateYellow.rectNode)
    n_slateGreen = RectNode('greenTest', [150, 0, 200, 50], [0, 0.5, 0, 1], 1, False, n_slateCyan.rectNode)
    n_slatePurple = RectNode('purpleTest', [200, 0, 250, 50], [0.5, 0, 0.5, 1], 1, False, n_slateGreen.rectNode)
    n_slateRed = RectNode('redTest', [250, 0, 300, 50], [0.5, 0, 0, 1], 1, False, n_slatePurple.rectNode)
    n_slateBlue = RectNode('blueTest', [300, 0, 350, 50], [0, 0, 0.5, 1], 1, False, n_slateRed.rectNode)
    n_slateRamp = RectNode('greyRamp', [0, 50, 500, 75], [0, 0, 0, 1], 1, True, n_slateBlue.rectNode)

    n_slateBlack = RectNode('blackTest', [350, 0, 400, 50], [0, 0, 0, 1], 1, False, n_slateRamp.rectNode)
    n_slateMid = RectNode('midGreyTest', [400, 0, 450, 50], [0.5, 0.5, 0.5, 1], 1, False, n_slateBlack.rectNode)
    n_slateWhite = RectNode('whiteTest', [450, 0, 500, 50], [1, 1, 1, 1], 1, False, n_slateMid.rectNode)
    n_slateStrip = RectNode('whiteStrip', [0, 75, 500, 85], [1, 1, 1, 1], 1, False, n_slateWhite.rectNode)

    # Create switch
    n_switch = nuke.createNode("Switch", inpanel=False)
    n_switch['name'].setValue('SlateSwitch')
    n_switch['which'].setAnimated()
    n_switch['which'].setValueAt(0, int(nuke.root().knob("first_frame").value()) - 1)
    n_switch['which'].setValueAt(1, int(nuke.root().knob("first_frame").value()))
    n_switch.setInput(0, n_slateStrip.rectNode)
    n_switch.setInput(1, n_authorName.textNode)

    # Link up the input and output of the group node
    # Close the group node
    n_timecode.setInput(0, nuke.toNode('Input1'))
    nuke.toNode('Output1').setInput(0, n_switch)
    n_burnInGroup.end()

    # Create DynamicFont Python Knob
    # k_DynFont = nuke.PyCustom_Knob('dyfont', 'dyfont')
    # dynfont_code = ''
    #
    # k_DynFont.setValue(dynfont_code)
    # n_burnInGroup.addKnob(k_DynFont)

# Add an BurnIn option to the Image menu
nuke.tprint('Adding BurnIn to Image menu.')
menubar = nuke.menu('Nodes')
m = menubar.findItem('Image')
m.addSeparator()
m.addCommand('BurnIn', 'burnin.dropBurnIn()')
