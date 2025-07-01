#!/usr/bin/env python3
import os
import re
import sys
import inspect
from pathlib import Path


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

def RecurseMiscPowers(menustruct):
    powerlist = []

    for data in menustruct.values():
        if isinstance(data, dict):
            plist = RecurseMiscPowers(data)
            powerlist.extend(plist)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, str):
                    powerlist.append(item)
                else:
                    plist = RecurseMiscPowers(item)
                    powerlist.extend(plist)

    return powerlist

def SplitNameAndIcon(namestr):
    if re.search(r'\|', namestr):
        name, iconstr = re.split(r'\|', namestr)
        iconlist = re.split(r'_', iconstr)
        return [name, iconlist]
    else:
        return [namestr, [namestr]]

count = 0
filecheck = set()
for filename in Path(f"{parentdir}/icons/Archetypes/").glob('**/*.png'):
    filecheck.add(filename)
for filename in Path(f"{parentdir}/icons/Origins/").glob('**/*.png'):
    filecheck.add(filename)
for filename in Path(f"{parentdir}/icons/Powers/").glob('**/*.png'):
    filecheck.add(filename)
for filename in Path(f"{parentdir}/icons/Incarnate/").glob('**/*.png'):
    filecheck.add(filename)
for filename in Path(f"{parentdir}/icons/Inspirations/").glob('**/*.png'):
    filecheck.add(filename)

icondir = Path(parentdir) / 'icons'

for server in ('Homecoming', 'Rebirth'):
    GameData.SetupGameData(server)

    # Archetype, Primary, and Secondary
    for archname, archdata in GameData.Archetypes.items():
        archname = re.sub(r'\W+', '', archname)
        archfn = icondir / 'Archetypes' / f"{archname}.png"
        if not archfn.exists():
            count = count + 1
        else:
            if archfn in filecheck: filecheck.remove(archfn)

        for category in ['Primary', 'Secondary', 'Epic']:
            for powerset, powers in archdata[category].items():
                powerset = re.sub(r'\W+', '', powerset)
                for power in powers:
                    if isinstance(power, dict):
                        [(power, items)] = power.items()
                        for p in items:
                            p = re.sub(r'\W+', '', p)
                            filename = icondir / 'Powers' / powerset / f"{p}.png"
                            if not filename.exists():
                                print(f"{server} {archname}: {filename}")
                                count = count + 1
                            else:
                                if filename in filecheck: filecheck.remove(filename)
                    power = re.sub(r'\W+', '', power)
                    filename = icondir / 'Powers' / powerset / f"{power}.png"
                    if not filename.exists():
                        print(f"{server} {archname}: {filename.relative_to(icondir)}")
                        count = count + 1
                    else:
                        if filename in filecheck: filecheck.remove(filename)

    # Origins
    for origin in GameData.Origins:
        filename = icondir / 'Origins' / f"{origin}.png"
        if not filename.exists():
            print(f"{server} Origin: {filename.relative_to(icondir)}")
            count = count + 1
        else:
            if filename in filecheck: filecheck.remove(filename)

    # Pool Powers
    for poolname, pool in GameData.PoolPowers.items():
        for power in pool:

            power = re.sub(r'\W+', '', power)
            poolname = re.sub(r'\W+', '', poolname)
            filename = icondir / 'Powers' / poolname / f"{power}.png"
            if not filename.exists():
                print(f"{server} Pool Power: {filename.relative_to(icondir)}")
                count = count + 1
            else:
                if filename in filecheck: filecheck.remove(filename)

    # Incarnate Powers
    for slot, slotdata in GameData.IncarnatePowers.items():
        for type in slotdata['Types']:
            aliasedtype = Aliases.get(type, type)
            for rarity in ['Common', 'Uncommon', 'Rare', 'VeryRare']:
                filename = icondir / 'Incarnate' / f"Incarnate_{slot}_{aliasedtype}_{rarity}.png"
                if not filename.exists():
                    print(f"{server} Incarnate: {filename.relative_to(icondir)}")
                    count = count + 1
                else:
                    if filename in filecheck: filecheck.remove(filename)

    # Misc Powers
    miscpowerlist = RecurseMiscPowers(GameData.MiscPowers)
    for power in miscpowerlist:
        power = re.sub(r'[^\w|]+', '', power)
        _, icon = SplitNameAndIcon(power)
        icon = '_'.join(icon)
        filename = icondir / 'Powers' / 'Misc' / f"{icon}.png"
        if not filename.exists():
            print(f"{server} Misc Power: {filename.relative_to(icondir)}")
            count = count + 1
        else:
            if filename in filecheck: filecheck.remove(filename)

    # Inspirations
    for _, type in GameData.Inspirations.items():
        for _, data in type.items():
            for insp in data['tiers']:
                insp = re.sub(r'\W+', '',  insp)
                filename = icondir / 'Inspirations' / f"{insp}.png"
                if not filename.exists():
                    print(f"{server} Inspirations: {filename.relative_to(icondir)}")
                    count = count + 1
                else:
                    if filename in filecheck: filecheck.remove(filename)



## TODO - turn all of this into a proper test without "print" all over it
if count: print(f"Total of {count} missing icons")

if filecheck:
    for fn in sorted(filecheck):
        print(f"Extra icon file: {fn.relative_to(icondir)}")
    print(f"Total of {len(filecheck)} extra icons")

if not (count or filecheck):
    print("Icons are as expected.")
