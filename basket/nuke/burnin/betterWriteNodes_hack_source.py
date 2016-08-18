nuke.root().knob('onScriptSave').setValue('''
import re
for n in nuke.allNodes():
	if n.Class() == 'Write':
		code = """
import re
fileVersion = re.search( r'[vV]\d+', os.path.split(nuke.root().name())[1]).group()
print fileVersion

for node in nuke.allNodes():
	if node.Class() == 'Write':
		node.knob('file').setValue(re.sub( r'[vV]\d+', fileVersion,node.knob('file').value()))

file = nuke.filename(nuke.thisNode())
dir = os.path.dirname(file)
osdir = nuke.callbacks.filenameFilter(dir)
try:
	os.makedirs (osdir)
except OSError:
	pass
		"""

		n['beforeRender'].setValue(code)

	if n.Class() == 'Group':
		print 'group'
		for g_node in n.nodes():
			if g_node.Class() == 'Write':				
				code = """
import re
fileVersion = re.search( r'[vV]\d+', os.path.split(nuke.root().name())[1]).group()
print fileVersion
curNode = nuke.thisNode()
curNode['file'].setValue(re.sub( r'[vV]\d+', fileVersion,nuke.thisNode().knob('file').value()))

file = nuke.filename(nuke.thisNode())
dir = os.path.dirname(file)
print dir
osdir = nuke.callbacks.filenameFilter(dir)
print osdir
try:
	os.makedirs (osdir)
except OSError:
	pass
		"""

				g_node['beforeRender'].setValue(code)
''')