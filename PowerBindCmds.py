#!/usr/bin/perl

use strict;

package PowerBindCmds;
use GameData;
use Powerbinder;

sub match1arg {
	my ($s,$arg1,$arg2match) = @_;
	$arg2match ||= qr|(\S*)|;
	if ($s =~ /^$arg1 ($arg2match)/i) { return $1; }
}

sub match2arg {
	my ($s,$arg1,$arg2match,$arg3match) = @_;
	$arg2match ||= qr|(\S*)|;
	$arg3match ||= qr|(\S*)|;
	if ($s =~ /^$arg1 ($arg2match) ($arg3match)/i) { return ($1, $2); }
}

################################################################################
sub formUsePowerCmd {
	my ($t,$profile,$refreshcb) = @_;
	my $powerlist = $profile->{'powerset'} || {};
# 	$t->{'settings'} = iup.frame{iup.vbox{
# 		(cbListBox("Method",{"Toggle","On","Off"},3,t.method,
# 			function(_,s,i,v)
# 				if (v == 1) { t.method = i }
# 				profile.modified = 1
# 				if (refreshcb) { refreshcb() }
# 			}
# 		)),
# 		(cbListBox("Power",powerlist,table.getn(powerlist),t.power,
# 			function(_,s,i,v)
# 				if (v == 1) { t.power = s }
# 				profile.modified = 1
# 				if (refreshcb) { refreshcb() }
# 			},
# 		196,undef,100,undef,1))
# 	}}
	return $t;
}

sub newUsePowerCmd { { type => "Use Power", method => 1, power => ''}; }

sub makeUsePowerCmd {
	my ($t) = @_;
	if ($t->{'method'} == 1) {
		return "powexecname $t->{'power'}";
	} elsif ($t->{'method'} == 2) {
		return "powexectoggleon $t->{'power'}";
	} else {
		return "powexectoggleoff $t->{'power'}";
	}
}

sub matchUsePowerCmd {
	my ($s,$profile) = @_;
	my $power = match1arg($s,"powexecname");
	if ($power) { return {type => "Use Power", method => 1, power => $power} }
	$power    = match1arg($s,"powexectoggleon");
	if ($power) { return {type => "Use Power", method => 2, power => $power} }
	$power    = match1arg($s,"powexectoggleoff");
	if ($power) { return {type => "Use Power", method => 3, power => $power} }
}

Powerbinder::addCmd("Use Power",\&newUsePowerCmd,\&formUsePowerCmd,\&makeUsePowerCmd,\&matchUsePowerCmd);
################################################################################
################################################################################
sub formCostumeChange {
	my ($t,$profile,$refreshcb) = @_;
#	t.settings = iup.frame{(cbListBox("Costume",{"First","Second","Third","Fourth","Fifth"},5,t.cslot+1,function(_,s,i,v)
#			if (v == 1) { t.cslot = i - 1 }
#			profile.modified = 1
#			if (refreshcb) { refreshcb() }
#		},undef,undef,196))}
	return $t;
}

sub newCostumeChange { return { type => "Costume Change", cslot => 0 } }

sub makeCostumeChange {
	my $s = shift;
	return $s ? "cc " . shift()->{'cslot'} : '';
}

sub matchCostumeChange {
	my ($s,$profile) = @_;
	if (my $cslot = match1arg($s,"cc|costumechange",'(\d+)')) {
		if ($cslot > -1 and $cslot < 5) {
			return { type => "Costume Change", cslot => $cslot };
		}
	}
}

Powerbinder::addCmd("Costume Change",\&newCostumeChange,\&formCostumeChange,\&makeCostumeChange,\&matchCostumeChange);
################################################################################


################################################################################
sub formAFKMessage {
	my ($t,$profile,$refreshcb) = @_;
	# t.settings = iup.frame{cbTextBox(undef,t.afkmsg,cbTextBoxCB(profile,t,"afkmsg",refreshcb),296)}
	return $t;
}

sub newAFKMessage { { type => "Away From Keyboard", afkmsg => '' } }

sub makeAFKMessage {
	my $t = shift;
	return ($t->{'afkmsg'} eq "") ? "afk" : "afk $t->{'afkmsg'}";
}

sub matchAFKMessage {
	my ($s,$profile);
	if (lc $s eq "afk ") { return }  # hmm why?
	if (lc $s eq "afk")  { return {type => "Away From Keyboard", afkmsg => ""} }
	if (my $afkmsg = match1arg($s,"afk")) { return {type => "Away From Keyboard", afkmsg => $afkmsg } }
}

