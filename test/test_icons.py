#!/usr/bin/env python3
import os
import re
import sys
import inspect
from pathlib import Path
from Util.Incarnate import Aliases


currframe = inspect.currentframe()
if currframe:
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(currframe)))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)
else:
    assert currframe != None
    exit()

import GameData
GameData.SetupGameData()

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
    filecheck.add(str(filename))
for filename in Path(f"{parentdir}/icons/Origins/").glob('**/*.png'):
    filecheck.add(str(filename))
for filename in Path(f"{parentdir}/icons/Powers/").glob('**/*.png'):
    filecheck.add(str(filename))
for filename in Path(f"{parentdir}/icons/Incarnate/").glob('**/*.png'):
    filecheck.add(str(filename))
for filename in Path(f"{parentdir}/icons/Inspirations/").glob('**/*.png'):
    filecheck.add(str(filename))

def test_archetype_icons_exist():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Archetype, Primary, and Secondary
        for archname, archdata in GameData.Archetypes.items():
            archname = re.sub(r'\W+', '', archname)
            filename = f"{parentdir}/icons/Archetypes/{archname}.png"
            assert os.path.exists(filename), f"Archetype icon missing: {filename}"
            if filename in filecheck: filecheck.remove(filename)

            for category in ['Primary', 'Secondary', 'Epic']:
                for powerset, powers in archdata[category].items():
                    powerset = re.sub(r'\W+', '', powerset)
                    for power in powers:
                        if isinstance(power, dict):
                            [(power, items)] = power.items()
                            for p in items:
                                p = re.sub(r'\W+', '', p)
                                filename = f"{parentdir}/icons/Powers/{powerset}/{p}.png"
                                assert os.path.exists(filename), f"Powers icon missing: {filename}"
                                if filename in filecheck: filecheck.remove(filename)
                        power = re.sub(r'\W+', '', power)
                        filename = f"{parentdir}/icons/Powers/{powerset}/{power}.png"
                        assert os.path.exists(filename), f"Powers icon missing: {filename}"
                        if filename in filecheck: filecheck.remove(filename)

def test_origin_icons_exist():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Origins
        for origin in GameData.Origins:
            filename = f"{parentdir}/icons/Origins/{origin}.png"
            assert os.path.exists(filename), f"Origins icon missing: {filename}"
            if filename in filecheck: filecheck.remove(filename)

def test_pool_power_icons_exist():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Pool Powers
        for poolname, pool in GameData.PoolPowers.items():
            for power in pool:
                power = re.sub(r'\W+', '', power)
                poolname = re.sub(r'\W+', '', poolname)
                filename = f"{parentdir}/icons/Powers/{poolname}/{power}.png"
                assert os.path.exists(filename), f"Pool power icond missing: {filename}"
                if filename in filecheck: filecheck.remove(filename)

def test_incarnate_icons_exist():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Incarnate Powers
        for slot, slotdata in GameData.IncarnatePowers.items():
            for type in slotdata['Types']:
                aliasedtype = Aliases.get(type, type)
                for rarity in ['Common', 'Uncommon', 'Rare', 'VeryRare']:
                    filename = f"{parentdir}/icons/Incarnate/Incarnate_{slot}_{aliasedtype}_{rarity}.png"
                    assert os.path.exists(filename), f"Incarnate icon missing: {filename}"
                    if filename in filecheck: filecheck.remove(filename)

def test_miscpowers_icons_exist():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Misc Powers
        # TODO generalize this more?


        miscpowerlist = RecurseMiscPowers(GameData.MiscPowers)
        for power in miscpowerlist:
            power = re.sub(r'[^\w|]+', '', power)
            _, icon = SplitNameAndIcon(power)
            icon = '_'.join(icon)
            filename = f'{parentdir}/icons/Powers/Misc/{icon}.png'
            assert os.path.exists(filename), f"Misc Powers icon missing: {filename}"
            if filename in filecheck: filecheck.remove(filename)

def test_inspiration_icons_exist():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Inspirations
        for _, type in GameData.Inspirations.items():
            for _, data in type.items():
                for insp in data['tiers']:
                    insp = re.sub(r'\W+', '',  insp)
                    filename = f"{parentdir}/icons/Inspirations/{insp}.png"
                    assert os.path.exists(filename), f"Inspiration icon missing: {filename}"
                    if filename in filecheck: filecheck.remove(filename)

def test_no_extra_icons():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        assert not filecheck, f"{len(filecheck)} extra icons exist: {filecheck}"
