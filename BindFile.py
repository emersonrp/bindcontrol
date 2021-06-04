class BindFile():

    def __init__(self, filename):

        #$filename = File::Spec->catfile(@filename)
        #unless ($BindFiles{$filename}) {
            #$BindFiles{$filename} =  bless {filename = $filename, binds = {}}, $class
        #}
        #return $BindFiles{$filename}
        return

    def SetBind(self, key, bindtext):

        if key == None:
            die("invalid key: {key}, bindtext {bindtext}")

        bindtext = bindtext.strip()

        # TODO -- how to call out the 'reset file' object as special?
        # if ($file eq $resetfile1 and $key eq $resetkey) {
            # $resetfile2->{$key} = $s
        # }

        self.binds[key] = bindtext

    def BaseReset(self, profile):
        return '$$bindloadfilesilent ' + profile.General.BindsDir + "\\subreset.txt"

    # BLF == full "$$bindloadfilesilent path/to/file/kthx"
    def BLF(self, *args, **kwargs):
        return '$$' + self.BLFs(*args, **kwargs)

    # BLFs == same as above but no '$$' for use at start of binds.  Unnecessary?
    def BLFs(self, *args, **kwargs):
        return 'bindloadfilesilent ' . self.BLFPath(*args, **kwargs)

    # BLFPath == just the path to the file
    def BLFPath(self, profile, *args, **kwargs):
        # TODO - re-make this os-agnostic
        #file = pop @bits
        #($vol, $bdir, undef) = File::Spec->splitpath( $profile->General->{'BindsDir'}, 1 )
        #$dirpath = File::Spec->catdir($bdir, @bits)
        #return File::Spec->catpath($vol, $dirpath, $file)

        filepath = profile.General.Bindsdir
        for arg in args:
            filepath = filepath + "/" + arg

        return filepath

    def Write(self, profile):

        # TODO -- construct this all correctly with file modules; stubbed out for now
        return

        ## # Pick apart the binds directory
        ## ($vol, $bdir, undef) = File::Spec->splitpath( $profile->General->{'BindsDir'}, 1 )

        ## # Pick apart the filename into component bits.
        ## (undef, $dir, $file) = File::Spec->splitpath( $self->{'filename'} )

        ## # mash together the two 'directory' parts:
        ## $dir = File::Spec->catdir($bdir, $dir)

        ## # now we want the fully-qualified dir name so we can make sure it exists...
        ## $newpath = File::Spec->catpath( $vol, $dir, '' )
        ## # and the fully-qualified filename so we can write to it.
        ## $fullname = File::Spec->catpath( $vol, $dir, $file )
        ## # Make the dir if it doesn't exist already.
        ## if ( ! -d $newpath ) {
        ##     File::Path::make_path( $newpath, {verbose=1} ) or warn "can't make dir $newpath: $!"
        ## }

        ## # open the file and blast the poop into it.  whee!
        ## open ($fh, '>', $fullname ) or warn "can't write to $fullname: $!"
        ## for $k (sort keys %{ $self->{'binds'} }) {
        ##     print $fh qq|$k "$self->{'binds'}->{$k}"\n|
        ## }
        ## # print STDERR "Done $fullname!\n"