Powerbinder::addCmd("Away From Keyboard",\&newAFKMessage,\&formAFKMessage,\&makeAFKMessage,\&matchAFKMessage);
################################################################################

################################################################################
sub formSGMode {
	my $t = shift;
	undef $t->{'settings'};
	return $t;
}

sub newSGMode { { type => "SGMode Toggle", nosettings => 1 } }

sub makeSGMode { "sgmode" }

sub matchSGMode {
	my $s = shift;
	if (lc $s eq "sgmode") { return { type => "SGMode Toggle", nosettings => 1 } }
}

Powerbinder::addCmd("SGMode Toggle",\&newSGMode,\&formSGMode,\&makeSGMode,\&matchSGMode);
################################################################################

################################################################################
sub formUnselect {
	my $t = shift;
	undef $t->{'settings'};
	return $t;
}

sub newUnselect { { type => "Unselect", nosettings => 1 } }

sub makeUnselect { "unselect" }

sub matchUnselect {
	my $s = shift;
	if (lc $s eq "unselect") { return { type => "Unselect", nosettings => 1 } }
}

Powerbinder::addCmd("Unselect",\&newUnselect,\&formUnselect,\&makeUnselect,\&matchUnselect);
################################################################################

################################################################################
sub formTargetEnemy {
	my ($t,$profile,$refreshcb) = @_;
#	t.settings = iup.frame{(cbListBox("Target Mode",{"Near","Far","Next","Prev"},4,t.mode,cbListBoxCB(profile,t,"mode",undef,refreshcb),undef,undef,196))}
	return $t;
}

sub newTargetEnemy { { type => "Target Enemy", mode => 1 } }

sub makeTargetEnemy {
	my $t = shift;
	return "targetenemy" . qw(near far next prev)[$t->{'mode'} - 1];
}

sub matchTargetEnemy {
	return {
		type => "Target Enemy",
		mode => {
			targetenemynear => 1,
			targetenemyfar => 2,
			targetenemynext => 3,
			targetenemyprev => 4,
		}->{ lc shift() },
	};
}

Powerbinder::addCmd("Target Enemy",\&newTargetEnemy,\&formTargetEnemy,\&makeTargetEnemy,\&matchTargetEnemy);
################################################################################

################################################################################
sub formTargetFriend {
	my ($t,$profile,$refreshcb) = @_;
#	t.settings = iup.frame{(cbListBox("Target Mode",{"Near","Far","Next","Prev"},4,t.mode,cbListBoxCB(profile,t,"mode",undef,refreshcb),undef,undef,196))}
	return $t;
}

sub newTargetFriend { { type => "Target Friend", mode => 1 } }

sub makeTargetFriend {
	my $t = shift;
	return "targetfriend" . qw(near far next prev)[$t->{'mode'} - 1];
}

sub matchTargetFriend {
	return {
		type => "Target Friend",
		mode => {
			targetfriendnear => 1,
			targetfriendfar => 2,
			targetfriendnext => 3,
			targetfriendprev => 4,
		}->{ lc shift() },
	};
}

Powerbinder::addCmd("Target Friend",\&newTargetFriend,\&formTargetFriend,\&makeTargetFriend,\&matchTargetFriend);
################################################################################

################################################################################
sub formTargetCustom {
	my ($t,$profile,$refreshcb) = @_;
#	t.settings = iup.frame{iup.vbox{
#		(cbListBox("Target Mode",{"Near","Far","Next","Prev"},4,t.mode,cbListBoxCB(profile,t,"mode",undef,refreshcb),undef,undef,196)),
#		iup.hbox{(cbCheckBox("Target Enemies",t.enemy,cbCheckBoxCB(profile,t,"enemy",refreshcb),148)),
#			(cbCheckBox("Target Friends",t.friend,cbCheckBoxCB(profile,t,"friend",refreshcb),148))},
#		iup.hbox{(cbCheckBox("Target Defeated",t.defeated,cbCheckBoxCB(profile,t,"defeated",refreshcb),148)),
#			(cbCheckBox("Target Living",t.alive,cbCheckBoxCB(profile,t,"alive",refreshcb),148))},
#		iup.hbox{(cbCheckBox("Target My Pets",t.mypet,cbCheckBoxCB(profile,t,"mypet",refreshcb),148)),
#			(cbCheckBox("Target Not My Pets",t.notmypet,cbCheckBoxCB(profile,t,"notmypet",refreshcb),148))},
#		iup.hbox{(cbCheckBox("Target Base Items",t.base,cbCheckBoxCB(profile,t,"base",refreshcb),148)),
#			(cbCheckBox("Target No Base Items",t.notbase,cbCheckBoxCB(profile,t,"notbase",refreshcb),148))}
#		}
#	}
	return $t;
}

