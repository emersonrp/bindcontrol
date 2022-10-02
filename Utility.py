import wx
import re
import UI

conflictbinds = {
    'binds' : {},
    'conflicts' : {},
}

def ColorDefault():
    return {
        'border'     : { 'r' : 0,   'g' : 0,   'b' : 0, },
        'foreground' : { 'r' : 0,   'g' : 0,   'b' : 0, },
        'background' : { 'r' : 255, 'g' : 255, 'b' : 255, },
    }

def BLF(profile, *args):
    return "bindloadfile " + BLFPath(profile, *args)

def BLFPath(profile, *args):
    filepath = profile.GameBindsDir()
    for arg in args:
        filepath = filepath + "/" + arg
    return filepath

Icons = {}
def Icon(iconname):
    if not Icons.get('iconname', None):
        Icons[iconname] = wx.Bitmap(
            wx.Image(
                f"icons/{iconname}.png", wx.BITMAP_TYPE_ANY, -1,
            )
        )
    return Icons[iconname]


#####################################################
from UI.ControlGroup import bcKeyButton
def CheckConflict(profile, key):
    conflicts = []

    for pageName in profile.Pages:
        page = getattr(profile, pageName, None)
        for ctrlname, ctrl in page.Ctrls.items():
            # TODO TODO TODO this next line is breaking this on Win wxpython 4.2.0
            if not ctrl.IsEnabled(): continue
            if isinstance(ctrl, bcKeyButton):
                if key == ctrl.GetLabel():
                    print(f"conflict found for key {key}: page {pageName}, {UI.Labels[ctrlname]}")
                    conflicts.append( {'page' : pageName, 'ctrl': UI.Labels[ctrlname]})
    return conflicts


def getMainKey(key):
    return re.sub('[LR]?(SHIFT|CTRL|ALT)\+?', '', key)

def ChatColors(fg,bg,bd): return f'<color {fg}><bgcolor {bg}><bordercolor {bd}>'

