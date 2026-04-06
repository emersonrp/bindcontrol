# parent class for various custom bindpane types
from pubsub import pub
from typing import Any
from UI.ListPanel import ListPanel
import wx

class CustomBindPaneParent(ListPanel):
    def __init__(self, parent, init):
        super().__init__(parent, init)
        self.Description  = "Custom Bind"
        self.Topic        = 'bind'
        self.CreatesFiles = False

    def BuildBindUI(self) -> None:
        wx.LogError(f"{self.Class} did not override BuildBindUI.  This is a bug.")
        # build the UI needed to edit/create this bind, and shim
        # it into 'page'

    def CheckIfWellFormed(self) -> bool:
        wx.LogWarning(f"{self.Class} did not override CheckIfWellFormed.  This is a bug.")
        return False

    def PopulateBindFiles(self) -> None:
        wx.LogError(f"{self.Class} did not override PopulateBindFiles.  This is a bug.")
        # for overriding on child classes this will be called in the course of
        # the Custom Binds page doing its own PopulateBindFiles, iteratively
        # over all of its kids

    def OnDeleteButton(self, evt) -> None:
        with PanelDeletionDialog(self) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return
            if dlg.DeleteFilesCB and dlg.DeleteFilesCB.GetValue():
                # do the delete of the files
                # TODO PUBSUB
                if self.Profile:
                    files = self.AllBindFiles()
                    self.Profile.doDeleteBindFiles(files)
        pub.sendMessage(f'deletepanel.{self.Topic}', panel = self)
        self.DestroyLater()
        evt.Skip()

    def CreateSerialization(self, data) -> dict[str, Any]:
        return {
            'CustomID' : self.CustomID,
            'Type'     : self.Type,
            'Title'    : self.Title,
            **data
        }

class PanelDeletionDialog(wx.Dialog):
    def __init__(self, parent):
        bindpane = parent
        super().__init__(parent)
        self.SetTitle(f"Delete {bindpane.Title}")

        self.DeleteFilesCB = None

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(wx.StaticText(self, label = f'Delete Custom Bind "{bindpane.Title}"?'), 0, wx.ALL, 20)

        if bindpane.CreatesFiles:
            self.DeleteFilesCB = wx.CheckBox(self, label = "Delete all associated bindfiles")
            self.DeleteFilesCB.SetValue(True)
            mainSizer.Add(self.DeleteFilesCB, 0, wx.ALL|wx.ALIGN_CENTER, 10)

        mainSizer.Add(self.CreateButtonSizer(wx.OK|wx.CANCEL), 0, wx.ALL|wx.ALIGN_CENTER, 20)

        self.SetSizerAndFit(mainSizer)
