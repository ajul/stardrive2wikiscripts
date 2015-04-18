from sd2wiki.techs import buildings

result = '{|class = "wikitable sortable"\n'
result += '! Icon !! Building !! Description !! Requires technology !! Cost !! Maintenance \n'

for buildingUID in sorted(buildings):
    building = buildings[buildingUID]
    result += '|-\n'
    result += '| [[File:%s.png]] || %s || %s ' % (
        building.uid,
        building.name,
        building.desc,
        )
    if building.tech:
        result += '|| [[Technology#%s|%s %s: %s]] ' % (
        building.tech.uid,
        building.tech.category,
        building.tech.level,
        building.tech.name,
        )
    else:
        result += '|| (none) '
        
    result += '|| %d || %d \n' % (
        building.cost,
        building.maintenance,
        )
    
result += '|}\n'

print(result)
