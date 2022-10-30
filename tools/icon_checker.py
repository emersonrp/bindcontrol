#!/usr/bin/env python3
import os
import re
import sys
import inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

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
for filename in [f for f in os.listdir(f"{parentdir}/icons/Powers/") if f.endswith('png')]:
    filecheck.add(os.path.basename(filename))
for filename in [f for f in os.listdir(f"{parentdir}/icons/Incarnate/") if f.endswith('png')]:
    filecheck.add(os.path.basename(filename))
for filename in [f for f in os.listdir(f"{parentdir}/icons/Inspirations/") if f.endswith('png')]:
    filecheck.add(os.path.basename(filename))

# Archetype Primary and Secondary
for archname, archdata in GameData.Archetypes.items():
    for category in ['Primary', 'Secondary', 'Epic']:
        for powerset, powers in archdata[category].items():
            powerset = re.sub(r'\W+', '', powerset)
            for power in sorted(powers):
                power = re.sub(r'\W+', '', power)
                filename = f"{powerset}_{power}.png"
                if not os.path.exists(f"{parentdir}/icons/Powers/{filename}"):
                    print(f"{archname}: {filename}")
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
            print(f"Pool Power: {filename}")
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
                print(f"Incarnate: {filename}")
                count = count + 1
            else:
                if filename in filecheck: filecheck.remove(filename)

# Inspirations
for type, data in GameData.Inspirations.items():
    for insp in data['tiers']:
        insp = re.sub(r'\W+', '',  insp)
        filename = f"{insp}.png"
        if not os.path.exists(f"{parentdir}/icons/Inspirations/{filename}"):
            print(f"Inspirations: {filename}")
            count = count + 1
        else:
            if filename in filecheck: filecheck.remove(filename)



## TODO - turn all of this into a proper test without "print" all over it
if count: print(f"Total of {count} missing icons")

if filecheck:
    for fn in sorted(filecheck):
        print(f"Extra icon file: {fn}")
    print(f"Total of {len(filecheck)} extra icons")

