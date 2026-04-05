# parent class for various custom bindpane types
from pubsub import pub
from typing import Any
from UI.ListPanel import ListPanel
import wx

class CustomBindPaneParent(ListPanel):
    def __init__(self, parent, init):
        super().__init__(parent, init)
        self.Description = "Custom Bind"

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

    def CreateSerialization(self, data) -> dict[str, Any]:
        return {
            'CustomID' : self.CustomID,
            'Type'     : self.Type,
            'Title'    : self.Title,
            **data
        }

    # override the more general ListPanel one completely.  Would be nice to
    # DRY it up a bit but no
    def SetPanelLabel(self, new = False) -> bool:
        # marshal up the files to delete, before we change the name
        deletefiles = None if new else self.AllBindFiles()
        dlg = wx.TextEntryDialog(self, f'Enter name for {self.Description or "bind"}:')
        if self.Title:
            dlg.SetValue(self.Title)

        if dlg.ShowModal() == wx.ID_OK:
            self.Title = dlg.GetValue()
            self.Pane.SetLabel(self.Title)
            if not new:
                self.DelButton.SetToolTip(f'Delete bind "{self.Title}"')
                self.RenButton.SetToolTip(f'Rename bind "{self.Title}"')
                self.DupButton.SetToolTip(f'Duplicate bind "{self.Title}"')
                self.ExpButton.SetToolTip(f'Export bind "{self.Title}"')
                # if we have files to delete (we do, if not new) then delete them.
                if deletefiles and self.Profile:
                    self.Profile.doDeleteBindFiles(deletefiles)
            pub.sendMessage('updatebinds')
            dlg.Destroy()
            return True # successful name change
        else:
            if new:
                self.doDeletePanel()
            dlg.Destroy()
            return False

