# this abstract class represents all the info about a particular key's binding
# state -- derived classes contextualize it into "during bind selection" and
# "during bindfile writing"

class KeyBind():
    def __init__(self, key, name, page, contents):

        if type(contents) == str: contents = [contents]

        self.Key      = key      # actual key combo
        self.Name     = name     # friendly name, ie, "Select All Pets"
        self.Page     = page     # which tab the bind originated on
        self.Contents = contents # a list of strings to '$$'-join to create the actual payload
