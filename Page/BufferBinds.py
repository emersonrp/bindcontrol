#1/usr/bin/perl

use strict;

package Page::BufferBinds;
use parent "Page::Page";

use BindFile;

our $PageName = 'BufferBinds';

sub addBBind {
	my ($bbinds,$n,$profile) = @_;
#	my $bbind = $bbinds[$n]
#	my $bbtitle = cbTextBox("Buffer Bind Name",$bbind->{'title'},cbTextBoxCB($profile,$bbind,"title"),300,undef,100)
#	# my $selchattext = cbToggleText("Select Chat",$bbind->{'selchatenabled'},$bbind->{'selchat'},
#		# cbCheckBoxCB($profile,$bbind,"selchatenabled"),cbTextBoxCB($profile,$bbind,"selchat"),100,undef,300)
#	my $selchattext = cbPowerBindBtn("Select Chat",$bbind,"selchat",chatnogloballimit,300,undef,$profile)
#	# my $buffpower1 = cbTextBox("Buff Power",$bbind->{'power1'},cbTextBoxCB($profile,$bbind,"power1"))
#	my $buffpower1 = cbPowerList("First Buff Power",$profile->{'powerset'},$bbind,"power1",$profile,200)
#	my $chat1text = cbPowerBindBtn("First Chat Command",$bbind,"chat1",chatnogloballimit,300,undef,$profile)
#	my $chat3text = cbPowerBindBtn("Third Chat Command",$bbind,"chat3",chatnogloballimit,300,undef,$profile)
#	if (not $bbind->{'power3enabled'}) { chat3text.active = "NO" }
#	my $buffpower3 = cbTogglePower("Third Buff Power",$profile->{'powerset'},$bbind->{'power3enabled'},$bbind,"power3",
#		sub { my(_,v) $profile->{'modified'} = true 
#			if (v == 1) {
#				$bbind->{'power3enabled'} = true
#				chat3text.active = "YES"
#			} else {
#				$bbind->{'power3enabled'} = undef
#				chat3text.active = "NO"
#			}
#		},$profile,undef,undef,200)
#	if (not $bbind->{'power2enabled'}) { buffpower3.active = "NO" }
#	my $chat2text = cbPowerBindBtn("Second Chat Command",$bbind,"chat2",chatnogloballimit,300,undef,$profile)
#	if (not $bbind->{'power2enabled'}) { chat2text.active = "NO" }
#	my $buffpower2 = cbTogglePower("Second Buff Power",$profile->{'powerset'},$bbind->{'power2enabled'},$bbind,"power2",
#		sub { my(_,v) $profile->{'modified'} = true 
#			if (v == 1) {
#				$bbind->{'power2enabled'} = true
#				chat2text.active = "YES"
#				buffpower3.active = "YES"
#				if ($bbind->{'power3enabled'}) {
#					chat3text.active = "YES"
#				}
#			} else {
#				$bbind->{'power2enabled'} = undef
#				chat2text.active = "NO"
#				buffpower3.active = "NO"
#				chat3text.active = "NO"
#			}
#		},$profile,undef,undef,200)
#	my $team1key = cbBindBox("Team 1 Key",$bbind,"team1",cbMakeDescLink("Buff Bind ",$bbind,"title",": Team 1 Key"),$profile)
#	my $team2key = cbBindBox("Team 2 Key",$bbind,"team2",cbMakeDescLink("Buff Bind ",$bbind,"title",": Team 2 Key"),$profile)
#	my $team3key = cbBindBox("Team 3 Key",$bbind,"team3",cbMakeDescLink("Buff Bind ",$bbind,"title",": Team 3 Key"),$profile)
#	my $team4key = cbBindBox("Team 4 Key",$bbind,"team4",cbMakeDescLink("Buff Bind ",$bbind,"title",": Team 4 Key"),$profile)
#	my $team5key = cbBindBox("Team 5 Key",$bbind,"team5",cbMakeDescLink("Buff Bind ",$bbind,"title",": Team 5 Key"),$profile)
#	my $team6key = cbBindBox("Team 6 Key",$bbind,"team6",cbMakeDescLink("Buff Bind ",$bbind,"title",": Team 6 Key"),$profile)
#	my $team7key = cbBindBox("Team 7 Key",$bbind,"team7",cbMakeDescLink("Buff Bind ",$bbind,"title",": Team 7 Key"),$profile)
#	my $team8key = cbBindBox("Team 8 Key",$bbind,"team8",cbMakeDescLink("Buff Bind ",$bbind,"title",": Team 8 Key"),$profile)
#	my $usepetnames = cbCheckBox("Use Pet Names to Select?",$bbind->{'usepetnames'},cbCheckBoxCB($profile,$bbind,"usepetnames"))
#	my $pet1key = cbBindBox("Pet 1 Key",$bbind,"pet1",cbMakeDescLink("Buff Bind ",$bbind,"title",": Pet 1 Key"),$profile)
#	my $pet2key = cbBindBox("Pet 2 Key",$bbind,"pet2",cbMakeDescLink("Buff Bind ",$bbind,"title",": Pet 2 Key"),$profile)
#	my $pet3key = cbBindBox("Pet 3 Key",$bbind,"pet3",cbMakeDescLink("Buff Bind ",$bbind,"title",": Pet 3 Key"),$profile)
#	my $pet4key = cbBindBox("Pet 4 Key",$bbind,"pet4",cbMakeDescLink("Buff Bind ",$bbind,"title",": Pet 4 Key"),$profile)
#	my $pet5key = cbBindBox("Pet 5 Key",$bbind,"pet5",cbMakeDescLink("Buff Bind ",$bbind,"title",": Pet 5 Key"),$profile)
#	my $pet6key = cbBindBox("Pet 6 Key",$bbind,"pet6",cbMakeDescLink("Buff Bind ",$bbind,"title",": Pet 6 Key"),$profile)
#	#  we use a custom listbox callback to enable/disable bufferbind UI elements based on the selection of this list.
#	my $target = cbListBox("Buffs affect...",{"Teammates","Pets","Both"},3,$bbind->{'target'},
#		sub { my(_,str,i,v) $profile->{'modified'} = true 
#			if (v == 1) {
#				$bbind->{'target'} = i
#				#  activate bind boxes based on the value of i.
#				if (i == 1) {
#					team1key.active="YES"
#					team2key.active="YES"
#					team3key.active="YES"
#					team4key.active="YES"
#					team5key.active="YES"
#					team6key.active="YES"
#					team7key.active="YES"
#					team8key.active="YES"
#					pet1key.active="NO"
#					pet2key.active="NO"
#					pet3key.active="NO"
#					pet4key.active="NO"
#					pet5key.active="NO"
#					pet6key.active="NO"
#				} elsif (i == 2) {
#					team1key.active="NO"
#					team2key.active="NO"
#					team3key.active="NO"
#					team4key.active="NO"
#					team5key.active="NO"
#					team6key.active="NO"
#					team7key.active="NO"
#					team8key.active="NO"
#					pet1key.active="YES"
#					pet2key.active="YES"
#					pet3key.active="YES"
#					pet4key.active="YES"
#					pet5key.active="YES"
#					pet6key.active="YES"
#				} else {
#					team1key.active="YES"
#					team2key.active="YES"
#					team3key.active="YES"
#					team4key.active="YES"
#					team5key.active="YES"
#					team6key.active="YES"
#					team7key.active="YES"
#					team8key.active="YES"
#					pet1key.active="YES"
#					pet2key.active="YES"
#					pet3key.active="YES"
#					pet4key.active="YES"
#					pet5key.active="YES"
#					pet6key.active="YES"
#				}
#			}
#		})
#	if ($bbind->{'target'} == 1) {
#		pet1key.active="NO"
#		pet2key.active="NO"
#		pet3key.active="NO"
#		pet4key.active="NO"
#		pet5key.active="NO"
#		pet6key.active="NO"
#	} elsif ($bbind->{'target'} == 2) {
#		team1key.active="NO"
#		team2key.active="NO"
#		team3key.active="NO"
#		team4key.active="NO"
#		team5key.active="NO"
#		team6key.active="NO"
#		team7key.active="NO"
#		team8key.active="NO"
#	}
#
#	my $delbtn = cbButton("Delete this Bind",sub {
#		if (iup.Alarm("Confirm Deletion","Are you sure you want to delete this bind?","Yes","No") == 1) {
#			table.remove($bbinds,n)
#			$bbinds->{'curset'} = $bbinds->{'curset'} - 1
#			if ($bbinds->{'curset'} == 0) { $bbinds->{'curset'} = 1 }
#			cbCleanDlgs($profile,$bbinds->{'dlg'})
#			$bbinds->{'dlg'}:hide()
#			# $bbinds->{'dlg'}:destroy()
#			$bbinds->{'dlg'} = undef
#			module.createDialog($bbinds,$profile)
#			cbShowDialog($bbinds->{'dlg'},218,10,$profile,$bbinds->{'dlg_close_cb'})
#			$profile->{'modified'} = true 
#		}
#	})
#	my $exportbtn = cbButton("Export...",sub { cbExportPageSettings($profile,n,$bbinds,"BuffBind") })
#
#	return iup.vbox{bbtitle,selchattext,buffpower1,chat1text,buffpower2,chat2text,buffpower3,chat3text,
#		iup.hbox{iup.vbox{team1key,team2key,team3key,team4key,team5key,team6key,team7key,team8key},
#			iup.vbox{target,iup.fill{},usepetnames,pet1key,pet2key,pet3key,pet4key,pet5key,pet6key,iup.fill{}}},
#		iup.hbox{delbtn,exportbtn}
#	}
}