sub newTargetCustom { { type => "Target Custom", mode => 1 } }

sub makeTargetCustom {
	my $t = shift;
	my $bind = "targetcustom" . qw(near far next prev)[$t->{'mode'} - 1];

	for (qw(enemy friend defeated alive mypet notmypet base notbase)) {
		$bind .= " $_" if $t->{$_};
	}
	return $bind;

}

sub matchTargetCustom {
	my $s = shift;

	my $return = {};

	for my $v (qw( near far next prev )) {
		return if (lc $s eq "targetcustom$v");  # bail if there's nothing special
		if (my $msg = match1arg($s,"targetcustom$v")) {

			for my $case (qw(enemy friend defeated alive mypet notmypet base notbase)) {
				$return->{$case} = $msg =~ s/ $case//ig;
			}
		}
	}

	return $return;
}

Powerbinder::addCmd("Target Custom",\&newTargetCustom,\&formTargetCustom,\&makeTargetCustom,\&matchTargetCustom);
################################################################################

################################################################################
sub formPowExecTray {
	my ($t,$profile,$refreshcb) = @_;
#	t.settings = iup.frame{iup.hbox{
#		(cbListBox("Power Tray",{"Main Tray","Alt Tray","Alt 2 Tray","Tray 1","Tray 2","Tray 3","Tray 4","Tray 5","Tray 6","Tray 7","Tray 8","Tray 9","Tray 10"},13,t.tray,cbListBoxCB(profile,t,"tray",undef,refreshcb),74,undef,74)),
#		(cbListBox("Power Slot",{"1","2","3","4","5","6","7","8","9","10"},10,t.slot,cbListBoxCB(profile,t,"slot",undef,refreshcb),74,undef,74)),
#		}
#	}
	return $t;
}

sub newPowExecTray { { type => "Use Power From Tray", tray => 1, slot => 1 } }

sub makePowExecTray {
	my $t = shift;
	my $mode = "slot";
	my $mode2 = "";
	if ($t->{'tray'}  > 3) { $mode = "tray"; $mode2 = " ".($t->{'tray'} - 3); }
	if ($t->{'tray'} == 3) { $mode = "alt2slot"; }
	if ($t->{'tray'} == 2) { $mode = "altslot"; }
	return "powexec$mode $t->{'slot'}$mode2";
}

sub matchPowExecTray {
	my $s = shift;
	my ($tray, $slot);

	if ($slot = match1arg($s,"powexecslot"))     { return { type => "Use Power From Tray", tray => 1, slot => $slot }; }
	if ($slot = match1arg($s,"powexecaltslot"))  { return { type => "Use Power From Tray", tray => 2, slot => $slot }; }
	if ($slot = match1arg($s,"powexecalt2slot")) { return { type => "Use Power From Tray", tray => 3, slot => $slot }; }

	($slot,$tray) = match2arg($s,"powexectray");
	if ($slot and $tray) { return { type => "Use Power From Tray", tray => $tray+3, slot => $slot }; }
}

Powerbinder::addCmd("Use Power From Tray",\&newPowExecTray,\&formPowExecTray,\&makePowExecTray,\&matchPowExecTray);
################################################################################

################################################################################
sub formCustomBind {
	my ($t,$profile,$refreshcb) = @_;
#	t.settings = iup.frame{(cbTextBox(undef,t.custom,cbTextBoxCB(profile,t,"custom",refreshcb),296))}
	return $t;
}

sub newCustomBind { { type => "Custom Bind", custom => '' } }

sub makeCustomBind {
	my $s = shift;
	return $s ? $s->{'custom'} : '';
}

Powerbinder::addCmd("Custom Bind",\&newCustomBind,\&formCustomBind,\&makeCustomBind);
################################################################################

