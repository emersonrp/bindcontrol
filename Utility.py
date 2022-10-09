import wx
import re
import os

def ColorDefault():
    return {
        'border'     : { 'r' : 0,   'g' : 0,   'b' : 0, },
        'foreground' : { 'r' : 0,   'g' : 0,   'b' : 0, },
        'background' : { 'r' : 255, 'g' : 255, 'b' : 255, },
    }

Icons = {}
def Icon(name = '', powerset = '', power = ''):
    # parse powerset and power to get name, if supplied
    if powerset and power:
        powerset = re.sub(r'\W+', '', powerset)
        power    = re.sub(r'\W+', '', power)
        name     = f"Powers/{powerset}_{power}"

    if not Icons.get(name, None):
        if os.path.exists(f"icons/{name}.png"):
            Icons[name] = wx.Bitmap(
                wx.Image(
                    f"icons/{name}.png", wx.BITMAP_TYPE_ANY, -1,
                )
            )
        else:
            print(f"Missing powers icon: {name}")

    return Icons.get(name, None)

def getMainKey(key):
    return re.sub('[LR]?(SHIFT|CTRL|ALT)\+?', '', key)

def ChatColors(fg,bg,bd): return f'<color {fg}><bgcolor {bg}><bordercolor {bd}>'

