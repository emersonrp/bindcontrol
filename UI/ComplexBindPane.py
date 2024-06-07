import re
import wx
import UI
from UI.CustomBindPaneParent import CustomBindPaneParent
from UI.KeySelectDialog import bcKeyButton, EVT_KEY_CHANGED
from UI.PowerBinderDialog import PowerBinderButton

class ComplexBindPane(CustomBindPaneParent):
    def __init__(self, page, init = {}):
        CustomBindPaneParent.__init__(self, page, init)

        self.Steps = []

    def Serialize(self):
        data = {
            'Type' : 'ComplexBind',
            'Title': self.Title,
            'Key'  : self.Ctrls[self.MakeCtlName('BindKey')].Key,
            'Steps': [],
        }
        for step in self.Steps:
            if step.BindContents.GetValue():
                data['Steps'].append({
                    'contents'        : step.BindContents.GetValue(),
                    'powerbinderdata' : step.PowerBinder.SaveToData()
                })
        return data

    def BuildBindUI(self, page):
        pane = self.GetPane()

        self.BindSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.BindStepSizer = wx.BoxSizer(wx.VERTICAL)
        AddBindStepButton = wx.Button(pane, -1, "Add Step...")
        AddBindStepButton.Bind(wx.EVT_BUTTON, self.onAddStepButton)
        self.BindStepSizer.Add(AddBindStepButton, 0, wx.TOP, 10)
        if self.Init.get('Steps', ''):
            for step in self.Init['Steps']:
                self.onAddStepButton(None, step)
        else:
            self.onAddStepButton()

        self.BindSizer.Add ( self.BindStepSizer, 1, wx.EXPAND)

        BindKeyCtrl = bcKeyButton(pane, -1, {
            'CtlName' : self.MakeCtlName('BindKey'),
            'Page'    : page,
            'Key'     : self.Init.get('Key', ''),
        })
        BindKeyCtrl.Bind(EVT_KEY_CHANGED, self.onKeyChanged)

        BindKeySizer = wx.BoxSizer(wx.HORIZONTAL)
        BindKeySizer.Add(wx.StaticText(pane, -1, "Bind Key:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)
        BindKeySizer.Add(BindKeyCtrl,                          0)
        self.BindSizer.Add(BindKeySizer, 0, wx.LEFT|wx.RIGHT, 10)
        self.Ctrls[BindKeyCtrl.CtlName] = BindKeyCtrl
        UI.Labels[BindKeyCtrl.CtlName] = f'Complex Bind "{self.Title}"'

        self.BindSizer.Layout()

        # border around the addr box
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(self.BindSizer, 1, wx.EXPAND|wx.ALL, 10)
        pane.SetSizer(border)

        self.checkIfWellFormed()

    def onContentsChanged(self, _):
        self.checkIfWellFormed()

    def onKeyChanged(self, _):
        self.checkIfWellFormed()
        if self.Profile:
            self.Profile.CheckAllConflicts()

    def checkIfWellFormed(self):
        isWellFormed = True

        # TODO - check each step for > 255 char
        firststep = self.Steps[0].BindContents
        fullsteps = list(filter(lambda x: x.BindContents.GetValue(), self.Steps))
        if fullsteps:
            firststep.SetBackgroundColour(wx.NullColour)
        else:
            firststep.SetBackgroundColour((255,200,200))
            isWellFormed = False

        bk = self.Ctrls[self.MakeCtlName('BindKey')]
        if bk.Key:
            bk.SetError(False)
        else:
            bk.SetError(True)
            isWellFormed = False

        return isWellFormed

    def onAddStepButton(self, _ = None, stepdata = {}):
        pane = self.GetPane()
        pane.Page = self.Page
        step = self.MakeBindStepUI(pane, stepdata)
        step.BindContents.Bind(wx.EVT_TEXT, self.onContentsChanged)
        self.BindStepSizer.Insert(self.BindStepSizer.GetItemCount()-1, step, 0, wx.EXPAND)
        self.Steps.append(step)
        self.Page.Layout()
        self.Profile.SetModified()

    def MakeBindStepUI(self, parent, step):
        stepNumber = self.BindStepSizer.GetItemCount() # is already the next step because of the add button
        panel = wx.Panel(parent)
        panel.Page = parent.Page
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        StepLabel = wx.StaticText(panel, -1, f"Step {stepNumber}:")
        setattr(panel, 'StepLabel', StepLabel)
        sizer.Add(StepLabel, 0, wx.ALIGN_CENTER_VERTICAL)

        BindContents = wx.TextCtrl(panel, -1, step.get('contents', ''))
        setattr(panel, 'BindContents', BindContents)
        sizer.Add(BindContents, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        PowerBinder = PowerBinderButton(panel, BindContents, step.get('powerbinderdata', {}))
        setattr(panel, 'PowerBinder', PowerBinder)
        sizer.Add(PowerBinder, 0)

        delButton = wx.Button(panel, -1, "X", size = (40,-1))
        delButton.SetForegroundColour(wx.RED)
        delButton.Bind(wx.EVT_BUTTON, self.onDelButton)
        sizer.Add(delButton, 0)

        panel.SetSizer(sizer)

        return panel

    def onDelButton(self, evt):
        button = evt.EventObject
        step = button.GetParent()
        self.Steps.remove(step)
        step.Destroy()
        self.RenumberSteps()
        self.Page.Layout()
        self.Profile.SetModified()

    def RenumberSteps(self):
        for i, step in enumerate(self.Steps, start = 1):
            step.StepLabel.SetLabel(f"Step {i}:")
        #self.Layout()

    def PopulateBindFiles(self):
        if not self.checkIfWellFormed():
            wx.MessageBox(f"Custom Bind \"{self.Title}\" is not complete or has errors.  Not written to bindfile.")
            return

        resetfile = self.Profile.ResetFile()
        # fish out only the steps that have contents
        fullsteps = list(filter(lambda x: x.BindContents.GetValue(), self.Steps))
        title = re.sub(r'\W+', '', self.Title)
        for i, step in enumerate(fullsteps, start = 1):
            cbindfile = self.Profile.GetBindFile("cbinds", f"{title}-{i}.txt")
            nextCycle = 1 if (i+1 > len(fullsteps)) else i+1

            cmd = [step.BindContents.GetValue(), self.Profile.BLF(f'cbinds\\{title}-{nextCycle}.txt')]
            key = self.Ctrls[self.MakeCtlName('BindKey')].Key

            if i == 1: resetfile.SetBind(key, self, title, cmd)
            cbindfile.SetBind(key, self, title, cmd)
