#!/usr/bin/env python

'''
colormake
---------

A script to color the output of make,
ripping-off colormake.pl by Bjarni R.
Einarsson, with some small changes and
improvements.

Daniel C. Jones <dcjones@cs.washington.edu>
2011.06.01.20.30

'''

import sys
import re

# Some useful color codes.

col_black =        '\033[30m'
col_red =          '\033[31m'
col_green =        '\033[32m'
col_yellow =       '\033[33m'
col_blue =         '\033[34m'
col_magenta =      '\033[35m'
col_cyan =         '\033[36m'
col_ltgray =       '\033[37m'

col_norm =	       '\033[00m'
col_background =   '\033[07m'
col_brighten =     '\033[01m'
col_underline =    '\033[04m'
col_blink = 	   '\033[05m'




# This script works simply by matching regular expressions and wrapping the
# matches in ANSI terminal codes. 'patterns' is an array of (pattern, prefix)
# pairs. If a pattern is matched, the prefix is inserted before the line.

# common patterns
filename_pat = r'[A-z0-9_\/\. ]+'
gcc_msg_pat  = filename_pat + r':( In |\d+:\d+:)'

patterns = [
        # make messages
        (r'^make\[\d+\]:',  col_cyan),
        (r'^Making all in', col_cyan + col_brighten),

        # make silent rules
        (r'^  (CC|CXX|CCLD|CXXLD)', col_norm + col_brighten),

        # gcc warnings, errors, etc
        (gcc_msg_pat + r' warning:', col_yellow),
        (gcc_msg_pat + r' error:',   col_red),
        (gcc_msg_pat,                col_yellow + col_brighten),

        # normal
        (r'', col_norm)]

patterns = [(re.compile(pat[0]),pat[1]) for pat in patterns]


def line_add_color(line):
    line_out = ''
    line = line.rstrip()
    for (pat, form) in patterns:
        if pat.match(line):
            line_out += form
            break

    line_out += line
    line_out += col_norm
    line_out += '\n'
    return line_out


if __name__ == '__main__':
    for line in iter(sys.stdin.readline, ''):
        line_color = line_add_color(line)
        sys.stdout.write(line_color)

