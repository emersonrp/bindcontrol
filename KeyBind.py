import re
class KeyBind():
    def __init__(self, key, name, page, contents):

        if type(contents) == str: contents = [contents]

        self.Key      = key      # actual key combo
        self.Name     = name     # friendly name, ie, "Select All Pets"
        self.Page     = page     # which tab the bind originated on
        self.Contents = contents # a list of strings to '$$'-join to create the actual payload

    # this is cruft leftover from the original control vs file keybind scheme
    def WithContents(self, contents):
        if isinstance(contents, str): contents = [contents]
        self.Contents = contents
        return self

    def GetKeyBindString(self):

        payload = '$$'.join([i for i in self.Contents if i])

        # remove any initial $$ if we snuck in here with it.
        payload = re.sub(r'^\$\$', '', payload)
        # and any doubled up '$$'
        payload = re.sub(r'\$\$\$\$', '$$', payload)

        return f'{self.Key} "{payload}"\n'


