# mkv_subtitle_info
Get subtitle info from an MKV file

Can be used as a SABnzbd post-processing script: put it in the SABnzbd scripts directory


To run this on any download: SABnzbd -> Config -> Categories: at Default, select as Script. And Save.

- Requirements

Python3 and python3-pip
Python modules listed in `requirements.txt`. Install with `python3 -m pip install -r requirements.txt -U`

Example result in SABnzbd's History:

![image](https://github.com/sanderjo/mkv_subtitle_info/assets/1273502/f8276e0e-1acd-41af-8bf0-0f60e7065982)



## ugly but easy: from commandline with standard linux commands

Subtitles:

```
$ head -10000 blabla.mkv | strings -2 | grep -A 1 "TEXT/UTF8"  | grep -v "TEXT/UTF8"
es
--
ro
--
hu
--
de
--
fr
--
en
```

Audio:
```
$ head -10000 blabla.mkv | strings -2 | grep -A 1 "AAC"  | grep -v "AAC"
en
```

