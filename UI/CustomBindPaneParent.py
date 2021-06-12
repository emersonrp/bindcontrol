# parent class for various bind types
class CustomBindPaneParent():
    def __init__(self, page, bind = None):

        self.Key      = 'UNBOUND'
        self.Name     = ''
        self.Contents = ''
        self.Page = page

        if bind:
            if bind.get('key',      None): self.Key      = bind['key']
            if bind.get('name',     None): self.Title    = bind['title']
            if bind.get('contents', None): self.Contents = bind['contents']

    def BuildBindUI(parent, self):
        # build the UI needed to edit/create this bind, and shim
        # it into 'parent'
        pass

    def MakeBinds(self):
        # for overriding on child classes
        # take whatever the internal representation of the bind is,
        # and put it into one or more key / title / contents dicts
        pass

