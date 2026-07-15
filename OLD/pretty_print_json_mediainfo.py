#!/usr/bin/env python3

import pymediainfo
import json
import sys

#videofile = "Finding.Alice.S01E01.1080p.HEVC.x265-MeGusta.mkv"

videofile = sys.argv[1]

json_data = pymediainfo.MediaInfo.parse(videofile, output="JSON")

json_object = json.loads(json_data)

json_formatted_str = json.dumps(json_object, indent=2)

print(json_formatted_str)


