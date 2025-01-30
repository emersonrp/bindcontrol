#!/usr/bin/env python3
import os
import re
import sys
import inspect


currframe = inspect.currentframe()
if currframe:
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(currframe)))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)
else:
    exit()

import GameData

# from UI/IncarnateBox - TODO - put this in GameData or somewhere?
Aliases = {
    "Banished Pantheon"   : "Banished",
    "Carnival of Shadows" : "Carnival",
    "Cimerorans"          : "Cimeroran",
    "Knives of Vengeance" : "Knives",
    "Phantom"             : "Phantoms",
    "Polar Lights"        : "Lights",
    "Robotic Drones"      : "Drones",
    "Storm Elementals"    : "Elementals",
    "Talons of Vengeance" : "Talons",
    "Warworks"            : "WarWorks",
}

count = 0
filecheck = set()
for filename in [f for f in os.listdir(f"{parentdir}/icons/Archetypes/") if f.endswith('png')]:
    filecheck.add(os.path.basename(filename))
for filename in [f for f in os.listdir(f"{parentdir}/icons/Origins/") if f.endswith('png')]:
    filecheck.add(os.path.basename(filename))
for filename in [f for f in os.listdir(f"{parentdir}/icons/Powers/") if f.endswith('png')]:
    filecheck.add(os.path.basename(filename))
for filename in [f for f in os.listdir(f"{parentdir}/icons/Incarnate/") if f.endswith('png')]:
    filecheck.add(os.path.basename(filename))
for filename in [f for f in os.listdir(f"{parentdir}/icons/Inspirations/") if f.endswith('png')]:
    filecheck.add(os.path.basename(filename))

for server in ('Homecoming', 'Rebirth'):
    GameData.SetupGameData(server)

    # Archetype, Primary, and Secondary
    for archname, archdata in GameData.Archetypes.items():
        archfn = f"{archname}.png"
        if not os.path.exists(f"{parentdir}/icons/Archetypes/{archfn}"):
            print(f"{archfn}")
            count = count + 1
        else:
            if archfn in filecheck: filecheck.remove(archfn)

        for category in ['Primary', 'Secondary', 'Epic']:
            for powerset, powers in archdata[category].items():
                powerset = re.sub(r'\W+', '', powerset)
                for power in sorted(powers):
                    power = re.sub(r'\W+', '', power)
                    filename = f"{powerset}_{power}.png"
                    if not os.path.exists(f"{parentdir}/icons/Powers/{filename}"):
                        print(f"{server} {archname}: {filename}")
                        count = count + 1
                    else:
                        if filename in filecheck: filecheck.remove(filename)

    # Origins
    for origin in GameData.Origins:
        filename = f"{origin}.png"
        if not os.path.exists(f"{parentdir}/icons/Origins/{filename}"):
            print(f"{server} Origin: {filename}")
            count = count + 1
        else:
            if filename in filecheck: filecheck.remove(filename)

    # Pool Powers
    for poolname, pool in GameData.MiscPowers['Pool'].items():
        for power in pool:

            power = re.sub(r'\W+', '', power)
            poolname = re.sub(r'\W+', '', poolname)
            filename = f"{poolname}_{power}.png"
            if not os.path.exists(f"{parentdir}/icons/Powers/{filename}"):
                print(f"{server} Pool Power: {filename}")
                count = count + 1
            else:
                if filename in filecheck: filecheck.remove(filename)

    # Incarnate Powers
    for slot, slotdata in GameData.MiscPowers['Incarnate'].items():
        for type in slotdata['Types']:
            aliasedtype = Aliases.get(type, type)
            for rarity in ['Common', 'Uncommon', 'Rare', 'VeryRare']:
                filename = f"Incarnate_{slot}_{aliasedtype}_{rarity}.png"
                if not os.path.exists(f"{parentdir}/icons/Incarnate/{filename}"):
                    print(f"{server} Incarnate: {filename}")
                    count = count + 1
                else:
                    if filename in filecheck: filecheck.remove(filename)

    # Misc Powers
    # TODO generalize this more?
    miscpowerlist = GameData.MiscPowers['Badge']['Accolade'] + GameData.MiscPowers['General']['Inherent'] + GameData.MiscPowers['General']['SMART']
    for power in miscpowerlist:
        power = re.sub(r'\W+', '', power)
        filename = f"Misc_{power}.png"
        if not os.path.exists(f"{parentdir}/icons/Powers/{filename}"):
            print(f"{server} Misc Power: {filename}")
            count = count + 1
        else:
            if filename in filecheck: filecheck.remove(filename)

    # Inspirations
    for _, type in GameData.Inspirations.items():
        for _, data in type.items():
            for insp in data['tiers']:
                insp = re.sub(r'\W+', '',  insp)
                filename = f"{insp}.png"
                if not os.path.exists(f"{parentdir}/icons/Inspirations/{filename}"):
                    print(f"{server} Inspirations: {filename}")
                    count = count + 1
                else:
                    if filename in filecheck: filecheck.remove(filename)



## TODO - turn all of this into a proper test without "print" all over it
if count: print(f"Total of {count} missing icons")

if filecheck:
    for fn in sorted(filecheck):
        print(f"Extra icon file: {fn}")
    print(f"Total of {len(filecheck)} extra icons")

if not (count or filecheck):
    print("Icons are as expected.")
