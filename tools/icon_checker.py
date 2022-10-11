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
for archname, archdata in GameData.Archetypes.items():
    for category in ['Primary', 'Secondary', 'Epic']:
        for powerset, powers in archdata[category].items():
            powerset = re.sub(r'\W+', '', powerset)
            for power in sorted(powers):
                power = re.sub(r'\W+', '', power)
                if not os.path.exists(f"{parentdir}/icons/Powers/{powerset}_{power}.png"):
                    print(f"{archname}: {powerset}_{power}.png")
                    count = count + 1

print(f"Total of {count} missing icons")
