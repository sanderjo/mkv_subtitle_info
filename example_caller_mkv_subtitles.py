#!/usr/bin/env python3
"""Example of calling mkv_subtitles() from another script."""

import sys

sys.path.insert(0, "/home/claude")
from mkv_subtitles import mkv_subtitles, TruncatedFile, InvalidMatroska

path = "/media/sander/Zeegat/Dangerous.Liaisons.1988.720p.BRrip.x264-NGP/Dangerous.Liaisons.1988.720p.BRrip.x264-NGP.mkv"

try:
    result = mkv_subtitles(path)
    print(result)
except (TruncatedFile, InvalidMatroska, OSError) as e:
    print(f"could not read {path}: {e}")
