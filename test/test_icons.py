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
    assert currframe != None
    exit()

import GameData
GameData.SetupGameData()

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

def test_archetype_icons_exist():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Archetype, Primary, and Secondary
        for archname, archdata in GameData.Archetypes.items():
            filename = f"{archname}.png"
            assert os.path.exists(f"{parentdir}/icons/Archetypes/{filename}"), f"Archetype icon missing: {filename}"
            if filename in filecheck: filecheck.remove(filename)

            for category in ['Primary', 'Secondary', 'Epic']:
                for powerset, powers in archdata[category].items():
                    powerset = re.sub(r'\W+', '', powerset)
                    for power in powers:
                        if isinstance(power, dict):
                            [(power, items)] = power.items()
                            for p in items:
                                p = re.sub(r'\W+', '', p)
                                filename = f"{powerset}_{p}.png"
                                assert os.path.exists(f"{parentdir}/icons/Powers/{filename}"), f"Powers icond missing: {filename}"
                                if filename in filecheck: filecheck.remove(filename)
                        power = re.sub(r'\W+', '', power)
                        filename = f"{powerset}_{power}.png"
                        assert os.path.exists(f"{parentdir}/icons/Powers/{filename}"), f"Powers icon missing: {filename}"
                        if filename in filecheck: filecheck.remove(filename)

def test_origin_icons_exist():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Origins
        for origin in GameData.Origins:
            filename = f"{origin}.png"
            assert os.path.exists(f"{parentdir}/icons/Origins/{filename}"), f"Origins icon missing: {filename}"
            if filename in filecheck: filecheck.remove(filename)

def test_pool_power_icons_exist():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Pool Powers
        for poolname, pool in GameData.MiscPowers['Pool'].items():
            for power in pool:

                power = re.sub(r'\W+', '', power)
                poolname = re.sub(r'\W+', '', poolname)
                filename = f"{poolname}_{power}.png"
                assert os.path.exists(f"{parentdir}/icons/Powers/{filename}")
                if filename in filecheck: filecheck.remove(filename)

def test_incarnate_icons_exist():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Incarnate Powers
        for slot, slotdata in GameData.MiscPowers['Incarnate'].items():
            for type in slotdata['Types']:
                aliasedtype = Aliases.get(type, type)
                for rarity in ['Common', 'Uncommon', 'Rare', 'VeryRare']:
                    filename = f"Incarnate_{slot}_{aliasedtype}_{rarity}.png"
                    assert os.path.exists(f"{parentdir}/icons/Incarnate/{filename}"), "Incarnate icon missing: {filename}"
                    if filename in filecheck: filecheck.remove(filename)

def test_miscpowers_icons_exist():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Misc Powers
        # TODO generalize this more?
        miscpowerlist = GameData.MiscPowers['Badge']['Accolade'] + GameData.MiscPowers['General']['Inherent'] + GameData.MiscPowers['General']['SMART']
        for power in miscpowerlist:
            power = re.sub(r'\W+', '', power)
            filename = f"Misc_{power}.png"
            assert os.path.exists(f"{parentdir}/icons/Powers/{filename}"), f"Misc Powers icon missing: {filename}"
            if filename in filecheck: filecheck.remove(filename)

def test_inspiration_icons_exist():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Inspirations
        for _, type in GameData.Inspirations.items():
            for _, data in type.items():
                for insp in data['tiers']:
                    insp = re.sub(r'\W+', '',  insp)
                    filename = f"{insp}.png"
                    assert os.path.exists(f"{parentdir}/icons/Inspirations/{filename}"), f"Inspiration icon missing: {filename}"
                    if filename in filecheck: filecheck.remove(filename)

def test_no_extra_icons():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        assert not filecheck, f"{len(filecheck)} extra icons exist: {filecheck}"
