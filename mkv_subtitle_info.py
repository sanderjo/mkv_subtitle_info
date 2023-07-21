#!/usr/bin/env python3

# Gets subtitle info from a MKV file
# If there is no MKV: print number of srt files
# input: directory or file

# to run this on any download: SABnzbd -> Config -> Categories: at Default, select as Script. And Save.

import pymediainfo
import os
import json
import sys

wanted_language_prio = {}
wanted_language_prio['Flemish']=1
wanted_language_prio['Dutch']=2
wanted_language_prio['English']=3

print("Preferred:", wanted_language_prio)

subtitle_prio_found = 9999
audio_prio_found = 9999

subtitle_track_number = audio_track_number = None



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
		# Audio:
		if i['@type'] == 'Audio':
			#print("SJ: Audio",  i['StreamCount'], i['Language_String1'])
			try:
				language = i['Language_String1']
			except:
				language = "unknown"
			if language in wanted_language_prio:
				print("SJ200: yes, audio wanted language ... ", language, "prio", wanted_language_prio[language])
				if wanted_language_prio[language] < audio_prio_found:
					audio_prio_found = wanted_language_prio[language]
					audio_track_number = i['StreamCount']

		# Subtitle:
		if i['@type'] == 'Text':
			#print("SJ100", i)
			print("SJ: subtitle ", i['@typeorder'], i['Language_String1'])
			try:
				language = i['Language_String1']
			except:
				language = "unknown"

			if language in wanted_language_prio:
				print("SJ300: yes, subtitle wanted language ... ", language, "prio",wanted_language_prio[language])
				if wanted_language_prio[language] < subtitle_prio_found:
					subtitle_prio_found = wanted_language_prio[language]
					subtitle_track_number = i['@typeorder']
					print("SJ300", subtitle_prio_found, subtitle_track_number)

			subtitle_info += language + " "

			if i["Default_String"] == "Yes":
				subtitle_info += "(default) "
				#print("(default) ", end="")


	if audio_track_number:
		print("audio_track_number", audio_track_number)

	if subtitle_track_number:
		print("subtitle_track_number", subtitle_track_number)

	# As last output, so it will appear in SABnzbd's History overview:
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