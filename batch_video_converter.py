#!/usr/bin/env python3

# Python Batch Video Converter
# Author: Alessandro Paganelli (alessandro.paganelli@gmail.com)

# Dependencies:
# - ffmpeg binary (/usr/bin/ffmpeg)

__author__ = "Alessandro Paganelli"
__version__ = "0.1"
__license__ = "GPL3"

import argparse
import os
import datetime
import time
from sys import exit

#------------------------------------------------------------------------------
class ConversionReport():
    """A simple report to summarizye the conversion process."""
    
    def __init__(self):
        self.input_file_path = ''
        self.output_file_path = ''
        self.input_file_size_byte = 0
        self.output_file_size_byte = 0
        self.compression_ratio = 0

    def SetInputFilePath(self, input_file_path):
        self.input_file_path = input_file_path

    def SetOutputFilePath(self, output_file_path):
        self.output_file_path = output_file_path

    def SetInputFileSizeByte(self, input_file_size_byte):
        self.input_file_size_byte = input_file_size_byte

    def SetOutputFileSizeByte(self, output_file_size_byte):
        self.output_file_size_byte = output_file_size_byte

    def SetCompressionRatio(self, compression_ratio):
        self.compression_ratio = compression_ratio

    def ToString(self):
        """Create a string out of the current report."""
        out_string = 'Original: ' + str(self.input_file_path) + ', compressed: ' + str(self.output_file_path) + ', original size = ' + str(self.input_file_size_byte) + ', compressed size = ' + str(self.output_file_size_byte) + ', ratio = ' + "{:.2f}".format(self.compression_ratio)
        return out_string


class VideoConverter():
    """Class to manage file conversion."""
    
    # class constants
    FFMPEG_BIN='/usr/bin/ffmpeg'
    TARGET_VIDEO_BITRATE='250k'
    TARGET_AUDIO_BITRATE='128k'
    OUTPUT_FILE_LABEL='_conv'

    # report keys
    INPUT_KEY = 'input_file_path'
    OUTPUT_KEY = 'output_file_path'
    INPUT_BYTES = 'input_file_size_bytes'
    OUTPUT_BYTES = 'output_file_size_bytes'
    COMPRESSION_RATIO = 'compression_ratio'

    @staticmethod
    def Convert(inputfile):
        """
        Converts inputfile into an output file with the same name and 
        OUTPUT_FILE_LABEL as name identifier.
        """

        # get filename and ext
        split = os.path.splitext(inputfile)

        file_name = split[0]
        file_ext = split[1]

        # create output file name by sanitizing input file
        # goal: avoid spaces and duplicate dashes
        sanitized = file_name.replace(' ', '_')
        sanitized = sanitized.replace('-_', '_')
        sanitized = sanitized.replace('_-', '_')
        sanitized = sanitized.replace('__', '_')

        outputfile = sanitized + VideoConverter.OUTPUT_FILE_LABEL + file_ext

        # 2-pass conversion with ffmpeg
        first_pass_cmd = VideoConverter.FFMPEG_BIN + ' -y -i \'' + inputfile + '\' -c:v libx264 -preset ultrafast -tune animation -b:v ' + VideoConverter.TARGET_VIDEO_BITRATE + ' -pass 1 -an -f mp4 /dev/null'
        second_pass_cmd = VideoConverter.FFMPEG_BIN + ' -i \'' + inputfile + '\' -c:v libx264 -preset ultrafast -tune animation -b:v ' + VideoConverter.TARGET_VIDEO_BITRATE + ' -pass 2 -c:a aac -b:a ' + VideoConverter.TARGET_AUDIO_BITRATE + ' ' + outputfile

        # actual compression
        os.system(first_pass_cmd)
        os.system(second_pass_cmd)

        isize = os.stat(inputfile).st_size
        osize = os.stat(outputfile).st_size
        compression_ratio = (float(osize) / float(isize)) * 100

        rep = ConversionReport()
        rep.SetInputFilePath(inputfile)
        rep.SetOutputFilePath(outputfile)
        rep.SetInputFileSizeByte(isize)
        rep.SetOutputFileSizeByte(osize)
        rep.SetCompressionRatio(compression_ratio)

        return rep


#------------------------------------------------------------------------------
def process_dir(directory, extension, remove=False, summary_file_path=''):
    """Process a single directory"""

    # get files matching the required extension
    file_path_list = [os.path.join(directory, name) for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name)) and name.endswith(extension)]

    total_files = len(file_path_list)

    print('Processing dir: %s' % directory)
    print('Found %s files.\n' % str(total_files))

    file_number = 1
    total_elapsed_time = 0
    start_time = datetime.datetime.now()
    summary_list = []
    for file_path in file_path_list:
        print('[%s/%s] Considering file %s' % (str(file_number), str(total_files), file_path))

        current_file_start_time = datetime.datetime.now()

        # actual processing of current file
        report = VideoConverter.Convert(file_path)

        if summary_file_path:
            summary_list.append(report.ToString())

        # TODO: manage file removal

        # Compute required time
        current_file_end_time = datetime.datetime.now()
        current_file_elapsed_time = current_file_end_time - current_file_start_time
        total_elapsed_time = current_file_end_time - start_time
        print('Current file elapsed time: %s [total elapsed time: %s]' % (current_file_elapsed_time.seconds, total_elapsed_time.seconds))
        file_number += 1

    # dump summary lists
    if summary_file_path:
        # append newlines to the list
        summary_list_fixed = map(lambda x: x+'\n', summary_list)
        with open(summary_file_path, 'w') as summary_file:
            summary_file.writelines(summary_list_fixed)

#------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()

    # required args
    required_args = parser.add_argument_group('required named arguments')
    required_args.add_argument('-d', '--directory', help='Target directory absolute path to look for videos', required=True)
    required_args.add_argument('-e', '--extension', help='Video file extension to be used to identify video files', required=True)

    # optional args
    parser.add_argument('-r', '--remove', help='Remove original file after compression', action='store_true')
    parser.add_argument('-s', '--summary', help='Absolute path of the output file for the final summary')
    
    args = parser.parse_args()

    if not os.path.isabs(args.directory):
        print('Directory %s is not an absolute path. Exiting.' % args.directory)
        exit(1)

    if args.summary and not os.path.isabs(args.summary):
        print('Summary file %s is not an absolute path. Exiting.' % args.summary)
        exit(2)

    print('----- Batch video converter -----')
    print('Using:') 
    print('- directory: %s' % args.directory)
    print('- extension: %s' % args.extension)
    if (args.remove):
        print('- remove:    yes')
    if (args.summary):
        print('- summary:   %s' % args.summary)
    print()

    process_dir(args.directory, args.extension, args.remove, args.summary)

#------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
