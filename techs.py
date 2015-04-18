from core import *
from loc import *
import csv, re

def getOptions(src, prefix):
    for option in re.split(',\s*', src):
        if option == '': return
        optionName = getLoc(prefix, advanceOption, 'name')
        optionDetails = getLoc(prefix, advanceOption, 'details')
        yield '%s: %s' % (optionName, optionDetails)
        
f = open(os.path.join(basedir, 'Techs', 'TechTree.txt'))

result = ''

for line in csv.reader(f, csv.excel_tab):
    advanceData = [['', ''], ['', '']]
    (techID, cost,
     advanceOptions, buildingOptions, moduleOptions, skillOptions,
     skills, advanceData[0][0], advanceData[0][1], advanceData[1][0], advanceData[1][1]) = line
    if techID == '': continue
    techCategory, techLevel = techID.split('_', 1)
    options = []
    # advances
    for advanceOption in re.split(',\s*', advanceOptions):
        if advanceOption == '': break
        advanceName = getLoc('Advance', advanceOption, 'name')
        advanceDetails = getLoc('Advance', advanceOption, 'details')
        option = '%s: %s' % (advanceName, advanceDetails)
        options.append(option)
    # buildings
    for buildingOption in re.split(',\s*', buildingOptions):
        if buildingOption == '': break
        option = '%s: building' % buildingOption
        options.append(option)
    # modules
    for moduleOption in re.split(',\s*', moduleOptions):
        if moduleOption == '': break
        option = '%s: module' % moduleOption
        options.append(option)
    # skills
    for skillOption in re.split(',\s*', skillOptions):
        if skillOptions == '': break
        option = '%s: skill' % skillOption
        options.append(option)
    result += '|-\n'
    result += '| %s || ? || %s ' % (techLevel, cost)
    for i in range(3):
        if i < len(options):
            result += '|| %s ' % options[i]
        else:
            result += '|| '
    result += '\n'

f.close()

print(result)
