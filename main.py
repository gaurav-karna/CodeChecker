
# AUTHOR - Gaurav K. Karna | Copyright Gaurav K. Karna 2019

import sys
import os.path
import argparse

# Declare Global Variables

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
SLASHES = ['//', '/*', '*/', ['"']]

# dictionary where keys are extensions, and values are list of comment syntax for the different languages
# first value in list is single line comment, second is start of block, third is end of block
# the fourth value is a list of the ways in which the language supports Strings
SUPPORTED_FILE_TYPES = {
    '.py': ['#', '\'\'\'', '\'\'\'', ['\'', '"']],
    '.java': SLASHES,
    '.js': ['//', '/*', '*/', ['\'', '"']],
    '.c': SLASHES,
    '.cpp': SLASHES,
    ',go': SLASHES,
    '.cs': SLASHES,
    '.ts': ['//', '/*', '*/', ['\'', '"']],
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
            if is_code_with_comment(line):
                CRITERIA['total_comments'] += 1
                continue
    result()


# checks if the string is a line of code with a trailing comment
def is_code_with_comment(s):
    global SUPPORTED_FILE_TYPES
    global FILE_TYPE
    global CRITERIA
    # major caveat is to ensure the comment syntax is not within a string or similar escape characters
    in_str = False
    escaped = False     # True if the previous character was an escape character
    first_slash = False     # True if current character is a slash - useful for determining comments with SLASHES
    py_multi_count = 0      # Counts number of ' encountered previously
    for count, current_char in enumerate(s):
        if escaped:             # previous escape character means we can disregard the current character
            escaped = False
            continue
        if not in_str:
            if current_char == '\\':        # escape character encountered
                escaped = True
                continue
            if current_char in SUPPORTED_FILE_TYPES[FILE_TYPE][3]:      # character is starting a string
                in_str = True
                continue
            if current_char == SUPPORTED_FILE_TYPES[FILE_TYPE][0][0]:      # checks if character is == to '#' or '/'
                if current_char == '/':
                    if not first_slash:
                        first_slash = True
                        continue
                    else:                   # first slash encountered + second slash encountered = single comment!
                        CRITERIA['total_single_line_comments'] += 1
                        if is_todo(s[count:]):  # passing rest of comment to check TODO
                            CRITERIA['total_todo'] += 1
                        return True
                elif current_char == '*' and first_slash:  # first slash encountered + asterisk = multi-block comment!
                    CRITERIA['total_block_line_comments'] += 1
                    CRITERIA['total_blocks'] += 1
                    if is_todo(s[count:]):  # passing rest of comment to check TODO
                        CRITERIA['total_todo'] += 1
                    global BLOCK_FLAG
                    BLOCK_FLAG = True  # end of block comment handled in start()
                    return True
                elif current_char == '#':
                    first_slash = False     # not a SLASH comment, likely Python single line comment
                    CRITERIA['total_single_line_comments'] += 1
                    if is_todo(s[count:]):                                  # passing rest of comment to check TODO
                        CRITERIA['total_todo'] += 1
                    return True
            # if current_char == SUPPORTED_FILE_TYPES[FILE_TYPE][1]:      # start of block comment after code
            #     CRITERIA['total_block_line_comments'] += 1
            #     CRITERIA['total_blocks'] += 1
            #     if is_todo(s[count:]):                                  # passing rest of comment to check TODO
            #         CRITERIA['total_todo'] += 1
            #     global BLOCK_FLAG
            #     BLOCK_FLAG = True                                       # end of block comment handled in start()
            #     return True
        else:
            if current_char in SUPPORTED_FILE_TYPES[FILE_TYPE][3] and not escaped:
                in_str = False
    return False


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


def result():
    global CRITERIA
    print('Finished parsing {}:'.format(args.file))
    print('Total # of lines: {}'.format(CRITERIA['total_lines']))
    print('Total # of comment lines: {}'.format(CRITERIA['total_comments']))
    print('Total # of single line comments: {}'.format(CRITERIA['total_single_line_comments']))
    print('Total # of comment lines within block comments: {}'.format(CRITERIA['total_block_line_comments']))
    print('Total # of block line comments: {}'.format(CRITERIA['total_blocks']))
    print('Total # of TODOs: {}'.format(CRITERIA['total_todo']))


if __name__ == '__main__':
    args = parse_input()
    sanity()
    print(FILE_TYPE)
    start()
