#!/usr/bin/env python3

# Gets subtitle info from a MKV file
# If there is no MKV: print number of srt files
# input: directory or file

# to run this on any download: SABnzbd -> Config -> Categories: at Default, select as Script. And Save.

import pymediainfo
import os
import json
import sys

def find_biggest_file(path):
	path = os.path.abspath(path)
	size = 0
	max_size = 0
	max_file =""
	# walking through the entire folder,
	# including subdirectories
	for folder, subfolders, files in os.walk(path):
		# checking the size of each file
		for file in files:
			try:
				size = os.stat(os.path.join( folder, file )).st_size
			except:
				size = 0		
			# updating maximum size
			if size>max_size:
				max_size = size
				max_file = os.path.join( folder, file )
	return(max_file)

def find_srt_files(dir):
	srt_counter = 0
	srt_info = ""
	for root, dirs, files in os.walk(dir):
		for file in files:
			if file.lower().endswith(".srt"):
				srt_info += file + " - "
				srt_counter += 1
	return srt_info

try:
	input = sys.argv[1]
except:
	print("You must specify a directory or file as parameter")
	sys.exit(1)

if os.path.isdir(input):
	videofile = find_biggest_file(input)
elif os.path.isfile(input):
	videofile = input
else:
	print("no valid input: must be a dir or a file")
	sys.exit(1)	

if videofile.lower().endswith(".mkv"):
	subtitle_info = ""
	mi = pymediainfo.MediaInfo.parse(videofile, output="JSON")
	for i in json.loads(mi)["media"]["track"]:
		if i['@type'] == 'Text':
			try:
				subtitle_info += i['Language_String1'] + " "
			except:
				# no 'Language_String1' found
				subtitle_info += "Unknown Language" + " "
			if i["Default_String"] == "Yes":
				subtitle_info += "(default) "
				#print("(default) ", end="")
	if subtitle_info != "":
		print("MKV subtitles:", subtitle_info)
	else:
		print("MKV: no subtitles found")
elif os.path.isdir(input):
	# check if there are .srt files in that dir
	srts_found = find_srt_files(input)
	if srts_found != "":
		print("No MKV, but srt files found:", srts_found)
	else:
		print("No MKV, and no srt files found")

sys.exit(0) # all good