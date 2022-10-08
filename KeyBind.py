class KeyBind():
    def __init__(self, key, name, page, contents):

        if type(contents) == str: contents = [contents]

        self.Key      = key      # actual key combo
        self.Name     = name     # friendly name, ie, "Select All Pets"
        self.Page     = page     # which tab the bind originated on
        self.Contents = contents # a list of strings to '$$'-join to create the actual payload

class ControlKeyBind(KeyBind):
    def __init__(self, key = "", name = "", page = "", contents = ()):
        KeyBind.__init__(self, key, name, page, contents)


    # factory for PopulateBindFiles to use
    def MakeFileKeyBind(self, contents):
        self.Contents = contents

        return FileKeyBind(self.Key, self.Name, self.Page, contents)

class FileKeyBind(KeyBind):
    def __init__(self, key = "", name = "", page = "", contents = ()):
        KeyBind.__init__(self, key, name, page, contents)


    def GetKeyBindString(self):

        payload = '$$'.join([i for i in self.Contents if i])

        return f'{self.Key} "{payload}"\n'


