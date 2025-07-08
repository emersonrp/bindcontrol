import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Graphics Command
class CameraCmd(PowerBinderCommand):
    Name = "Camera Commands"
    Menu = "Misc"

    def BuildUI(self, dialog):
        centeringSizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.GridSizer(2)

        self.camdistcb = wx.CheckBox(dialog, label = "camdist")
        self.camdistcb.SetToolTip('Sets the distance in feet that the third person camera pulls back behind the player')
        sizer.Add(self.camdistcb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.camdistsc = wx.SpinCtrl(dialog, initial = 30, min = 1, max = 120)
        self.camdistsc.SetToolTip('Sets the distance in feet that the third person camera pulls back behind the player')
        sizer.Add(self.camdistsc, 1, wx.ALIGN_CENTER_VERTICAL)

        self.camresetcb = wx.CheckBox(dialog, label = "camreset")
        self.camresetcb.SetToolTip('Resets the camera to behind the player; resets camera distance')
        sizer.Add(self.camresetcb, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(wx.StaticText(dialog, wx.ID_ANY, ''))

        self.camturncb = wx.CheckBox(dialog, label = "camturn")
        self.camturncb.SetToolTip('Resets the camera to behind the player without changing camera distance')
        sizer.Add(self.camturncb, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(wx.StaticText(dialog, wx.ID_ANY, ''))

        self.camrotatecb = wx.CheckBox(dialog, label = "camrotate")
        self.camrotatecb.SetToolTip('Enable or toggle camera rotation using the mouse;  does not affect player facing')
        sizer.Add(self.camrotatecb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.camrotatech = wx.Choice(dialog, choices = ["+", "++", "0", "1"])
        self.camrotatech.SetToolTip('+ to activate while key is held, ++ to toggle, 0 to disable, 1 to enable')
        self.camrotatech.SetSelection(0)
        sizer.Add(self.camrotatech, 1, wx.ALIGN_CENTER_VERTICAL)

        self.mouselookcb = wx.CheckBox(dialog, label = "mouselook")
        self.camrotatecb.SetToolTip('Enable or toggle camera rotation using the mouse;  player facing turns to match')
        sizer.Add(self.mouselookcb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.mouselookch = wx.Choice(dialog, choices = ["+", "++", "0", "1"])
        self.mouselookch.SetToolTip('+ to activate while key is held, ++ to toggle, 0 to disable, 1 to enable')
        self.mouselookch.SetSelection(0)
        sizer.Add(self.mouselookch, 1, wx.ALIGN_CENTER_VERTICAL)

        self.lookupcb = wx.CheckBox(dialog, label = "lookup")
        self.lookupcb.SetToolTip('Pitch the camera upwards')
        sizer.Add(self.lookupcb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.lookupch = wx.Choice(dialog, choices = ["+", "++", "0", "1"])
        self.lookupch.SetToolTip('+ to activate while key is held, ++ to toggle, 0 to disable, 1 to enable')
        self.lookupch.SetSelection(0)
        sizer.Add(self.lookupch, 1, wx.ALIGN_CENTER_VERTICAL)

        self.lookdowncb = wx.CheckBox(dialog, label = "lookdown")
        self.lookdowncb.SetToolTip('Pitch the camera downwards')
        sizer.Add(self.lookdowncb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.lookdownch = wx.Choice(dialog, choices = ["+", "++", "0", "1"])
        self.lookdownch.SetToolTip('+ to activate while key is held, ++ to toggle, 0 to disable, 1 to enable')
        self.lookdownch.SetSelection(0)
        sizer.Add(self.lookdownch, 1, wx.ALIGN_CENTER_VERTICAL)

        self.firstcb = wx.CheckBox(dialog, label = "first")
        self.firstcb.SetToolTip('Zooms the camera in to first-person view')
        sizer.Add(self.firstcb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.firstch = wx.Choice(dialog, choices = ["+", "++", "0", "1"])
        self.firstch.SetToolTip('+ to activate while key is held, ++ to toggle, 0 to disable, 1 to enable')
        self.firstch.SetSelection(0)
        sizer.Add(self.firstch, 1, wx.ALIGN_CENTER_VERTICAL)

        self.thirdcb = wx.CheckBox(dialog, label = "third")
        self.thirdcb.SetToolTip('Zooms the camera out to third person mode')
        sizer.Add(self.thirdcb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.thirdch = wx.Choice(dialog, choices = ["+", "++", "0", "1"])
        self.thirdch.SetToolTip('+ to activate while key is held, ++ to toggle, 0 to disable, 1 to enable')
        self.thirdch.SetSelection(0)
        sizer.Add(self.thirdch, 1, wx.ALIGN_CENTER_VERTICAL)

        centeringSizer.Add(sizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        return centeringSizer

    def MakeBindString(self):
        # choice 1, do this one at a time by hand;  choice 2, hack up some data-driven iterable.  I choose 1.
        bindstrings = []
        if self.camdistcb.IsChecked():
            bindstrings.append("camdist " + str(self.camdistsc.GetValue()))
        if self.camresetcb.IsChecked():
            bindstrings.append("camreset")
        if self.camrotatecb.IsChecked():
            camrotatevalue = "+"
            camrotateselection = self.camrotatech.GetSelection()
            if camrotateselection != wx.NOT_FOUND:
                camrotatevalue = self.camrotatech.GetString(camrotateselection)
            if camrotatevalue == '+' or camrotatevalue == '++':
                camrotcmd = f"{camrotatevalue}camrotate"
            else:
                camrotcmd = f"camrotate {camrotatevalue}"
            bindstrings.append(camrotcmd)
        if self.camturncb.IsChecked():
            bindstrings.append("camturn")
        if self.mouselookcb.IsChecked():
            mouselookvalue = "+"
            mouselookselection = self.mouselookch.GetSelection()
            if mouselookselection != wx.NOT_FOUND:
                mouselookvalue = self.mouselookch.GetString(mouselookselection)
            if mouselookvalue == '+' or mouselookvalue == '++':
                mlcmd = f"{mouselookvalue}mouselook"
            else:
                mlcmd = f"mouselook {mouselookvalue}"
            bindstrings.append(mlcmd)
        if self.lookupcb.IsChecked():
            lookupvalue = "+"
            lookupselection = self.lookupch.GetSelection()
            if lookupselection != wx.NOT_FOUND:
                lookupvalue = self.lookupch.GetString(lookupselection)
            if lookupvalue == '+' or lookupvalue == '++':
                lookupcmd = f"{lookupvalue}lookup"
            else:
                lookupcmd = f"lookup {lookupvalue}"
            bindstrings.append(lookupcmd)
        if self.lookdowncb.IsChecked():
            lookdownvalue = "+"
            lookdownselection = self.lookdownch.GetSelection()
            if lookdownselection != wx.NOT_FOUND:
                lookdownvalue = self.lookdownch.GetString(lookdownselection)
            if lookdownvalue == '+' or lookdownvalue == '++':
                lookdowncmd = f"{lookdownvalue}lookdown"
            else:
                lookdowncmd = f"lookdown {lookdownvalue}"
            bindstrings.append(lookdowncmd)
        if self.firstcb.IsChecked():
            firstvalue = "+"
            firstselection = self.firstch.GetSelection()
            if firstselection != wx.NOT_FOUND:
                firstvalue = self.firstch.GetString(firstselection)
            if firstvalue == '+' or firstvalue == '++':
                firstcmd = f"{firstvalue}first"
            else:
                firstcmd = f"first {firstvalue}"
            bindstrings.append(firstcmd)
        if self.thirdcb.IsChecked():
            thirdvalue = "+"
            thirdselection = self.thirdch.GetSelection()
            if thirdselection != wx.NOT_FOUND:
                thirdvalue = self.thirdch.GetString(thirdselection)
            if thirdvalue == '+' or thirdvalue == '++':
                thirdcmd = f"{thirdvalue}third"
            else:
                thirdcmd = f"third {thirdvalue}"
            bindstrings.append(thirdcmd)
        return '$$'.join(bindstrings)

    def Serialize(self):
        camrotatevalue = ""
        camrotateselection = self.camrotatech.GetSelection()
        if camrotateselection != wx.NOT_FOUND:
            camrotatevalue = self.camrotatech.GetString(camrotateselection)
        mouselookvalue = ""
        mouselookselection = self.mouselookch.GetSelection()
        if mouselookselection != wx.NOT_FOUND:
            mouselookvalue = self.mouselookch.GetString(mouselookselection)
        lookupvalue = ""
        lookupselection = self.lookupch.GetSelection()
        if lookupselection != wx.NOT_FOUND:
            lookupvalue = self.lookupch.GetString(lookupselection)
        lookdownvalue = ""
        lookdownselection = self.lookdownch.GetSelection()
        if lookdownselection != wx.NOT_FOUND:
            lookdownvalue = self.lookdownch.GetString(lookdownselection)
        firstvalue = ""
        firstselection = self.firstch.GetSelection()
        if firstselection != wx.NOT_FOUND:
            firstvalue = self.firstch.GetString(firstselection)
        thirdvalue = ""
        thirdselection = self.thirdch.GetSelection()
        if thirdselection != wx.NOT_FOUND:
            thirdvalue = self.thirdch.GetString(thirdselection)
        return {
            'camdistcb'   : self.camdistcb.IsChecked(),
            'camdistsc'   : self.camdistsc.GetValue(),
            'camresetcb'  : self.camresetcb.IsChecked(),
            'camrotatecb' : self.camrotatecb.IsChecked(),
            'camrotatech' : camrotatevalue,
            'camturncb'   : self.camturncb.IsChecked(),
            'mouselookcb' : self.mouselookcb.IsChecked(),
            'mouselookch' : mouselookvalue,
            'lookupcb'    : self.lookupcb.IsChecked(),
            'lookupch'    : lookupvalue,
            'lookdowncb'  : self.lookdowncb.IsChecked(),
            'lookdownch'  : lookdownvalue,
            'firstcb'     : self.firstcb.IsChecked(),
            'firstch'     : firstvalue,
            'thirdcb'     : self.thirdcb.IsChecked(),
            'thirdch'     : thirdvalue,
        }

    def Deserialize(self, init):
        self.camdistcb.SetValue(init.get('camdistcb', False))
        self.camdistsc.SetValue(init.get('camdistsc', 1.0))
        self.camresetcb.SetValue(init.get('camresetcb', False))
        self.camrotatecb.SetValue(init.get('camrotatecb', False))
        self.camrotatech.SetSelection(self.camrotatech.FindString(init.get('camrotatech', '')))
        self.camturncb.SetValue(init.get('camturncb', False))
        self.mouselookcb.SetValue(init.get('mouselookcb', False))
        self.mouselookch.SetSelection(self.mouselookch.FindString(init.get('mouselookch', '')))
        self.lookupcb.SetValue(init.get('lookupcb', False))
        self.lookupch.SetSelection(self.lookupch.FindString(init.get('lookupch', '')))
        self.lookdowncb.SetValue(init.get('lookdowncb', False))
        self.lookdownch.SetSelection(self.lookdownch.FindString(init.get('lookdownch', '')))
        self.firstcb.SetValue(init.get('firstcb', False))
        self.firstch.SetSelection(self.firstch.FindString(init.get('firstch', '')))
        self.thirdcb.SetValue(init.get('thirdcb', False))
        self.thirdch.SetSelection(self.thirdch.FindString(init.get('thirdch', '')))
