#!/usr/bin/env python3
import os
import re
import sys
import inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import GameData

count = 0
filecheck = set()
for filename in [f for f in os.listdir(f"{parentdir}/icons/Powers/") if f.endswith('png')]:
    filecheck.add(os.path.basename(filename))

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
                    # we found it, pull it back out of the set
                    if filename in filecheck: filecheck.remove(filename)

for poolname, pool in GameData.MiscPowers['Pool'].items():
    for power in pool:

        power = re.sub(r'\W+', '', power)
        filename = f"{poolname}_{power}.png"
        if not os.path.exists(f"{parentdir}/icons/Powers/{filename}"):
            print(f"Pool Power: {filename}")
            count = count + 1
        else:
            # we found it, pull it back out of the set
            if filename in filecheck: filecheck.remove(filename)

if count: print(f"Total of {count} missing icons")

if filecheck:
    for fn in sorted(filecheck):
        print(f"Extra icon file: {fn}")
    print(f"Total of {len(filecheck)} extra icons")

