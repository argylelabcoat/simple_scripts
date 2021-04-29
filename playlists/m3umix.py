#!/usr/bin/python

import string, sys
import os, shutil
from os.path import join

# If no arguments were given, print a helpful message
if len(sys.argv)==1:
    print 'Usage:  m3utime filename.m3u'

    sys.exit(0)

make_mp3 = False
if len(sys.argv) > 2:
	arg_makemp3 = sys.argv[2].lower()
	if arg_makemp3.startswith('t') or arg_makemp3.startswith('y'):
		make_mp3 = True
		from pydub import AudioSegment 

filename = sys.argv[1]

mixtape_location = './'

if filename.lower().find('.m3u') > 0:
	mixtape_location = os.path.join('./', filename.lower().split('.m3u')[0])
else:
	mixtape_location = os.path.join('./', filename + "_folder")

if os.path.exists(mixtape_location) :
	shutil.rmtree(mixtape_location)

os.mkdir(mixtape_location)

mp3_location = os.path.join(mixtape_location,'mp3')

playlist_location = os.path.join(mixtape_location,'playlist.m3u')

os.mkdir(mp3_location)


metadata = ''
path = ''

newlist = []
playlist_position = 1
for line in file(filename):
	path = line.strip()
	if os.path.isfile(path):
		base = '{0:03d}-{1}'.format(playlist_position,os.path.basename(path))
		destination = os.path.join(mp3_location,base)
		if path.endswith('.mp3') or make_mp3 is False:
			shutil.copyfile(path,destination)
		else:
			destination = os.path.splitext(destination)[0]+'.mp3'
			audio = AudioSegment.from_file(path)
			audio.export(destination, format="mp3")
		newlist.append(os.path.join('./',os.path.join('mp3',base)))
		playlist_position += 1
	else:
		newlist.append(line.strip())

		
playlist_file = open(playlist_location,'w')

for line in newlist:
	playlist_file.write('%s\n'%line)

playlist_file.close()

