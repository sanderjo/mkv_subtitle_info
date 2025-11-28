# Audio stuff


Pretty `mkvmerge -J` output:

```
    {
      "codec": "DTS-HD Master Audio",
      "id": 1,
      "properties": {
        "audio_channels": 6,
        "audio_sampling_frequency": 48000,
        "codec_id": "A_DTS",
        "codec_private_length": 0,
        "default_track": true,
        "enabled_track": true,
        "forced_track": false,
        "language": "fre",
        "minimum_timestamp": 0,
        "num_index_entries": 0,
        "number": 2,
        "tag_duration": "01:31:35.840000000",
        "track_name": "Surround",
        "uid": 2093827378492420331
      },
      "type": "audio"
    }
```

Goal seeking:
```
cat blabla.mkv | head -c1000 | hd
```
... relevant part:
```
000001f0  40 d7 81 02 73 c5 88 1d  0e c4 e8 3c 07 30 eb 9c  |@...s......<.0..|
00000200  81 00 53 6e 88 53 75 72  72 6f 75 6e 64 22 b5 9c  |..Sn.Surround"..|
00000210  83 66 72 65 86 85 41 5f  44 54 53 83 81 02 e1 8d  |.fre..A_DTS.....|
00000220  9f 81 06 b5 88 40 e7 70  00 00 00 00 00 55 ee 81  |.....@.p.....U..|
00000230  00 12 54 c3 67 40 92 bf  84 08 61 c1 44 73 73 9f  |..T.g@....a.Dss.|
```


# Something Dutch

```
$ cat blabla.S02E05.DUTCH.1080p.WEB-DL.AAC2.0.x264-UGDV.mkv | head -c5000 | hd | grep -B3 -A3 -i nl
00001140  d7 81 02 73 c5 88 45 56  21 42 19 ef 0c a4 83 81  |...s..EV!B......|
00001150  02 22 b5 9c 83 64 75 74  86 85 41 5f 41 41 43 63  |."...dut..A_AACc|
00001160  a2 82 11 90 23 e3 83 84  01 45 85 55 22 b5 9d 82  |....#....E.U"...|
00001170  6e 6c e1 89 b5 84 47 3b  80 00 9f 81 02 ec 44 55  |nl....G;......DU|
00001180  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00001380  00 00 00 00 00 00 00 00                           |........|
```



