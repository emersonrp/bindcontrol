import wx
import re
import os

Icons = {}

def GetIcon(name = '', powerset = '', power = ''):
    # parse powerset and power to get name, if supplied
    if powerset and power:
        powerset = re.sub(r'\W+', '', powerset)
        power    = re.sub(r'\W+', '', power)
        name     = f"Powers/{powerset}_{power}"

    if not Icons.get(name, None):
        filename = f"icons/{name}.png"
        if os.path.exists(filename):
            Icons[name] = Icon( wx.Image( filename, wx.BITMAP_TYPE_ANY, -1,))
            Icons[name].Filename = name
        else:
            print(f"Missing icon: {name}")

    return Icons.get(name, None)

class Icon(wx.Bitmap):
    def __init__(self, img:wx.Image):
        wx.Bitmap.__init__(self, img)

        self.Filename = ""

