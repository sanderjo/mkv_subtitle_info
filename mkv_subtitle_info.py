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



input = sys.argv[1]
if os.path.isdir(input):
	videofile = find_biggest_file(input)
elif os.path.isfile(input):
	videofile = file
else:
	print("no valid input: must be a dir or a file")
	sys.exit(1)	

_, file_extension = os.path.splitext(videofile)
if file_extension.lower() != ".mkv":
	print("no MKV")
	sys.exit(1)
	
mi = pymediainfo.MediaInfo.parse(videofile, output="JSON")
for i in json.loads(mi)["media"]["track"]:
	if i['@type'] == 'Text':
		print(i['Language_String1'] + " ", end="")
		if i["Default_String"] == "Yes":
			print("(default) ", end="")

