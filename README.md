A pure python script to detect & report AUDIO and SUBTITLES in .MKV files. No externals tools nor non-standard libraries needed.

It's faster than `ffprobe` and `mkvmerge`.



# Example usage

`python3 mkv_subtitles.py <some-file.mkv>`

With example outputs:

`AUDIO: en SUBS: en ar cs da de es es fi fr he hi hu id it ko nb nl pl pt ru sv tr uk zh zh`

`AUDIO: eng SUBS: dut`

`AUDIO: eng SUBS: eng fre spa`

# Full usage

```
usage: mkv_subtitles.py [-h] [--all-tracks] [--json] [--long] files [files ...]

Find subtitle tracks in .mkv files without ffprobe/mkvmerge.

positional arguments:
  files         path(s) to .mkv file(s)

options:
  -h, --help    show this help message and exit
  --all-tracks  show every track (video/audio/subtitle), not just subtitles
  --json        emit one JSON object per file
  --long        show full per-track detail; without this, print a short 'AUDIO: .. SUBS: ..' summary line per file
```



# Thanks to ...

All the hard work done by Claude Code. Thank you!
