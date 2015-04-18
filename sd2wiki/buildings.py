from sd2wiki.config import *
import sd2wiki.loc
import xml.etree.ElementTree as ElementTree
import os

class Building():
    def __init__(self, node):
        self.uid = node.findtext('UID')
        self.cost = int(node.findtext('Cost', '0'))
        self.maintenance = int(node.findtext('Maintenance', '0'))
        self.name = sd2wiki.loc.getLoc('Building', self.uid, 'name')
        self.desc = sd2wiki.loc.getLoc('Building', self.uid, 'desc')
        self.details = sd2wiki.loc.getLoc('Building', self.uid, 'details')
        # todo: parse stats directly

buildings = {}

buildingFile = ElementTree.parse(os.path.join(basedir, 'Buildings', 'Buildings.xml'))

for buildingData in buildingFile.find('Buildings').findall('Building'):
    uid = buildingData.findtext('UID')
    buildings[uid] = Building(buildingData)

    