################################################################################
sub formEmoteBind {
	my ($t,$profile,$refreshcb) = @_;
#	t.settings = iup.frame{(cbListBox("Emote",@GameData::Emotes,emotecount,t.emote,cbListBoxCB(profile,t,undef,"emote",refreshcb),196,undef,undef,undef,1))}
	return $t;
}

sub newEmoteBind { { type => "Emote", emote => "afraid" } }

sub makeEmoteBind {
	my $s = shift;
	return $s ? "em $s->{'emote'}" : '';
}

sub matchEmoteBind { if (my $emote = match1arg(shift(),"e|em|me|emote")) { return {type => "Emote",emote => $emote } } }

Powerbinder::addCmd("Emote",\&newEmoteBind,\&formEmoteBind,\&makeEmoteBind,\&matchEmoteBind);
################################################################################

################################################################################
sub formPowerAbort {
	my $t = shift;
	undef $t->{'settings'};
	return $t;
}

sub newPowerAbort { { type => "Power Abort", nosettings => 1 } }

sub makePowerAbort { "powexecabort" }

sub matchPowerAbort { if (lc shift() eq "powexecabort") { return { type => "Power Abort", nosettings => 1 } } }

Powerbinder::addCmd("Power Abort",\&newPowerAbort,\&formPowerAbort,\&makePowerAbort,\&matchPowerAbort);
################################################################################

################################################################################
sub formPowerUnqueue {
	my $t = shift;
	undef $t->{'settings'};
	return $t;
}

sub newPowerUnqueue { { type => "Power Unqueue", nosettings => 1 } }

sub makePowerUnqueue { "powexecunqueue" }

sub matchPowerUnqueue { if (lc shift() eq "powexecunqueue") { return { type => "Power Unqueue", nosettings => 1 } } }

Powerbinder::addCmd("Power Unqueue",\&newPowerUnqueue,\&formPowerUnqueue,\&makePowerUnqueue,\&matchPowerUnqueue);
################################################################################

################################################################################
sub formAutoPower {
	my ($t,$profile,$refreshcb) = @_;
#	my powerlist = profile.powerset or {}
#	t.settings = iup.frame{(cbListBox("Power",powerlist,table.getn(powerlist),t.power,
#		function(_,s,i,v)
#			if (v == 1) { t.power = s }
#			profile.modified = 1
#			if (refreshcb) { refreshcb() }
#		},196,undef,100,undef,1))
#	}
	return $t;
}

sub newAutoPower { { type => "Auto Power", power => '' } }

sub makeAutoPower {
	my $s = shift;
	return $s ? "powexecauto $s->{'power'}" : '';
}

sub matchAutoPower {
	my $s = shift;
	if (my $power = match1arg($s, "powexecauto")) {
		return { type => "Auto Power", power => $power } };
	}

Powerbinder::addCmd("Auto Power",\&newAutoPower,\&formAutoPower,\&makeAutoPower,\&matchAutoPower);
################################################################################

################################################################################
sub formInspExecTray {
	my ($t,$profile,$refreshcb) = @_;
#	t.settings = iup.frame{iup.hbox{
#		(cbTextBox("Row",t.row,cbTextBoxCB(profile,t,"row",refreshcb),74,undef,74)),
#		(cbTextBox("Column",t.col,cbTextBoxCB(profile,t,"col",refreshcb),74,undef,74)),
#		}
#	}
	return $t;
}

sub newInspExecTray { { type => "Use Inspiration From Row/Column", row => 1, col => 1 } }

sub makeInspExecTray {
	my $t = shift;
	if ($t->{'row'} == "1") {
		return "inspexecslot $t->{'col'}"
	} else {
		return "inspexectray $t->{'col'} $t->{'row'}"
	}
}

sub matchInspExecTray {
	my $s = shift;
	my ($col,$row) = match2arg($s,"inspexectray","(%d*)","(%d*)");
	if ($col and $row) { return { type => "Use Inspiration From Row/Column", row => $row, col => $col } }

	$col = match1arg($s,"inspexecslot","(%d*)");
	if ($col) { return { type => "Use Inspiration From Row/Column", row => 1, col => $col } }
}

Powerbinder::addCmd("Use Inspiration From Row/Column",\&newInspExecTray,\&formInspExecTray,\&makeInspExecTray,\&matchInspExecTray);
################################################################################

################################################################################

sub formInspExecName {
	my ($t,$profile,$refreshcb) = @_;
#	t.settings = iup.frame{
#		(cbListBox("Inspiration",insps,table.getn(insps),t.insp,cbListBoxCB(profile,t,"insp",undef,refreshcb),196))
#	}
	return $t;
}

