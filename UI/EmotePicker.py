import wx
import GameData

import pprint
pp = pprint.PrettyPrinter(indent = 1, width = 132)

def doEmotePicker(evt):
    button = evt.EventObject

    button.PopupMenu(EmotePicker(), (0,0))

class EmotePicker(wx.Menu):
    def __init__(self):
        wx.Menu.__init__(self)

        EmoteData = GameData.Emotes

        #self.AppendSubMenu(self.BuildMenu(self, EmoteData['emotes']))
        self.BuildMenu(self, EmoteData['emotes'])


    # tangly recursive menu builder
    def BuildMenu(self, menuroot, data):

        for emote in data:
            newthing = None

            if isinstance(emote, dict):
                # recurse up a submenu
                for name, subdata in emote.items():
                    newthing = wx.Menu(name)
                    toappend = self.BuildMenu(newthing, subdata)
                    if isinstance(toappend, wx.Menu):
                        newthing.AppendSubMenu(self.BuildMenu(self, subdata), name)
                    else:
                        newthing.Append(-1, item = name)

            elif isinstance(emote, list):
                # iterate
                for item in emote:
                    newthing = item
                    menuroot.Append(self.BuildMenu(self, item))
                    # menuroot.append(self.BuildMenu(item)

            elif isinstance(emote, str):
                # stick it in the menu thingie
                menuroot.Append(-1, item = emote)
                # parse the string for | % etc
                # add the visible string to the menu,
                # add the massaged bind string as ClientData()
                #
                # add event handler?
                # return it
        return newthing
