#!/usr/bin/env python3

# Python Batch Video Converter
# Author: Alessandro Paganelli (alessandro.paganelli@gmail.com)

__author__ = "Alessandro Paganelli"
__version__ = "0.1"
__license__ = "GPL3"

import argparse
import os
import datetime
import time
from sys import exit

#------------------------------------------------------------------------------
class VideoConverter():
    """Class to manage a single file to be converted."""
    pass
    # TODO

#------------------------------------------------------------------------------
def process_dir(directory, extension, remove=False, summary=False):
    """Process a single directory"""

    # get files matching the required extension
    file_path_list = [os.path.join(directory, name) for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name)) and name.endswith(extension)]

    total_files = len(file_path_list)

    print('Processing dir: %s' % directory)
    print('Found %s files.\n' % str(total_files))

    file_number = 1
    total_elapsed_time = 0
    start_time = datetime.datetime.now()
    for file_path in file_path_list:
        print('[%s/%s] Considering file %s' % (str(file_number), str(total_files), file_path))

        current_file_start_time = datetime.datetime.now()

        # TODO: actual processing of current file
        time.sleep(1)

        # Compute required time
        current_file_end_time = datetime.datetime.now()
        current_file_elapsed_time = current_file_end_time - current_file_start_time
        total_elapsed_time = current_file_end_time - start_time
        print('Current file elapsed time: %s [total elapsed time: %s]' % (current_file_elapsed_time.seconds, total_elapsed_time.seconds))
        file_number += 1

#------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()

    # required args
    required_args = parser.add_argument_group('required named arguments')
    required_args.add_argument('-d', '--directory', help='Target directory absolute path to look for videos', required=True)
    required_args.add_argument('-e', '--extension', help='Video file extension to be used to identify video files', required=True)

    # optional args
    parser.add_argument('-r', '--remove', help='Remove original file after compression', action='store_true')
    parser.add_argument('-s', '--summary', help='Create a final summary after the run', action='store_true')
    
    args = parser.parse_args()

    if not os.path.isabs(args.directory):
        print('Directory %s is not an absolute path. Exiting.' % args.directory)
        exit(1)

    print('----- Batch video converter -----')
    print('Using:') 
    print('- directory: %s' % args.directory)
    print('- extension: %s' % args.extension)
    if (args.remove):
        print('- remove:    yes')
    if (args.summary):
        print('- summary:   yes')
    print()

    process_dir(args.directory, args.extension, args.remove, args.summary)

#------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