sub newInspExecName { { type => "Use Inspiration By Name", insp => 1 } }

sub makeInspExecName {
	my $s = shift;
	return $s ? "inspexecname " . $GameData::Inspirations[$s->{'insp'}] : '';
}

sub matchInspExecName {
	my $s = shift;
	for my $v (@GameData::Inspirations) {
		if (lc $s eq lc "inspexecname $v") { return { type => "Use Inspiration By Name" , insp => $v } }
	}
}

Powerbinder::addCmd("Use Inspiration By Name",\&newInspExecName,\&formInspExecName,\&makeInspExecName,\&matchInspExecName);
################################################################################

################################################################################
sub formGlobalChat {
	my ($t,$profile,$refreshcb) = @_;
#	if (t.prefix) { t.msg = t.prefix..' '..t.msg t.prefix = undef }
#	t.settings = iup.frame{iup.vbox{
#		(cbTextBox("Channel",t.channel,cbTextBoxCB(profile,t,"channel",refreshcb),196,undef,100)),
#		(cbCheckBox("Use Beginchat",not t.usemsg,cbCheckBoxCB(profile,t,"usemsg",
#			function()
#				t.usemsg = not t.usemsg
#				if (refreshcb) {
#					refreshcb()
#				}
#			}),196,undef,100)),
#		(cbTextBox("Message",t.msg,cbTextBoxCB(profile,t,"msg",refreshcb),100,undef,196))}
#	}
	return $t;
}

sub newGlobalChat { { type => "Chat Command (Global)", channel => "BindControl", msg => '[$name $level]' } }

sub makeGlobalChat {
	my $t = shift;
	if ($t->{'prefix'}) {
		$t->{'msg'} = "$t->{'prefix'} $t->{'msg'}";
		undef $t->{'prefix'};
	}
	if ($t->{'usemsg'}) {
		return qq|send "$t->{'channel'}" $t->{'msg'}|;
	} else {
		return qq|beginchat /send "$t->{'channel'}" $t->{'msg'}|;
	}
}

sub matchGlobalChat {
	my $s = shift;

	my ($channel, $msg) = match2arg($s,'send','"([^"]*)"','(.*)');

	if ($channel and $msg) { return { type => "Chat Command (Global)", usemsg => 1, channel => $channel, msg => $msg } }
	# channel, msg = match2arg(s,'beginchat /send','"([^"]*)"','(.*) ')
	# if (channel and msg) { return {type="Chat Command (Global)",channel=channel,msg=msg} }
	if ($s =~ s(^beginchat )()) {
		($channel, $msg) = match2arg($s,'send','"([^"]*)"','(.*)')
	} else {
		return undef
	}
	if ($channel and $msg) { return { type => "Chat Command (Global)", channel => $channel, msg => $msg } }
}

Powerbinder::addCmd("Chat Command (Global)",\&newGlobalChat,\&formGlobalChat,\&makeGlobalChat,\&matchGlobalChat);
################################################################################

################################################################################
my @windowlist = ("powers","manage","chat","tray","target","nav","map","menu","pets");

sub formWindowToggle {
	my ($t,$profile,$refreshcb) = @_;
#	t.settings = iup.frame{(cbListBox("Window",windowlist,table.getn(windowlist),t.window,
#		function(_,s,i,v)
#			if (v == 1) { t.window = s }
#			profile.modified = 1
#			if (refreshcb) { refreshcb() }
#		},196,undef,100,undef,1))
#	}
	return $t;
}

sub newWindowToggle { { type => "Window Toggle", window => "powers" } }

sub makeWindowToggle {
	my $s = shift;
	return $s ? $s->{'window'} : '';
}

sub matchWindowToggle {
	my $s = lc shift;
	if ($s ~~ @windowlist) { return { type => "Window Toggle", window => $s} }
}

Powerbinder::addCmd("Window Toggle",\&newWindowToggle,\&formWindowToggle,\&makeWindowToggle,\&matchWindowToggle);
################################################################################

