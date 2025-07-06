import re
import wx
import UI
from UI.CustomBindPaneParent import CustomBindPaneParent
from UI.KeySelectDialog import bcKeyButton, EVT_KEY_CHANGED
from UI.PowerBinderDialog import PowerBinderButton
from UI.ControlGroup import cgTextCtrl

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
        setattr(pane, 'Page', page)

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

        self.BindSizer.Add (self.BindStepSizer, 1, wx.EXPAND)

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

        self.RenumberSteps()
        self.checkIfWellFormed()

    def onContentsChanged(self, _):
        self.Profile.SetModified()
        self.checkIfWellFormed()

    def onKeyChanged(self, _):
        self.Profile.SetModified()
        self.checkIfWellFormed()
        if self.Profile:
            self.Profile.CheckAllConflicts()

    def checkIfWellFormed(self):
        isWellFormed = True

        # TODO - check each step for > 255 char
        firststep = self.Steps[0].BindContents
        fullsteps = list(filter(lambda x: x.BindContents.GetValue(), self.Steps))
        if fullsteps:
            firststep.RemoveError('undef')
        else:
            firststep.AddError('undef', 'At least one step must be defined')
            isWellFormed = False

        stepsWellFormed = True
        for step in self.Steps:
            if len(step.BindContents.GetValue()) <= 255:
                step.BindContents.RemoveError('length')
            else:
                step.BindContents.AddError('length', 'This step is longer than 255 characters, which will cause problems in-game.')
                stepsWellFormed = False

        if (not stepsWellFormed): isWellFormed = False

        bk = self.Ctrls[self.MakeCtlName('BindKey')]
        if not bk.Key:
            bk.AddError('undef', 'The keybind has not been selected')
            isWellFormed = False
        else:
            bk.RemoveError('undef')

        return isWellFormed

    def onAddStepButton(self, _ = None, stepdata = {}):
        stepNumber = self.BindStepSizer.GetItemCount() # already the next step because of the add button
        step = BindStep(self, stepNumber, stepdata)
        self.BindStepSizer.Insert(self.BindStepSizer.GetItemCount()-1, step, 0, wx.EXPAND)
        self.Steps.append(step)
        self.Profile.SetModified()
        self.RenumberSteps()

    def onMoveUpButton(self, evt):
        button = evt.GetEventObject()
        step = button.GetParent()
        idx = self.Steps.index(step)
        self.BindStepSizer.Detach(idx)
        self.BindStepSizer.Insert(idx-1, self.Steps[idx], 0, wx.EXPAND)
        self.Steps[idx], self.Steps[idx-1] = self.Steps[idx-1], self.Steps[idx]
        self.Profile.SetModified()
        self.RenumberSteps()

    def onMoveDownButton(self, evt):
        button = evt.GetEventObject()
        step = button.GetParent()
        idx = self.Steps.index(step)
        self.BindStepSizer.Detach(idx)
        self.BindStepSizer.Insert(idx+1, self.Steps[idx], 0, wx.EXPAND)
        self.Steps[idx], self.Steps[idx+1] = self.Steps[idx+1], self.Steps[idx]
        self.Profile.SetModified()
        self.RenumberSteps()

    def onDelButton(self, evt):
        button = evt.GetEventObject()
        step = button.GetParent()
        self.Steps.remove(step)
        step.Destroy()
        self.Profile.SetModified()
        self.RenumberSteps()

    def RenumberSteps(self):
        for i, step in enumerate(self.Steps, start = 1):
            step.moveUpButton.Enable(i > 1)
            step.moveDownButton.Enable(i < len(self.Steps))
            step.StepLabel.SetLabel(f"Step {i}:")
        self.Page.Layout()

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

    def AllBindFiles(self):
        files = []
        title = re.sub(r'\W+', '', self.Title)
        for i, _ in enumerate(self.Steps, start = 1):
            files.append(self.Profile.GetBindFile('cbinds', f'{title}-{i}.txt'))

        return {
            'files' : files,
            'dirs'  : ['cbinds'],
        }

class BindStep(wx.Panel):
    def __init__(self, parent, stepNumber, step):

        self.Page = parent.Page
        pane = parent.GetPane()

        super().__init__(pane)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        StepLabel = wx.StaticText(self, -1, f"Step {stepNumber}:")
        self.StepLabel = StepLabel
        sizer.Add(StepLabel, 0, wx.ALIGN_CENTER_VERTICAL)

        BindContents = cgTextCtrl(self, -1, step.get('contents', ''))
        self.BindContents = BindContents
        sizer.Add(BindContents, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        self.BindContents.Bind(wx.EVT_TEXT, parent.onContentsChanged)

        self.PowerBinder = PowerBinderButton(self, BindContents, step.get('powerbinderdata', {}))
        sizer.Add(self.PowerBinder, 0)

        self.moveUpButton = wx.Button(self, -1, '\u25B2', size = wx.Size(40, -1))
        self.moveUpButton.Bind(wx.EVT_BUTTON, parent.onMoveUpButton)
        sizer.Add(self.moveUpButton, 0)

        self.moveDownButton = wx.Button(self, -1, '\u25BC', size = wx.Size(40, -1))
        self.moveDownButton.Bind(wx.EVT_BUTTON, parent.onMoveDownButton)
        sizer.Add(self.moveDownButton, 0)

        delButton = wx.Button(self, -1, "X", size = wx.Size(40,-1))
        delButton.SetForegroundColour(wx.RED)
        delButton.Bind(wx.EVT_BUTTON, parent.onDelButton)
        sizer.Add(delButton, 0)

        self.SetSizer(sizer)
