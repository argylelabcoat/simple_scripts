#!/bin/bash
#
# box_text [options] <text
#
# Wrap incomming text in a simple box of ASCII or Unicode characters.
#
# Options...
#
#   -s {style}    Style of box - default rounded (utf-8)
#                    none, banner, curses, ascii, lines,
#                    box, round, bold, double, shadow, thick
#
#   -i #          Indent output on left side this many characters
#   -w #          Box width minimum, expands to fit text.
#
#   -r            Remove any initial indent the text has (block left)
#   -c            Center the whole text in the box  (center justify)
#
#   -W            Size box match width of the TTY (using COLUMNS env)
#   -C            Center the the box on the TTY (using COLUMNS env)
#
#   -help         This Documentation
#
# Warning: at this time this program can not handle TABs :-(
#
# Example, fortune with tabs cleaned up
#
#   fortune | col -x | box_text -s double -c -W
#
# The "none" style still places a box, but it is all spaces.
#
# This means you can use this as a poor man's, 'center text' using...
#   cat text | box_text -s none -w 86 -c | sed 's/^   //; s/ *$//; /^$/d'
#
#####
#
# Anthony Thyssen,  25 Nov 2020    <Anthony.Thyssen@gmail.com>
#
# Developed from a simple boxing function published in...
#    https://antofthy.gitlab.io/info/shell/small_functions.txt
#
# Also see the command "boxes", which has a large number of options, and can
# wrap text in complex ASCII ART, but can not handle simple Unicode!
#
#####
# Discover where the shell script resides
PROGNAME="${BASH_SOURCE##*/}"    # script name (basename)
PROGDIR="${BASH_SOURCE%/*}"      # directory (dirname - may be relative)

Error() {  # Just output an error condition and exit (no usage)
  echo >&2 "$PROGNAME:" "$@"
  exit 2
}
Usage() {  # Report error and Synopsis line only
  echo >&2 "$PROGNAME:" "$@"
  sed >&2 -n '1,2d; /^###/q; /^#/!q; /^#$/q; s/^#  */Usage: /p;' \
          "$PROGDIR/$PROGNAME"
  echo >&2 "For help use  $PROGNAME --help"
  exit 10;
}
Help() {   # Output Full header comments as documentation
  sed >&2 -n '1d; /^###/q; /^#/!q; s/^#*//; s/^ //; p' \
          "$PROGDIR/$PROGNAME"
  exit 10;
}

# Basic defauls
box_style='rounded'  # Default Box Style (unicode rounded box)
box_indent=0         # box indent

: ${COLUMNS:=80}     # tty size if unset

# minimal option handling
while [ $# -gt 0 ]; do
  case "$1" in

  -\?|-help|--help) Help ;;             # Standard help options.
  -doc|--doc)       Help ;;

  -s*) box_style="${1:2}"               # select the box style
      [[ -z $box_style ]]  && { shift; box_style="$1"; }
      ;;
  -i*) box_indent="${1:2}"              # set indent of whole box
      [[ -z $box_indent ]] && { shift; box_indent="$1"; }
      [[ $box_indent != *[^0-9]* ]] ||
        Usage "Box Indent (-i) is not an integer"
      ;;
  -w*) box_width="${1:2}"               # set width of whole box
      [[ -z $box_width ]]  && { shift; box_width="$1"; }
      [[ $box_width  != *[^0-9]* ]] ||
        Usage "Box Width (-w) is not an integer"
      ;;
  -r) remove=true ;;                    # remove any initial text indent
  -c) center=true ;;                    # center text in box if box is larger

  -W) box_width=$(( COLUMNS-2 )) box_indent=1 ;;  # box width to match TTY
  -C) box_indent=-1 ;;                  # center the whole box in TTY

  --) shift; break ;;                   # forced end of user options
  -*) Usage "Unknown option \"$1\"" ;;
  *)  break ;;                          # unforced  end of user options

  esac
  shift                                 # next option
