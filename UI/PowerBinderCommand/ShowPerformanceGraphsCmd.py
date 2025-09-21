import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Window Save / Load
class ShowPerformanceGraphsCmd(PowerBinderCommand):
    Name = "Performance Graphs"
    Menu = "Graphics / UI"

    def BuildUI(self, dialog) -> wx.BoxSizer:
        CenteringSizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.FlexGridSizer(2, 3, 3)

        self.FPSEnable = wx.CheckBox(dialog, wx.ID_ANY, 'Show FPS')
        self.FPSEnable.Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        sizer.Add(self.FPSEnable, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.FPSChoice = wx.Choice(dialog, wx.ID_ANY,
                                   choices = ['Camera POS/PYR', 'FPS Only', 'FPS + POS/PYR', 'FPS + large POS/PYR', 'Off'])
        self.FPSChoice.SetSelection(4)
        sizer.Add(self.FPSChoice, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.NetgraphEnable = wx.CheckBox(dialog, wx.ID_ANY, 'Show Netgraph')
        self.NetgraphEnable.Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        sizer.Add(self.NetgraphEnable, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.NetgraphChoice = wx.Choice(dialog, wx.ID_ANY, choices = ['Off', 'Small', 'Large'])
        self.NetgraphChoice.SetSelection(0)
        sizer.Add(self.NetgraphChoice, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.FPSGraphEnable = wx.CheckBox(dialog, wx.ID_ANY, 'Show FPS Graph')
        self.FPSGraphEnable.Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        sizer.Add(self.FPSGraphEnable, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        fpsgraphboxes = wx.BoxSizer(wx.HORIZONTAL)
        self.FPSGraphSwap = wx.CheckBox(dialog, wx.ID_ANY, 'Swap')
        fpsgraphboxes.Add(self.FPSGraphSwap, 0, wx.ALL, 3)
        self.FPSGraphGPU = wx.CheckBox(dialog, wx.ID_ANY, 'GPU')
        fpsgraphboxes.Add(self.FPSGraphGPU, 0, wx.ALL, 3)
        self.FPSGraphCPU = wx.CheckBox(dialog, wx.ID_ANY, 'CPU')
        fpsgraphboxes.Add(self.FPSGraphCPU, 0, wx.ALL, 3)
        self.FPSGraphSLI = wx.CheckBox(dialog, wx.ID_ANY, 'SLI')
        fpsgraphboxes.Add(self.FPSGraphSLI, 0, wx.ALL, 3)
        sizer.Add(fpsgraphboxes, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)


        CenteringSizer.Add(sizer, 1, wx.ALIGN_CENTER_HORIZONTAL)
        self.SynchronizeUI()
        return CenteringSizer

    def MakeBindString(self) -> str:
        commands = []
        if self.FPSEnable.IsChecked():
            sel = self.FPSChoice.GetSelection()
            if sel == 4:
                commands.append("-setfps")
            else:
                commands.append(f'setfps {sel}')

        if self.NetgraphEnable.IsChecked():
            commands.append(f"netgraph {self.NetgraphChoice.GetSelection()}")

        if self.FPSGraphEnable.IsChecked():
            fpsgraphval = 0
            if self.FPSGraphSwap.IsChecked(): fpsgraphval += 1
            if self.FPSGraphGPU .IsChecked(): fpsgraphval += 2
            if self.FPSGraphCPU .IsChecked(): fpsgraphval += 4
            if self.FPSGraphSLI .IsChecked(): fpsgraphval += 8
            commands.append(f"graphfps {fpsgraphval}")

        return '$$'.join(commands)

    def Serialize(self) -> dict:
        return {
            'fpsenable'      : self.FPSEnable.IsChecked(),
            'fpschoice'      : self.FPSChoice.GetSelection(),
            'netgraphenable' : self.NetgraphEnable.IsChecked(),
            'netgraphchoice' : self.NetgraphChoice.GetSelection(),
            'fpsgraphenable' : self.FPSGraphEnable.IsChecked(),
            'fpsgraphswap'   : self.FPSGraphSwap.IsChecked(),
            'fpsgraphgpu'    : self.FPSGraphGPU.IsChecked(),
            'fpsgraphcpu'    : self.FPSGraphCPU.IsChecked(),
            'fpsgraphsli'    : self.FPSGraphSLI.IsChecked(),
        }

    def Deserialize(self, init) -> None:
        self.FPSEnable.SetValue(init.get('fpsenable', False))
        self.FPSChoice.SetSelection(init.get('fpschoice', 0))
        self.NetgraphEnable.SetValue(init.get('netgraphenable', False))
        self.NetgraphChoice.SetSelection(init.get('netgraphchoice', 0))
        self.FPSGraphEnable.SetValue(init.get('fpsgraphenable', 0))
        self.FPSGraphSwap.SetValue(init.get('fpsgraphswap', 0))
        self.FPSGraphGPU.SetValue(init.get('fpsgraphgpu', 0))
        self.FPSGraphCPU.SetValue(init.get('fpsgraphcpu', 0))
        self.FPSGraphSLI.SetValue(init.get('fpsgraphsli', 0))

        self.SynchronizeUI()

    def SynchronizeUI(self, evt = None) -> None:
        if evt: evt.Skip()
        self.FPSChoice.Enable(self.FPSEnable.IsChecked())
        self.NetgraphChoice.Enable(self.NetgraphEnable.IsChecked())
        self.FPSGraphSwap.Enable(self.FPSGraphEnable.IsChecked())
        self.FPSGraphGPU.Enable(self.FPSGraphEnable.IsChecked())
        self.FPSGraphCPU.Enable(self.FPSGraphEnable.IsChecked())
        self.FPSGraphSLI.Enable(self.FPSGraphEnable.IsChecked())
