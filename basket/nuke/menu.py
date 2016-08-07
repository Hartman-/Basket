from basket import config
import assetManager
proj_Manager = assetManager.HManager()

shotMenu = '%s - %s' % ( os.getenv( 'SEQ' ), os.getenv('SHOT') )


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
createUI(shotMenu)
nuke.addOnScriptSave(proj_Manager.checkScriptName)


def nkPanelHelper(key):
    nkScripts = config.getNukeScripts()
    if not nkScripts:
        return
    p = assetManager.LoaderPanel(nkScripts)
    p.setMinimumSize(200,200)

    if p.showModalDialog():
        if p.selectedScript:
            if key == 'newUser':
                nuke.Root().setModified(False)
            nuke.scriptOpen(p.selectedScript)


nuke.addOnUserCreate(nkPanelHelper, 'newUser', nodeClass='Root')