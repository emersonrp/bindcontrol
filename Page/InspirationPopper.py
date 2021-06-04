#!/usr/bin/perl

use strict;

package Page::InspirationPopper;
use parent "Page::Page";

use Wx qw();

use Utility qw(id);

our $PageName = 'InspPop';

sub InitKeys {

	my $self = shift;

	$self->Profile->InspPop ||= {
		Enable => undef,
		AccuracyKey     => "LSHIFT+A",
		HealthKey       => "LSHIFT+S",
		DamageKey       => "LSHIFT+D",
		EnduranceKey    => "LSHIFT+Q",
		DefenseKey      => "LSHIFT+W",
		BreakFreeKey    => "LSHIFT+E",
		ResistDamageKey => "LSHIFT+SPACE",
	};
}

sub FillTab {

	my $self = shift;

	$self->TabTitle = 'Inspiration Popper';

	my $InspPop = $self->Profile->InspPop;

	my $sizer = Wx::BoxSizer->new(Wx::wxVERTICAL);

	my $InspRows =    Wx::FlexGridSizer->new(0,10,2,2);
	my $RevInspRows = Wx::FlexGridSizer->new(0,10,2,2);

	for my $Insp (sort keys %GameData::Inspirations) {

		$InspPop->{"Rev${Insp}Key"}    ||= 'UNBOUND';
		$InspPop->{"${Insp}Colors"}    ||= Utility::ColorDefault();
		$InspPop->{"Rev${Insp}Colors"} ||= Utility::ColorDefault();

		for my $order ('', 'Rev') {


			my ($KeyPicker, $ColorsCB, $bc, $fc);

			my $RowSet = $order ? $RevInspRows : $InspRows;

			$RowSet->Add ( Wx::StaticText->new($self, -1, "$order $Insp Key"), 0, Wx::wxALIGN_RIGHT|Wx::wxALIGN_CENTER_VERTICAL);

			$KeyPicker =  Wx::Button->    new($self, id("${order}${Insp}Key"), $InspPop->{"${order}${Insp}Key"});
			$KeyPicker->SetToolTip( Wx::ToolTip->new("Choose the key combo to activate a $Insp inspiration") );
			$RowSet->Add ( $KeyPicker, 0, Wx::wxEXPAND);

			$RowSet->AddStretchSpacer(Wx::wxEXPAND);

			$ColorsCB = Wx::CheckBox->    new($self, id("${order}${Insp}Colors"), '');
			$ColorsCB->SetToolTip( Wx::ToolTip->new("Colorize Inspiration-Popper chat feedback") );
			$RowSet->Add ( $ColorsCB, 0, Wx::wxALIGN_CENTER_VERTICAL);

			$RowSet->Add( Wx::StaticText->new($self, -1, "Border"), 0, Wx::wxALIGN_RIGHT|Wx::wxALIGN_CENTER_VERTICAL);
			$bc = $InspPop->{"${order}${Insp}Colors"}->{'border'};
			$RowSet->Add( Wx::ColourPickerCtrl->new(
					$self, id("${order}${Insp}BorderColor"),
					Wx::Colour->new($bc->{'r'}, $bc->{'g'}, $bc->{'b'}),
					Wx::wxDefaultPosition, Wx::wxDefaultSize,
				)
			);

			$RowSet->Add( Wx::StaticText->new($self, -1, "Background"), 0, Wx::wxALIGN_RIGHT|Wx::wxALIGN_CENTER_VERTICAL);
			$bc = $InspPop->{"${order}${Insp}Colors"}->{'background'};
			$RowSet->Add( Wx::ColourPickerCtrl->new(
					$self, id("${order}${Insp}BackgroundColor"),
					Wx::Colour->new($bc->{'r'}, $bc->{'g'}, $bc->{'b'}),
					Wx::wxDefaultPosition, Wx::wxDefaultSize,
				)
			);
			$RowSet->Add( Wx::StaticText->new($self, -1, "Text"), 0, Wx::wxALIGN_RIGHT|Wx::wxALIGN_CENTER_VERTICAL);
			$fc = $InspPop->{"${order}${Insp}Colors"}->{'foreground'};
			$RowSet->Add( Wx::ColourPickerCtrl->new(
					$self, id("${order}${Insp}ForegroundColor"),
					Wx::Colour->new($fc->{'r'}, $fc->{'g'}, $fc->{'b'}),
					Wx::wxDefaultPosition, Wx::wxDefaultSize,
				)
			);
		}
	}

	my $useCB = Wx::CheckBox->new( $self, -1, 'Enable Inspiration Popper Binds (prefer largest)');
	$useCB->SetToolTip(Wx::ToolTip->new('Check this to enable the Inspiration Popper Binds, (largest used first)'));
	$sizer->Add($useCB, 0, Wx::wxALL, 10);

	$sizer->Add($InspRows);

	my $useRevCB = Wx::CheckBox->new( $self, -1, 'Enable Reverse Inspiration Popper Binds (prefer smallest)');
	$useCB->SetToolTip(Wx::ToolTip->new('Check this to enable the Reverse Inspiration Popper Binds, (smallest used first)'));
	$sizer->Add($useRevCB, 0, Wx::wxALL, 10);

	$sizer->Add($RevInspRows);

	$self->SetSizerAndFit($sizer);

	return $self;
}

