from sd2wiki.config import *

import csv, re

encoding = 'utf_16_le'

locFile = open(os.path.join(basedir, 'Misc', 'LocKit.txt'), encoding=encoding)

loc = {}

for line in csv.reader(locFile, csv.excel_tab):
    key = line[0]
    if key == '': continue
    loc[key] = line[1]

locFile.close()

def getLoc(*args):
    key = '_'.join(args)
    return loc[key]
