import wx
import re
import os
import sys
from typing import Dict

class Icon(wx.Bitmap):
    def __init__(self, img:wx.Image):
        wx.Bitmap.__init__(self, img)

        self.Filename = ""

Icons: Dict[str, Icon] = {}
def GetIcon(name = '', powerset = '', power = ''):
    # parse powerset and power to get name, if supplied
    if powerset and power:
        powerset = re.sub(r'\W+', '', powerset)
        power    = re.sub(r'\W+', '', power)
        name     = f"Powers/{powerset}_{power}"

    if not name in Icons:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        filename = f"{base_path}/icons/{name}.png"
        if os.path.exists(filename):
            Icons[name] = Icon( wx.Image( filename, wx.BITMAP_TYPE_ANY, -1,))
            Icons[name].Filename = name
        else:
            print(f"Missing icon: {name}")
            return Icons['Empty']

    return Icons.get(name, Icons.get('Empty'))

