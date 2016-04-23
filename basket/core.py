# !/usr/bin/env python
#from __future__ import unicode_literals


# RIPPED CODE
# Execute with
# $ python basket/__main__.py (2.6+)
# $ python -m basket         (2.7+)

# import basket

# if __name__ == '__main__':
#     basket.main()

import os
import config as cfg
from utils import filetransfer as ft

root, dirs, files = os.walk(cfg.__project_dir__).next()

ft.enforce_name(root, dirs, files)
ft.create_local_dir(cfg.__project_dir__, cfg.__local_dir__)
