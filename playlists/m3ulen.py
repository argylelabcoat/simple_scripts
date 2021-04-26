#!/usr/bin/python

import string, sys

def sec_to_days(seconds) :
    return seconds / 86400

def sec_to_hours(seconds) :
    return seconds / 3600

def sec_to_minutes(seconds) :
    return seconds / 60

def sec_to_minutes_seconds(seconds) :
    minutes = sec_to_minutes(seconds)
    sec = seconds % 60
    return "%(n1)02d:%(n2)02d" % {"n1": minutes, "n2": sec}

# If no arguments were given, print a helpful message
if len(sys.argv)==1:
    print 'Usage:  m3utime filename.m3u'

    sys.exit(0)

filename = sys.argv[1]

items = [line.replace("#EXTINF:", "").strip() for line in file(filename) if line.startswith('#EXTINF')]

splitList = [line.split(",") for line in items ]

time = 0
for s in splitList : time = time + int(s[0])

days = sec_to_days(time)
hours = sec_to_hours(time) - (days * 24)
minutes = sec_to_minutes(time) - (days * 1440) - (hours * 60)
seconds = time % 60

print filename + " : " + str(time) + "s\n"

for s in splitList :
    print sec_to_minutes_seconds(int(s[0])), s[1]

print

print "Total play time : " + str(days) + ":" + str(hours) + ":" + str(minutes) + ":" + str(seconds) + "\n"
