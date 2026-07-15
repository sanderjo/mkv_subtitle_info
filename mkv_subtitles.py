#!/usr/bin/env python3
"""Find subtitle tracks in Matroska (.mkv) files by parsing the EBML
container directly. No external tools (ffprobe, mkvmerge) and no
non-standard-library Python packages are used.

Only the file header up to and including the Tracks element is read;
Clusters (the actual audio/video/subtitle payload) are never touched,
so this is fast even on multi-gigabyte files.
"""

import argparse
import json
import sys

EBML_ID = 0x1A45DFA3
SEGMENT_ID = 0x18538067
TRACKS_ID = 0x1654AE6B
TRACKENTRY_ID = 0xAE

# TrackEntry child elements we care about: id -> (field name, value type)
FIELD_IDS = {
    0xD7: ("number", "uint"),
    0x83: ("type", "uint"),
    0x86: ("codec_id", "ascii"),
    0x536E: ("name", "utf8"),
    0x22B59C: ("language", "ascii"),
    0x22B59D: ("language_ietf", "ascii"),
    0x88: ("default", "uint"),
    0x55AA: ("forced", "uint"),
    0xB9: ("enabled", "uint"),
}

# ISO 639-2 codes that were later deprecated in favour of a replacement
# code. Old muxers still write the deprecated form into the Language
# element; mkvmerge normalizes these for display, so we match that.
LANGUAGE_ALIASES = {
    "scr": "hrv",  # Croatian
    "scc": "srp",  # Serbian
    "mol": "ron",  # Moldavian -> Romanian
}

TRACK_TYPE_NAMES = {
    0x01: "video",
    0x02: "audio",
    0x03: "complex",
    0x10: "logo",
    0x11: "subtitle",
    0x12: "buttons",
    0x20: "control",
    0x21: "metadata",
}

# Friendly names for common codec IDs, purely cosmetic (parsing does not
# depend on this map).
CODEC_NAMES = {
    "S_TEXT/UTF8": "SubRip (SRT)",
    "S_TEXT/ASS": "ASS",
    "S_TEXT/SSA": "SSA",
    "S_TEXT/USF": "USF",
    "S_TEXT/WEBVTT": "WebVTT",
    "S_HDMV/PGS": "PGS (image-based)",
    "S_VOBSUB": "VobSub (image-based)",
    "S_DVBSUB": "DVB (image-based)",
    "S_KATE": "Kate",
}


class TruncatedFile(Exception):
    pass


class InvalidMatroska(Exception):
    pass


def read_exact(f, n):
    data = f.read(n)
    if len(data) < n:
        raise TruncatedFile(f"expected {n} bytes, got {len(data)}")
    return data


def read_element_id(f):
    """Return the raw element ID (marker bits included), or None at EOF."""
    first = f.read(1)
    if not first:
        return None
    b0 = first[0]
    if b0 == 0:
        raise InvalidMatroska("invalid EBML ID byte 0x00")
    length = 9 - b0.bit_length()
    rest = read_exact(f, length - 1)
    return int.from_bytes(first + rest, "big")


def read_vint_size(f):
    """Return the decoded size of an EBML element, or None if it uses the
    reserved "unknown size" all-ones encoding."""
    first = read_exact(f, 1)
    b0 = first[0]
    if b0 == 0:
        raise InvalidMatroska("invalid EBML size byte 0x00")
    length = 9 - b0.bit_length()
    rest = read_exact(f, length - 1)
    mask = (1 << (8 - length)) - 1
    value = b0 & mask
    for byte in rest:
        value = (value << 8) | byte
    if value == (1 << (7 * length)) - 1:
        return None  # unknown size
    return value


def decode_str(raw, encoding):
    return raw.rstrip(b"\x00").decode(encoding, errors="replace")


def parse_track_entry(f, end):
    entry = {
        "number": None,
        "type": None,
        "codec_id": None,
        "name": None,
        "language": None,
        "language_ietf": None,
        "default": None,
        "forced": None,
        "enabled": None,
    }
    while f.tell() < end:
        eid = read_element_id(f)
        if eid is None:
            break
        size = read_vint_size(f)
        if size is None:
            break  # a child with unknown size should not occur here
        if eid in FIELD_IDS:
            key, kind = FIELD_IDS[eid]
            raw = read_exact(f, size)
            if kind == "uint":
                entry[key] = int.from_bytes(raw, "big") if raw else 0
            elif kind == "ascii":
                entry[key] = decode_str(raw, "ascii")
            elif kind == "utf8":
                entry[key] = decode_str(raw, "utf-8")
        else:
            f.seek(size, 1)  # skip Video/Audio/CodecPrivate/etc, unneeded

    # EBML elements that are absent take their spec-defined default value,
    # not "unset" -- mkvmerge/ffprobe report these defaults too.
    if entry["default"] is None:
        entry["default"] = 1
    if entry["enabled"] is None:
        entry["enabled"] = 1
    if entry["forced"] is None:
        entry["forced"] = 0
    if entry["language"] is None:
        entry["language"] = "eng"
    entry["language"] = LANGUAGE_ALIASES.get(entry["language"], entry["language"])
    return entry


