import getpass
import os

user = str(getpass.getuser())
userPath = os.path.join("W:\\SRPJ_LAW\\nuke\\user\\", user)
if os.path.isdir(userPath):
    nuke.pluginAddPath( userPath )

showPath = "W:\\SRPJ_LAW\\nuke\\show\\HONU"
if os.path.isdir(showPath):
    nuke.pluginAddPath(showPath)