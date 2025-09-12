import wx
import GameData

def OnEmotePicker(evt):
    button = evt.EventObject

    button.PopupMenu(EmotePicker(button))

# TODO -- self.payloadMap is only generated once we first make the menu, but it
# might be accessed after loading a profile and trying to edit an emote step.
# We need to go through the exercise of building it proactively at init time.
class EmotePicker(wx.Menu):

    payloadMap = { '...': '' }

    def __init__(self, target):
        super().__init__()

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
                                if isinstance(leafitem, str):
                                    self.HandleEmoteString(leafitem, subsubmenu)

                                elif isinstance(leafitem, dict):
                                    # Thanks, "kneel" subsubsubsubmenu
                                    for subsubitem, deeperdata in leafitem.items():
                                        subsubsubmenu = wx.Menu()
                                        subsubmenu.AppendSubMenu(subsubsubmenu, subsubitem)

                                        for kneelitem in deeperdata:
                                            self.HandleEmoteString(kneelitem, subsubsubmenu)

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

            menu.Append(-1, label)

    def OnMenuSelection(self, evt):
        menuitem = self.FindItemById(evt.GetId())
        label = menuitem.GetItemLabel()
        self.UpdateTarget.SetLabel(label)

# generate the payloadMap at init time instead of lazy-building it.
# This is ugly and fragile.  TODO -- DRY this up some with HandleEmoteString()
payloadMap = {}
data = GameData.Emotes['emotes']
def parseEmoteString(item):
    if item != "---":
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

        payloadMap[label] = payload
for category in data:
    for catname, cat in category.items():
        for subcat in cat:
            if isinstance(subcat, str):
                parseEmoteString(subcat)
            elif isinstance(subcat, dict):
                for subitem, deepdata in subcat.items():
                    for leafitem in deepdata:
                        if isinstance(leafitem, str):
                            parseEmoteString(leafitem)
                        elif isinstance(leafitem, dict):
                            for subsubitem, deeperdata in leafitem.items():
                                for kneelitem in deeperdata:
                                    parseEmoteString(kneelitem)

