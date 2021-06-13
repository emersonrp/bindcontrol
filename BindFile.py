from pathlib import Path

class BindFile():

    def __init__(self, profile, *pathbits):
        bindsdir = profile.BindsDir()
        pathbits = (bindsdir, *pathbits)
        self.Path = Path(*pathbits)

        self.Binds = {}

    def SetBind(self, key, contents):

        if key == None:
            print(f"invalid key: {self.Path}, {key}, contents {contents}")

        if key == "UNBOUND": return

        contents = '"' + contents.strip() + '"'

        bind = self.Binds[key] if self.Binds.get(key, None) else {}

        bind[key] = contents

        ## TODO - do we actually need to objectinate individual binds?
        # bind.Key = key
        # bind.Contents = contents

        # TODO -- how to call out the 'reset file' object as special?
        # if ($file eq $resetfile1 and $key eq $resetkey) {
            # $resetfile2->{$key} = $s
        # }

        self.Binds[key] = contents

    def BaseReset(self, profile):
        return '$$bindloadfilesilent ' + profile.General.BindsDir + "\\subreset.txt"

    # BLF == full "$$bindloadfilesilent path/to/file/kthx"
    def BLF(self):
        return '$$' + self.BLFs()

    # BLFs == same as above but no '$$' for use at start of binds.  Unnecessary?
    def BLFs(self):
        return 'bindloadfilesilent ' . str(self.Path)

    def Write(self, profile):
        try:
            self.Path.touch(exist_ok = True)
        except e:
            Wx.Error("Can't instantiate file {self}: {e}")

        # TODO -- sort all this stuff by the Alpha key, subsort by mod keys

        output = ''
        for bind, contents in self.Binds.items():
            output = output + f'{bind} {contents}\n'

        print(output)
        self.Path.write_text(output)