################################################################################
sub formTeamPetSelect {
	my ($t,$profile,$refreshcb) = @_;
#	t.settings = iup.frame{iup.vbox{(cbListBox("Team or Pet Select",{"Teammate","Henchman"},2,t.teamsel,
#			function(_,s,i,v)
#				if (v == 1) { t.teamsel = i }
#				profile.modified = 1
#				if (refreshcb) { refreshcb() }
#			},196,undef,100,undef)),
#		(cbListBox("Team/Pet Number",{"1","2","3","4","5","6","7","8","9","10","11"},11,t.number,
#			function(_,s,i,v)
#				if (v == 1) { t.number = i }
#				profile.modified = 1
#				if (refreshcb) { refreshcb() }
#			},196,undef,100,undef))
#	}}
	return $t;
}

sub newTeamPetSelect { { type => "Team/Pet Select", teamsel => 1, number => 1 } }

sub makeTeamPetSelect {
	my $t = shift;
	return ($t->{'teamsel'} == 1) ? "teamselect $t->{'number'}" : "petselect " . $t->{'number'}-1;
}

sub matchTeamPetSelect {
	my $s = shift;
	my $number = match1arg($s,"teamselect","(%d*)");
	if ($number) { return { type => "Team/Pet Select", teamsel => 1, number => $number } }
	$number = match1arg($s,"petselect","(%d*)");
	if ($number) { return { type => "Team/Pet Select", teamsel => 2, number => $number+1 } }
}

Powerbinder::addCmd("Team/Pet Select",\&newTeamPetSelect,\&formTeamPetSelect,\&makeTeamPetSelect,\&matchTeamPetSelect);
################################################################################

################################################################################
sub cbGetColor {
	my ($r,$g,$b) = @_;
# 	my tr, tg, tb = r,g,b
# 	my redbox, greenbox, bluebox
# 	my colorbox
# 	my okbtn, cancelbtn
# 	colorbox = iup.colorbrowser{rgb=tr.." "..tg.." "..tb}
# 	redbox,redtext = cbTextBox("Red:",tr,function(_,c,s) tr = tonumber(s) colorbox.rgb = tr.." "..tg.." "..tb return iup.DEFAULT })
# 	greenbox,greentext = cbTextBox("Green:",tg,function(_,c,s) tg = tonumber(s) colorbox.rgb = tr.." "..tg.." "..tb return iup.DEFAULT })
# 	bluebox,bluetext = cbTextBox("Blue:",tb,function(_,c,s) tb = tonumber(s) colorbox.rgb = tr.." "..tg.." "..tb return iup.DEFAULT })
# 	colorbox.drag_cb = function(_,cbr,cbg,cbb) tr, tg, tb = cbr, cbg, cbb redtext.value = cbr greentext.value = cbg bluetext.value = cbb }
# 	okbtn = iup.button{title="OK";rastersize="100x21"}
# 	cancelbtn = iup.button{title="Cancel";rastersize="100x21"}
# 	my box = iup.hbox{colorbox,iup.vbox{redbox,greenbox,bluebox,iup.hbox{okbtn,cancelbtn}}}
# 	my colordlg = iup.dialog{box,title="Select a Color",maxbox="NO",resize="NO"}
# 	okbtn.action = function() colordlg:hide() }
# 	cancelbtn.action = function() tr,tg,tb = r,g,b colordlg:hide() }
# 	colordlg:popup(iup.CENTER,iup.CENTER)
# 	return tr, tg, tb
}

