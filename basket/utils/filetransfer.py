# !/usr/bin/env python
import os, time
import shutil
import json

from tinydb import TinyDB, Query
from string import find

from pprint import pprint

import config as cfg


proj_dir = str(cfg.__project_dir__)
img_dir = "01. Plates\\"


class Transfer():
    def __init__(self, proj_dir, local_dir):
        self.shot_file_db = TinyDB('C:\\Users\\IanHartman\\Basket-App\\basket\\assets\\shot_file_db.json')
        self.proj_json = 'C:\\Users\\IanHartman\\Basket-App\\basket\\assets\\data.json'

        self.proj_dir = proj_dir
        self.local_dir = local_dir

        self.shot_files = []

    def splitFilePath(self, path):
        basedir, filename = os.path.split(path)
        filename_noext, ext = os.path.splitext(filename)
        filename_init_digits = filename_noext.rsplit('.')[len(filename_noext.rsplit('.')) - 1]
        filename_end_digits = filename_init_digits
        return [basedir, filename, filename_noext, ext, filename_init_digits, filename_end_digits]

    def encodeSequence(self, filepath):
        basedir, filename = os.path.split(filepath)
        filename_noext, ext = os.path.splitext(filename)
        filename_init_digits = filename_noext.rsplit('.')[len(filename_noext.rsplit('.')) - 1]
        filename_end_digits = filename_init_digits

        from string import digits
        if isinstance(filepath, bytes):
            digits = digits.encode()

        filename_nodigits = filename_noext.rstrip(digits)

        # Equal length would be a result of a file that didn't have a trailing ####
        if len(filename_nodigits) == len(filename_noext):
            return []

        # List all files in the directory given for the initial file
        files = os.listdir(basedir)
        seq_files = []

        # Iterate through directory files
        for file in files:
            # Look for files that match the pattern of the initial file
            if file.startswith(filename_nodigits) and file.endswith(ext) and file[len(filename_nodigits):-len(ext) if ext else -1].isdigit():
                # Split the input file into necessary parts
                file_noext, file_ext = os.path.splitext(file)
                file_digits = str(file_noext.rsplit('.')[len(file_noext.rsplit('.')) -1])

                # Iterate through the sequence and count up how many files there are
                if int(file_digits) > int(filename_end_digits):
                    filename_end_digits = file_digits
                else:
                    filename_end_digits = filename_init_digits

                # Add the file to the list
                seq_files.append(file)

        # Build a stamp to represent the entire sequence in the DB
        seq_stamp = [basedir, filename_nodigits + ("#" * len(str(filename_end_digits))) + ext + "_FR" + "[{}-{}]".format(str(int(filename_init_digits)), str(filename_end_digits))]

        return seq_stamp

    def resolveSequence(self, stamp):
        if stamp.find("_FR[") != -1:
            seq_file_base =  stamp.split("_FR[")
            all_seq_files = []

            seq_file_range = seq_file_base[1].rstrip(']')
            seq_file_start = seq_file_range.split('-')[0]
            seq_file_end = seq_file_range.split('-')[1]
            seq_file_pad = seq_file_base[0].count('#')

            i = int(seq_file_start)
            while (i <= int(seq_file_end)):
                seq_file_fullname = str(seq_file_base[0]).replace('#'*seq_file_pad, '0'*(seq_file_pad - len(str(i))) + str(i))
                all_seq_files.append(seq_file_fullname)
                i = i + 1

            return all_seq_files

        else:
            print("Normal File")

    def getShotFiles(self):
        with open(self.proj_json) as proj_data:
            shot_data = json.load(proj_data)['shots']

        for script in shot_data[str(cfg.__shot_num__)]['scripts']:
            self.shot_files.append(script)

        for seq in shot_data[str(cfg.__shot_num__)]['sequences']:
            seq_files = self.resolveSequence(seq)
            for seq_file in seq_files:
                self.shot_files.append(seq_file)

    def ignoreFiles(self, folder, files):
        ignore_list = []
        for file in files:
            full_path = os.path.join(folder, file)
            if not os.path.isdir(full_path) and file not in self.shot_files:
                print(file)
                ignore_list.append(file)
        return ignore_list

    def createLocalCopy(self):
        try:
            shutil.copytree(self.proj_dir, self.local_dir, ignore=self.ignoreFiles)
        except OSError as err:
            return err.args[0]

test = Transfer(str(cfg.__project_dir__), str(cfg.__local_dir__))
test.getShotFiles()
test.createLocalCopy()
