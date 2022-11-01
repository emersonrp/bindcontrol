BindControl
===========

BindControl is a helper app for creating and maintaining keybinds for City of Heroes.

It is an enhanced port of Konoko and Monorail's [CityBinder 0.76](http://sourceforge.net/projects/citybinder/), using Python and the WxWidgets UI toolkit.

During City of Heroes' original run, CityBinder was the go-to app for keybinds.  It's written in lua, using the IUP toolkit, and the required versions of those can be difficult to set up for development on modern OSes.  I wanted to add features and clean up the UI, so in a stunning and likely unwise act of hubris, I instead started work on BindControl.

I worked on it on-and-off for the remainder of the original run of the game, then shelved it, ostensibly forever.  Now here in the age of the SCORE, Homecoming, and other servers, it once again has value, so I've dusted it off and continued to add features and modernize it.

BindControl is initially targeted at Homecoming players, but currently almost all features will work regardless of server.  The intent is to make it server-agnostic as much as possible, and to allow the user to choose the type of server they play on for the features that differ.

Features
--------

* Runs on Windows, MacOS, and Linux
* Separate profiles for different characters or situations
* One-key next-teammate / previous-teammate selection
* Various helpful shortcut binds, "Quit to Desktop", "Invite Target", "Show FPS", "Show Netgraph" - more to come.
* Chat binds with optional 'typing' notifier
* Custom Binds
    * create simple binds using PowerBinder, a flexible tool for putting together arbitrary commands into bind strings
    * buffer binds, allowing quick one-key buffing of each teammate and/or pet
* Speed-on-Demand
    * based on [citybinder](http://sourceforge.net/projects/citybinder/) and the original Gnarly's SoD keybinds
    * supports Super Speed, Super Jump, Flight, Teleport, and Sprint powers
    * one-key reset in case SoD binds get tangled up
* Inspiration Popper
    * by-type
    * largest-first or smallest-first
    * optional /say feedback
* Mastermind / Pet Binds
    * select pets by power level: all, minions, lieutenants, and boss
    * orders for aggressive / defensive / passive stances; attack, follow, go to, and stay
    * pets can give feedback on each order;  chattiness can be toggled via keybind
    * "bodyguard mode" shortcuts -- define which pets should be treated as bodyguards, and toggle Bodyguard Mode on and off for them, <strike>with attack/follow/stance/etc orders then applying to the remaining pets.</strike> (<i>Not working as intended</i>)
    * by-name pet selection
    * next-pet / previous-pet binds

TODO
----

* Bodyguard mode, as implemented in citybinder, doesn't work as intended, and might not be able to due to game restrictions.
* Investigate improvements to Mastermind binds to clarify and expand the behavior.
* More error detection and handling
* Support [Homecoming travel power changes](https://forums.homecomingservers.com/topic/27807-travel-power-updates-in-issue-27-page-2/) in SoD
* Kheldian form/travel binds in speed-on-demand
* Temporary powers in speed-on-demand
* Additional custom bind types
* Roll standalone binaries for Windows, MacOS, Linux
    * In progress... TODO: sign / notarize MacOS App?
* More and better help text and documentation
* Fix bugs as found

Using
-----

<b>Windows and MacOS users:  try the binaries from the [latest release](https://github.com/emersonrp/bindcontrol/releases), and give feedback.  If they work for you, they're the quickest path to victory.</b>

Failing that, or if you want to run bleeding edge code:

Dependencies
------------

* [Python](https://www.python.org) version 3.10 or later
* [wxPython](https://www.wxpython.org) version 4.1 or later

Windows and MacOS users, follow the instructions on the above sites' download pages to install Python and wxPython.

<i>MacOS users: fiddling with installing recent versions of Python can be a rabbit hole.  Use the pre-rolled Bindcontrol.app if it's available and works for you.</i>

Linux users, install your distribution's packages for Python 3 and wxPython.

Running from Source
-------------------

Clone this repo.

Windows users:  Double-click `BindControl.py` in the top-level folder

Mac / Linux users: In a terminal, `cd` to where you put the BindControl source, then `python BindControl.py`.  Some distributions might need `python3` instead of `python`.

Credits and License
-------------------

BindControl is in many places a direct port of [CityBinder](http://sourceforge.net/projects/citybinder/) code, and in most other places was extremely influenced by it.  Keybinding code drew from similar code in [PADRE](https://padre.perlide.org/).

Citybinder's acknowledgements are reproduced below:
```
    Obviously, without Cryptic and NCSoft to have created/funded/published
    City of Heroes and City of Villains, there would be no point to this
    program.  Thanks to Gnarly and the numerous people who contributed to the
    creation of the Speed on Demand System.  Thanks to Sandolphan/Khaiba and
    the many people who posted Mastermind binds in the CoV Beta forums.
    Again thanks to Sandolphan for the Bodyguard mode binds.  Also thanks
    to the following people, who directly contributed to CityBinder, either
    with bug reports, feature suggestions, or contirbuted binds.
    PerezPersuader, Blue_Daze, Back_Blast, IronVulture, Darkelven,
    Shadowhand, Knight_Marshal, Nilt_, Psygon, DuskA, CyberKnight7, ErieFF,
    Darc_Reign, Beerninja, BarfBag, Oronis, TrystarMojo, Pyrobard,
    Ang_Rui_Shen, Konoko, Draznar, Local_Man, tyrose, Caustic, 80sboi,
    DarknessEternal, reiella, Robotech_Master, Ground_Zeroo, Stylina, and
    ShieldBearer.
```

BindControl is licensed under the GPL, version 3 or later.

emerson@hayseed.net
