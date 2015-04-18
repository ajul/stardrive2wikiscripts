from core import *
import loc

class Building():
    def __init__(self, node):
        self.uid = node.findtext('UID')
        self.cost = int(node.findtext('Cost', '0'))
        self.maintenance = int(node.findtext('Maintenance', '0'))
        self.name = loc.getLoc('Building', self.uid, 'name')
        self.desc = loc.getLoc('Building', self.uid, 'desc')
        self.details = loc.getLoc('Building', self.uid, 'details')
        # todo: parse stats directly

buildings = {}

buildingFile = ElementTree.parse(os.path.join(basedir, 'Buildings', 'Buildings.xml'))

for buildingData in buildingFile.find('Buildings').findall('Building'):
    uid = buildingData.get('UID')
    buildings[uid] = Building(buildingData)

    
