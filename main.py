import sys
import re

# Declare Global Vasriables
CRITERIA = {
    'total_lines': 0,
    'total_comments': 0,
    'total_single_line_comments': 0,
    'total_block_line_comments': 0,
    'total_blocks': 0,
    'total_todo': 0
}
# dictionary where keys are extensions, and values are list of comment syntax
# first value in list is single line comment, second is start of block, third is end of block
SUPPORTED_FILE_TYPES = {
    '.py': ['#', '\'\'\'', '\'\'\''],
    '.java': ['//', '/*', '*/'],
    '.js': ['//', '/*', '*/'],
}


def start():
    pass


if __name__ == '__main__':
    start()
