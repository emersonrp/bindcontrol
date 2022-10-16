BindControl
===========

BindControl is a helper app for creating and maintaining keybinds for City of Heroes.

It is an enhanced port of Konoko and Monorail's [CityBinder 0.76](http://sourceforge.net/projects/citybinder/), using the WxWidgets UI toolkit.

During City of Heroes' original run, CityBinder was the go-to app for keybinds.  It's written in lua, using the IUP toolkit, which is difficult to set up for development on modern OSes.  I wanted to add features and clean up the UI, so in a stunning and likely unwise act of hubris, I instead started work on BindControl.

I worked on it on-and-off for the remainder of the original run of the game, then shelved it, ostensibly forever.  Now here in the age of the SCORE, Homecoming, and other servers, it once again has value, so I've dusted it off.

Features
--------

* Runs on Windows, MacOS, and Linux
* Separate profiles for different characters or situations
* Chat binds with optional 'typing' notifier
* Rotational next/prev team and pet selection
* Custom Binds
    * create simple binds using PowerBinder, a flexible tool for stringing together arbitrary commands into bind strings
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
    * orders for aggressive/defensive/passive; attack, follow, go to, and stay
    * pets can give feedback on each order;  chattiness is toggleable via keybind
    * by-name pet selection
    * "bodyguard mode" shortcuts

TODO
----

* Clarify new / save / load profile flow
* Move preferences to separate dialog;  show during "new profile" creation
* More error detection and handling
* Log errors and warnings in less intrusive, more readable way
* Store PowerBinder state for re-editing;  save state with Profile
* Kheldian form/travel binds in speed-on-demand
* Temporary powers in speed-on-demand
* Account for [Homecoming travel power changes](https://forums.homecomingservers.com/topic/27807-travel-power-updates-in-issue-27-page-2/) in SoD
* Buffer bind sets in Custom Binds
* Roll binaries for Windows, MacOS, flatpak for Linux
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

BindControl is licensed under the GPL, version 3 or later.

emerson@hayseed.net
