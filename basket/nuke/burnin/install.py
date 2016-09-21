import os
import sys
import shutil

files = ['init.py', 'lawSetup.py', 'Hartman_dynamicFonts.py', 'Hartman_BurnIn.py', 'Hartman_betterWriteNodes.py', 'icons\imh29_NUKE_icon_Package.png']
instDirs = ['icons', 'python']

homedir = os.path.expanduser('~')

srcdir = os.path.dirname(os.path.realpath(__file__))
srcfile = os.path.join(srcdir, 'install.py')

dstroot = ''

# Build the correct path to the nuke install
if sys.platform == 'darwin':
	dstroot = os.path.join(homedir, '/Applications/Nuke9.0v6/Nuke9.0v6.app/Contents/')
if sys.platform == 'win32':
	dstroot = os.path.join(homedir, '.nuke')

# Check to see if the sub directories exist
# If not, Create them
for idir in instDirs:
	subdir = os.path.join(dstroot, idir)
	if not os.path.isdir(subdir):
		os.makedirs(subdir)

#assert not os.path.isabs(srcfile)

for f in files:
	splt = os.path.split(f)
	dstpath = os.path.join(dstroot, splt[0])
	filedir = os.path.join(srcdir, f)
	shutil.copy(filedir, dstpath)