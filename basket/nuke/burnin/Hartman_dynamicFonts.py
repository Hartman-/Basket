import nuke, os

# === ENVIRONMENT VARIABLES ===

fontKnob = 'font'
winDrive = os.environ['SYSTEMDRIVE']
SSPPath = ''

SSPMacPath = '/Library/Fonts/SourceSansPro-Regular.otf'
SSPWinPath = '{}/Windows/Fonts/SourceSansPro-Regular.otf'.format(winDrive)

def setFontPath():
	if (nuke.env["WIN32"] == True):
		OS = 'Win'
		SSPPath = SSPWinPath
	if (nuke.env["MACOS"] == True):
		OS = 'Mac'
		SSPPath = SSPMacPath

	nuke.root().knob('free_type_font_path').setValue(SSPPath)

	# This might be all the code needed with recent updates to NUKE...
	for node in nuke.allNodes():
		if node.knob( fontKnob ):
			node.knob( fontKnob ).setValue("Source Sans Pro", "Regular")