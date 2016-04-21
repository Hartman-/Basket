# !/usr/bin/env python
from __future__ import absolute_import
#from __future__ import unicode_literals

# Execute with
# $ python basket/__main__.py (2.6+)
# $ python -m basket         (2.7+)

# import basket

# if __name__ == '__main__':
#     basket.main()

# !/usr/bin/env python

import os
import shutil
from basket.nofilethisname import __version__

print (__version__)
print ("bin")

__proj_dir__ = "C:\Users\IanHartman\BasketTestProj"
__dst_dir__ = "C:\Users\IanHartman\SecondProj"


def create_local_dir(src_dir, dst_dir):
    try:
        if os.path.exists(dst_dir) == False:
            shutil.copytree(src_dir, dst_dir)
        else:
            print("exists")
            while os.path.exists(dst_dir) == True:
                user_dir = raw_input("Please input a directory that doesn't exist.")
                input_dir = str(user_dir)
                # Check if the input directory Exists
                if os.path.exists(input_dir) == False:
                    shutil.copytree(src_dir, input_dir)
                    print(str("Directory Created at: {0}").format(input_dir))
                    break
    except OSError as err:
        # print type(err)
        print(err)
        print("Invalid Operation!")

create_local_dir(__proj_dir__, __dst_dir__)