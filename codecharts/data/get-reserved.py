import csv
import os
import sys

UNICODE_DATA_FILE_PATH   = os.sep.join([os.getcwd(), 'UnicodeData.txt'])
UNICODE_BLOCKS_FILE_PATH = os.sep.join([os.getcwd(), 'Blocks.txt'])

CJK_BLOCKS = {
    0x3400,   # CJK Unified Ideographs Extension A
    0x4E00,   # CJK Unified Ideographs
    0xAC00,   # Hangul Syllables
    0xD800,   # High Surrogates
    0xDB80,   # High Private Use Surrogates
    0xDC00,   # Low Surrogates
    0xE000,   # Private Use Area
    0x17000,  # Tangut
    0x18D00,  # Tangut Ideograph Supplement
    0x20000,  # CJK Unified Ideographs Extension B
    0x2A700,  # CJK Unified Ideographs Extension C
    0x2B740,  # CJK Unified Ideographs Extension D
    0x2B820,  # CJK Unified Ideographs Extension E
    0x2CEB0,  # CJK Unified Ideographs Extension F
    0x30000,  # CJK Unified Ideographs Extension G
}

with open(UNICODE_DATA_FILE_PATH) as unicode_data_file:
    reader = csv.reader(unicode_data_file, delimiter=';')
    code_point = [int(row[0], 16) for row in reader]

with open(UNICODE_BLOCKS_FILE_PATH) as unicode_blocks_file:
    reader = csv.reader(unicode_blocks_file, delimiter=';')
    blocks = [row for row in reader][34:-2]
    blocks = [(row[1][1:], tuple(int(i, 16) for i in row[0].split('..'))) for row in blocks]

code_point_diff = [(i + 1, j - i - 1) for i, j in zip(code_point[:-1], code_point[1:])
                   if j - i != 1 and j <= 0x3FFFF]

def to_usv(x):
    return '"' + hex(x)[2:].upper()

def find_reserved_in_block(block_start, block_end):
    _reserved = []
    if block_start in CJK_BLOCKS:
        return _reserved
    for i in code_point_diff:
        if i[0] > block_end:
            return _reserved
        if i[0] >= block_start:
            if i[1] == 1:
                _reserved.append(_item(i[0], i[0]))
            else:
                _reserved.append(_item(i[0], min(i[0] + i[1] - 1, block_end)))
        if i[0] < block_start and i[0] + i[1] > block_start:
            _reserved.append(_item(block_start, i[0] + i[1] - 1))
    return _reserved

def _item(a, b):
    return f'{{{to_usv(a)}}} {{{to_usv(b)}}}'

reserved = [(i[0], find_reserved_in_block(*i[1])) for i in blocks]
reserved = [(i[0].replace(' ', '~'), ', '.join(i[1])) for i in reserved if i[1]]

max_block_name_len = max([len(i[0]) for i in reserved])

for i in reserved:
    print(f'    {i[0]:<{max_block_name_len}} = {{ {i[1]} }},')
