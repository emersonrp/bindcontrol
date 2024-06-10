BindControl
===========

BindControl is a helper app for creating and maintaining keybinds for City of Heroes.

It is an enhanced port of Konoko and Monorail's [CityBinder 0.76](http://sourceforge.net/projects/citybinder/), using Python and the WxWidgets UI toolkit.

During City of Heroes' original run, CityBinder was the go-to app for keybinds.  It's written in lua, using the IUP toolkit, and the required versions of those can be difficult to set up for development on modern OSes.  I wanted to add features and clean up the UI, so in a stunningly unwise act of hubris, I instead started work on BindControl.

I worked on it on-and-off for the remainder of the original run of the game, then shelved it, ostensibly forever.  Now here in the age of the SCORE, Homecoming, and other servers, it once again has value, so I've dusted it off and continued to add features and modernize it.

With Homecoming recently securing the licensing for City of Heroes from NCSoft, development of the game and its ecosystem, BindControl included, is likely to remain very Homecoming-centric in the near to medium term.  Recent changes to BindControl's Speed on Demand code incorporate changes made specifically in Homecoming Issue 27, and while it will probably continue to work elsewhere, I don't currently have a presence on these other servers to test and validate.  Please feel free to open issues for non-Homecoming servers, but know that they might not receive as much attention as Homecoming-specific ones do.

Features
--------

* Runs on Windows, MacOS, and Linux
* Separate profiles for different characters, archetypes, or situations
* One-key next-teammate / previous-teammate selection, with support for setting team size and optionally skipping the player in the next/previous rotation
* Various helpful shortcut binds, "Quit to Desktop", "Invite Target", "Show FPS", "Show Netgraph" - more to come.
* Chat binds with optional 'typing' notifier and custom chat colors
* Controller support (WIP, binds created with a controller work perfectly, but BindControl itself sometimes has trouble detecting controller input)

* Custom Binds
    * Create simple binds using PowerBinder, a flexible tool for stringing together arbitrary commands for keybinding
    * Complex binds, chains of PowerBinder actions that fire sequentially on multiple presses of a keybind
    * Buffer binds, allowing quick one-key buffing of each teammate and/or pet
* Movement / Speed-on-Demand
    * Speed-on-Demand based on [citybinder](http://sourceforge.net/projects/citybinder/) and the original Gnarly's SoD keybinds
    * Supports all formal travel powers:  Fly, Mystic Flight, Group Fly, Super Jump, Mighty Leap, Super Speed, Speed of Sound, Teleport, and Team Teleport
    * Secondary travel powers like Mystic Flight's "Translocation" are starting to be better integrated
    * Supports [Homecoming travel power changes](https://forums.homecomingservers.com/topic/27807-travel-power-updates-in-issue-27-page-2/) - WIP but functional
    * Homecoming's <code>powexec_location cursor</code> feature incorporated into Teleport binds, with "teleport immediately" and "teleport on key release" options available
    * Kheldian form toggles;  Kheldian movement powers incorporated into Speed-on-Demand
    * One-key reset in case SoD binds get tangled up
* Inspiration Popper
    * By-type; dual and team inspirations supported
    * Option to use or skip "super" inspirations
    * Largest-first or smallest-first
    * Optional /say feedback with per-inspiration custom colors
* Mastermind / Pet Binds
    * Select pets by power level: all, minions, lieutenants, and boss
    * Orders for aggressive / defensive / passive stances; attack, follow, go to, and stay
    * Pets can give feedback on each order;  chattiness can be toggled via keybind
    * "Bodyguard mode" shortcuts -- define which pets should be treated as bodyguards, and toggle Bodyguard Mode on and off for them, <strike>with attack/follow/stance/etc orders then applying to the remaining pets.</strike> (<i>Not working as intended</i>)
    * By-name pet selection
    * Next-pet / previous-pet binds

TODO
----

* Access to MacOS for testing is via a MacOS VM several OS versions old.  I don't want to buy an actual Mac just for this wee vanity project, so mileage may vary on how it acts in an actual recent Mac environment.
* Bodyguard mode, as implemented in citybinder, doesn't work as intended, and might not be able to due to game restrictions.
* Investigate improvements to Mastermind binds to clarify and expand the behavior.
* More error detection and handling
* Temporary powers in speed-on-demand
* Roll standalone binaries for Windows, MacOS, Linux - partially implemented
    * Windows binary distribution of Python apps can trigger <a href="Help/MalwareWarnings.md">anti-malware warnings</a>
    * MacOS binaries need signing and notarization;  I release them anyway for the brave
    * Linux binaries might be possible with some container scheme
* More and better help text and documentation
* Fix bugs as found

Using Binary Releases
---------------------

Windows users:  try the ZIP file from the [latest release](https://github.com/emersonrp/bindcontrol/releases), and give feedback.  If that works for you, it's the quickest path to victory.

MacOS users:  an experimental binary release has been made available.  It is not signed and/or notarized, and might or might not work at all.  Any feedback is encouraged.

<b>If you receive malware warnings</b>, please read <a href="Help/MalwareWarnings.md">my comments on that issue</a>.

Running From Source
-------------------

### Dependencies

1. [Python](https://www.python.org) version 3.10 or later
2. [wxPython](https://www.wxpython.org) version 4.1 or later

* Windows users, follow the instructions on the above sites' download pages to install Python and wxPython.

* MacOS users, I recommend following the instructions in [this article at opensource.com](https://www.opensource.com/article/19/5/python-3-default-mac) to get Python 3 installed and working by default.  Once everything is working, you will want to run `pip3 install wxPython`.

* Linux users, install your distribution's packages for Python 3 and wxPython.

### Getting and running the code

* Clone this repo.

* Windows (and possibly Mac) users:  Double-click `BindControl.py` in the top-level folder

* Mac / Linux users: In a terminal, `cd` to where you put the BindControl source, then `python BindControl.py`.  Some distributions might need `python3` instead of `python`.

Credits
-------

BindControl is in many places a direct port of [CityBinder](http://sourceforge.net/projects/citybinder/) code, and in most other places was extremely influenced by it.  Keybinding code drew from similar code in [PADRE](https://padre.perlide.org/).

Various newer functionality was added to [CityBinder for Homecoming](https://sourceforge.net/projects/citybinder-for-homecoming/) by tailcoat, who kindly provided his source code and permission to adapt for use with BindControl, as well as offered suggestions and advice for improvements.

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

The improved Inspiration Popper design was gratefully adapted from an unreleased version of [CityBinder for Homecoming](https://sourceforge.net/projects/citybinder-for-homecoming/) by Tailcoat.

Github Actions for automated building of binary releases graciously provided by <a href="https://github.com/JamzTheMan">JamzTheMan</a>.

Additional feedback and suggestions provided in the <a href="https://forums.homecomingservers.com/topic/38674-bindcontrol-alternative-to-citybinder/">Homecoming Forums thread</a> and in <a href="https://github.com/emersonrp/bindcontrol/issues">Github issues</a> by:<br>
DevoDog68, BlackSpectre, Premmy, kenlon, Lumenia, xizar, autobotpinto


License
-------

BindControl is licensed under the <a href="Help/LICENSE.html">GPL version 3</a> or later.


emerson@hayseed.net