sub newBBind {
	return {
		target => 3,
		team1 => "UNBOUND",
		team2 => "UNBOUND",
		team3 => "UNBOUND",
		team4 => "UNBOUND",
		team5 => "UNBOUND",
		team6 => "UNBOUND",
		team7 => "UNBOUND",
		team8 => "UNBOUND",
		pet1 => "UNBOUND",
		pet2 => "UNBOUND",
		pet3 => "UNBOUND",
		pet4 => "UNBOUND",
		pet5 => "UNBOUND",
		pet6 => "UNBOUND",
	}
}

sub createDialog {
	my ($bbinds,$profile) = @_;
#	my $box = {};
#	for i = 1,table.getn($bbinds) do
#		table.insert(box,addBBind($bbinds,i,$profile))
#	}
#	$bbinds->{'curset'} = $bbinds->{'curset'} or 1
#	cbToolTip("Click this to add a new bind")
#	my $newbindbtn = cbButton("New Buff Bind",
#		sub {
#			table.insert($bbinds,newBBind())
#			$bbinds->{'curbind'} = table.getn($bbinds)
#			$bbinds->{'dlg'}:hide()
#			# $bbinds->{'dlg'}:destroy()
#			$bbinds->{'dlg'} = undef
#			module.createDialog($bbinds,$profile)
#			cbShowDialog($bbinds->{'dlg'},218,10,$profile,$bbinds->{'dlg_close_cb'})
#			$profile->{'modified'} = true
#		},100)
#	my $importbtn = cbButton("Import Buff Bind",sub {
#		my $new$bbind = newBBind() #  we will be filling this new BBind up.
#		table.insert($bbinds,new$bbind)
#		my $new$bbind_n = table.getn($bbinds)
#		if (cbImportPageSettings($profile,new$bbind_n,$bbinds,"BuffBind")) {
#			$bbinds->{'curbind'} = table.getn($bbinds)
#			$bbinds->{'dlg'}:hide()
#			$bbinds->{'dlg'} = undef
#			#  Resolve Key COnflicts.
#			cbResolveKeyConflicts($profile,true)
#			module.createDialog($bbinds,$profile)
#			cbShowDialog($bbinds->{'dlg'},218,10,$profile,$bbinds->{'dlg_close_cb'})
#			$profile->{'modified'} = true
#		} else {
#			#  user cancelled, remove the new table from $bbinds.
#			table.remove($bbinds)
#		}
#	},100)
#	my $bbEnablePrev = "NO"
#	my $bbEnableNext = "NO"
#	if ($bbinds->{'curset'} > 1) { bbEnablePrev = "YES" }
#	cbToolTip("Click this to go to the previous bind")
#	$bbinds->{'prevbind'} = cbButton("<<",sub { my(self)
#			$bbinds->{'curset'} = $bbinds->{'curset'} - 1
#			if ($bbinds->{'curset'} < 1) { $bbinds->{'curset'} = 1 }
#			$bbinds->{'zbox'}.value = box[$bbinds->{'curset'}]
#			$bbinds->{'poslabel'}.title = $bbinds->{'curset'}.."/"..table.getn($bbinds)
#			my $bbEnablePrev = "NO"
#			if ($bbinds->{'curset'} > 1) { bbEnablePrev = "YES" }
#			$bbinds->{'prevbind'}.active=bbEnablePrev
#			my $bbEnableNext = "NO"
#			if ($bbinds->{'curset'} < table.getn($bbinds)) { bbEnableNext = "YES" }
#			$bbinds->{'nextbind'}.active=bbEnableNext
#		},25,undef,{active=bbEnablePrev})
#	if ($bbinds->{'curset'} < table.getn($bbinds)) { bbEnableNext = "YES" }
#	cbToolTip("Click this to go to the previous bind")
#	$bbinds->{'nextbind'} = cbButton(">>",sub { my(self)
#			$bbinds->{'curset'} = $bbinds->{'curset'} + 1
#			if ($bbinds->{'curset'} > table.getn($bbinds)) { $bbinds->{'curset'} = table.getn($bbinds) }
#			$bbinds->{'zbox'}.value = box[$bbinds->{'curset'}]
#			$bbinds->{'poslabel'}.title = $bbinds->{'curset'}.."/"..table.getn($bbinds)
#			my $bbEnablePrev = "NO"
#			if ($bbinds->{'curset'} > 1) { bbEnablePrev = "YES" }
#			$bbinds->{'prevbind'}.active=bbEnablePrev
#			my $bbEnableNext = "NO"
#			if ($bbinds->{'curset'} < table.getn($bbinds)) { bbEnableNext = "YES" }
#			$bbinds->{'nextbind'}.active=bbEnableNext
#		},25,undef,{active=bbEnableNext})
#	$bbinds->{'poslabel'} = iup.label{title = $bbinds->{'curset'}.."/"..table.getn($bbinds);rastersize="50x";alignment="ACENTER"}
#	box.value = box[$bbinds->{'curset'}]
#	$bbinds->{'zbox'} = iup.zbox(box)
#	$bbinds->{'dlg'} = iup.dialog{iup.vbox{$bbinds->{'zbox'},iup.hbox{$bbinds->{'prevbind'};newbindbtn;importbtn;$bbinds->{'poslabel'};$bbinds->{'nextbind'};alignment="ACENTER"};alignment="ACENTER"};title = "Gameplay : Buffer Binds",maxbox="NO",resize="NO",mdichild="YES",mdiclient=mdiClient}
#	$bbinds->{'dlg_close_cb'} = sub { my(self) $bbinds->{'dlg'} = undef }
}

