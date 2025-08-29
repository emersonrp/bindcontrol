import re
from pathlib import Path
def ParseBuildFile(file:Path):
    if buildtext := file.read_text():
        lines = buildtext.splitlines()

        firstline = lines[0]

        name, rest      = re.split(r':', firstline)
        restwords       = re.split(r'\s', rest)
        origin, rawarch = restwords[-2], restwords[-1]
        _, archetype    = re.split(r'_', rawarch)

        data = {
            'Name' : name,
            'Origin' : origin,
            'Archetype' : archetype,
            'Server' : 'Homecoming', # Rebirth doesn't have /build_save I think
        }

        for line in lines:
            if not re.match(r'Level', line): continue

            print(line)

        print(data)
        return data
