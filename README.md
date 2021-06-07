This is something between a clone and a port of CityBinder
(http://sourceforge.net/projects/citybinder/), using the Wxpython Widget UI
toolkit so that it's cross-platform.

Currently it does almost nothing -- it'll display the main window, and some of
the ui elements sort of work, but it won't save or load profiles, generate
bindfiles, or really anything useful.

The majority of the bind-generating logic from CityBinder has been
implemented, so remaining is the wiring together the middle bits
between the UI and the logic.


The intent is to make this available pre-rolled into standalone
binaries for Windows, MacOS, and Linux.

BindControl is licensed under the GPL, version 2 or later.

emerson@hayseed.net