sub bindsettings {
	my ($profile) = @_;
	my $buffer = $profile->{'buffer'};
	unless (defined $buffer) {
		$profile->{'buffer'} = $buffer = {};
	}
	# buffer.number = buffer.number or 0
	# buffer.curset = buffer.curset or 0
	# buffer.set = buffer.set or {}
	if ($buffer->{'dlg'}) {
#		buffer.dlg:show()
	} else {
#		module.createDialog(buffer,$profile)
#		cbShowDialog(buffer.dlg,218,10,$profile,buffer.dlg_close_cb)
	}
}

sub PopulateBindFiles {
	my $profile = shift->Profile;

	my $ResetFile = $profile->General->{'ResetFile'};
	my $buffer = $profile->{'buffer'} || [];
	my ($afile, $bfile, $cfile, $dfile);
	#  for each bindset, create the binds.
	for my $i (1 .. scalar @$buffer) {
		my $bbind = $buffer->[$i];

		my $selchat = $bbind->{'selchatenabled'} ? cbPBindToString($bbind->{'selchat'}) . '$$' : '';
		my $chat1   = $bbind->{'chat1enabled'}   ? cbPBindToString($bbind->{'chat1'})   . '$$' : '';
		my $chat2   = $bbind->{'chat2enabled'}   ? cbPBindToString($bbind->{'chat2'})   . '$$' : '';
		my $chat3   = $bbind->{'chat3enabled'}   ? cbPBindToString($bbind->{'chat3'})   . '$$' : '';

		my $npow = 1;
		if ($bbind->{'power2enabled'}) {
			$npow = 2;
			if ($bbind->{'power3enabled'}) { $npow = 3 };
		}
		if (($bbind->{'target'} == 1) or ($bbind->{'target'} == 3)) {
			for my $j (1..8) {
				my $teamid = "team$j";
				my $filebase = "$profile->{'base'}\\buff$i\\bufft${j}";
				$afile = $profile->GetBindFile("${filebase}a.txt");
				$bfile = $profile->GetBindFile("${filebase}b.txt");
				$afile->SetBind(    $teamid,'+down$$teamselect ' . $j . '$$' . "${selchat}bindloadfile ${filebase}b.txt");
				$ResetFile->SetBind($teamid,'+down$$teamselect ' . $j . '$$' . "${selchat}bindloadfile ${filebase}b.txt");
				if ($npow == 1) {
					$bfile->SetBind($teamid,'-down$$' . "${chat1}powexecname $bbind->{'power1'}" . '$$bindloadfile ' . "${filebase}a.txt");
				} else {
					$bfile->SetBind($teamid,'-down$$' . "${chat1}powexecname $bbind->{'power1'}" . '$$bindloadfile ' . "${filebase}c.txt");
					$cfile = $profile->GetBindFile("${filebase}c.txt");
					if ($npow == 2) {
						$cfile->SetBind($teamid,"${chat2}powexecname $bbind->{'power2'}" . '$$bindloadfile ' . "${filebase}a.txt");
					} else {
						$dfile = $profile->GetBindFile("${filebase}d.txt");
						$cfile->SetBind($teamid,'+down$$' . "${chat2}powexecname $bbind->{'power2'}" . '$$bindloadfile ' ."${filebase}d.txt");
						$dfile->SetBind($teamid,'-down$$' . "${chat3}powexecname $bbind->{'power3'}" . '$$bindloadfile ' ."${filebase}a.txt");
					}
				}
			}
		}
		if (($bbind->{'target'} == 2) or ($bbind->{'target'} == 3)) {
			for my $j (1..6) {
				my $petid = "pet$j";
				my $filebase = "$profile->{'base'}\\buff$i\\buffp${j}";
				if ($bbind->{'usepetnames'}) {
					$ResetFile->SetBind($petid,'+down$$petselectname ' . $profile->{'petaction'}->{"pet${j}name"} . '$$' . "${selchat}bindloadfile ${filebase}b.txt");
				} else {
					$ResetFile->SetBind($petid,'+down$$petselect ' . ($j-1) . '$$' . "${selchat}bindloadfile ${filebase}b.txt");
				}
				$afile = $profile->GetBindFile("${filebase}a.txt");
				$bfile = $profile->GetBindFile("${filebase}b.txt");
				if ($bbind->{'usepetnames'}) {
					$afile->SetBind($petid,'+down$$petselectname ' . $profile->{'petaction'}->{"pet${j}name"} . '$$' . "${selchat}bindloadfile ${filebase}b.txt");
				} else {
					$afile->SetBind($petid,'+down$$petselect ' . ($j-1) . '$$' . "${selchat}bindloadfile ${filebase}b.txt");
				}
				if ($npow == 1) {
					$bfile->SetBind($petid,'-down$$' . "${chat1}powexecname $bbind->{'power1'}" . '$$bindloadfile '."${filebase}a.txt");
				} else {
					$bfile->SetBind($petid,'-down$$' . "${chat1}powexecname $bbind->{'power1'}" . '$$bindloadfile '."${filebase}c.txt");
					$cfile = $profile->GetBindFile("${filebase}c.txt");
					if ($npow == 2) {
						$cfile->SetBind($petid,"${chat2}powexecname $bbind->{'power2'}" . '$$bindloadfile '. "${filebase}a.txt");
					} else {
						$dfile = $profile->GetBindFile("${filebase}d.txt");
						$cfile->SetBind($petid,'+down$$' . "${chat2}powexecname $bbind->{'power2'}" . '$$bindloadfile '."${filebase}d.txt");
						$dfile->SetBind($petid,'-down$$' . "${chat3}powexecname $bbind->{'power3'}" . '$$bindloadfile '."${filebase}a.txt");
					}
				}
			}
		}
	}
}

sub findconflicts {
	my ($profile) = @_;
	my $ResetFile = $profile->General->{'ResetFile'};
	my $buffer = $profile->{'buffer'};
	for my $bbind (@$buffer) {
		my $title = $bbind->{'title'} || 'unknown';
		if (($bbind->{'target'} == 1) or ($bbind->{'target'} == 3)) {
			for my $j (1..8) {
				cbCheckConflict($bbind,"team$j","Buff bind $title: Team $j Key");
			}
		}
		if (($bbind->{'target'} == 2) or ($bbind->{'target'} == 3)) {
			for my $j (1..6) {
				cbCheckConflict($bbind,"pet$j","Buff bind $title: Pet $j Key");
			}
		}
	}
}

sub bindisused {
	my ($profile) = @_;
	return $profile->{'buffer'} ? (scalar @{$profile->{'buffer'}} > 0) : undef;
}

1;
