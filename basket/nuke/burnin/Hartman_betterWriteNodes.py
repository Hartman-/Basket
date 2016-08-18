import nuke, os, re

def addBeforeRender():
	for n in nuke.allNodes():
		if n.Class() == 'Write':
			n.knob( 'beforeRender' ).setValue('renderControl()')

def makeWriteDirs():
	file = nuke.filename(nuke.thisNode())
	dir = os.path.dirname(file)
	osdir = nuke.callbacks.filenameFilter(dir)
	try:
		os.makedirs (osdir)
	except OSError:
		pass

def autoVersion():
	fileVersion = re.search( r'[vV]\d+', os.path.split(nuke.root().name())[1]).group()
	print fileVersion

	for node in nuke.allNodes():
		if node.Class() == 'Write':
			node.knob('file').setValue(re.sub( r'[vV]\d+', fileVersion,node.knob('file').value()))

def renderControl():

	#Run before makeWriteDirs to make sure the directory version and file version are correct
	autoVersion()

	makeWriteDirs()