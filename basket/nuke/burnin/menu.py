import Hartman_dynamicFonts, Hartman_BurnIn, Hartman_betterWriteNodes

nukeMenu = nuke.menu( 'Nodes' )

imh29_ToolsMenu = nukeMenu.addMenu( 'HartmanScripts', icon='imh29_NUKE_icon_Package.png')
imh29_ToolsMenu.addCommand( 'Burn-In', Hartman_BurnIn.initBurnIn)
imh29_ToolsMenu.addCommand( 'BetterWriteNodes', Hartman_betterWriteNodes.addBeforeRender)
imh29_ToolsMenu.addCommand( 'SourceSansPro Font', Hartman_dynamicFonts.setFontPath)