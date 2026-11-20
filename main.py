#!/usr/bin/env python3
"""Entrypoint: place the committed front page at /output/entry.png.

The 19 November front page ships in this repo as entry.png. This
script copies it byte-for-byte to the output path the scorer reads.
No network, no randomness, so repeated runs are identical.
"""
import os
import shutil

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DEST = os.path.join(OUT_DIR, "entry.png")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    size = os.path.getsize(DEST)
    print("wrote %s (%d bytes)" % (DEST, size))

if __name__ == "__main__":
    main()
