import wx
import re

def ColorDefault():
    return {
        'border'     : { 'r' : 0,   'g' : 0,   'b' : 0, },
        'foreground' : { 'r' : 0,   'g' : 0,   'b' : 0, },
        'background' : { 'r' : 255, 'g' : 255, 'b' : 255, },
    }

Icons = {}
def Icon(iconname):
    if not Icons.get('iconname', None):
        Icons[iconname] = wx.Bitmap(
            wx.Image(
                f"icons/{iconname}.png", wx.BITMAP_TYPE_ANY, -1,
            )
        )
    return Icons[iconname]

def getMainKey(key):
    return re.sub('[LR]?(SHIFT|CTRL|ALT)\+?', '', key)

def ChatColors(fg,bg,bd): return f'<color {fg}><bgcolor {bg}><bordercolor {bd}>'

