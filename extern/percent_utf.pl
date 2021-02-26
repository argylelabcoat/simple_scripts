#!/usr/bin/perl
#
# percent_utf value [title]
# percent_utf numerator denominator "title"
#
# Show a percentage bargraph of a value using UTF Box Drawing Characters.
# A bar length of 50 charaectrs is used to make it look nice and neat.
#
###
#
# Included in commented code below is 'ascii' and 'graphic set' versions,
# from in the the older "percent_ascii" version of this script.
#
# Note that while the older ASCII version uses centered chars of ten unit
# marks, this UTF version used character edge marks for the ten unit marks.
# This actually makes it more accurite.
#
# Anthony Thyssen, 12 May 2020
#
###
use strict;
use warnings;
use utf8;
use FindBin;
my $PROGNAME = $FindBin::Script;

sub Usage {
  print STDERR "$PROGNAME: ", @_, "\n"  if @_;
  @ARGV = ( "$FindBin::Bin/$PROGNAME" ); # locate script file
  while( <> ) {
    next if 1 .. 2;
    last if /^###/;
    last unless /^#/;
    s/^#$//; s/^# //;
    last if /^$/;
    print STDERR "Usage: " if 3 .. 4;
    print STDERR;
  }
  #print STDERR "For full manual use --help\n";
  exit 10;
}

# Arguments
my ($value, $max_value, $title);
$max_value=100.0;

Usage("Options not permitted.")
   if @ARGV && $ARGV[0] =~ /^-[^0-9]/;

if    ( @ARGV == 1 ) { $value = shift; }
elsif ( @ARGV == 2 ) { ($value, $title) = @ARGV; }
elsif ( @ARGV == 3 ) { ($value, $max_value, $title) = @ARGV; }
else { Usage("Invalid number of arguments"); }

$value =~ s/^\s*$//;  # clean up value of allowed extra chars
$value =~ s/\s*\%\s*$//;
Usage("Value given is not a number") unless $value =~ /^-?[\d.]+$/;

# ---------------------------------------------------------------------------

# perl is printing UTF8 'wide character in print'
binmode(STDOUT, ":utf8");

# Scale in UTF
# Note: Each major mark is actually two characters, '▕' and '▏'
# This scale is to have ANSI color codes added if TTY allows.
my $scale = " 0   10   20   30   40   50   60   70   80   90   100";
my $rule  = "▕▏ ╻ ▕▏ ╻ ▕▏ ╻ ▕▏ ╻ ▕▏ ╻ ▕▏ ╻ ▕▏ ╻ ▕▏ ╻ ▕▏ ╻ ▕▏ ╻ ▕▏";

# Plain Ascii Scale (character centered)
# " 0   10   20   30   40   50   60   70   80   90   100";
# " |----+----+----+----+----|----+----+----+----+----| ";

# Alt Grpahic Char Set (character centered)
# $Gon="\e(0"; $Goff="\e(B";
# $Gon=`tput smacs`; $Goff=`tput rmacs`
# $rule = " ${Gon}tqqqqnqqqqnqqqqnqqqqnqqqqnqqqqnqqqqnqqqqnqqqqnqqqqu${Goff}"
# OR in UTF     " ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤"

# Terminal Output?
my ($B,$N,$U,$E) = map('',1..10);
$ENV{TERM}='dumb' unless $ENV{TERM};

# output to a xterm?  EG: not a file
if ( $ENV{TERM} =~ /xterm/ && -t STDOUT ) {
  $B = `tput bold 2>/dev/null`;       # bold ON    "\e[1m"
  $N = `tput sgr0 2>/dev/null`;       # bold OFF   "\e(B\e[m"
  #$U = `tput smul 2>/dev/null`;      # Underline - not as good as expected
  #$E = `tput rmul 2>/dev/null`;

  # Bold the numbers in scale: start, center, end.
  $scale =~ s/^ 0 / ${B}0${N} /;
  $scale =~ s/ 50 / ${B}50${N} /;
  $scale =~ s/ 100$/ ${B}100${N}/;

  # My Bold XTerm Font does not include unicode characters!  Arrgghhh...
  # So I need to color them instead (purple, can seem to get full-white.
  # But that color depends on background Which I do not know at this time!
  # So only do it if I reconise my own home directory, not someone elses.
  #$B=$N='';   # turn off completely for unicode output
  $B="\e[95m",$N="\e[m"  if -f "$ENV{HOME}/bin/home_scripts/sh_rc";

  # need to color middle tick mark, before adding escapes at start of line
  $rule  =~ s/^(.{24}) (\S+) /$1 ${B}$2${N} /;
  $rule  =~ s/^../$B$&$N/;
  $rule  =~ s/..$/$B$&$N/;
  #$rule  =~ s/^(.)(.)/$B$1$U$2$N$U/u;    # gets tricy if underline is used
  #$rule  =~ s/(.)(.)$/$B$1$E$B$2$N/u;
}

# indent prefix (center in 72 columns)
my $P = ' ' x 9;    # (72-52)/2 - 1  =>  9 character prefix

print ' 'x((72-length($title))/2), $title, "\n"  if $title;
print "$P$scale\n";
print "$P$rule\n";

if( $value < 0 ) {
  print  "$P$B◁▏$N$U                                                 $E$B▏$N\n"
  #print "$P$B<|$N$U                                                 $E$B|$N
}
#elsif( $value == 0 ) {
#  print  "$P$B ▏$N$U                                                 $E$B▏$N\n"
#  #print "$P$B |$N$U                                                 $E$B|$N
#}
elsif( $value > $max_value ) {
  print  "$P$B▕$N$U██████████████████████████████████████████████████$E$B▷$N\n"
  #print "$P|$U▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒$E$B>$N
}
else {
  printf  "$P$B▕$N$U%-50s$E$B▏$N\n", graph_line($value,$max_value,50);
  #printf "$P$B|$N$U%-50s$E$B|$N\n", graph_line($value,$max_value,50,'▒');
}

# Draw the Bar Graph
#
# Extracted and Modified from vspark.pl
#   https://github.com/LuRsT/vspark
# By Gil Gonçalves
#
# Alternative character lists, examples
#   ASCII Only     "=", "#"
#   Hash Char      "▒",  "░▒▓█"
#   Half chars     "▌█",
#   Quarter chars  "▖▌▛█"
#   Incremental    "▏▎▍▌▋▊▉█"   <--- the ideal 8 character increment
#   Brail chars    "⡀⡄⡆⡇⣇⣧⣷⣿"
#
# That last brail method can be useful in a 50 character percentage bar.
# Four dots will then represents 1 percent, in increments of 1/4 percent
# A full character group of 8 dots is 2%
# As such users can fairly easily read a more exact percentage reading.
# But dots doesn't look nearly as cool as a solid bar.

sub graph_line {
    my $value      = shift;
    my $max_value  = shift;
    my $graph_size = shift;
    my $char_list  = shift || "▏▎▍▌▋▊▉█";  # optional character set
    #$char_list = "⡀⡄⡆⡇⣇⣧⣷⣿";

    #$graph_size--;   # reduce by one (if count from 0)
    my @char_list = ($char_list =~ /(.)/g);
    my $char_len = scalar(@char_list);    # increments over a single character

    # Number character increments to plot
    my $increments = $value * $char_len*$graph_size/$max_value -.5;

    return ""  if $increments <= 0;
    return $char_list[-1] x $graph_size
               if $increments >= $char_len*$graph_size;

    return( ($char_list[-1] x int($increments / $char_len )) .
            ($char_list[int($increments % $char_len)])  );
}


