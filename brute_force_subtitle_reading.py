#!/usr/bin/env python3

'''
Brute force finding of subtiles in an .MKV file
No external libraries or tools needed
'''

# inputfile is first parameter given, otherwise default to "first_100k.mkv"
import sys

inputfile = sys.argv[1] if len(sys.argv) > 1 else "first_100k.mkv"

# of file "first_100k.mkv", read first 10_000 bytes into bytes object
with open(inputfile, "rb") as f:
    data = f.read(10_000)

# print(f"Read {len(data)} bytes from first_100k.mkv")

# # find "dutch" in data (case-insensitive)
# index = data.lower().find(b"dutch")
# if index != -1:
#     print(f"Found 'dutch' at byte index {index}")
# else:
#     print("Did not find 'dutch' in the first 10,000 bytes")

# split data into lines, with each non-ASCII byte replaced by newline
lines = []
current_line = bytearray()
for byte in data:
    if 32 <= byte <= 126:  # ASCII printable range
        current_line.append(byte)
    else:
        if current_line:
            lines.append(current_line.decode('ascii', errors='ignore'))
            current_line = bytearray()
if current_line:
    lines.append(current_line.decode('ascii', errors='ignore'))

# print(lines)
# print("40 is", lines[40])  # print the 41st line (0-based index)

i = 1
while i < len(lines):
    if lines[i].startswith('S_TEXT/UTF8'):
        print(lines[i-1], lines[i+1].replace("Sn", ""), lines[i+2])
    if lines[i].startswith("A_EAC3"):
        # print("AUDIO:",lines[i-1])
        # print("AUDIO:",lines[i+1])
        # print("AUDIO:",lines[i+2])
        print("AUDIO:",lines[i+3].replace("Sn", ""))
        print("AUDIO:",lines[i+4])
    i += 1

# combine lines into a single string, separated by newlines
all_text = "\n".join(lines)
if all_text.lower().find("norwegian") != -1:
    print(f"Found 'norwegian' in the {inputfile} file")


# Note: "Norwegian Bokmål" is not pure ASCII, but ... UTF8. So the above is ... ugly
# 000016e0  00 9c 81 00 22 b5 9c 83  6e 6f 62 86 8b 53 5f 54  |...."...nob..S_T|
# 000016f0  45 58 54 2f 55 54 46 38  22 b5 9d 85 6e 62 2d 4e  |EXT/UTF8"...nb-N|
# 00001700  4f 53 6e 91 4e 6f 72 77  65 67 69 61 6e 20 42 6f  |OSn.Norwegian Bo|
# 00001710  6b 6d c3 a5 6c ae bc d7  81 18 73 c5 88 a5 a6 5c  |km..l.....s....\|


