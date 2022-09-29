import re
import wx
import GameData

def OnEmotePicker(evt):
    button = evt.EventObject

    button.PopupMenu(EmotePicker(button))


class EmotePicker(wx.Menu):

    payloadMap = { '...': '' }

    def __init__(self, target):
        wx.Menu.__init__(self)

        self.UpdateTarget = target
        self.BuildMenu(GameData.Emotes['emotes'])

        self.Bind(wx.EVT_MENU, self.OnMenuSelection)

    def BuildMenu(self, data):
        for category in data:
            # 'Converse' : []
            for catname, cat in category.items():
                submenu = wx.Menu()
                self.AppendSubMenu(submenu, catname)

                # [ {submenu: [ list, of, emotes ]},  "or just strings" ]
                for subcat in cat:
                    if isinstance(subcat, str):
                        self.HandleEmoteString(subcat, submenu)

                    elif isinstance(subcat, dict):
                        # { submenu : [ list, of, emotes ]}
                        for subitem, deepdata in subcat.items():
                            subsubmenu = wx.Menu()
                            submenu.AppendSubMenu(subsubmenu, subitem)

                            for leafitem in deepdata:
                                self.HandleEmoteString(leafitem, subsubmenu)

    def HandleEmoteString(self, item, menu):
        if item == "---":
            menu.AppendSeparator()
        else:
            label, *payload = item.split('%')
            if payload and payload[0]:
                # contains the entire necessary bindstring
                payload = payload[0]
            else:
                label, *payload = item.split('|')
                if payload and payload[0]:
                    # contains different string for emote name
                    payload = f"em {payload[0]}"
                else:
                    # no extra info needed, just lower and de-space the name
                    payload = "em " + label.lower().replace(" ","")


            self.payloadMap[label] = payload
            menuitem = menu.Append(-1, label)

    def OnMenuSelection(self, evt):
        menuitem = self.FindItemById(evt.GetId())
        label = menuitem.GetItemLabel()
        self.UpdateTarget.SetLabel(label)
