#  KeyBind mixin -- intended to be mixed into each of page.Controls
# so we can just iterate and create the bind tuples to push into
# bindfiles.

class KeyBind():
    def __init__(self, key, name, page, contents):

        if type(contents) == str:
            contents = [contents]

        if type(contents) != list:
            print("Got contents not-a-list:")
            print(f"Instead it's a {type(contents)}")
            print(contents)

        self.KeyBindKey      = key # actual key combo
        self.KeyBindName     = name # friendly name, ie, "Select All Pets"
        self.KeyBindTab      = page # which tab the bind originated on
        self.KeyBindContents = contents #the actual bindstring (without surrounding "")


    def GetKeyBindString(self):

        payload = '$$'.join(self.KeyBindContents)

        return f'{self.KeyBindKey} "{payload}"\n'


