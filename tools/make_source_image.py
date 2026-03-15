#!/usr/bin/env python3
# ruff: noqa

import re
import sys
from PIL import Image

from pathlib import Path

# Hack to allow us to import stuff from the parent dir.
#
# Get the absolute path of the current file
current_file = Path(__file__).resolve()

# Get the parent directory (us_housing_project/)
parent_directory = current_file.parent.parent

# Add the parent to sys.path
sys.path.append(str(parent_directory))

from Util.SourceFileIcons import sourcemaps # noqa

IMAGE_SIZE = 32

if len(sys.argv) != 2:
    print()
    print("Usage:  make_source_image.py <source>")
    print()
    print(f"Example:  {sys.argv[0]} Powers")
    print()
    exit()

sourcename = sys.argv[1]
if sourcename not in sourcemaps:
    print()
    print(f"{sourcename} not found in sourcemaps - add it to Util.SourceFileIcons!  Bailing out...")
    print()
    exit()

sourcelist = sourcemaps[sourcename]['list']

bigimage = Image.new(mode = 'RGBA', size = (IMAGE_SIZE * len(sourcelist), IMAGE_SIZE))

icondir = Path('icons') / sourcename
for index, iconname in enumerate(sourcelist):

    iconname = re.sub(r'[^\w\-\\/.]+', '', iconname)
    if not Path(icondir / f"{iconname}.png").exists():
        print()
        print(f"Icon file {icondir}/{iconname}.png does not exist -- you have at least one missing icon!  Bailing...")
        print()
        exit()

    icon = Image.open(icondir / f"{iconname}.png")

    print(f"pasting {iconname}")
    bigimage.paste(im = icon, box = (index * IMAGE_SIZE, 0))

print()
print(f"writing {Path('icons')}/{sourcename}.png")
bigimage.save(Path('icons') / f'{sourcename}.png', 'PNG')
