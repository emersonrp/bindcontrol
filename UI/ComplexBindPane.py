import re
import wx
import UI
from UI.CustomBindPaneParent import CustomBindPaneParent
from UI.KeySelectDialog import bcKeyButton, EVT_KEY_CHANGED
from UI.PowerBinder import PowerBinder
from Icon import GetIcon

class ComplexBindPane(CustomBindPaneParent):
    def __init__(self, page, init : dict|None = None) -> None:
        init = init or {}
        super().__init__(page, init)

        self.Description = "Complex Bind"
        self.Type        = "ComplexBind"

        self.Steps = []

    def Serialize(self) -> dict[str, str|list]:
        data = self.CreateSerialization({
            'Key'  : self.GetCtrl('BindKey').Key,
            'Steps': [],
        })
        for step in self.Steps:
            if step.PowerBinder.GetValue():
                data['Steps'].append({
                    'contents'        : step.PowerBinder.GetValue(),
                    'powerbinderdata' : step.PowerBinder.SaveToData()
                })
        return data

    def BuildBindUI(self, page) -> None:
        pane = self.GetPane()
        self.Page = page

        self.BindSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.BindStepSizer = wx.BoxSizer(wx.VERTICAL)
        AddBindStepButton = wx.Button(pane, label = "Add Step")
        AddBindStepButton.Bind(wx.EVT_BUTTON, self.onAddStepButton)
        self.BindStepSizer.Add(AddBindStepButton, 0, wx.TOP, 10)
        if self.Init.get('Steps', ''):
            for step in self.Init['Steps']:
                self.doAddStep(step)
        else:
            self.doAddStep()

        self.BindSizer.Add (self.BindStepSizer, 1, wx.EXPAND)

        BindKeyCtrl = bcKeyButton(pane, init = {
            'CtlName' : self.MakeCtrlName('BindKey'),
            'Page'    : page,
            'Key'     : self.Init.get('Key', ''),
        })
        BindKeyCtrl.Bind(EVT_KEY_CHANGED, self.onKeyChanged)

        BindKeySizer = wx.BoxSizer(wx.HORIZONTAL)
        BindKeySizer.Add(wx.StaticText(pane, label = "Bind Key:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)
        BindKeySizer.Add(BindKeyCtrl,                          0)
        self.BindSizer.Add(BindKeySizer, 0, wx.LEFT|wx.RIGHT, 10)
        self.SetCtrl('BindKey', BindKeyCtrl)
        UI.Labels[BindKeyCtrl.CtlName] = f'Complex Bind "{self.Title}"'

        self.BindSizer.Layout()

        # border around the addr box
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(self.BindSizer, 1, wx.EXPAND|wx.ALL, 10)
        pane.SetSizer(border)

        self.RenumberSteps()
        self.CheckIfWellFormed()

    def onContentsChanged(self, evt) -> None:
        evt.Skip()
        self.CheckIfWellFormed()

    def onKeyChanged(self, evt) -> None:
        evt.Skip()
        self.CheckIfWellFormed()

    def CheckIfWellFormed(self) -> bool:
        isWellFormed = True

        firststep = self.Steps[0]
        fullsteps = list(filter(lambda x: x.PowerBinder.GetValue(), self.Steps))
        if fullsteps:
            firststep.PowerBinder.RemoveError('undef')
        else:
            firststep.PowerBinder.AddError('undef', 'At least one step must be defined')
            isWellFormed = False

        stepsWellFormed = True
        for step in self.Steps:
            if len(step.PowerBinder.GetValue()) + step.PowerBinder.ExtraLength <= 255:
                step.PowerBinder.RemoveError('length')
            else:
                step.PowerBinder.AddError('length', 'This step, when written to file, will be longer than 255 characters, which will cause problems in-game.')
                stepsWellFormed = False

        if (not stepsWellFormed): isWellFormed = False

        bk = self.GetCtrl('BindKey')
        if not bk.Key:
            bk.AddError('undef', 'The keybind has not been selected')
            isWellFormed = False
        else:
            bk.RemoveError('undef')

        return isWellFormed

    def onAddStepButton(self, _ = None, stepdata : dict|None = None) -> None:
        self.doAddStep(stepdata or {})
        self.Page.UpdateAllBinds()

    def doAddStep(self, stepdata : dict|None = None) -> None:
        stepdata = stepdata or {}
        stepNumber = self.BindStepSizer.GetItemCount() # already the next step because of the add button
        step = BindStep(self, stepNumber, stepdata)
        self.BindStepSizer.Insert(self.BindStepSizer.GetItemCount()-1, step, 0, wx.EXPAND)
        self.Steps.append(step)
        self.RenumberSteps()

    def onMoveUpButton(self, evt) -> None:
        button = evt.GetEventObject()
        step = button.GetParent()
        idx = self.Steps.index(step)
        self.BindStepSizer.Detach(idx)
        self.BindStepSizer.Insert(idx-1, self.Steps[idx], 0, wx.EXPAND)
        self.Steps[idx], self.Steps[idx-1] = self.Steps[idx-1], self.Steps[idx]
        self.Page.UpdateAllBinds()
        self.RenumberSteps()

    def onMoveDownButton(self, evt) -> None:
        button = evt.GetEventObject()
        step = button.GetParent()
        idx = self.Steps.index(step)
        self.BindStepSizer.Detach(idx)
        self.BindStepSizer.Insert(idx+1, self.Steps[idx], 0, wx.EXPAND)
        self.Steps[idx], self.Steps[idx+1] = self.Steps[idx+1], self.Steps[idx]
        self.Page.UpdateAllBinds()
        self.RenumberSteps()

    def onDupeButton(self, evt) -> None:
        button = evt.GetEventObject()
        step = button.GetParent()
        stepidx = self.Steps.index(step)
        data = {
            'contents'        : step.PowerBinder.GetValue(),
            'powerbinderdata' : step.PowerBinder.SaveToData()
        }
        newstep = BindStep(self, stepidx+1, data)
        self.BindStepSizer.Insert(stepidx+1, newstep, 0, wx.EXPAND)
        self.Steps.insert(stepidx+1, newstep)
        self.Page.UpdateAllBinds()
        self.RenumberSteps()

    def onDelButton(self, evt) -> None:
        button = evt.GetEventObject()
        step = button.GetParent()
        self.Steps.remove(step)
        step.DestroyLater()
        self.Page.UpdateAllBinds()
        self.RenumberSteps()

    def RenumberSteps(self) -> None:
        for i, step in enumerate(self.Steps, start = 1):
            step.delButton.Show(i>1) # don't even show the del button on step 1
            step.moveUpButton.Enable(i > 1)
            step.moveDownButton.Enable(i < len(self.Steps))
            step.StepLabel.SetLabel(f"Step {i}:")
        self.Page.Layout()

    def PopulateBindFiles(self) -> None:
        resetfile = self.Profile.ResetFile()
        # fish out only the steps that have contents
        fullsteps = list(filter(lambda x: x.PowerBinder.GetValue(), self.Steps))
        title = re.sub(r'\W+', '', self.Title)
        cid = self.CustomID
        for i, step in enumerate(fullsteps, start = 1):
            cbindfile = self.Profile.GetBindFile("cb", f"{cid}-{i}.txt")
            nextCycle = 1 if (i+1 > len(fullsteps)) else i+1

            cmd = [step.PowerBinder.GetValue(), self.Profile.BLF(f'cb\\{cid}-{nextCycle}.txt')]
            key = self.GetCtrl('BindKey').Key

            if i == 1: resetfile.SetBind(key, self, title, cmd)
            cbindfile.SetBind(key, self, title, cmd)

    def AllBindFiles(self) -> dict[str, list]:
        files = []
        # we do both of these for backwards compat but might eventually just do cid
        title = re.sub(r'\W+', '', self.Title)
        cid = self.CustomID
        for i, _ in enumerate(self.Steps, start = 1):
            files.append(self.Profile.GetBindFile('cbinds', f'{title}-{i}.txt'))
            files.append(self.Profile.GetBindFile('cb', f'{cid}-{i}.txt'))

        return {
            'files' : files,
            'dirs'  : ['cbinds', 'cb'],
        }

class BindStep(wx.Panel):
    def __init__(self, parent, stepNumber, step) -> None:

        self.Page = parent.Page
        pane = parent.GetPane()

        super().__init__(pane)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        StepLabel = wx.StaticText(self, label = f"Step {stepNumber}:")
        self.StepLabel = StepLabel
        sizer.Add(StepLabel, 0, wx.ALIGN_CENTER_VERTICAL)

        extralength = len(parent.Profile.BLF(f'cb\\{parent.CustomID}-X.txt'))
        self.PowerBinder = PowerBinder(self, step.get('powerbinderdata', {}), extralength = extralength)
        self.PowerBinder.ChangeValue(step.get('contents', ''))
        self.PowerBinder.Bind(wx.EVT_TEXT, parent.onContentsChanged)
        sizer.Add(self.PowerBinder, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        self.moveUpButton = wx.Button(self, label = '\u25B2', size = wx.Size(40, -1))
        self.moveUpButton.Bind(wx.EVT_BUTTON, parent.onMoveUpButton)
        self.moveUpButton.SetToolTip('Move step up')
        sizer.Add(self.moveUpButton, 0)

        self.moveDownButton = wx.Button(self, label = '\u25BC', size = wx.Size(40, -1))
        self.moveDownButton.Bind(wx.EVT_BUTTON, parent.onMoveDownButton)
        self.moveDownButton.SetToolTip('Move step down')
        sizer.Add(self.moveDownButton, 0)

        self.dupeButton = wx.BitmapButton(self, bitmap = GetIcon('UI', 'copy'))
        self.dupeButton.Bind(wx.EVT_BUTTON, parent.onDupeButton)
        self.dupeButton.SetToolTip('Duplicate step')
        sizer.Add(self.dupeButton, 0)

        self.delButton = wx.BitmapButton(self, bitmap = GetIcon('UI', 'delete'))
        self.delButton.SetForegroundColour(wx.RED)
        self.delButton.Bind(wx.EVT_BUTTON, parent.onDelButton)
        self.delButton.SetToolTip('Delete step')
        sizer.Add(self.delButton, 0, flag = wx.RESERVE_SPACE_EVEN_IF_HIDDEN)

        self.SetSizer(sizer)
