from functools import partial
import wx
import UI
from Icon import GetIcon
from UI.BindWizard import WizardParent
from UI.IncarnateBox import IncarnateBox
from UI.KeySelectDialog import bcKeyButton, EVT_KEY_CHANGED

class IncarnateConfig(WizardParent):
    WizardName  = 'Incarnate Powers Set'
    WizToolTip  = 'Create a keybind that, with multiple presses, will load a particular set of Incarnate Powers'

    def BuildUI(self, init = {}):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.SetMinSize(wx.Size(700,-1))

        if setName := init.get('Title', ''):
            setName = f' "{setName}"'

        self.SetTitle(f"Incarnate Set{setName}")

        self.IncarnateBox = IncarnateBox(self, wx.App.Get().Main.Profile.Server)
        mainSizer.Add(self.IncarnateBox, 1, wx.EXPAND|wx.ALL, 10)

        return mainSizer

    def GetData(self):
        return self.IncarnateBox.GetData()

    def PaneContents(self, collPane):
        pane = collPane.GetPane()
        paneSizer = wx.BoxSizer(wx.HORIZONTAL)

        listSizer = wx.BoxSizer(wx.HORIZONTAL)
        incarnateData = self.IncarnateBox.GetData()
        for slot in ['Alpha', 'Interface', 'Judgement', 'Destiny', 'Lore', 'Hybrid', 'Genesis',]:
            if slotData := incarnateData.get(slot, None):
                icon = GetIcon(slotData['iconfile'])
                bitmap = wx.GenericStaticBitmap(pane, wx.ID_ANY, icon)
                bitmap.Bind(wx.EVT_ENTER_WINDOW, partial(self.OnHoverIcon, f"<b>{slot}</b>: {slotData['power']}"))
                bitmap.Bind(wx.EVT_LEAVE_WINDOW, partial(self.OnHoverIcon, None))
                listSizer.Add(bitmap, 0, wx.ALL, 5)

        self.HoverDisplay = wx.StaticText(pane, wx.ID_ANY)
        listSizer.Add(self.HoverDisplay, 1, wx.ALL, 10)

        paneSizer.Add(listSizer, 1, wx.ALIGN_CENTER|wx.ALL, 15)

        BindSizer = wx.BoxSizer(wx.HORIZONTAL)
        BindKeyCtrl = bcKeyButton(pane, -1, {
            'CtlName' : collPane.MakeCtlName("BindKey"),
            'Page'    : pane.Page,
            'Key'     : collPane.Init.get('Key', ''),
        })
        BindKeyCtrl.Bind(EVT_KEY_CHANGED, self.OnKeyChanged)
        BindSizer.Add(wx.StaticText(pane, -1, "Bind Key:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)
        BindSizer.Add(BindKeyCtrl,                          0, wx.ALIGN_CENTER_VERTICAL)
        pane.Page.Ctrls[BindKeyCtrl.CtlName] = BindKeyCtrl
        UI.Labels[BindKeyCtrl.CtlName] = f'Simple Bind "{self.Title}"'

        paneSizer.Add(BindSizer, 0, wx.EXPAND|wx.ALL, 15)

        self.OnHoverIcon('')

        return paneSizer

    def OnHoverIcon(self, markup, evt = None):
        if markup:
            self.HoverDisplay.SetForegroundColour(wx.BLACK)
            self.HoverDisplay.SetLabelMarkup(markup)
        else:
            self.HoverDisplay.SetForegroundColour(wx.Colour(128, 128, 128))
            self.HoverDisplay.SetLabelMarkup("Incarnate Power Set - Hover any icon for details")
        if evt: evt.Skip()

    def OnKeyChanged(self, evt):
        ...
