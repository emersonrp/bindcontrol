# parent class for various bind types
class CustomBind():
    def __init__(self, page, bind = None):

        self.Key     = 'UNBOUND'
        self.Name    = ''
        self.Payload = ''
        self.Page = page

        if bind:
            if bind.get('key',     None): self.Key     = bind['key']
            if bind.get('name',    None): self.Title   = bind['title']
            if bind.get('payload', None): self.Payload = bind['payload']

    def BuildBindUI(parent, self):
        # build the UI needed to edit/create this bind, and shim
        # it into 'parent'
        pass

    def MakeBinds(self):
        # for overriding on child classes
        # take whatever the internet representation of the bind is,
        # and put it into one or more key / title / payload dicts

        pass