sub formChatCommand {
	my ($t,$profile,$refreshcb) = @_;
#	my bordercolor = iup.label{title=" ";image = buildColorImage(t.border.r,t.border.g,t.border.b); rastersize="17x17"}
#	my borderbtn = iup.button{title="Border";rastersize="46x21"}
#	borderbtn.action=function()
#		t.border.r,t.border.g,t.border.b = cbGetColor(t.border.r,t.border.g,t.border.b)
#		bordercolor.image = buildColorImage(t.border.r,t.border.g,t.border.b)
#		if (refreshcb) { refreshcb() }
#		profile.modified = 1
#	}
#	my bgcolor = iup.label{title=" ";image = buildColorImage(t.bgcolor.r,t.bgcolor.g,t.bgcolor.b); rastersize="17x17"}
#	my bgbtn = iup.button{title="BG";rastersize="45x21"}
#	bgbtn.action=function()
#		t.bgcolor.r,t.bgcolor.g,t.bgcolor.b = cbGetColor(t.bgcolor.r,t.bgcolor.g,t.bgcolor.b)
#		bgcolor.image = buildColorImage(t.bgcolor.r,t.bgcolor.g,t.bgcolor.b)
#		if (refreshcb) { refreshcb() }
#		profile.modified = 1
#	}
#	my textcolor = iup.label{title=" ";image = buildColorImage(t.fgcolor.r,t.fgcolor.g,t.fgcolor.b); rastersize="17x17"}
#	my textbtn = iup.button{title="Text";rastersize="46x21"}
#	textbtn.action=function()
#		t.fgcolor.r,t.fgcolor.g,t.fgcolor.b = cbGetColor(t.fgcolor.r,t.fgcolor.g,t.fgcolor.b)
#		textcolor.image = buildColorImage(t.fgcolor.r,t.fgcolor.g,t.fgcolor.b)
#		if (refreshcb) { refreshcb() }
#		profile.modified = 1
#	}
#
#	t.settings = iup.frame{iup.vbox{
#		(cbCheckBox("Chat Bubble Colors",t.usecolors,function(_,v) if (v == 1) { t.usecolors = 1 } else { t.usecolors = undef } profile.modified = 1 if (refreshcb) { refreshcb() } })),
#		iup.hbox{
#			iup.frame{bordercolor;sunken="YES"; rastersize="21x21";margin="1x1"},borderbtn,
#			iup.frame{bgcolor;sunken="YES"; rastersize="21x21";margin="1x1"},bgbtn,
#			iup.frame{textcolor;sunken="YES"; rastersize="21x21";margin="1x1"},textbtn},
#		(cbListBox("Duration",{"1","2","3","4","5","6","7 (Default)","8","9","10","11","12","13","14","15","16","17","18","19","20"},20,t.duration,function(_,s,i,v)
#			if (v == 1) { t.duration = i } profile.modified = 1 if (refreshcb) { refreshcb() } })),
#		(cbListBox("Size",{"0.5","0.6","0.7","0.8","0.9","1.0","1.1","1.2","1.3","1.4","1.5"},11,tostring(t.size),function(_,s,i,v)
#			if (v == 1) { t.size = tonumber(s) } profile.modified = 1 if (refreshcb) { refreshcb() } },undef,undef,undef,undef,1)),
#		(cbListBox("Channel",{"say","group","broadcast","my","yell","fri}s","request","arena","supergroup","coalition","tell $target,","tell $name,"},12,t.channel,cbListBoxCB(profile,t,"channel",undef,refreshcb))),
#		--(cbToggleText("Message",t.usemsg,t.text,cbCheckBoxCB(profile,t,"usemsg"),cbTextBoxCB(profile,t,"text",refreshcb),undef,undef,196))
#		(cbCheckBox("Use Beginchat",not t.usemsg,cbCheckBoxCB(profile,t,"usemsg",
#			function()
#				t.usemsg = not t.usemsg
#				if (refreshcb) { refreshcb() }
#			}),196)),
#		(cbTextBox("Message",t.text,cbTextBoxCB(profile,t,"text",refreshcb),196,undef,100))
#		--iup.label{title="Text"},
#		--cbTextBox(undef,t.text,function(_,c,s) profile.modified = 1 t.text = s return iup.DEFAULT },296)
#	}}
	return $t;
}

sub newChatCommand {
	{
		type => "Chat Command",
		channel => 1,
		text => "",
		duration => 7,
		size => 1.0,
		usecolors => undef,
		border => {r=>0,g=>0,b=>0},
		fgcolor => {r=>0,g=>0,b=>0},
		bgcolor => {r=>255,g=>255,b=>255},
	}
}

my @chatchannelmap = ("s","g","b","l","y","f","req","ac","sg","c",'t $target,','t $name,');

sub makeChatCommand {
	my $t = shift;

	my $size =     ($t->{'size'}     == 1) ? '' : "<scale $t->{'size'}>";
	my $duration = ($t->{'duration'} == 7) ? '' : "<duration $t->{'duration'}>";

	my $border =  sprintf("<bordercolor #%02x%02x%02x>",$t->{'border'}->{'r'}, $t->{'border'}->{'g'} ,$t->{'border'}->{'b'});
	my $color =   sprintf("<color #%02x%02x%02x>",      $t->{'fgcolor'}->{'r'},$t->{'fgcolor'}->{'g'},$t->{'fgcolor'}->{'b'});
	my $bgcolor = sprintf("<bgcolor #%02x%02x%02x>",    $t->{'bgcolor'}->{'r'},$t->{'bgcolor'}->{'g'},$t->{'bgcolor'}->{'b'});
	if (not $t->{'usecolors'}) {
		$border = "";
		$color = "";
		$bgcolor = "";
	}
	if ($t->{'usemsg'}) {
		return "$chatchannelmap[$t->{'channel'}] $size$duration$border$color$bgcolor$t->{'text'}";
	} else {
		return "beginchat /$chatchannelmap[$t->{'channel'}] $size$duration$border$color$bgcolor$t->{'text'}";
	}
}

