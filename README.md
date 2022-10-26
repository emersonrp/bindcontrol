BindControl
===========

BindControl is a helper app for creating and maintaining keybinds for City of Heroes.

It is an enhanced port of Konoko and Monorail's [CityBinder 0.76](http://sourceforge.net/projects/citybinder/), using the WxWidgets UI toolkit.

During City of Heroes' original run, CityBinder was the go-to app for keybinds.  It's written in lua, using the IUP toolkit, and the required versions of those can be difficult to set up for development on modern OSes.  I wanted to add features and clean up the UI, so in a stunning and likely unwise act of hubris, I instead started work on BindControl.

I worked on it on-and-off for the remainder of the original run of the game, then shelved it, ostensibly forever.  Now here in the age of the SCORE, Homecoming, and other servers, it once again has value, so I've dusted it off and continued to add features and modernize it.

BindControl is initially targeted at Homecoming players, but currently almost all features will work regardless of server.  The intent is to make it server-agnostic as much as possible, and to allow the user to choose the type of server they play on for the features that differ.

Features
--------

* Runs on Windows, MacOS, and Linux
* Separate profiles for different characters or situations
* Chat binds with optional 'typing' notifier
* Custom Binds
    * create custom binds using PowerBinder, a flexible tool for putting together arbitrary commands into bind strings
* Speed-on-Demand
    * based on [citybinder](http://sourceforge.net/projects/citybinder/) and the original Gnarley's SoD keybinds
    * supports Super Speed, Super Jump, Flight, Teleport, and Sprint powers
    * one-key reset in case SoD binds get tangled up
* Inspiration Popper
    * by-type
    * largest-first or smallest-first
    * optional /say feedback
* Mastermind / pet binds
    * select pets by power level: all, minions, lieutenants, and boss
    * orders for aggressive / defensive / passive stances; attack, follow, go to, and stay
    * pets can give feedback on each order;  chattiness can be toggled via keybind
    * "bodyguard mode" shortcuts -- define which pets should be treated as bodyguards, and toggle Bodyguard Mode on and off for them, with future orders then applying to the remaining pets.
    * by-name pet selection

TODO
----

* Rotational next/prev team and pet selection
* Additional useful Gameplay binds, eg, "Invite Target," "Quit to Desktop," more
* Save binds in $bindsdir/$profile directories
* More error detection and handling
* Kheldian form/travel binds in speed-on-demand
* Temporary powers in speed-on-demand
* Support [Homecoming travel power changes](https://forums.homecomingservers.com/topic/27807-travel-power-updates-in-issue-27-page-2/) in SoD
* Buffer bind sets, as well as others TBD, in Custom Binds
* Roll standalone binaries for Windows, MacOS, Linux (flatpak?)
* More and better help text and documentation

Dependencies
------------

* [Python](https://www.python.org) version 3.10 or later
* [wxPython](https://www.wxpython.org) version 4.1 or later

For Windows and MacOS users, follow the instructions on the above sites' download pages to install Python and wxPython.

Linux users, install your distribution's packages for python 3 and wxPython.

Using
-----

Clone this app, or get the source as a ZIP file and unzip it somewhere.

Windows users:  Double-click `BindControl.py` in the top-level folder

Mac / Linux users: In a terminal, `cd` to where you put the BindControl source, then `python BindControl.py`.  Some distributions might need `python3` instead of `python`.


Credits and License
-------------------

BindControl is in many places a direct port of [CityBinder](http://sourceforge.net/projects/citybinder/) code, and in most other places was extremely influenced by it.

Speed on Demand binds are based on the [original SoD binds by Gnarley](https://mega.nz/folder/4HB2kAoC#Hy1m4EXbcyrPXxPPMCSb8w).  Advanced teleport binds are based on a (long-lost) program written by Dr Letharga.  Mastermind binds adapted from [Sandalphan's Mastermind Numeric Keypad Pet Controls](https://web.archive.org/web/20120904222729/http://boards.cityofheroes.com/showthread.php?t=117256)

BindControl is licensed under the GPL, version 3 or later.

emerson@hayseed.net
