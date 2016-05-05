# !/usr/bin/env python
import os, time
import shutil
import json

from pprint import pprint

import config as cfg

# === === === === === === === === === === === === === === === === === === === === === === === === === === === === === ===
# A PORTION OF THE CODE THANKS TO ideasman42
# Taken from http://blender.stackexchange.com/questions/21092/how-to-get-all-images-for-an-image-sequence-from-python
# === === === === === === === === === === === === === === === === === === === === === === === === === === === === === ===


def image_sequence_resolve_all(filepath):
    import os

    basedir, filename = os.path.split(filepath)
    filename_noext, ext = os.path.splitext(filename)

    from string import digits
    if isinstance(filepath, bytes):
        digits = digits.encode()

    filename_nodigits = filename_noext.rstrip(digits)

    if len(filename_nodigits) == len(filename_noext):
        # input isn't from a sequence
        return []

    files = os.listdir(basedir)
    seq_files = []
    filename_endingdigits = filename_noext.rsplit('.')[len(filename_noext.rsplit('.')) - 1]
    ending_digits = filename_endingdigits

    for f in files:
        if f.startswith(filename_nodigits) and f.endswith(ext) and f[len(filename_nodigits):-len(ext) if ext else -1].isdigit():
            f_noext, ext = os.path.splitext(f)
            f_digits = int(f_noext.rsplit('.')[len(f_noext.rsplit('.')) - 1])
            if f_digits > int(filename_endingdigits):
                ending_digits = f_digits
            else:
                ending_digits = int(filename_endingdigits)
            seq_files.append(f)

    seq_str = "[{}-{}]".format(str(int(filename_endingdigits)), str(ending_digits))
    seq_template = basedir + "\\" + filename_nodigits + ("#" * len(filename_endingdigits)) + ext + "_FR" + seq_str

    # return [
    #     os.path.join(basedir, f)
    #     for f in files
    #         if f.startswith(filename_nodigits) and
    #             f.endswith(ext) and
    #             f[len(filename_nodigits):-len(ext) if ext else -1].isdigit()]

    return seq_template


# === === === === === === === === === === === === === === === === === === === === === === === === === === === === === ===
#
# === === === === === === === === === === === === === === === === === === === === === === === === === === === === === ===

proj_dir = str(cfg.__project_dir__)
img_dir = "01. Plates\\"
# print(proj_dir)
file_dir = os.path.join(proj_dir, img_dir, 'BSKP_imageSequence_v0001.0001.txt')
# print(file_dir)
print(image_sequence_resolve_all(file_dir))


# Build the List of copied files
def build_file_list():
    json_path = 'C:\\Users\\IanHartman\\Basket-App\\basket\\assets\\data.json'
    s_files = []

    with open(json_path) as data_file:
        shot_data = json.load(data_file)['shots']

    for f in shot_data[str(cfg.__shot_num__)]['scripts']:
        s_files.append(f)

    for s in shot_data[str(cfg.__shot_num__)]['sequences']:
        print(image_sequence_resolve_all(s))

    s_files.append('ThisIsATest.txt')

    return s_files


# Given List of needed files
# Ignore all other files, copy all directories
def ignore_files(folder, files):
    ignore_list = []
    important_files = build_file_list()
    for file in files:
        full_path = os.path.join(folder, file)
        if not os.path.isdir(full_path) and file not in important_files:
            ignore_list.append(file)
    return ignore_list

def create_local_files(src_dir, dst_dir):
    try:
        shutil.copytree(src_dir, dst_dir, ignore=ignore_files)
    except OSError as err:
        return err.args[0]


def main(src_dir, dst_dir):
    # Arbitrary Value to start the loop
    err_code = 999
    important_files = build_file_list()
    while err_code != None:
        err_code = create_local_files(src_dir, dst_dir)
        if err_code == None:
            print('All Clear')
            break
        if err_code == 3:
            print('Error 3')
        if err_code == 183:
            print('Error 183')
            user_dir = raw_input("Please input a directory that doesn't exist.")
            input_dir = str(user_dir)
            if os.path.exists(input_dir) == False:
                err_code = create_local_files(src_dir, input_dir)
                print(str("Directory Created at: {0}").format(input_dir))

# def sync_local_files():


def enforce_name(root, dirs, files):
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
            confirm = raw_input("File Already Exists but a Newer version has been found... version up? (y/n)")
            if confirm.lower() == 'yes' or confirm.lower() == 'y':
                cfg.__shot_version__ += 1
                # UPDATE THIS VALUE IN THE DATABASE
                # PULL UPDATED VALUED FROM DATABASE
                filerename(cur_nk, 'Comp', '.nk')
            else:
                pass
