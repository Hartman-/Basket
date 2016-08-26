import BasketGlobals as config
import assetManager
proj_Manager = assetManager.HManager()


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
nuke.addOnScriptSave(proj_Manager.checkScriptName)

setupMenu()

def savelocalscript():
    print('fuck you da bitch')
    if not os.path.isdir(config.nukeDir()):
        print('what do?')
    else:
        proj_Manager.s_easySave('testMyAsshole')

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