import wx
import re
import base64
from pathlib import Path

import bcColours
import Util.Paths
from Util.SourceFileIcons import GetImageFromSourceFile, sourcemaps

# just a BitmapBundle with a filename attached.
class Icon(wx.BitmapBundle):
    def __init__(self, img:wx.Image|wx.Bitmap, filename):
        super().__init__(img)
        self.Filename = filename

# The global Icon cache
Icons: dict[str, Icon] = { }

# This is the one way in.
def GetIcon(*args) -> Icon:

    # If we haven't initialized the empty/fallback icon, do that now.
    # We don't do this at start-time b/c wx is not initialized.
    if 'Empty.png' not in Icons:
        Icons['Empty.png'] = Icon(wx.Image(1, 1, transparentPNG), 'Empty')

    pathbits = []

    # this next bit is because we're still using "filename" in Icon even though we're cropping
    # from the sourcefile, so we're saving the filename in Icon as <sourcefile>/<iconname>.
    # I think this is only a deal in the Incarnate Box, so there might want to be some cleanup of
    # this whole scheme.
    if len(args) == 1:
        args = (re.sub(r'\.png$', '', args[0], flags = re.IGNORECASE),) # trailing comma important
        args = re.split(r'[/\\]', args[0])

    for arg in args:

        # we renamed icons because we like simplicity and parallelism.  But we need to munch Incarnate
        # icons' filenames now, forever and ever amen.  Ah well.
        # ETA:  ...except in Macros land where the Incarnate_ is still there and needs to remain.
        if pathbits and pathbits[0] != 'Macros':
            if re.match('Incarnate_', arg):
                arg = re.sub('^Incarnate_', '', arg)

        # UGH
        # The devs left ONE icon in there with a ' in it and scraped out the rest.
        # Just in the Macro set;  we have control of the names in the Powers set.
        if pathbits and pathbits[0] == 'Macros' and arg == "MartialArts_Warrior'sChallenge":
            arg = re.sub(r'[^\w\-\\/\'.]+', '', arg)
        else:
            arg = re.sub(r'[^\w\-\\/.]+', '', arg)

        pathbits.append(arg)

    iconpath    = Path(*pathbits).with_suffix('.png')
    # dark/light the UI icons
    if 'UI' in iconpath.parts:
        darklight = 'dark' if bcColours.DarkMode() else 'light'
        iconpath = Path('UI') / darklight / iconpath.parts[1] # shim 'dark' or 'light' in there.
    iconpathstr = str(iconpath)
    if iconpathstr not in Icons:
        source = pathbits[0]
        if source in sourcemaps:
            sourcename = '_'.join(pathbits[1:]) # probably not needed on this code path, but just in case
            if sourcename in sourcemaps[source]['list']:
                if bitmap := GetImageFromSourceFile(source, sourcename):
                    Icons[iconpathstr] = Icon(bitmap, filename = f"{source}/{sourcename}")
                else:
                    wx.LogWarning(f"Missing Icon: SourceFile {source} returned None for {sourcename} - check logs!")
            else:
                wx.LogWarning(f"Missing icon: {source} icon not in sourcemap: {sourcename}")
        else:  # we don't have any such source file, so check the filesystem for the leftover UI icons etc
            filepath = Util.Paths.GetRootDirPath() / 'icons' / iconpath
            if filepath.exists():
                Icons[iconpathstr] = Icon( wx.Image(str(filepath), wx.BITMAP_TYPE_ANY, -1,), iconpathstr)
            # TODO - maybe put this behind an "if debug" sort of thing
            else:
                wx.LogWarning(f"Missing icon: Not found in filesystem: {iconpathstr}")

    return Icons.get(iconpathstr, Icons['Empty.png'])

def GetIconBitmap(*args, **kwargs):
    size : tuple = kwargs.get('size', (32,32))
    return GetIcon(*args).GetBitmap(wx.Size(*size))

# get the correct icon path bits for GetIcon based on how we
# store Misc power names in GameData.  Used here and in PowerPicker
def SplitNameAndIcon(namestr) -> list:
    if re.search(r'\|', namestr):
        name, iconstr = re.split(r'\|', namestr)
        iconstr = re.sub(r'[^\w|]+', '', iconstr)
        iconpathparts = re.split(r'_', iconstr)
        return [name, iconpathparts]
    else:
        iconstr = re.sub(r'[^\w|]+', '', namestr)
        return [namestr, [iconstr]]

transparentPNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")