done
[ $# -gt 0 ] && Usage "Too Many Arguments"

# remove indent if centered in box (or it does not make much sense!)
[[ "$center" ]] && remove=true

# Select the box style
#
# This are characters for the edges and corners, for the box.
# Currently program assumes all strings are single characters.
#
# See config for "boxes" program for a more advanced handling style
# Shame that program does not handle unicode (string lengths are wrong).
#
#    c = corner  e = edge  t = top  b = bottom  l = left  r = right
#
case  "$box_style" in
  none)      ctl=" " et=" " ctr=" " el=" " er=" " cbl=" " eb=" " cbr=" " ;;
  # ASCII Art
  banner)    ctl="#" et="#" ctr="#" el="#" er="#" cbl="#" eb="#" cbr="#" ;;
  curses)    ctl="+" et="-" ctr="+" el="|" er="|" cbl="+" eb="-" cbr="+" ;;
  ascii)     ctl="." et="-" ctr="." el="|" er="|" cbl="'" eb="-" cbr="'" ;;
  lines)     ctl="-" et="-" ctr="-" el=" " er=" " cbl="-" eb="-" cbr="-" ;;
  # Unicode
  box)       ctl="┌" et="─" ctr="┐" el="│" er="│" cbl="└" eb="─" cbr="┘" ;;
  round)     ctl="╭" et="─" ctr="╮" el="│" er="│" cbl="╰" eb="─" cbr="╯" ;;
  bold)      ctl="┏" et="━" ctr="┓" el="┃" er="┃" cbl="┗" eb="━" cbr="┛" ;;
  double)    ctl="╔" et="═" ctr="╗" el="║" er="║" cbl="╚" eb="═" cbr="╝" ;;
  shadow)    ctl="┌" et="─" ctr="┒" el="│" er="┃" cbl="┕" eb="━" cbr="┛" ;;
  thick)     ctl="▛" et="▀" ctr="▜" el="▌" er="▐" cbl="▙" eb="▄" cbr="▟" ;;
  # Error
  *) Error "Unknown Box Style given" ;;
esac

# ------------------------------------------
# Read input text and details of the text

text_length=0             # get the maxim length of lines
text_indent=999           # existing indent of whole text
while IFS= read -r line; do
  text+=( "$line" )                                   # save the line
  ((text_length<${#line})) && text_length=${#line}    # get max length
  line=${line%%[^ ]*}                                 # remove non-indent
  ((text_indent>${#line})) && text_indent=${#line}    # get overall indent
done

(( ${#text[@]} > 0 )) || Error "No text input!"

#echo "DEBUG: line count  = ${#text[@]}"
#echo "DEBUG: text_length = $text_length"
#echo "DEBUG: text_indent = $text_indent"

# ------------------------------------------
# Adject text and box size and indents as appropriate

if [[ $remove ]]; then                     # remove original text indent?
  text_length=$((text_length-text_indent)) # adjust text length
else
  text_indent=0                            # don't remove any indent (leave it)
fi

# If box isn't large enough or unset - expand to just contain the text
# The alternative would be to generate an error!
if (( box_width < text_length+4 )); then
  box_width=$((text_length+4))
fi

# Center the text in the box, by adjusting the amount of indent
if [[ $center ]]; then        # block center the text as a whole
  # calculate amount of the original text indent to remove
  text_indent=$((text_indent-(box_width-4-text_length)/2))
  # if indent is negative, then we need to add more indent
  if (( text_indent < 0 )); then
    printf -v add_indent "%*s" $text_indent;
    text_indent=0
  fi
else
  add_indent=''                # not adding any extra indent
fi

# Center the whole box on the TTY
((box_indent<0)) && box_indent=$(( (COLUMNS-box_width)/2 ))

#echo "DEBUG: box_indent  = $box_indent"
#echo "DEBUG: box_width   = $box_width"
#echo "DEBUG: line count  = ${#text[@]}"
#echo "DEBUG: text_length = $text_length"
#echo "DEBUG: text_indent = $text_indent"

# ------------------------------------------

# Top of box
printf -v line "%*s" $((box_width-2))
printf "%*s%s%s%s\n" $box_indent '' "$ctl" "${line//?/$et}" "$ctr"

# Text in Box (with appropriate indent adjustments)
for line in "${text[@]}"; do
   line="${add_indent}${line}"    # add more indent to the line (if needed)
   line="${line:text_indent}"     # remove the appropriate amount of indent
   printf "%*s%s %*s %s\n" $box_indent '' "$el" $((4-box_width)) "$line" "$er"
done

# Bottom of box
printf -v line "%*s" $((box_width-2))
printf "%*s%s%s%s\n" $box_indent '' "$cbl" "${line//?/$eb}" "$cbr"


