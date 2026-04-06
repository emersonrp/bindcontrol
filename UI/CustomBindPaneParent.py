# parent class for various custom bindpane types
from typing import Any
from UI.ListPanel import ListPanel
import wx

class CustomBindPaneParent(ListPanel):
    def __init__(self, parent, init):
        super().__init__(parent, init)
        self.Description = "Custom Bind"
        self.Topic       = 'bind'

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
