#!/bin/bash

# check if file is MKV, and if so: how many subtitles, and which languages
# ... and that with only linux shell commands!

# Check if at least one file was provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 file1 [file2 ...]"
    exit 1
fi

# Loop through each argument provided to the script
for file in "$@"; do
    # Check if the file exists and is a regular file
    if [ -f "$file" ]; then
        echo "--- Processing: $file ---"
        # Your specific command pipeline
        echo -n "MKV or not: "
        head -c9999 "$file" | strings -3 | head -1 | grep matroska | wc -l
        echo -n "Number of S_TEXT: "
        #head -c 7111 "$file" | strings -3 | grep "S_TEXT" | wc -l
        head -c9999 "$file" | strings -3 | grep -e ^S_TEXT | wc -l
        echo -n "Languages: "
        #head -c 7111 "$file" | strings -3 | grep -B1 "S_TEXT" | grep -x '[a-z]*' | sort -u | tr "\n" " "
        head -c9999 "$file"  | strings -3 | grep -B1 -A1 "S_TEXT" | sed -e 's/Sn$//g' | grep -x '[a-z]*' | sort -u | tr "\n" " "
        echo "" # Adds a newline for readability between files
    else
        echo "Skip: '$file' not found or not a file."
    fi
done

