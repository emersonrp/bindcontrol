from KeyBind import KeyBind
from KeyBind.FileKeyBind import FileKeyBind

class ControlKeyBind(KeyBind):
    def __init__(self, key = "", name = "", page = "", contents = ()):
        KeyBind.__init__(self, key, name, page, contents)


    # factory for PopulateBindFiles to use
    def MakeFileKeyBind(self, contents):
        self.Contents = contents

        return FileKeyBind(self.Key, self.Name, self.Page, contents)
