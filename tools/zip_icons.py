#!/usr/bin/env python3

import zipfile
from pathlib import Path

with zipfile.ZipFile('icons/Icons.zip', 'w') as iconzip:
    for subdir in ['Alignments', 'Archetypes', 'Incarnate', 'Inspirations', 'Origins', 'Powers', 'UI']:
        subpath = Path('icons') / subdir

        for icon in subpath.glob('**/*.png'):
            print(icon.relative_to('icons'))
            iconzip.write(icon, icon.relative_to('icons'))

    iconzip.write('icons/Help.png', 'Help.png')

    iconzip.close()
