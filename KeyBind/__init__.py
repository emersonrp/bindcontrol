class KeyBind():
    def __init__(self, key, name, page, contents):

        if type(contents) == str: contents = [contents]

        self.Key      = key      # actual key combo
        self.Name     = name     # friendly name, ie, "Select All Pets"
        self.Page     = page     # which tab the bind originated on
        self.Contents = contents # the actual bindstring (without surrounding "")
