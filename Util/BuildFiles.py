import re
from pathlib import Path
import GameData

def ParseBuildFile(file:Path):
    if buildtext := file.read_text():
        lines = buildtext.splitlines()

        firstline = lines[0]

        if parts := re.match(r'(.*?): Level \d+ (\w+) Class_(\w+)', firstline):
            name      = parts.group(1)
            origin    = parts.group(2)
            archetype = parts.group(3)
        else:
            return None

        data = {
            'Name' : name,
            'Origin' : origin,
            'Archetype' : archetype,
            'Server' : 'Homecoming', # Rebirth doesn't have /build_save I think
        }

        Pools = []
        Archetypes = list(GameData.Archetypes)

        for line in lines:
            if match := re.match(r'Level \d+: (\w+) (\w+)', line):
                powersettype = PSMap[match.group(1)]
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
                    if word in Archetypes:
                        powersetwords.remove(word)
                powerset = ' '.join(powersetwords)
                data[powersettype] = powerset

                # TODO TODO TODO - some Epic powersets, at least, have diffeent names
                # than are in the picker.  Grarr, for instance, has Body_Mastery_Stalker
                # but there is no "Body Mastery" in the Stalker Epic / Patron power pool.
                # Ugh.

            else:
                continue

        for i, pool in enumerate(Pools, start = 1):
            data['Pool'+str(i)] = pool

        return data


PSMap = {
    'Epic'      : 'Epic',
    'Inherent'  : 'Inherent',
    'Pool'      : 'Pool',
    'Redirects' : None,

# TODO - get these for all archetypes
    'Mastermind_Summon': 'Primary',
    'Mastermind_Buff'  : 'Secondary',
    'Peacebringer_Offensive' : 'Primary',
    'Peacebringer_Defensive' : 'Secondary',
    'Stalker_Melee' : 'Primary',
    'Stalker_Defense' : 'Secondary',
    'Tanker_Defense' : 'Primary',
    'Tanker_Melee' : 'Secondary',
}
