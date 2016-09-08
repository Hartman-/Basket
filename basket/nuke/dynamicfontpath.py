import nuke

def updatefonts():
    for i, n in enumerate (nuke.allNodes()):
        if n.Class() == 'Text2':
            try:
                n.knob('font').setValue('Source Sans Pro', 'Regular')
            except:
                ValueError