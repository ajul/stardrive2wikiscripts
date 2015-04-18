from sd2wiki.config import *
from sd2wiki.core import *
from sd2wiki.loc import getLoc
from sd2wiki.buildings import buildings
import csv, re, os

techs = {}

class TechOption():
    def __init__(self, type, uid, tech):
        self.uid = uid
        self.tech = tech
        self.name = getLoc(type, uid, 'name')
        self.reference = None # todo

class Tech():
    def __init__(self, uid, cost,
            advanceOptions, buildingOptions, moduleOptions, skillOptions,
            skills, advance1Instruction, advance1Value, advance2Instruction, advance2Value):
        uid = uid.strip()
        self.uid = uid
        self.cost = int(cost)
        self.options = []
        self.name = getLoc(uid) or uid.split('_')[0]
        self.level = uid.split('_')[-1]
        self.category = uid.split('_')[-2]
        
        for buildingUID in re.split(',', buildingOptions):
            buildingUID = buildingUID.strip()
            if buildingUID == '': continue
            techOption = TechOption('Building', buildingUID, self)
            buildings[buildingUID].tech = self

techFile = open(os.path.join(basedir, 'Techs', 'TechTree.txt'))

for building in buildings.values():
    building.tech = None

for line in csv.reader(techFile, csv.excel_tab):
    uid = line[0].strip()
    if uid == '': continue
    techs[uid] = Tech(*line)
    
techFile.close()

