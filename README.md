BindControl
===========

BindControl is a helper app for creating and maintaining keybinds for City of Heroes and its various spinoff servers.

It is something between a clone and a port of Konoko and Monorail's [CityBinder 0.76](http://sourceforge.net/projects/citybinder/), using the WxWidgets UI toolkit.

During City of Heroes' original run, CityBinder was the go-to app for keybinds.  It's written in lua, using the IUP toolkit, which is difficult to set up for development on modern OSes.  I wanted to add features and clean up the UI, so in a stunning and likely unwise act of hubris, I instead started work on BindControl.

I worked on it on-and-off for the remainder of the original run of the game, then shelved it, ostensibly forever.  Now here in the age of the SCORE, Homecoming, and other servers, it once again has value, so I've dusted it off.

Features
--------

* runs on Windows, MacOS, and Linux
* separate profiles for different characters or situations
* chat binds with optional 'typing' notifier
* rotational next/prev team and pet selection
* speed-on-demand
    * based on the original Gnarley's SoD keybinds
    * incorporates movement power changes in Homecoming
    * supports Super Speed, Super Jump, Flight, Teleport, Sprint powers, Temp powers, and Kheldian powers
    * one-key reset in case SoD binds get tangled up
* inspiration popper
    * by-type
    * largest-first or smallest-first
    * optional /say feedback
* mastermind / pet binds
    * select pets by power level: all, minions, lieutenants, and boss
    * orders for aggressive/defensive/passive; attack, follow, go to, and stay
    * pets can give feedback on each order;  chattiness is toggleable
    * by-name pet selection
    * "bodyguard mode"  (TODO: describe)
* custom binds
    * create simple binds using PowerBuilder, a flexible tool for stringing together arbitrary macro commands into bind strings
    * create buffer bind sets for quick buff rotation on friendly units
    * more to comes

Status
------

* saving and loading profiles is a work in progress
* chat and inspiration-popper binds are 100% complete
* mastermind binds are working apart from bodyguard mode
* team / pet rotational binds are tentatively working, more testing is needed
* speed-on-demand is a giant mess still
* simple PowerBinder binds work;  buffer binds aren't there yet.


Dependencies
------------

* [Python](https://www.python.org) version 3 or later
* [wxPython](https://www.wxpython.org) version 4 or later

For Windows and MacOS users, follow the instructons on the above sites' download pages to install Python and wxPython.

Linux users, install your distribution's packages for python 3 and wxPython.

The eventual intent is to make this available pre-rolled into standalone binaries for Windows and MacOS, and a flatpak or the like for Linux.

Using
-----

Clone this app, or get the source as a ZIP file.

Windows users:  Double-click `BindControl.py` in the top-level folder

Mac / Linux users: In a terminal, `cd` to where you put the BindControl source, then `python BindControl.py`.  Some distributions might need `python3` instead of `python`.


Credits and License
-------------------

* BindControl is in many places a direct port of [CityBinder](http://sourceforge.net/projects/citybinder/) code, and in most other places was extremely influenced by it.

BindControl is licensed under the GPL, version 3 or later.

emerson@hayseed.net
