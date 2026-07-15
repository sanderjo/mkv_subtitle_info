#!/usr/bin/env python3
"""Benchmark ffprobe vs mkvmerge vs mkv_subtitles.py on a directory of .mkv files."""

import argparse
import os
import shutil
import statistics
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from mkv_subtitles import mkv_subtitles, TruncatedFile, InvalidMatroska

MKV_SUBTITLES_PY = os.path.join(SCRIPT_DIR, "mkv_subtitles.py")


def timed(fn, files):
    times = []
    for path in files:
        t0 = time.perf_counter()
        fn(path)
        times.append(time.perf_counter() - t0)
    return times


def run_ffprobe(path):
    subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=index,codec_type,codec_name:stream_tags=language",
         "-of", "default=noprint_wrappers=0", path],
        capture_output=True, timeout=30)


def run_mkvmerge(path):
    subprocess.run(["mkvmerge", "-J", path], capture_output=True, timeout=30)


def run_mkv_subtitles_cli(path):
    subprocess.run([sys.executable, MKV_SUBTITLES_PY, path],
                    capture_output=True, timeout=30)


def run_mkv_subtitles_inproc(path):
    try:
        mkv_subtitles(path)
    except (TruncatedFile, InvalidMatroska, OSError):
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark ffprobe vs mkvmerge vs mkv_subtitles.py.")
    parser.add_argument("directory", help="directory containing .mkv files to benchmark")
    parser.add_argument("--count", type=int, default=100,
                         help="number of files to benchmark (default: 100)")
    parser.add_argument("--exclude", action="append", default=[], metavar="SUBSTRING",
                         help="skip filenames containing this substring "
                              "(repeatable; e.g. to skip a known-corrupt file)")
    args = parser.parse_args()

    files = sorted(f for f in os.listdir(args.directory) if f.endswith(".mkv"))
    for substr in args.exclude:
        files = [f for f in files if substr not in f]
    files = [os.path.join(args.directory, f) for f in files[:args.count]]

    if not files:
        sys.exit(f"no .mkv files found in {args.directory}")
    print(f"benchmarking against {len(files)} files")

    candidates = [
        ("ffprobe (subprocess)", "ffprobe", run_ffprobe),
        ("mkvmerge (subprocess)", "mkvmerge", run_mkvmerge),
        ("mkv_subtitles.py (subprocess CLI)", None, run_mkv_subtitles_cli),
        ("mkv_subtitles() (in-process call)", None, run_mkv_subtitles_inproc),
    ]

    results = {}
    for name, required_tool, fn in candidates:
        if required_tool and shutil.which(required_tool) is None:
            print(f"{name}: skipped ({required_tool} not found on PATH)")
            continue
        times = timed(fn, files)
        results[name] = times
        print(f"{name}: mean={statistics.mean(times)*1000:.2f}ms  "
              f"median={statistics.median(times)*1000:.2f}ms  "
              f"min={min(times)*1000:.2f}ms  max={max(times)*1000:.2f}ms")

    if "ffprobe (subprocess)" in results:
        print()
        base_mean = statistics.mean(results["ffprobe (subprocess)"])
        for name, times in results.items():
            speedup = base_mean / statistics.mean(times)
            print(f"{name}: {speedup:.1f}x vs ffprobe")


if __name__ == "__main__":
    main()
