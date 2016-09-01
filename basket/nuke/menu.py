import re

import BasketGlobals as config
import assetManager
import autowrite
proj_Manager = assetManager.HManager()


# Add beforeRender script to automatically create write directories that don't exist
nuke.knobDefault( 'Write.beforeRender', 'assetManager.createWriteDirs()')


def checkEnv():
    if os.getenv('SEQ') is None or os.getenv('SHOT') is None or os.getenv('SHOW') is None:
        config.setupSession()


def setupMenu():
    # If any of the environment variables are missing, set the basics
    checkEnv()
    shotMenu = '%s - %s' % (os.getenv('SEQ'), os.getenv('SHOT'))
    createUI(shotMenu)


def setProject():
    panel = nuke.Panel('Set Project')

    panel.addSingleLineInput('Scene', 'scene...')
    panel.addSingleLineInput('Shot', 'shot...')

    prevProj = '%s - %s' % ( os.getenv( 'SEQ' ), os.getenv('SHOT') )

    ret = panel.show()

    config.setSeq(panel.value('Scene'))
    config.setShot(panel.value('Shot'))
    refreshUI(prevProj)


def createUI(name):
    nuke.menu('Nuke').addCommand(name + '/Easy Save', proj_Manager.easySave)
    nuke.addFavoriteDir(
    name='NUKE Scripts',
    directory=config.nukeDir(),
    type=nuke.SCRIPT)


def refreshUI(prev):
    nuke.removeFavoriteDir('NUKE Scripts', nuke.SCRIPT)
    nuke.menu( 'Nuke' ).removeItem(prev)

    # UPDATE LOCAL VARIABLES TO MATCH ENVIRONMENT
    newMenu = '%s - %s' % ( os.getenv( 'SEQ' ), os.getenv('SHOT') )
    createUI(newMenu)


nuke.menu('Nuke').addCommand('Manage/Set Project', setProject)
nuke.menu('Nuke').addCommand('Manage/Localize', assetManager.localizeRead)
nuke.addOnScriptSave(proj_Manager.checkScriptName)

setupMenu()

def savelocalscript():
    if not os.path.isdir(config.nukeDir()):
        print('what do?')
    else:
        nkName = os.path.basename(nuke.root().knob('name').value())
        desc = nkName.split('_')[2]
        fileVersion = int(re.search(r'[vV]\d+', os.path.split(nkName)[1]).group().lstrip('vV'))
        proj_Manager.s_easySave(desc, ver=fileVersion)

def saveserverscript():
    if not os.path.isdir(config.nukeDir()):
        print('what do?')
    else:
        serverDir = os.path.join(config.serverDir(), os.getenv('SHOW'), 'Working', os.getenv('SEQ'), os.getenv('SHOT'), '07. Comp')

        nkName = os.path.basename(nuke.root().knob('name').value())
        desc = nkName.split('_')[2]
        fileVersion = int(re.search(r'[vV]\d+', os.path.split(nkName)[1]).group().lstrip('vV'))
        proj_Manager.s_easySave(desc, server=serverDir, ver=fileVersion)

# def nkPanelHelper(key):
#     nkScripts = config.getNukeScripts()
#     if not nkScripts:
#         return
#     p = assetManager.LoaderPanel(nkScripts)
#     p.setMinimumSize(200,200)
#
#     if p.showModalDialog():
#         if p.selectedScript:
#             if key == 'newUser':
#                 nuke.Root().setModified(False)
#             nuke.scriptOpen(p.selectedScript)


# nuke.addOnUserCreate(nkPanelHelper, 'newUser', nodeClass='Root')
nuke.addOnScriptLoad(savelocalscript)
nuke.addOnScriptClose(saveserverscript)