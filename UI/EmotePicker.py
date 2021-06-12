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

        self.BuildMenu(EmoteData['emotes'])


    def BuildMenu(self, data):
        for category in data:
            # 'Converse' : []
            for catname, cat in category.items():
                submenu = wx.Menu()
                self.AppendSubMenu(submenu, catname)

                # [ {submenu: [ list, of, emotes ]},  "or just strings" ]
                for subcat in cat:
                    if isinstance(subcat, str):
                        if subcat == "---":
                            submenu.AppendSeparator()
                        else:
                            # TODO - split into visible string and actual emote,
                            # TODO - and bind event with, I guess, a closure
                            submenu.Append(-1, subcat)

                    elif isinstance(subcat, dict):
                        # { submenu : [ list, of, emotes ]}
                        for subitem, deepdata in subcat.items():
                            print(f"subitem is {subitem}")
                            print(f"deepdata is {deepdata}")
                            subsubmenu = wx.Menu()
                            submenu.AppendSubMenu(subsubmenu, subitem)

                            for leafitem in deepdata:
                                if leafitem == "---":
                                    subsubmenu.AppendSeparator()
                                else:
                                    # TODO - split into visible string and actual emote,
                                    # TODO - and bind event with, I guess, a closure
                                    subsubmenu.Append(-1, leafitem)
