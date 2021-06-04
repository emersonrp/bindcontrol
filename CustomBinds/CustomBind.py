#!/usr/bin/perl

use strict;

package CustomBinds::CustomBind;
use Wx;

sub new {
	my ($class) = @_;

	bless {}, $class;
}

sub Bind : lvalue { shift->{'Bind'} }
sub Key  : lvalue { shift->{'Key'} }

sub CreateDialog { 1; }

sub ListData {
	my $self = shift;

	return ('Burn Nougat', 'CTRL-L', 'FEEL THE BURN$$em bbnougat');

}

1;