def parse_tracks(f, end):
    tracks = []
    while f.tell() < end:
        eid = read_element_id(f)
        if eid is None:
            break
        size = read_vint_size(f)
        if size is None:
            break
        if eid == TRACKENTRY_ID:
            entry_end = f.tell() + size
            tracks.append(parse_track_entry(f, entry_end))
            f.seek(entry_end)
        else:
            f.seek(size, 1)
    return tracks


def find_tracks(path):
    """Parse just enough of an mkv file to return its track list."""
    with open(path, "rb") as f:
        if read_element_id(f) != EBML_ID:
            raise InvalidMatroska("file does not start with an EBML header")
        size = read_vint_size(f)
        if size is None:
            raise InvalidMatroska("EBML header has unexpected unknown size")
        f.seek(size, 1)

        if read_element_id(f) != SEGMENT_ID:
            raise InvalidMatroska("no Segment element found")
        read_vint_size(f)  # Segment size is unreliable/unbounded; ignore it

        while True:
            eid = read_element_id(f)
            if eid is None:
                return []  # ran out of file before finding Tracks
            size = read_vint_size(f)
            if eid == TRACKS_ID:
                if size is None:
                    raise InvalidMatroska("Tracks element has unknown size")
                return parse_tracks(f, f.tell() + size)
            if size is None:
                # An unknown-size element (typically a Cluster) reached
                # before Tracks was found; nothing more we can safely skip.
                return []
            f.seek(size, 1)


def format_track(t):
    kind = TRACK_TYPE_NAMES.get(t["type"], f"unknown({t['type']})")
    codec = t["codec_id"] or "?"
    friendly = CODEC_NAMES.get(codec)
    codec_str = f"{codec} ({friendly})" if friendly else codec
    lang = t["language_ietf"] or t["language"] or "und"
    flags = []
    if t["default"]:
        flags.append("default")
    if t["forced"]:
        flags.append("forced")
    flag_str = f" [{','.join(flags)}]" if flags else ""
    name_str = f" \"{t['name']}\"" if t["name"] else ""
    return f"  #{t['number']} {kind}: {codec_str} lang={lang}{name_str}{flag_str}"


def track_lang(t):
    return t["language_ietf"] or t["language"] or "und"


def mkv_subtitles(path):
    """Return a short "AUDIO: .. SUBS: .." summary string for an mkv file.

    Raises TruncatedFile / InvalidMatroska / OSError if the file can't be
    read or isn't a valid Matroska file.
    """
    tracks = find_tracks(path)
    audio_langs = [track_lang(t) for t in tracks if t["type"] == 0x02]
    sub_langs = [track_lang(t) for t in tracks if t["type"] == 0x11]
    audio_str = " ".join(audio_langs) if audio_langs else "(none)"
    subs_str = " ".join(sub_langs) if sub_langs else "(none)"
    return f"AUDIO: {audio_str} SUBS: {subs_str}"


def process_file(path, all_tracks, as_json, long):
    try:
        tracks = find_tracks(path)
    except (TruncatedFile, InvalidMatroska, OSError) as e:
        if as_json:
            print(json.dumps({"file": path, "error": str(e)}))
        else:
            print(f"{path}: ERROR: {e}")
        return "error"

    subs = [t for t in tracks if t["type"] == 0x11]
    audio = [t for t in tracks if t["type"] == 0x02]
    audio_langs = [track_lang(t) for t in audio]
    sub_langs = [track_lang(t) for t in subs]

    if as_json:
        print(json.dumps({
            "file": path,
            "tracks": tracks if all_tracks else subs + audio,
            "audio_languages": audio_langs,
            "has_subtitles": bool(subs),
        }))
        return "ok" if subs else "missing"

    if not long:
        print(mkv_subtitles(path))
        return "ok" if subs else "missing"

    audio_str = "audio=[{}]".format(",".join(audio_langs)) if audio_langs else "audio=(none found)"

    if all_tracks:
        print(f"{path}: {audio_str}")
        for t in tracks:
            print(format_track(t))
        if not tracks:
            print("  (no tracks found)")
    else:
        if subs:
            print(f"{path}: {audio_str}, {len(subs)} subtitle track(s)")
            for t in subs:
                print(format_track(t))
        else:
            print(f"{path}: {audio_str}, NO SUBTITLES")

    return "ok" if subs else "missing"


def main():
    parser = argparse.ArgumentParser(
        description="Find subtitle tracks in .mkv files without ffprobe/mkvmerge.")
    parser.add_argument("files", nargs="+", help="path(s) to .mkv file(s)")
    parser.add_argument("--all-tracks", action="store_true",
                         help="show every track (video/audio/subtitle), not just subtitles")
    parser.add_argument("--json", action="store_true", help="emit one JSON object per file")
    parser.add_argument("--long", action="store_true",
                         help="show full per-track detail; without this, print a short "
                              "'AUDIO: .. SUBS: ..' summary line per file")
    args = parser.parse_args()

    had_error = False
    had_missing = False
    for path in args.files:
        result = process_file(path, args.all_tracks, args.json, args.long)
        if result == "error":
            had_error = True
        elif result == "missing":
            had_missing = True

    if had_error:
        sys.exit(2)
    if had_missing:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
