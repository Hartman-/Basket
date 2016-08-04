import assetManager
proj_Environment = assetManager.Environment()
proj_Manager = assetManager.HManager()

shotMenu = '%s - %s' % ( os.getenv( 'SEQ' ), os.getenv('SHOT') )


def setProject():
  panel = nuke.Panel('Set Project')

  panel.addSingleLineInput('Scene', 'scene...')
  panel.addSingleLineInput('Shot', 'shot...')

  prevProj = '%s - %s' % ( os.getenv( 'SEQ' ), os.getenv('SHOT') )

  ret = panel.show()

  proj_Environment.setSeq(panel.value('Scene'))
  proj_Environment.setShot(panel.value('Shot'))
  refreshUI(prevProj)


def createUI(name):
  nuke.menu('Nuke').addCommand(name + '/Easy Save', proj_Manager.easySave)
  nuke.addFavoriteDir(
    name='NUKE Scripts',
    directory=proj_Environment.nukeDir(),
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
    nkScripts = proj_Manager.getNukeScripts()
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