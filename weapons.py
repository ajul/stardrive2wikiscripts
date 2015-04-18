import xml.etree.ElementTree as ElementTree
from core import *
import re, os

weaponSets = {}

weapons = {}

weaponHeaders = [

    ]

# get the human-readable name of each module set
moduleSetNames = {}

marketTree = ElementTree.parse(os.path.join(basedir, 'MarketTrees', 'Weapons.xml'))
for techEntry in marketTree.find('TechTree').findall('TechEntry'):
    name = techEntry.find('DisplayName').text
    for moduleSetID in techEntry.find('ModuleSetsProvided').findall('string'):
        moduleSetNames[moduleSetID.text] = name

# get the human-readable name of each weapon
moduleBaseNames = {}

for filename, moduleSet in iterDirXML(os.path.join(basedir, 'Modules', 'Module Sets')):
    if moduleSet.find('ModuleType').text != 'WeaponModule': continue
    moduleSetID, _ = os.path.splitext(filename)
    if moduleSetID not in moduleSetNames: continue
    for moduleID in moduleSet.find('ModulesInSet').findall('string'):
        moduleBaseNames[moduleID.text] = moduleSetNames[moduleSetID]

def getValue(module, key, constructor, default):
    valueNode = module.find(key)
    if valueNode is None: value = default
    else: value = constructor(valueNode.text)
    return value

def getPowPerShot(filename, module):
    duration = module.find('BeamDuration')
    if duration is None:
        duration = 0.0
    else:
        duration = float(duration.text)
    powPerShot = float(module.find('PowPerShot').text)
    return (1.0 + duration) * powPerShot

def getMaximumDamage(filename, module):
    if module.find('DamageGraph') is None: return None
    duration = module.find('BeamDuration')
    if duration is None:
        duration = 1.0
    else:
        duration = float(duration.text)
    damage = max(int(x.find('Damage').text) for x in module.find('DamageGraph').findall('DamagePlot'))
    return damage * duration

def getMaximumRange(filename, module):
    if module.find('DamageGraph') is None: return None
    return max(int(x.find('Range').text) for x in module.find('DamageGraph').findall('DamagePlot'))

def getName(filename, module):
    moduleID, _ = os.path.splitext(filename)
    if moduleID not in moduleBaseNames: return None
    baseName = moduleBaseNames[moduleID]
    return '%s, %s' % (baseName, module.find('variantName').text)

def getVariants(filename, module):
    variants = []
    for element in module.iter():
        m = re.match('V_(.*)', element.tag)
        if m is not None and element.text == 'true':
            variants.append(m.group(1))
    return ', '.join(variants)

def getDPS(filename, module):
    damage = getMaximumDamage(filename, module)
    fireRate = getValue(module, 'ShotsPerSecondBase', float, 1.0)
    salvo = getValue(module, 'SalvoCount', int, 1)
    return damage * fireRate * salvo

def getDPSPerCost(filename, module):
    dps = getDPS(filename, module)
    cost = getValue(module, 'Cost', int, 0)
    return dps / cost

def getDPSPerSize(filename, module):
    dps = getDPS(filename, module)
    x = getValue(module, 'XSIZE', int, 1)
    y = getValue(module, 'YSIZE', int, 1)
    return dps / x / y

moduleHeaders = [
    ('Name', getName),
    ('X', 'XSIZE', int, 1),
    ('Y', 'YSIZE', int, 1),
    ('Cost', 'Cost', int, 0),
    ('Mass', 'Mass', int, 0),
    # ('HP', 'HealthMax', int),
    ('Power', 'PowerDraw', int, 0),
    ('Ord Per Shot', 'OrdPerShot', float, 0.0),
    ('Pow Per Shot', getPowPerShot),
    # ('Projectile HP', 'ProjectileHitPoints', int),
    # ('Explosion Radius', 'ExplosionRadius', int),
    ('Rate of Fire', 'ShotsPerSecondBase', float, 1.0),
    ('Salvo', 'SalvoCount', int, 1),
    ('Damage', getMaximumDamage),
    ('Range', getMaximumRange),
    ('DPS', getDPS),
    ('DPS/Cost', getDPSPerCost),
    ('DPS/Size', getDPSPerSize),
    ('Variants', getVariants),
    ]

result = '{|class = "wikitable sortable"\n'
for header in moduleHeaders:
    result += '! %s \n' % header[0]

for filename, module in iterDirXML(os.path.join(basedir, 'Modules', 'Module Headers')):
    if getName(filename, module) is None: continue

    result += '|-\n'
    for header in moduleHeaders:
        if len(header) == 4:
            value = getValue(module, header[1], header[2], header[3])
        elif len(header) == 2:
            value = header[1](filename, module)
        result += '| %s \n' % value
    
result += '|}\n'

print(result)
