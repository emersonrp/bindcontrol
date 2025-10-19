import wx
import re
import base64
import threading
import zipfile
from pathlib import Path

import GameData
from Util.Incarnate import Aliases
import Util.Paths

class Icon(wx.BitmapBundle):
    def __init__(self, img:wx.Image|wx.Bitmap, filename):
        super().__init__(img)
        self.Filename = filename

Icons: dict[str, Icon] = { }
def GetIcon(*args) -> Icon:

    # If we haven't initialized the empty/fallback icon, do that now.
    if 'Empty.png' not in Icons:
        Icons['Empty.png'] = Icon(wx.Bitmap.NewFromPNGData(transparentPNG, len(transparentPNG)), '')

    pathbits = []
    for arg in args:
        arg = re.sub(r'[^\w\\/.]+', '', arg)
        pathbits.append(arg)

    iconpath    = Path(*pathbits).with_suffix('.png')
    iconpathstr = str(iconpath)
    if iconpathstr not in Icons:
        base_path = Util.Paths.GetRootDirPath()

        iconzippath = base_path / 'icons' / 'Icons.zip'
        if iconzippath.exists():
            with zipfile.ZipFile(iconzippath) as iconzip:
                try:
                    # as_posix is how we need this to index into the ZIPfile successfully on Windows
                    icondata = iconzip.read(iconpath.as_posix())
                    Icons[iconpathstr] = Icon(wx.Bitmap.NewFromPNGData(icondata, len(icondata)), iconpathstr)
                except Exception as e:
                    wx.LogError(f"Loading icon {iconpathstr} from ZIP file failed: {e}.  This is a bug.")

        else:  # we don't have the ZIP file, so maybe we're running directly from source
            filepath = Path(base_path) / 'icons' / iconpath
            if filepath.exists():
                Icons[iconpathstr] = Icon( wx.Image(str(filepath), wx.BITMAP_TYPE_ANY, -1,), iconpathstr)
            # TODO - maybe put this behind an "if debug" sort of thing
            else:
                wx.LogWarning(f"Missing icon: {iconpathstr}")

    return Icons.get(iconpathstr, Icons['Empty.png'])

def GetIconBitmap(*args) -> wx.Bitmap:
    return GetIcon(*args).GetBitmap(wx.Size(32,32))

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

##########
# This is so we can preload PowerPicker's icons in the background
# This returns the thread just for testing, so we can .join() it and wait for it to be done
def PrecacheIcons(profile):
    def doPrecacheIcons(profile):
        for picker in ('Primary', 'Secondary', 'Epic', 'Pool1', 'Pool2', 'Pool3', 'Pool4'):
            if powerset := profile.Data['General'][picker]:
                if picker in ('Primary', 'Secondary', 'Epic'):
                    powers = GameData.Archetypes[profile.Archetype()][picker].get(powerset, [])
                else:
                    powers = GameData.PoolPowers.get(powerset, [])
                for power in powers:
                    GetIcon('Powers', powerset, power)

        for slot, slotdata in GameData.IncarnatePowers.items():
            for inc_type in slotdata['Types']:
                aliasedtype = Aliases.get(inc_type, inc_type)
                for rarity in ['Common', 'Uncommon', 'Rare', 'VeryRare']:
                    GetIcon("Incarnate", f"Incarnate_{slot}_{aliasedtype}_{rarity}.png")

        RecurseMiscPowers(GameData.MiscPowers)

    def RecurseMiscPowers(menustruct):
        for data in menustruct.values():
            if isinstance(data, dict):
                RecurseMiscPowers(data)
            elif isinstance(data, list):
                for item in data:
                    item, iconlist = SplitNameAndIcon(item)
                    GetIcon('Powers', 'Misc', *iconlist)

    thread = threading.Thread(target = doPrecacheIcons, args = (profile,))
    thread.start()
    return thread

transparentPNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAC83pUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHja7ZdRkhsrDEX/WUWW0JIQEsuhoanKDrL8XNFtZ+xxPvzeV6rclAEL+kroAJ5Jx6+fM/3AQ9VLympeaikbnlxz5YaOb+fTVk1bXvV2fbu1D/Z0H2D0BK2cX71c82/2JyFq6OkXIe/XwP44UPOl709ClyOJiBidcQnVS0j4HKBLoJ3L2kp1+7qE/Tjb6/0zDR5LQzU717Dpfo49f8+G7A2FH2E+hGRDLcJnABIfTtJiADVL5dPcJKON+rZUJORVnu4P3KYZoeaXkx5p3Xr02p6eaWW+pshTksu9fWlPpK+prNR/8Zz96vGj3eSUSttT9lfy5/C51oxVtFyQ6nIt6raU1cM84Mjh2hP0ymb4KCRslYri2NUdW2FsfdtROlViUJmUaVCjScdqO3WEmPlIbOgwd5ZldDGu3MGOQA2FJptUGeIg2Rd2ML3HQstt3Xpa3hyeB2EqE8Qo9sW7Jb37wpxxFIg2v+cKcTFHshFGkIsa00CE5pVUXQm+lecnuAoIamQ5jkhFYvdTYlf6cxPIAi2YqGjPM0g2LgGkCK4VwZCAAKiRKBXajNmIkEgHoIbQWTLvIECqPBAkZ5ECNs7hGq8YramsDHOCHZdZnCspYmBTpQFWzor9Y9mxh5qKZlUtaupatRUpuWgpxUpcis3EcjK1YmZu1ZqLZ1cvbu5evVWugktTa6lWvdbaGnw2KDe83TChtZ132fOuaS+77b7XvXVsn5679tKte6+9DR4ycH+MMmz4qKMddGArHfnQoxx2+FGPNrHVpqSZp84ybfqss92pXVi/lTeo0UWNF6mYaHdqsJrdJCiuEw1mAMYpE4hbIMCG5mC2OeXMQS6YbZVxKpQRpAazQUEMBPNBrJNu7BKfRIPc/+KWLD9w4/9KLgW6N8l95/aK2oifob6InacwkroJTh/GD2/sLX7svrXpbwPvth+hj9BH6CP0EfoIfYT+IaGJPx7iv8DfAYKoyFD1D98AAAGEaUNDUElDQyBwcm9maWxlAAB4nH2RPUjDQBzFX1ulUioOdpAikqE6iAVREUetQhEqhFqhVQeTS7+gSUOS4uIouBYc/FisOrg46+rgKgiCHyCOTk6KLlLi/5JCixgPjvvx7t7j7h3gb1SYanaNA6pmGelkQsjmVoXgK0IYAjCKqMRMfU4UU/AcX/fw8fUuzrO8z/05epW8yQCfQDzLdMMi3iCe3rR0zvvEEVaSFOJz4jGDLkj8yHXZ5TfORYf9PDNiZNLzxBFiodjBcgezkqESTxHHFFWjfH/WZYXzFme1UmOte/IXhvPayjLXaQ4iiUUsQYQAGTWUUYGFOK0aKSbStJ/w8Ecdv0gumVxlMHIsoAoVkuMH/4Pf3ZqFyQk3KZwAul9s+2MYCO4Czbptfx/bdvMECDwDV1rbX20AM5+k19ta7Ajo2wYurtuavAdc7gADT7pkSI4UoOkvFID3M/qmHNB/C4TW3N5a+zh9ADLUVeoGODgERoqUve7x7p7O3v490+rvB31BcquNSSiRAAANeGlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNC40LjAtRXhpdjIiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iCiAgICB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIgogICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICAgeG1sbnM6R0lNUD0iaHR0cDovL3d3dy5naW1wLm9yZy94bXAvIgogICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iCiAgIHhtcE1NOkRvY3VtZW50SUQ9ImdpbXA6ZG9jaWQ6Z2ltcDo1NjcyNTBkOC01MjEzLTQyMWItOGVjMS1iNjEyODkxMDdlY2YiCiAgIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6OWU1N2VhYTgtYjAzOS00NGFkLTlkYzUtNzg3NzczNWU1NGY5IgogICB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6ZGJhMzkyYzEtNDA1ZS00NWJkLTgyYmEtMzg1NmIyY2ViMzI2IgogICBkYzpGb3JtYXQ9ImltYWdlL3BuZyIKICAgR0lNUDpBUEk9IjIuMCIKICAgR0lNUDpQbGF0Zm9ybT0iTGludXgiCiAgIEdJTVA6VGltZVN0YW1wPSIxNjY3MDkwNTY1MjQyNjg3IgogICBHSU1QOlZlcnNpb249IjIuMTAuMzIiCiAgIHRpZmY6T3JpZW50YXRpb249IjEiCiAgIHhtcDpDcmVhdG9yVG9vbD0iR0lNUCAyLjEwIgogICB4bXA6TWV0YWRhdGFEYXRlPSIyMDIyOjEwOjI5VDIwOjQyOjQ1LTA0OjAwIgogICB4bXA6TW9kaWZ5RGF0ZT0iMjAyMjoxMDoyOVQyMDo0Mjo0NS0wNDowMCI+CiAgIDx4bXBNTTpIaXN0b3J5PgogICAgPHJkZjpTZXE+CiAgICAgPHJkZjpsaQogICAgICBzdEV2dDphY3Rpb249InNhdmVkIgogICAgICBzdEV2dDpjaGFuZ2VkPSIvIgogICAgICBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjQ5YjkyYTA2LWY5OGEtNDgzZi1hMGY4LTFjYjYzYzYxMDc1NSIKICAgICAgc3RFdnQ6c29mdHdhcmVBZ2VudD0iR2ltcCAyLjEwIChMaW51eCkiCiAgICAgIHN0RXZ0OndoZW49IjIwMjItMTAtMjlUMjA6NDI6NDUtMDQ6MDAiLz4KICAgIDwvcmRmOlNlcT4KICAgPC94bXBNTTpIaXN0b3J5PgogIDwvcmRmOkRlc2NyaXB0aW9uPgogPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgIAo8P3hwYWNrZXQgZW5kPSJ3Ij8+p4vxbAAAAAZiS0dEAAAAAAAA+UO7fwAAAAlwSFlzAAAuIwAALiMBeKU/dgAAAAd0SU1FB+YKHgAqLdwL+m8AAAALSURBVAjXY2AAAgAABQAB4iYFmwAAAABJRU5ErkJggg==")

