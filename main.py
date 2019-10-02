import sys
import os.path
import re
import argparse

# Declare Global Vasriables

# results of program
CRITERIA = {
    'total_lines': 0,
    'total_comments': 0,
    'total_single_line_comments': 0,
    'total_block_line_comments': 0,
    'total_blocks': 0,
    'total_todo': 0
}

# Since multiple programming languages share // , /*, and */ as comments, it's more efficient to create one resource
# instead of multiple lists in the below dictionary
SLASHES = ['//', '/*', '*/']

# dictionary where keys are extensions, and values are list of comment syntax for the different languages
# first value in list is single line comment, second is start of block, third is end of block
SUPPORTED_FILE_TYPES = {
    '.py': ['#', '\'\'\'', '\'\'\''],
    '.java': SLASHES,
    '.js': SLASHES,
    '.c': SLASHES,
    '.cpp': SLASHES,
    ',go': SLASHES,
    '.cs': SLASHES,
    '.ts': SLASHES,
    '.rb': ['#', '=begin', '=end']
}

# will be used throughout codebase to ensure parsing of comments is done correctly
FILE_TYPE = None
# flag will be True when we are in a block comment
BLOCK_FLAG = False


def start():
    # open the file
    global CRITERIA
    with open(args.file, "r") as to_parse:
        global BLOCK_FLAG
        for line in to_parse.readlines():
            CRITERIA['total_lines'] += 1    # increment total number of lines by 1
            line = line.strip()             # strips the whitespaces at the beginning and end of a line
            # if in a block, check for end of block first
            if BLOCK_FLAG:
                if is_end_of_block(line):   # if end of block, increment total and block line comments, and flag = False
                    BLOCK_FLAG = False
                CRITERIA['total_comments'] += 1
                CRITERIA['total_block_line_comments'] += 1
                if is_todo(line):
                    CRITERIA['total_todo'] += 1
                continue
            # check for single line comment
            if is_comment(line):            # if single comment, increment total and single comments
                CRITERIA['total_comments'] += 1
                CRITERIA['total_single_line_comments'] += 1
                if is_todo(line):
                    CRITERIA['total_todo'] += 1
                continue
            if is_start_of_block(line):     # if beginning of block, increment total, block, and block line comments
                BLOCK_FLAG = True
                CRITERIA['total_comments'] += 1
                CRITERIA['total_block_line_comments'] += 1
                CRITERIA['total_blocks'] += 1
                if is_todo(line):
                    CRITERIA['total_todo'] += 1
                continue


# checks if the string is a line of code with a trailing comment
def is_code_with_comment(s):
    pass


# checks if the string is a comment
def is_comment(s):
    # if the line starts with the first index of the of the value from the dictionary, it is a single line comment
    global SUPPORTED_FILE_TYPES
    global FILE_TYPE
    return s.startswith(SUPPORTED_FILE_TYPES[FILE_TYPE][0])


# checks if the string is the start of a block comment
def is_start_of_block(s):
    # if the line starts with the second index of the of the value from the dictionary, it's the start of a block
    global SUPPORTED_FILE_TYPES
    global FILE_TYPE
    return s.startswith(SUPPORTED_FILE_TYPES[FILE_TYPE][1])


# checks if the string is the end of a block comment
def is_end_of_block(s):
    # if the line contains the third index of the of the value from the dictionary, it's the start of a block
    global SUPPORTED_FILE_TYPES
    global FILE_TYPE
    return SUPPORTED_FILE_TYPES[FILE_TYPE][2] in s


# checks if the string is a TODO
def is_todo(s):
    # classify the key word and check if it's in the comment
    return "TODO:" in s


def parse_input():
    parser = argparse.ArgumentParser(description='Program to assess comments and lines of code in a program file.')
    parser.add_argument('-f', '--file', required=True, help='Pass in a file path relative to main.py')
    return parser.parse_args()


# runs basic checks on passed in file, and determines the type of file we are working with
def sanity():
    if args is None or args.file is None:
        print('No file passed in, please try again.\nProgram complete.')
        sys.exit(0)
    if not os.path.exists(args.file):
        print('No such file exists, please try again with the correct path.\nProgram complete.')
        sys.exit(0)
    if not os.path.isfile(args.file):
        print('Path indicated is not a file, please try again with a program file.\nProgram complete.')
        sys.exit(0)
    # Ignore files starting with a .
    if args.file.startswith('.'):
        print('File passed in starts with a \'.\', ignoring...\nProgram complete.')
        sys.exit(0)
    # Ignore files without an extension
    if len(args.file.split('.')) != 2:
        print('File passed in does not have an extension, ignoring...\nProgram complete.')
        sys.exit(0)

    # At this point, we've ensured that the user has passed in a valid program file - now we have to find the extension
    global FILE_TYPE
    FILE_TYPE = '.{}'.format(args.file.split('.')[1])
    global SUPPORTED_FILE_TYPES
    if SUPPORTED_FILE_TYPES.get(FILE_TYPE, -1) == -1:
        print('File extension not supported. Please use one of the following:\n{}'.format(
            str(SUPPORTED_FILE_TYPES.keys()).replace('dict_keys', ''))
        )
        sys.exit(0)
    # Extension found, now let's parse...


if __name__ == '__main__':
    args = parse_input()
    sanity()
    start()
