Which streams, including subtitles

```
$ head -9999 blabla.2025.bdrip.x264.mkv | strings -2 | head -100 | grep -e ^S_ -e ^A_ -e ^V_
V_MPEG4/ISO/AVC"
A_AACc
S_TEXT/UTF8"
S_TEXT/UTF8"
```

Raw analyses of languages:

```
$ head -9999 ./Saipan.2025.BDRip.x264-RUSTED-xpost/rusted-saipan.2025.bdrip.x264.mkv | strings -2 | head -100 | grep -B3 -A3 -e ^S_ -e ^A_ -e ^V_
aT
kAC
und
V_MPEG4/ISO/AVC"
und
.T
.c
gd
V$
0c
A_AACc
U"
en
G;
S_TEXT/UTF8"
enSn
English (SRT)
*S4&2
S_TEXT/UTF8"
enSn
English (SDH SRT)U
DV
```

... which knowledge, or focussed:

```
$ head -9999 blabla.mkv | strings -2 | head -100 | grep -B3 -A3 -e ^S_ -e ^A_ -e ^V_ | grep -e und -e en -e English
und
und
en
enSn
English (SRT)
enSn
English (SDH SRT)U
```


