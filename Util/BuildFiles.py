import re
from pathlib import Path
import GameData

def ParseBuildFile(file:Path) -> dict:
    GameData.SetupGameData('Homecoming') # The whole notion of build_save is Homecoming-specific
    if buildtext := file.read_text():
        lines = buildtext.splitlines()

        firstline = lines[0]

        if parts := re.match(r'(.*?): Level \d+ (\w+) Class_(\w+)', firstline):
            name      = parts.group(1)
            origin    = parts.group(2)
            archetype = parts.group(3)
            archetype = re.sub(r'_', ' ', archetype)
        else:
            return {}

        data = {
            'Name'      : name,
            'Origin'    : origin,
            'Archetype' : archetype,
            'Server'    : 'Homecoming', # Rebirth doesn't have /build_save I think
        }

        Pools = []

        for line in lines:
            if match := re.match(r'Level \d+: (\w+) (\w+)', line):
                powersettype = PSTypeMap[match.group(1)]
                powerset     = match.group(2)

                if not powersettype: continue
                if powersettype == 'Inherent': continue
                if powersettype == 'Pool':
                    if not powerset in Pools:
                        Pools.append(powerset)
                    continue

                powerset = re.sub(r'_', ' ', powerset)
                powersetwords = re.split(r'\s+', powerset)
                for word in list(powersetwords): # make a new list since we modify the existing one as we go
                    if word in GameData.Archetypes:
                        powersetwords.remove(word)
                powerset = ' '.join(powersetwords)
                powerset = PowerSetMap.get(powerset, powerset)
                data[powersettype] = powerset

            else:
                continue

        for i, pool in enumerate(Pools, start = 1):
            data['Pool'+str(i)] = pool

        return data
    else:
        return {}

PSTypeMap = {
    'Epic'      : 'Epic',
    'Inherent'  : 'Inherent',
    'Pool'      : 'Pool',
    'Redirects' : None,

    'Arachnos_Soldiers'      : 'Primary',
    'Training_Gadgets'       : 'Secondary',
    'Widow_Training'         : 'Primary',
    'Teamwork'               : 'Secondary',
    'Blaster_Ranged'         : 'Primary',
    'Blaster_Support'        : 'Secondary',
    'Brute_Melee'            : 'Primary',
    'Brute_Defense'          : 'Secondary',
    'Controller_Control'     : 'Primary',
    'Controller_Buff'        : 'Secondary',
    'Corruptor_Ranged'       : 'Primary',
    'Corruptor_Buff'         : 'Secondary',
    'Defender_Buff'          : 'Primary',
    'Defender_Ranged'        : 'Secondary',
    'Dominator_Control'      : 'Primary',
    'Dominator_Assault'      : 'Secondary',
    'Mastermind_Summon'      : 'Primary',
    'Mastermind_Buff'        : 'Secondary',
    'Peacebringer_Offensive' : 'Primary',
    'Peacebringer_Defensive' : 'Secondary',
    'Scrapper_Melee'         : 'Primary',
    'Scrapper_Defense'       : 'Secondary',
    'Sentinel_Ranged'        : 'Primary',
    'Sentinet_Defense'       : 'Secondary',
    'Stalker_Melee'          : 'Primary',
    'Stalker_Defense'        : 'Secondary',
    'Tanker_Defense'         : 'Primary',
    'Tanker_Melee'           : 'Secondary',
    'Warshade_Offensive'     : 'Primary',
    'Warshade_Defensive'     : 'Secondary',
}

# Some powersets got renamed but the original "Body_Mastery_Stalker
# etc names remain in the export and in Mids.
PowerSetMap = {
    "Flame Mastery"         : "Fire Mastery",
    "Heat Mastery"          : "Fire Mastery",
    "Pyre Mastery"          : "Fire Mastery",
    "Blaze Mastery"         : "Fire Mastery",
    "Darkness Mastery"      : "Dark Mastery",
    "Stone Mastery"         : "Earth Mastery",
    "Electrical Mastery"    : "Electricity Mastery",
    "Charge Mastery"        : "Electricity Mastery",
    "Primal Forces Mastery" : "Energy Mastery",
    "Power Mastery"         : "Energy Mastery",
    "Body Mastery"          : "Energy Mastery",
    "Cold Mastery"          : "Ice Mastery",
    "Chill Mastery"         : "Ice Mastery",
    "Arctic Mastery"        : "Ice Mastery",
    "Psychic Mastery"       : "Psionic Mastery",
    "Ninja Tool Mastery"    : "Weapon Mastery",
    "Munitions Mastery"     : "Arsenal Mastery",
}