sub stringToColor {
	(my $s = shift) =~ /(..)(..)(..)/;
	my ($r, $g, $b) = (
		hex(sprintf('%x',$1)),
		hex(sprintf('%x',$2)),
		hex(sprintf('%x',$3)),
	);
	return { r => $r, g => $g, b => $b };
}

my @chatchannel = ('s','g','b','l','y','f','req','ac','sg','c','t $target,','t $name,','tell $target,','tell $name,','p $target,','p $name,',
	'private $target,','private $name,','whisper $target,','whisper $name,','friends','group','team','yell','broadcast','local','request','sell',
	'auction','supergroup','coalition','arena','say');

my %revchatchannel = (
	'say' => 1,
	's' => 1,
	't $target,' => 11,
	'tell $target,' => 11,
	'private $target,' => 11,
	'p $target,' => 11,
	'whisper $target,' => 11,
	't $name,' => 12,
	'tell $name,' => 12,
	'private $name,' => 12,
	'p $name,' => 12,
	'whisper $name,' => 12,
	'f' => 6,
	'group' => 2,
	'g' => 2,
	'team' => 2,
	'yell' => 5,
	'y' => 5,
	'broadcast' => 3,
	'b' => 3,
	'local' => 4,
	'l' => 4,
	'request' => 7,
	'req' => 7,
	'sell' => 7,
	'auction' => 7,
	'supergroup' => 9,
	'sg' => 9,
	'coalition' => 10,
	'c' => 10,
	'ac' => 8,
	'arena' => 8,
);

sub matchChatCommand {
	my $s = lc shift;
	for my $v (@chatchannel) {
		my $withmessage = 1;
		my $msg = match1arg($s,$v);
		if (not $msg) {
			if ((my $s2 = $s) =~ s#^beginchat /##) {
				$msg = match1arg($s2,$v);
				undef $withmessage if $msg;
			}
		}
		if (not $msg) {
			if ($s eq "beginchat /$v ") {
				$msg = "";
				undef $withmessage;
			}
		}
		if ($msg) {
			my $size = match1arg($msg,"<scale","(.*)>");
			if ($size) {
				$msg =~ s/<scale $size>//gi;
			}
			$size ||= 1;

			my $duration = match1arg($msg,"<duration","(.*)>");
			if ($duration) {
				$msg =~ s/<duration $duration>//gi;
			}
			$duration ||= 7;

			my $usecolors;
			my $border = match1arg($msg,"<bordercolor","#(%x%x%x%x%x%x)>");
			if ($border) {
				$msg =~ s/<bordercolor #$border>//gi;
				$border = stringToColor($border);
				$usecolors = 1;
			}
			$border ||= {r=>0,g=>0,b=>0};

			my $color = match1arg($msg,"<color","#(%x%x%x%x%x%x)>");
			if ($color) {
				$msg =~ s/<color #$color>//gi;
				$color = stringToColor($color);
				$usecolors = 1;
			}
			$color ||= {r=>0,g=>0,b=>0};

			my $bgcolor = match1arg($msg,"<bgcolor","#(%x%x%x%x%x%x)>");
			if ($bgcolor) {
				$msg = s/<bgcolor #$bgcolor>//gi;
				$bgcolor = stringToColor($bgcolor);
				$usecolors = 1;
			}
			$bgcolor ||= {r=>255,g=>255,b=>255};

			return {
				type => "Chat Command",
				channel => $revchatchannel{$v},
				usemsg => $withmessage,
				text => $msg,
				duration => $duration,
				size => $size,
				usecolors => $usecolors,
				border => $border,
				fgcolor => $color,
				bgcolor => $bgcolor,
			};
		}
	}
}

Powerbinder::addCmd("Chat Command",\&newChatCommand,\&formChatCommand,\&makeChatCommand,\&matchChatCommand);

# chatnogloballimit = {cmdlist={"Emote","Custom Bind","Costume Change","Chat Command"}};

1;
