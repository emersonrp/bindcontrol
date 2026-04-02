import wx
import GameData
import COHMenu as FM
from Icon import GetIcon
import UI

class EmotePicker(wx.Button):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.EmotePickerMenu = None
        self.SetBitmap(GetIcon('UI', 'QuickChat'))
        self.SetFont(UI.COHFont(13))

        self.Bind(wx.EVT_BUTTON, self.OnEmotePicker)

    def OnEmotePicker(self, evt) -> None:
        if not self.EmotePickerMenu:
            self.EmotePickerMenu = EmotePickerMenu(self)

        self.EmotePickerMenu.Popup(wx.GetMousePosition())

    def SetLabel(self, label):
        super().SetLabel(label)
        self.SetBitmap(GetIcon('UI', 'QuickChat'))

class EmotePickerMenu(FM.FlatMenu):
    def __init__(self, target) -> None:
        super().__init__(target)

        self.UpdateTarget = target
        self.BuildMenu(GameData.Emotes['emotes'])

        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnMenuSelected)

    # this is AWFUL
    def BuildMenu(self, data) -> None:
        for category in data:
            # 'Converse' : []
            for catname, cat in category.items():
                submenu = FM.FlatMenu(self.UpdateTarget)
                submenu.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnMenuSelected)
                self.AppendSubMenu(submenu, catname)

                # [ {submenu: [ list, of, emotes ]},  "or just strings" ]
                for subcat in cat:
                    if isinstance(subcat, str):
                        self.HandleEmoteString(subcat, submenu)

                    elif isinstance(subcat, dict):
                        # { submenu : [ list, of, emotes ]}
                        for subitem, deepdata in subcat.items():
                            subsubmenu = FM.FlatMenu(self.UpdateTarget)
                            subsubmenu.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnMenuSelected)
                            submenu.AppendSubMenu(subsubmenu, subitem)

                            for leafitem in deepdata:
                                if isinstance(leafitem, str):
                                    self.HandleEmoteString(leafitem, subsubmenu)

                                elif isinstance(leafitem, dict):
                                    # Thanks, "kneel" subsubsubsubmenu
                                    for subsubitem, deeperdata in leafitem.items():
                                        subsubsubmenu = FM.FlatMenu(self.UpdateTarget)
                                        subsubsubmenu.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnMenuSelected)
                                        subsubmenu.AppendSubMenu(subsubsubmenu, subsubitem)

                                        for kneelitem in deeperdata:
                                            self.HandleEmoteString(kneelitem, subsubsubmenu)

    def HandleEmoteString(self, item, menu) -> None:
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

    def OnMenuSelected(self, evt) -> None:
        if menuitem := self.FindItem(evt.GetId()):
            label = menuitem.GetLabel()
            self.UpdateTarget.SetLabel(label)
            self.UpdateTarget.SetBitmap(GetIcon('UI', 'QuickChat'))
