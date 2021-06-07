# parent class for various bind types
class CustomBind():
    def __init__(self, bind = None):

        self.Key = ''
        self.Title = ''
        self.Payload = ''

        if bind:
            if bind.get('key',     None): self.Key     = bind['key']
            if bind.get('title',   None): self.Title   = bind['title']
            if bind.get('payload', None): self.Payload = bind['payload']

    def MakeBind(self):
        # for overriding on child classes
        # take whatever the internet representation of the bind is,
        # and put it into key / title / payload

        pass
