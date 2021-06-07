from pathlib import Path

class BindFile():

    def __init__(self, profile, *pathbits):
        bindsdir = profile.BindsDir
        pathbits = (bindsdir, *pathbits)

        self.Path = Path(*pathbits)

        self.Binds = {}

    def SetBind(self, key, bindtext):

        if key == None:
            die("invalid key: {key}, bindtext {bindtext}")

        bindtext = bindtext.strip()

        # TODO -- how to call out the 'reset file' object as special?
        # if ($file eq $resetfile1 and $key eq $resetkey) {
            # $resetfile2->{$key} = $s
        # }

        self.Binds[key] = bindtext

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
            die("Can't instantiate file {self}: {e}")

        contents = ''
        for bind in self.Binds:
            contents = contents + bind + "\n"

        self.write_text(contents)
