import maya.cmds as cmds

def main():
    cmds.menu(label='Manage', tearOff=True, parent='MayaWindow')
    cmds.menuItem(divider=True, dividerLabel='Save')
    cmds.menuItem(label='Easy Save')
    cmds.menuItem(label='Easy Iterate')
    cmds.menuItem(divider=True, dividerLabel='Export')
    cmds.menuItem(label='Publish Asset')
    cmds.menuItem(divider=True, dividerLabel='Submit')
    cmds.menuItem(label='Submit to Qube')