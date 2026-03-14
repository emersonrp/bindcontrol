#!/usr/bin/env python3

import re
from PIL import Image

from Util.SourceFileIcons import POWERS_ICON_NAMES
from pathlib import Path

IMAGE_SIZE = 32

bigimage = Image.new(mode = 'RGBA', size = (IMAGE_SIZE * len(POWERS_ICON_NAMES), IMAGE_SIZE))

icondir = Path('icons') / 'Powers'
for index, iconname in enumerate(POWERS_ICON_NAMES):

    iconname = re.sub(r'[^\w\-\\/.]+', '', iconname)
    dirname, power = iconname.split('_')
    icon = Image.open(icondir / dirname / f"{power}.png")

    bigimage.paste(im = icon, box = (index * IMAGE_SIZE, 0))

bigimage.save(icondir / 'Powers.png', 'PNG')