sub PopulateBindFiles {
	my $profile = shift->Profile;

	my $ResetFile = $profile->General->{'ResetFile'};
	my $InspPop   = $profile->{'InspPop'};

	for my $Insp (sort keys %GameData::Inspirations) {

		my $forwardOrder = join '$$', map { "inspexecname $_" }         @{$GameData::Inspirations{$Insp}};
		my $reverseOrder = join '$$', map { "inspexecname $_" } reverse @{$GameData::Inspirations{$Insp}};

		if ($InspPop->{'Feedback'}) {
			$forwardOrder = cbChatColorOutput($InspPop->{"${Insp}Colors"})    . $Insp . '$$' . $forwardOrder;
			$reverseOrder = cbChatColorOutput($InspPop->{"Rev${Insp}Colors"}) . $Insp . '$$' . $reverseOrder;
		}

		cbWriteBind($ResetFile, $InspPop->{"${Insp}Key"},    $forwardOrder) if $InspPop->{'Enable'};
		cbWriteBind($ResetFile, $InspPop->{"Rev${Insp}Key"}, $reverseOrder) if $InspPop->{'Reverse'};
	}
}

sub findconflicts {
	my ($profile) = @_;
	my $InspPop = $profile->{'InspPop'};
	if ($InspPop->{'enable'}) {
		cbCheckConflict($InspPop,'acckey',"Accuracy Key");
		cbCheckConflict($InspPop,'hpkey',"Healing Key");
		cbCheckConflict($InspPop,'damkey',"Damage Key");
		cbCheckConflict($InspPop,'endkey',"Endurance Key");
		cbCheckConflict($InspPop,'defkey',"Defense Key");
		cbCheckConflict($InspPop,'bfkey',"Breakfree Key");
		cbCheckConflict($InspPop,'reskey',"Resistance Key");
	}
	if ($InspPop->{'reverse'}) {
		cbCheckConflict($InspPop,'racckey',"Reverse Accuracy Key");
		cbCheckConflict($InspPop,'rhpkey',"Reverse Healing Key");
		cbCheckConflict($InspPop,'rdamkey',"Reverse Damage Key");
		cbCheckConflict($InspPop,'rendkey',"Reverse Endurance Key");
		cbCheckConflict($InspPop,'rdefkey',"Reverse Defense Key");
		cbCheckConflict($InspPop,'rbfkey',"Reverse Breakfree Key");
		cbCheckConflict($InspPop,'rreskey',"Reverse Resistance Key");
	}
}

sub bindisused {
	my ($profile) = @_;
	return unless $profile->{'InspPop'};
	return $profile-{'InspPop'}->{'enable'} || $profile->{'InspPop'}->{'reverse'};
}

1;
