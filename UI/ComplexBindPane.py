from pubsub import pub
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

        self.Description  = "Complex Bind"
        self.Type         = "ComplexBind"
        self.CreatesFiles = True

        self.Steps = []

    def Serialize(self) -> dict[str, str|list]:
        bindkey = self.GetCtrl('BindKey')
        data = self.CreateSerialization({
            'Key'  : bindkey.Key if bindkey else '',
            'Steps': [],
        })
        for step in self.Steps:
            newstepdata = {}
            if step.PowerBinder:
                newstepdata['contents']        = step.PowerBinder.GetValue()
                newstepdata['powerbinderdata'] = step.PowerBinder.SaveToData()
            if step.ReleaseBinder:
                newstepdata['rcontents']         = step.ReleaseBinder.GetValue()
                newstepdata['releasebinderdata'] = step.ReleaseBinder.SaveToData()

            if newstepdata:
                newstepdata['isPRBind'] = step.IsPR()
                data['Steps'].append(newstepdata)

        return data

    def BuildBindUI(self) -> None:
        pane = self.Pane.GetPane()

        self.BindSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.BindStepSizer = wx.BoxSizer(wx.VERTICAL)
        AddBindStepButton = wx.Button(pane, label = "Add Step")
        AddBindStepButton.Bind(wx.EVT_BUTTON, self.onAddStepButton)
        self.BindStepSizer.Add(AddBindStepButton, 0, wx.TOP, 10)
        if steps := self.Init.get('Steps', []):
            for step in steps:
                self.doAddStep(step)
        else:
            self.doAddStep()

        self.BindSizer.Add(self.BindStepSizer, 1, wx.EXPAND)

        BindKeyCtrl = bcKeyButton(pane, init = {
            'CtlName' : self.MakeCtrlName('BindKey'),
            'Page'    : self.Page,
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

        if not self.Steps: return True

        firststep = self.Steps[0]
        fullsteps = list(filter(lambda x: x.CheckIfWellFormed(), self.Steps))
        if fullsteps:
            firststep.PowerBinder.RemoveError('undef')
        else:
            firststep.PowerBinder.AddError('undef', 'At least one valid step must be defined.')
            isWellFormed = False

        if bk := self.GetCtrl('BindKey'):
            if not bk.Key:
                bk.AddError('undef', 'The keybind has not been selected')
                isWellFormed = False
            else:
                bk.RemoveError('undef')

        return isWellFormed

    def onAddStepButton(self, evt = None, stepdata : dict|None = None) -> None:
        self.doAddStep(stepdata or {})
        pub.sendMessage('updatebinds')
        if evt: evt.Skip()

    def doAddStep(self, stepdata : dict|None = None) -> None:
        stepdata = stepdata or {}
        stepNumber = self.BindStepSizer.GetItemCount() # This is the correct (next) number because the Add button adds one to the count
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
        pub.sendMessage('updatebinds')
        self.RenumberSteps()
        evt.Skip()

    def onMoveDownButton(self, evt) -> None:
        button = evt.GetEventObject()
        step = button.GetParent()
        idx = self.Steps.index(step)
        self.BindStepSizer.Detach(idx)
        self.BindStepSizer.Insert(idx+1, self.Steps[idx], 0, wx.EXPAND)
        self.Steps[idx], self.Steps[idx+1] = self.Steps[idx+1], self.Steps[idx]
        pub.sendMessage('updatebinds')
        self.RenumberSteps()
        evt.Skip()

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
        pub.sendMessage('updatebinds')
        self.RenumberSteps()
        evt.Skip()

    def onDelButton(self, evt) -> None:
        button = evt.GetEventObject()
        step = button.GetParent()
        self.Steps.remove(step)
        step.DestroyLater()
        pub.sendMessage('updatebinds')
        self.RenumberSteps()
        evt.Skip()

    def RenumberSteps(self) -> None:
        for i, step in enumerate(self.Steps, start = 1):
            step.delButton.Show(i>1) # don't even show the del button on step 1
            step.moveUpButton.Enable(i > 1)
            step.moveDownButton.Enable(i < len(self.Steps))
            step.StepNumber = i
            step.StepLabel  .SetLabel(f"Step {i} Press Action:" if step.IsPR() else f"Step {i}:")
            step.ReleaseText.SetLabel(f"Step {i} Release Action:")
        if self.Page:
            self.Page.Layout()

    def PopulateBindFiles(self) -> None:
        if self.Profile:
            resetfile = self.Profile.ResetFile()
            # fish out only the steps that are valid
            fullsteps = list(filter(lambda x: x.CheckIfWellFormed(), self.Steps))
            title = re.sub(r'\W+', '', self.Title)
            cid = self.CustomID
            for i, step in enumerate(fullsteps, start = 1):
                nextCycle = 1 if (i+1 > len(fullsteps)) else i+1

                cbindfile = self.Profile.GetBindFile('cb', f'{cid}-{i}.txt')
                rbindfile = self.Profile.GetBindFile('cb', f'{cid}-{i}-r.txt') if step.IsPR() else None

                if key := self.GetCtrl('BindKey'):
                    key = key.Key

                    if step.IsPR():
                        cmd = ['+$$' + step.PowerBinder.GetValue(), self.Profile.BLF('cb', f'{cid}-{i}-r.txt')]
                    else:
                        cmd = [        step.PowerBinder.GetValue(), self.Profile.BLF('cb', f'{cid}-{nextCycle}.txt')]

                    if i == 1: resetfile.SetBind(key, title, self.Page, cmd)
                    cbindfile.SetBind(key, title, self.Page, cmd)
                    if rbindfile:
                        rcmd = ['+$$' + step.ReleaseBinder.GetValue(), self.Profile.BLF('cb', f'{cid}-{nextCycle}.txt')]
                        rbindfile.SetBind(key, title, self.Page, rcmd)

    def AllBindFiles(self) -> dict[str, list]:
        files = []
        # we do both of these for backwards compat but might eventually just do cid
        title = re.sub(r'\W+', '', self.Title)
        cid = self.CustomID
        if self.Profile:
            for i, _ in enumerate(self.Steps, start = 1):
                files.append(self.Profile.GetBindFile('cbinds', f'{title}-{i}.txt'))
                files.append(self.Profile.GetBindFile('cb', f'{cid}-{i}.txt'))
                files.append(self.Profile.GetBindFile('cb', f'{cid}-{i}-r.txt')) # 'release'

        return {
            'files' : files,
            'dirs'  : ['cbinds', 'cb'],
        }

class BindStep(wx.Panel):
    def __init__(self, parent, stepNumber, step) -> None:

        self.Page = parent.Page
        self.Pane : ComplexBindPane = parent
        self.StepNumber = stepNumber
        pane = parent.GetPane()

        super().__init__(pane)

        self.BindSizer = wx.FlexGridSizer(7, 0, 0)
        self.BindSizer.AddGrowableCol(1)

        self.StepLabel = wx.StaticText(self, label = f"Step {stepNumber}:")
        self.BindSizer.Add(self.StepLabel, 0, wx.ALIGN_CENTER_VERTICAL)

        # get the length of a hypothetical BLF string (don't need pathlib etc)
        extralength = len(parent.Profile.BLF(f'cb\\{parent.CustomID}-XX.txt'))
        self.PowerBinder = PowerBinder(self, step.get('powerbinderdata', {}), extralength = extralength, contents = step.get('contents', ''))
        self.PowerBinder.Bind(wx.EVT_TEXT, parent.onContentsChanged)
        self.BindSizer.Add(self.PowerBinder, 1, wx.EXPAND|wx.LEFT, 5)

        self.PRButton = wx.BitmapToggleButton(self, label = GetIcon('UI', 'add_circle'))
        self.BindSizer.Add(self.PRButton, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        self.PRButton.SetValue(step.get('isPRBind', False))
        self.PRButton.SetToolTip("Separate Press / Release Actions for this step")
        self.PRButton.Bind(wx.EVT_TOGGLEBUTTON, self.onPRButtonClicked)

        self.moveUpButton = wx.Button(self, label = '\u25B2', size = wx.Size(40, -1))
        self.moveUpButton.Bind(wx.EVT_BUTTON, parent.onMoveUpButton)
        self.moveUpButton.SetToolTip('Move step up')
        self.BindSizer.Add(self.moveUpButton, 0)

        self.moveDownButton = wx.Button(self, label = '\u25BC', size = wx.Size(40, -1))
        self.moveDownButton.Bind(wx.EVT_BUTTON, parent.onMoveDownButton)
        self.moveDownButton.SetToolTip('Move step down')
        self.BindSizer.Add(self.moveDownButton, 0)

        self.dupeButton = wx.BitmapButton(self, bitmap = GetIcon('UI', 'copy'))
        self.dupeButton.Bind(wx.EVT_BUTTON, parent.onDupeButton)
        self.dupeButton.SetToolTip('Duplicate step')
        self.BindSizer.Add(self.dupeButton, 0)

        self.delButton = wx.BitmapButton(self, bitmap = GetIcon('UI', 'delete'))
        self.delButton.SetForegroundColour(wx.RED)
        self.delButton.Bind(wx.EVT_BUTTON, parent.onDelButton)
        self.delButton.SetToolTip('Delete step')
        self.BindSizer.Add(self.delButton, 0, flag = wx.RESERVE_SPACE_EVEN_IF_HIDDEN)

        self.ReleaseText = wx.StaticText(self, label = f"Step {self.StepNumber} Release Action:")
        self.BindSizer.Add(self.ReleaseText, 0, wx.ALIGN_CENTER_VERTICAL)

        rb = PowerBinder(self, step.get('releasebinderdata', {}), contents = step.get('rcontents', ''))
        rb.Bind(wx.EVT_TEXT, parent.onContentsChanged)
        self.ReleaseBinder = rb
        self.BindSizer.Add(rb, 1, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.EXPAND, 5)

        self.SetSizer(self.BindSizer)

        self.onPRButtonClicked()

    def IsPR(self):
        return self.PRButton.GetValue()

    def onPRButtonClicked(self, evt = None) -> None:
        if evt: evt.Skip()
        checked = self.IsPR()
        if self.ReleaseText:
            self.BindSizer.Show(self.ReleaseText, checked)
        if self.ReleaseBinder:
            self.BindSizer.Show(self.ReleaseBinder, checked)
        self.StepLabel.SetLabel(f'Step {self.StepNumber} Press Action:' if checked else f'Step {self.StepNumber}:')
        self.BindSizer.Layout()
        self.Page.Layout()

    def CheckIfWellFormed(self) -> bool:
        isWellFormed = True
        if self.PowerBinder.GetValue() or self.ReleaseBinder.GetValue():
            self.PowerBinder.RemoveError('noaction')
        else:
            self.PowerBinder.AddError('noaction', 'This step has no action defined.')
            isWellFormed = False

        if len(self.PowerBinder.GetValue()) + self.PowerBinder.ExtraLength <= 255:
            self.PowerBinder.RemoveError('length')
        else:
            self.PowerBinder.AddError('length', 'This step, when written to file, will be longer than 255 characters, which will cause problems in-game.')
            isWellFormed = False

        # extra checks for Press/Release binds:
        if self.IsPR():
            if len(self.ReleaseBinder.GetValue()) + self.ReleaseBinder.ExtraLength <= 255:
                self.ReleaseBinder.RemoveError('length')
            else:
                self.ReleaseBinder.AddError('length', 'This step, when written to file, will be longer than 255 characters, which will cause problems in-game.')
                isWellFormed = False

            if self.PowerBinder.GetValue():
                if self.ReleaseBinder.GetValue():
                    self.ReleaseBinder.RemoveError('pressrelease')
                else:
                    self.ReleaseBinder.AddError('pressrelease', 'This step has a "Press" action but no "Release" action.  This is probably not what you want.')
                    isWellFormed = False
            else:
                if self.ReleaseBinder.GetValue():
                    self.PowerBinder.AddError('pressrelease', 'This step has a "Release" action but no "Press" action.  This is probably not what you want.')
                    isWellFormed = False
                else:
                    self.PowerBinder.RemoveError('pressrelease')

        return isWellFormed
