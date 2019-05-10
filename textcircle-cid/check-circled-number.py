"""Check circled numbers for fonts in TeX Live.

Usage: (python ./check-circled-number.py 3>&2 2>&1 1>&3) >result.log
"""

from __future__ import print_function

import itertools
import operator
import sys

import fontforge as ff

with open("texlive-fonts.txt") as fonts_file:
    FONT_LIST = [i[:-1] for i in fonts_file.readlines()]

CIRCLED_NUMBER_DICT = {
    "Circled":       [0x24EA, 0x2460, 0x2461, 0x2462, 0x2463, 0x2464, 0x2465, 0x2466, 0x2467, 0x2468, 0x2469, 0x246A, 0x246B, 0x246C, 0x246D, 0x246E, 0x246F, 0x2470, 0x2471, 0x2472, 0x2473, 0x3251, 0x3252, 0x3253, 0x3254, 0x3255, 0x3256, 0x3257, 0x3258, 0x3259, 0x325A, 0x325B, 0x325C, 0x325D, 0x325E, 0x325F, 0x32B1, 0x32B2, 0x32B3, 0x32B4, 0x32B5, 0x32B6, 0x32B7, 0x32B8, 0x32B9, 0x32BA, 0x32BB, 0x32BC, 0x32BD, 0x32BE, 0x32BF],
    "Inversed":      [0x24FF, 0x2776, 0x2777, 0x2778, 0x2779, 0x277A, 0x277B, 0x277C, 0x277D, 0x277E, 0x277F, 0x24EB, 0x24EC, 0x24ED, 0x24EE, 0x24EF, 0x24F0, 0x24F1, 0x24F2, 0x24F3, 0x24F4],
    "Sans":          [0x1F10B, 0x2780, 0x2781, 0x2782, 0x2783, 0x2784, 0x2785, 0x2786, 0x2787, 0x2788, 0x2789],
    "Sans-inversed": [0x1F10C, 0x278A, 0x278B, 0x278C, 0x278D, 0x278E, 0x278F, 0x2790, 0x2791, 0x2792, 0x2793]
}
TOOLBAR_WIDTH = 40

def check_circled_numbers(font_path):
    sys.stderr.write("==> " + font_path + "\n")
    font = ff.open(font_path)
    font_name = font.fontname
    result = {}
    for number_type, usv_list in CIRCLED_NUMBER_DICT.items():
        number_list = [i for i, usv in enumerate(usv_list) if usv in font]
        result[number_type] = ", ".join(list_to_segments(number_list))
    font.close()
    return font_name, result

def list_to_segments(_list):
    ranges = []
    for key, group in itertools.groupby(enumerate(_list), lambda (index, item): index - item):
        group = map(operator.itemgetter(1), group)
        if len(group) > 1:
            ranges.append(str(group[0]) + "-" + str(group[-1]))
        else:
            ranges.append(str(group[0]))
    return ranges

def _main():
    result = []
    for i, font_path in enumerate(FONT_LIST):
        sys.stdout.write('\r')
        sys.stdout.write("{0:.0%}".format((i + 1.0) / len(FONT_LIST)))
        sys.stdout.flush()
        font_name, circled_numbers = check_circled_numbers(font_path)
        if "".join(circled_numbers.values()) != "":
            result.append((font_name, circled_numbers))
    sys.stdout.write("\n")
    sys.stderr.write("\n")

    for i in result:
        sys.stderr.write(str(i) + "\n")

if __name__ == "__main__":
    _main()
