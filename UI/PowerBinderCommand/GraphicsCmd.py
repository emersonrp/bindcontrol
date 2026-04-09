import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Graphics Command
class GraphicsCmd(PowerBinderCommand):
    Name = "Graphics Settings"
    Menu = "Graphics / UI"

    def BuildUI(self, dialog) -> wx.BoxSizer:
        centeringSizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.FlexGridSizer(2)

        self.visscalecb = wx.CheckBox(dialog, label = "visscale")
        self.visscalecb.SetToolTip('Controls the distance at which world details are rendered (larger values render more details, farther away)')
        sizer.Add(self.visscalecb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.visscalesc = wx.SpinCtrlDouble(dialog, initial = 1.0, min = 0.5, max = 10, inc = 0.1)
        self.visscalesc.SetToolTip('Controls the distance at which world details are rendered (larger values render more details, farther away)')
        sizer.Add(self.visscalesc, 1, wx.ALIGN_CENTER_VERTICAL)

        self.usedofcb = wx.CheckBox(dialog, label = "usedof")
        self.usedofcb.SetToolTip('Enables or disables Depth of Field Effects')
        sizer.Add(self.usedofcb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.usedofch = wx.Choice(dialog, choices = ["0", "1"])
        self.usedofch.SetToolTip('Enables or disabany Depth of Field Effects')
        self.usedofch.SetSelection(0)
        sizer.Add(self.usedofch, 1, wx.ALIGN_CENTER_VERTICAL)

        self.dofweightcb = wx.CheckBox(dialog, label = "dofweight")
        self.dofweightcb.SetToolTip('Controls the distance for how "blurry" Depth of Field effects are - also enables /usedof 1')
        sizer.Add(self.dofweightcb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.dofweightcb.Bind(wx.EVT_CHECKBOX, self.OnDOFWeightCB)
        self.dofweightsc = wx.SpinCtrlDouble(dialog, initial = 1.0, min = 0.5, max = 2.0, inc = 0.1)
        self.dofweightsc.SetToolTip('Controls the distance for how "blurry" Depth of Field effects are - also enables /usedof 1')
        sizer.Add(self.dofweightsc, 1, wx.ALIGN_CENTER_VERTICAL)

        self.fsaacb = wx.CheckBox(dialog, label = "fsaa")
        self.fsaacb.SetToolTip('Sets the amount of full screen antialiasing')
        sizer.Add(self.fsaacb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.fsaach = wx.Choice(dialog, choices = ["0", "2", "4", "8"])
        self.fsaach.SetToolTip('Sets the amount of full screen antialiasing')
        self.fsaach.SetSelection(0)
        sizer.Add(self.fsaach, 1, wx.ALIGN_CENTER_VERTICAL)

        self.bloomscalecb = wx.CheckBox(dialog, label = "bloomscale")
        self.bloomscalecb.SetToolTip('Sets bloom blur scale (2 = Regular, 4 = Heavy)')
        sizer.Add(self.bloomscalecb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.bloomscalech = wx.Choice(dialog, choices = ["2", "4"])
        self.bloomscalech.SetToolTip('Sets bloom blur scale (2 = Regular, 4 = Heavy)')
        self.bloomscalech.SetSelection(0)
        sizer.Add(self.bloomscalech, 1, wx.ALIGN_CENTER_VERTICAL)

        self.bloomweightcb = wx.CheckBox(dialog, label = "bloomweight")
        self.bloomweightcb.SetToolTip('Sets bloom amount')
        sizer.Add(self.bloomweightcb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.bloomweightsc = wx.SpinCtrlDouble(dialog, initial = 1.0, min = 0.0, max = 2.0, inc = 0.1)
        self.bloomweightsc.SetToolTip('Sets bloom amount')
        sizer.Add(self.bloomweightsc, 1, wx.ALIGN_CENTER_VERTICAL)

        self.lodbiascb = wx.CheckBox(dialog, label = "lodbias")
        self.lodbiascb.SetToolTip('Sets "Loss of Detail" distance for entites (larger values retain detail farther)')
        sizer.Add(self.lodbiascb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.lodbiassc = wx.SpinCtrlDouble(dialog, initial = 1.0, min = 0.3, max = 20.0, inc = 0.1)
        self.lodbiassc.SetToolTip('Sets "Loss of Detail" distance for entites (larger values retain detail farther)')
        sizer.Add(self.lodbiassc, 1, wx.ALIGN_CENTER_VERTICAL)

        self.userenderscalecb = wx.CheckBox(dialog, label = "userenderscale")
        self.userenderscalecb.SetToolTip('Enables or disables any 3D rendering scaling')
        sizer.Add(self.userenderscalecb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.userenderscalech = wx.Choice(dialog, choices = ["0", "1"])
        self.userenderscalech.SetToolTip('Enables or disabany 3D rendering scaling')
        self.userenderscalech.SetSelection(0)
        sizer.Add(self.userenderscalech, 1, wx.ALIGN_CENTER_VERTICAL)

        self.renderscalecb = wx.CheckBox(dialog, label = "renderscale")
        self.renderscalecb.SetToolTip('Changes the scale at which the 3D world is rendered relative to your screen size - also enables /userenderscale 1')
        sizer.Add(self.renderscalecb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.renderscalecb.Bind(wx.EVT_CHECKBOX, self.OnRenderScaleCB)
        self.renderscalesc = wx.SpinCtrlDouble(dialog, initial = 1.0, min = 0.1, max = 20.0, inc = 0.1)
        self.renderscalesc.SetToolTip('Changes the scale at which the 3D world is rendered relative to your screen size - also enables /userenderscale 1')
        sizer.Add(self.renderscalesc, 1, wx.ALIGN_CENTER_VERTICAL)

        self.usecelshadercb = wx.CheckBox(dialog, label = "usecelshader")
        self.usecelshadercb.SetToolTip('Enables or disables the cel shader graphics setting that attempts to mimic a "comic book look"')
        sizer.Add(self.usecelshadercb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.usecelshaderch = wx.Choice(dialog, choices = ["0", "1"])
        self.usecelshaderch.SetToolTip('Enables or disables the cel shader graphics setting that attempts to mimic a "comic book look"')
        self.usecelshaderch.SetSelection(0)
        sizer.Add(self.usecelshaderch, 1, wx.ALIGN_CENTER_VERTICAL)

        self.usehdrcb = wx.CheckBox(dialog, label = "usehdr")
        self.usehdrcb.SetToolTip('Use HDR Lighting effects (bloom / tonemapping) if available')
        sizer.Add(self.usehdrcb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.usehdrch = wx.Choice(dialog, choices = ["0", "1"])
        self.usehdrch.SetToolTip('Use HDR Lighting effects (bloom / tonemapping) if available')
        self.usehdrch.SetSelection(0)
        sizer.Add(self.usehdrch, 1, wx.ALIGN_CENTER_VERTICAL)

        centeringSizer.Add(sizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        return centeringSizer

    def OnDOFWeightCB(self, evt):
        evt.Skip()
        if self.dofweightcb.IsChecked():
            self.usedofcb.SetValue(True)
            self.usedofch.SetSelection(1)

    def OnRenderScaleCB(self, evt):
        evt.Skip()
        if self.renderscalecb.IsChecked():
            self.userenderscalecb.SetValue(True)
            self.userenderscalech.SetSelection(1)

    def MakeBindString(self) -> str:
        # choice 1, do this one at a time by hand;  choice 2, hack up some data-driven iterable.  I choose 1.
        bindstrings = []
        if self.visscalecb.IsChecked():
            bindstrings.append("visscale " + str(self.visscalesc.GetValue()))
        if self.usedofcb.IsChecked():
            usedofvalue = ""
            usedofselection = self.usedofch.GetSelection()
            if usedofselection != wx.NOT_FOUND:
                usedofvalue = self.usedofch.GetString(usedofselection)
            bindstrings.append("usedof " + usedofvalue)
        if self.dofweightcb.IsChecked():
            bindstrings.append("dofweight " + str(self.dofweightsc.GetValue()))
        if self.fsaacb.IsChecked():
            fsaavalue = ""
            fsaaselection = self.fsaach.GetSelection()
            if fsaaselection != wx.NOT_FOUND:
                fsaavalue = self.fsaach.GetString(fsaaselection)
            bindstrings.append("fsaa " + fsaavalue)
        if self.bloomscalecb.IsChecked():
            bloomscalevalue = ""
            bloomscaleselection = self.bloomscalech.GetSelection()
            if bloomscaleselection != wx.NOT_FOUND:
                bloomscalevalue = self.bloomscalech.GetString(bloomscaleselection)
            bindstrings.append("bloomscale " + bloomscalevalue)
        if self.bloomweightcb.IsChecked():
            bindstrings.append("bloomweight " + str(self.bloomweightsc.GetValue()))
        if self.lodbiascb.IsChecked():
            bindstrings.append("lodbias " + str(self.lodbiassc.GetValue()))
        if self.userenderscalecb.IsChecked():
            userenderscalevalue = ""
            userenderscaleselection = self.userenderscalech.GetSelection()
            if userenderscaleselection != wx.NOT_FOUND:
                userenderscalevalue = self.userenderscalech.GetString(userenderscaleselection)
            bindstrings.append("userenderscale " + userenderscalevalue)
        if self.renderscalecb.IsChecked():
            bindstrings.append("renderscale " + str(self.renderscalesc.GetValue()))
        if self.usecelshadercb.IsChecked():
            usecelshadervalue = ""
            usecelshaderselection = self.usecelshaderch.GetSelection()
            if usecelshaderselection != wx.NOT_FOUND:
                usecelshadervalue = self.usecelshaderch.GetString(usecelshaderselection)
            bindstrings.append("usecelshader " + usecelshadervalue)
        if self.usehdrcb.IsChecked():
            usehdrvalue = ""
            usehdrselection = self.usehdrch.GetSelection()
            if usehdrselection != wx.NOT_FOUND:
                usehdrvalue = self.usehdrch.GetString(usehdrselection)
            bindstrings.append("usehdr " + usehdrvalue)

        return '$$'.join(bindstrings)

    def Serialize(self) -> dict:
        usedofvalue = ""
        usedofselection = self.usedofch.GetSelection()
        if usedofselection != wx.NOT_FOUND:
            usedofvalue = self.usedofch.GetString(usedofselection)
        fsaavalue = ""
        fsaaselection = self.fsaach.GetSelection()
        if fsaaselection != wx.NOT_FOUND:
            fsaavalue = self.fsaach.GetString(fsaaselection)
        bloomscalevalue = ""
        bloomscaleselection = self.bloomscalech.GetSelection()
        if bloomscaleselection != wx.NOT_FOUND:
            bloomscalevalue = self.bloomscalech.GetString(bloomscaleselection)
        userenderscalevalue = ""
        userenderscaleselection = self.userenderscalech.GetSelection()
        if userenderscaleselection != wx.NOT_FOUND:
            userenderscalevalue = self.userenderscalech.GetString(userenderscaleselection)
        usecelshadervalue = ""
        usecelshaderselection = self.usecelshaderch.GetSelection()
        if usecelshaderselection != wx.NOT_FOUND:
            usecelshadervalue = self.usecelshaderch.GetString(usecelshaderselection)
        usehdrvalue = ""
        usehdrselection = self.usehdrch.GetSelection()
        if usehdrselection != wx.NOT_FOUND:
            usehdrvalue = self.usehdrch.GetString(usehdrselection)
        return {
            'visscalecb'       : self.visscalecb.IsChecked(),
            'visscalesc'       : self.visscalesc.GetValue(),
            'usedofcb'         : self.usedofcb.IsChecked(),
            'usedofch'         : usedofvalue,
            'dofweightcb'      : self.dofweightcb.IsChecked(),
            'dofweightsc'      : self.dofweightsc.GetValue(),
            'fsaacb'           : self.fsaacb.IsChecked(),
            'fsaach'           : fsaavalue,
            'bloomscalecb'     : self.bloomscalecb.IsChecked(),
            'bloomscalech'     : bloomscalevalue,
            'bloomweightcb'    : self.bloomweightcb.IsChecked(),
            'bloomweightsc'    : self.bloomweightsc.GetValue(),
            'lodbiascb'        : self.lodbiascb.IsChecked(),
            'lodbiassc'        : self.lodbiassc.GetValue(),
            'userenderscalecb' : self.userenderscalecb.IsChecked(),
            'userenderscalech' : userenderscalevalue,
            'renderscalecb'    : self.renderscalecb.IsChecked(),
            'renderscalesc'    : self.renderscalesc.GetValue(),
            'usecelshadercb'   : self.usecelshadercb.IsChecked(),
            'usecelshaderch'   : usecelshadervalue,
            'usehdrcb'         : self.usehdrcb.IsChecked(),
            'usehdrch'         : usehdrvalue,
        }

    def Deserialize(self, init) -> None:
        self.visscalecb.SetValue(init.get('visscalecb', False))
        self.visscalesc.SetValue(init.get('visscalesc', 1.0))
        self.usedofcb.SetValue(init.get('usedofcb', False))
        self.usedofch.SetStringSelection(init.get('usedofch', ''))
        self.dofweightcb.SetValue(init.get('dofweightcb', False))
        self.dofweightsc.SetValue(init.get('dofweightsc', 1.0))
        self.fsaacb.SetValue(init.get('fsaacb', False))
        self.fsaach.SetStringSelection(init.get('fsaach', ''))
        self.bloomscalecb.SetValue(init.get('bloomscalecb', False))
        self.bloomscalech.SetStringSelection(init.get('bloomscalech', ''))
        self.bloomweightcb.SetValue(init.get('bloomweightcb', False))
        self.bloomweightsc.SetValue(init.get('bloomweightsc', 1.0))
        self.lodbiascb.SetValue(init.get('lodbiascb', False))
        self.lodbiassc.SetValue(init.get('lodbiassc', 1.0))
        self.userenderscalecb.SetValue(init.get('userenderscalecb', False))
        self.userenderscalech.SetStringSelection(init.get('userenderscalech', ''))
        self.renderscalecb.SetValue(init.get('renderscalecb', False))
        self.renderscalesc.SetValue(init.get('renderscalesc', 1.0))
        self.usecelshadercb.SetValue(init.get('usecelshadercb', False))
        self.usecelshaderch.SetStringSelection(init.get('usecelshaderch', ''))
        self.usehdrcb.SetValue(init.get('usehdrcb', False))
        self.usehdrch.SetStringSelection(init.get('usehdrch', ''))
