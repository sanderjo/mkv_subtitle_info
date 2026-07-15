# Benchmark: ffprobe vs mkvmerge vs mkv_subtitles.py

Benchmarked against 100 `.mkv` files from `/media/sander/Zeegat/head9999-superdir`
on brixit.local (one known-corrupt file excluded, since it makes `mkvmerge` hang).

## Results

Mean time per file:

| Tool | Mean | Median | Min | Max | vs ffprobe |
|---|---|---|---|---|---|
| `ffprobe` (subprocess) | 155.4 ms | 146.2 ms | 126.3 ms | 463.9 ms | 1.0x |
| `mkvmerge` (subprocess) | 92.4 ms | 87.2 ms | 81.2 ms | 452.5 ms | 1.7x faster |
| `mkv_subtitles.py` (subprocess CLI) | 77.9 ms | 77.4 ms | 75.9 ms | 87.5 ms | 2.0x faster |
| `mkv_subtitles()` (in-process call) | 0.95 ms | 0.52 ms | 0.36 ms | 9.92 ms | 163.7x faster |

## Explanation

- **ffprobe / mkvmerge** are full-featured tools: they initialize codec
  registries, container demuxers, and other machinery unrelated to just
  reading track metadata, so most of their time per file is fixed startup
  cost rather than actual parsing.
- **`mkv_subtitles.py` as a CLI** (`python3 mkv_subtitles.py FILE`) already
  beats both, because it does far less work: it walks the EBML structure
  only as far as the `Tracks` element and skips everything else (video/audio
  payload, `Cues`, `Tags`, `Attachments`, etc.) via declared element sizes.
  Even so, most of its ~78ms is just Python interpreter startup, not parsing.
- **`mkv_subtitles()` called in-process** (as in `example_caller_mkv_subtitles.py`,
  no `python3` subprocess spawned per file) removes that interpreter-startup
  cost entirely, dropping to well under 1ms per file on average. This is the
  relevant number if scanning a whole library (e.g. all ~735 files) from
  within a single running Python process, rather than shelling out once per
  file.

## Source

Benchmark script: `/home/claude/benchmark.py` on brixit.local.
