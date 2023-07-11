#!/usr/bin/env python3

# Gets subtitle info from a MKV file

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
	for root, dirs, files in os.walk(dir):
		for file in files:
			if file.lower().endswith(".srt"):
				srt_counter += 1
	return srt_counter


input = sys.argv[1]
if os.path.isdir(input):
	videofile = find_biggest_file(input)
elif os.path.isfile(input):
	videofile = input
else:
	print("no valid input: must be a dir or a file")
	sys.exit(1)	

if videofile.lower().endswith(".mkv"):
	mi = pymediainfo.MediaInfo.parse(videofile, output="JSON")
	for i in json.loads(mi)["media"]["track"]:
		if i['@type'] == 'Text':
			print(i['Language_String1'] + " ", end="")
			if i["Default_String"] == "Yes":
				print("(default) ", end="")
elif os.path.isdir(input):
	# check if there are .srt files in that dir
	srts = find_srt_files(input)
	if srts > 0:
		print("srt files found:", srts)

