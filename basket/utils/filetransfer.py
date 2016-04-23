# !/usr/bin/env python
import os, time
import shutil

import config as cfg

copy_these = ['ThisIsATest.txt']


# Given List of needed files
# Ignore all other files, copy all directories
def ignore_files(folder, files):
    ignore_list = []
    for file in files:
        full_path = os.path.join(folder, file)
        if not os.path.isdir(full_path):
            if file not in copy_these:
                ignore_list.append(file)
    return ignore_list


# Copies Included files
def create_local_dir(src_dir, dst_dir):
    try:
        if os.path.exists(dst_dir) == False:
            shutil.copytree(src_dir, dst_dir, ignore=ignore_files)
        else:
            print("exists")
            while os.path.exists(dst_dir) == True:
                user_dir = raw_input("Please input a directory that doesn't exist.")
                input_dir = str(user_dir)
                # Check if the input directory Exists
                if os.path.exists(input_dir) == False:
                    shutil.copytree(src_dir, input_dir, ignore=ignore_files)
                    print(str("Directory Created at: {0}").format(input_dir))
                    break
    except OSError as err:
        # print type(err)
        print(err)
        print("Invalid Operation!")
        pass


# def sync_local_files():


def enforce_name(root, dirs, files):
    # def filetypes(ext):
    #     switch = {
    #         0: nuke
    #     }
    #     return switch.get(ext, "None")

    lengths = {
        0: '0000',
        1: '000',
        2: '00',
        3: '0',
        4: ''
    }

    def filerename(f_in, type, ext):
        cur_file = os.path.join(root, f_in)
        shot_ver = lengths[len(str(cfg.__shot_version__))] + str(cfg.__shot_version__)
        file_name = cfg.__project_acr__ + '_' + cfg.__cur_user__ + '_' + type + '_s_' + cfg.__shot_num__ + '_v' + shot_ver + ext
        file_path = os.path.join(root, file_name)
        os.rename(cur_file, file_path)

    nuke_files = []

    for file in files:
        file_ext = os.path.splitext(file)[1]
        # Format NUKE Files
        if file_ext == '.nk':
            nuke_files.append(file)

    # Determine which nk file is the newest
    cur_nk = nuke_files[0]
    for nk_file in nuke_files:
        cur_f = os.path.join(root, cur_nk)
        cur_st = os.stat(cur_f)
        cur_mtime = time.asctime(time.localtime(cur_st.st_mtime))
        if cur_mtime < time.asctime(time.localtime(os.stat(os.path.join(root, nk_file)).st_mtime)):
            cur_nk = nk_file

    # Rename Newest NUKE file
    try:
        filerename(cur_nk, 'Comp', '.nk')
    except WindowsError as err:
        # If File Name Already Exists (WindowsError 183)
        if err.args[0] == 183:
            cfg.__shot_version__ += 1
            # UPDATE THIS VALUE IN THE DATABASE
            # PULL UPDATED VALUED FROM DATABASE
            filerename(cur_nk, 'Comp', '.nk')
