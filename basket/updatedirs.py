from glob import glob
import os

sdir = 'C:\Users\imh29\Desktop\LAW_server\PROJ'
ldir = 'C:\Users\imh29\Desktop\LAW_local\PROJ'

s_list = glob(os.path.join(sdir, '*/'))
l_list = glob(os.path.join(ldir, '*/'))

sclean = []
lclean = []

for i, n in enumerate(s_list):
    name = os.path.basename(os.path.normpath(n))
    sclean.append(name.lower())

for a, b in enumerate(l_list):
    name = os.path.basename(os.path.normpath(b))
    lclean.append(name.lower())

missing = list(set(sclean) - set(lclean))