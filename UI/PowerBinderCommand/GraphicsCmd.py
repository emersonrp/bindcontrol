import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Graphics Command
class GraphicsCmd(PowerBinderCommand):
    Name = "Graphics Settings"
    Menu = "Graphics / UI"

    def BuildUI(self, dialog):
        sizer = wx.FlexGridSizer(2)

        self.visscalecb = wx.CheckBox(dialog, label = "visscale")
        sizer.Add(self.visscalecb)
        self.visscalesc = wx.SpinCtrlDouble(dialog, initial = 1.0, min = 0.5, max = 10, inc = 0.1)
        sizer.Add(self.visscalesc)

        self.dofweightcb = wx.CheckBox(dialog, label = "dofweight")
        sizer.Add(self.dofweightcb)
        self.dofweightsc = wx.SpinCtrlDouble(dialog, initial = 1.0, min = 0.5, max = 2.0, inc = 0.1)
        sizer.Add(self.dofweightsc)

        self.fsaacb = wx.CheckBox(dialog, label = "fsaa")
        sizer.Add(self.fsaacb)
        self.fsaach = wx.Choice(dialog, choices = ["0", "2", "4", "8"])
        self.fsaach.SetSelection(0)
        sizer.Add(self.fsaach)

        self.bloomscalecb = wx.CheckBox(dialog, label = "bloomscale")
        sizer.Add(self.bloomscalecb)
        self.bloomscalech = wx.Choice(dialog, choices = ["2", "4"])
        self.bloomscalech.SetSelection(0)
        sizer.Add(self.bloomscalech)

        self.bloomweightcb = wx.CheckBox(dialog, label = "bloomweight")
        sizer.Add(self.bloomweightcb)
        self.bloomweightsc = wx.SpinCtrlDouble(dialog, initial = 1.0, min = 0.0, max = 2.0, inc = 0.1)
        sizer.Add(self.bloomweightsc)

        self.lodbiascb = wx.CheckBox(dialog, label = "lodbias")
        sizer.Add(self.lodbiascb)
        self.lodbiassc = wx.SpinCtrlDouble(dialog, initial = 1.0, min = 0.3, max = 20.0, inc = 0.1)
        sizer.Add(self.lodbiassc)

        self.renderscalecb = wx.CheckBox(dialog, label = "renderscale")
        sizer.Add(self.renderscalecb)
        self.renderscalesc = wx.SpinCtrlDouble(dialog, initial = 1.0, min = 0.1, max = 20.0, inc = 0.1)
        sizer.Add(self.renderscalesc)

        return sizer

    def MakeBindString(self):
        # choice 1, do this one at a time by hand;  choice 2, hack up some data-driven iterable.  I choose 1.
        bindstrings = []
        if self.visscalecb.IsChecked():
            bindstrings.append("visscale " + str(self.visscalesc.GetValue()))
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
        if self.renderscalecb.IsChecked():
            bindstrings.append("renderscale " + str(self.renderscalesc.GetValue()))

        return '$$'.join(bindstrings)

    def Serialize(self):
        fsaavalue = ""
        fsaaselection = self.fsaach.GetSelection()
        if fsaaselection != wx.NOT_FOUND:
            fsaavalue = self.fsaach.GetString(fsaaselection)
        bloomscalevalue = ""
        bloomscaleselection = self.bloomscalech.GetSelection()
        if bloomscaleselection != wx.NOT_FOUND:
            bloomscalevalue = self.bloomscalech.GetString(bloomscaleselection)
        return {
            'visscalecb'    : self.visscalecb.IsChecked(),
            'visscalesc'    : self.visscalesc.GetValue(),
            'dofweightcb'   : self.dofweightcb.IsChecked(),
            'dofweightsc'   : self.dofweightsc.GetValue(),
            'fsaacb'        : self.fsaacb.IsChecked(),
            'fsaach'        : fsaavalue,
            'bloomscalecb'  : self.bloomscalecb.IsChecked(),
            'bloomscalech'  : bloomscalevalue,
            'bloomweightcb' : self.bloomweightcb.IsChecked(),
            'bloomweightsc' : self.bloomweightsc.GetValue(),
            'lodbiascb'     : self.lodbiascb.IsChecked(),
            'lodbiassc'     : self.lodbiassc.GetValue(),
            'renderscalecb' : self.renderscalecb.IsChecked(),
            'renderscalesc' : self.renderscalesc.GetValue(),
        }

    def Deserialize(self, init):
        self.visscalecb.SetValue(init.get('visscalecb', False))
        self.visscalesc.SetValue(init.get('visscalesc', 1.0))
        self.dofweightcb.SetValue(init.get('dofweightcb', False))
        self.dofweightsc.SetValue(init.get('dofweightsc', 1.0))
        self.fsaacb.SetValue(init.get('fsaacb', False))
        self.fsaach.SetSelection(self.fsaach.FindString(init.get('fsaach', '')))
        self.bloomscalecb.SetValue(init.get('bloomscalecb', False))
        self.bloomscalech.SetSelection(self.bloomscalech.FindString(init.get('bloomscalech', '')))
        self.bloomweightcb.SetValue(init.get('bloomweightcb', False))
        self.bloomweightsc.SetValue(init.get('bloomweightsc', 1.0))
        self.lodbiascb.SetValue(init.get('lodbiascb', False))
        self.lodbiassc.SetValue(init.get('lodbiassc', 1.0))
        self.renderscalecb.SetValue(init.get('renderscalecb', False))
        self.renderscalesc.SetValue(init.get('renderscalesc', 1.0))
