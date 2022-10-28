#!/bin/bash
convert \
    Windows_icons/icon_16.png \
    Windows_icons/icon_32.png \
    Windows_icons/icon_48.png \
    Windows_icons/icon_128.png \
    Windows_icons/icon_256.png \
    -colors 256 \
    BindControl.ico
