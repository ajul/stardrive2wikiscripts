import xml.etree.ElementTree as ElementTree
from core import *
import re, os

races = []
hulls = []
hullRaces = {}
hullClasses = {}
hullStats = {}

sectionNames = ('Slots_Fore', 'Slots_Aft', 'Slots_Center', 'Slots_Port', 'Slots_Starboard')

shipDefinitions = ElementTree.parse(os.path.join(basedir, 'Misc', 'ShipDefinitions.xml'))
for shipDefinition in shipDefinitions.find('Definitions').findall('ShipDefinition'):
    raceName = shipDefinition.find('RaceName').text
    races.append(raceName)
    for shipDef in shipDefinition.find('ShipList').findall('ShipDef'):
        hull = shipDef.find('ResourceName').text
        hulls.append(hull)
        hullRaces[hull] = raceName
        hullClasses[hull] = shipDef.find('ShipClass').text

def processDesignDir(dirname):
    global hullStats
    for filename, data in iterDirXML(os.path.join(basedir, dirname)):
        hull = data.find('Hull').text
        if hull in hullStats: continue # already done
        hullStats[hull] = [sum(1 for x in data.find(sectionName).findall('SaveableModuleData')) for sectionName in sectionNames]

processDesignDir('Designs')
processDesignDir('Designs_AI')

result = '{|class = "wikitable sortable"\n'
result += '! Hull \n'
result += '! Race \n'
result += '! Class \n'

for sectionName in sectionNames:
    result += '! %s \n' % sectionName

result += '! Total Slots \n'

for hull in hulls:
    if hull not in hullStats:
        print('No stats found for hull %s.' % hull)
        continue
    result += '|-\n'
    result += '| %s \n' % hull
    result += '| %s \n' % hullRaces[hull]
    result += '| %s \n' % hullClasses[hull]

    for i, _ in enumerate(sectionNames):
        result += '| %d \n' % hullStats[hull][i]

    result += '| %d \n' % sum(hullStats[hull])

result += '|}\n'

print(result)
    
