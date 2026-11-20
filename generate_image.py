#!/usr/bin/env python3
"""Draw the 19 November 2026 front page as a 1024x1024 PNG.

Pure standard library: a small framebuffer, a 5x7 bitmap font and a
minimal PNG writer built on zlib. No network, no clock, no randomness,
so the output bytes are identical on every run. Usage:
    python3 generate_image.py [output.png]
With no argument the image goes to generated.png next to this file.
This is a build-time tool only: the entry itself is main.py, which
copies the committed entry.png, so this file never overwrites it.
"""
import binascii
import os
import struct
import sys
import zlib

WIDTH = 1024
HEIGHT = 1024

# 5x7 bitmap font, caps only. Each glyph is 7 rows of 5 cells,
# '#' = ink, '.' = blank. The front page is set entirely in caps,
# so no lowercase glyphs are needed.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#..##", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    "1": ("..#..", ".##..", "#.#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", "..#..", ".#...", ".#..."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ",": (".....", ".....", ".....", ".....", "..##.", "..##.", ".#..."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
    "/": ("....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."),
    "&": (".##..", "#..#.", "#..#.", ".#...", "#.#.#", "#..#.", ".##.#"),
    "(": ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ")": (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    "%": ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.#.#", "#..##"),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
}


def new_canvas(width, height, color):
    return bytearray(bytes(color) * (width * height))


def fill(buf, width, x, y, w, h, color):
    r, g, b = color
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(width, x + w)
    y1 = min(HEIGHT, y + h)
    for yy in range(y0, y1):
        base = (yy * width + x0) * 3
        for xx in range(x0, x1):
            o = base + (xx - x0) * 3
            buf[o] = r
            buf[o + 1] = g
            buf[o + 2] = b


def border(buf, width, x, y, w, h, color, thick=2):
    fill(buf, width, x, y, w, thick, color)
    fill(buf, width, x, y + h - thick, w, thick, color)
    fill(buf, width, x, y, thick, h, color)
    fill(buf, width, x + w - thick, y, thick, h, color)


def draw_glyph(buf, width, x, y, ch, color, scale):
    glyph = FONT.get(ch, FONT["?"])
    for row in range(7):
        for col in range(5):
            if glyph[row][col] == "#":
                fill(buf, width, x + col * scale, y + row * scale,
                     scale, scale, color)


def text_width(text, scale):
    return len(text) * 6 * scale


def draw_text(buf, width, x, y, text, color, scale):
    cx = x
    for ch in text:
        draw_glyph(buf, width, cx, y, ch, color, scale)
        cx += 6 * scale


def draw_centred(buf, width, y, text, color, scale):
    draw_text(buf, width, (width - text_width(text, scale)) // 2,
              y, text, color, scale)


def wrap(text, max_chars):
    lines = []
    cur = ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(buf, width, x, y, text, color, scale, max_chars, line_h):
    lines = wrap(text, max_chars)
    for i, line in enumerate(lines):
        draw_text(buf, width, x, y + i * line_h, line, color, scale)
    return y + len(lines) * line_h


def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    return out + struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)


def write_png(path, width, height, buf):
    raw = b"".join(
        b"\x00" + bytes(buf[y * width * 3:(y + 1) * width * 3])
        for y in range(height)
    )
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", zlib.compress(raw, 9))
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


PAPER = (251, 248, 241)
CARD = (255, 255, 255)
INK = (24, 24, 32)
NAVY = (17, 24, 39)
GOLD = (201, 162, 39)
GREY = (100, 116, 139)
LINE = (203, 213, 225)
WHITE = (255, 255, 255)

STORIES = [
    {
        "kicker": "DIPLOMACY",
        "accent": (37, 99, 235),
        "headline": "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
        "body": "FIRST EVER US-CHINA-RUSSIA THREE-WAY SUMMIT AT APEC. "
                "NUCLEAR RISKS, UKRAINE AND IRAN ON THE TABLE.",
        "source": "REUTERS - AP - BBC",
    },
    {
        "kicker": "JUSTICE",
        "accent": (124, 58, 237),
        "headline": "ICJ: MYANMAR COMMITTED GENOCIDE",
        "body": "COURT RULES 9-6 OVER THE 2017 ROHINGYA CRACKDOWN. "
                "ABOUT 10,000 KILLED.",
        "source": "AP - REUTERS - BBC",
    },
    {
        "kicker": "MIDDLE EAST",
        "accent": (220, 38, 38),
        "headline": "HOUTHI STRIKE HITS RIYADH TOWER",
        "body": "MISSILE HITS THE PIF TOWER, HOME OF SAUDI ARABIA'S "
                "SOVEREIGN WEALTH FUND. WINDOWS BLOWN OUT ACROSS "
                "SEVEN FLOORS.",
        "source": "REUTERS",
    },
    {
        "kicker": "WAR IN EUROPE",
        "accent": (217, 119, 6),
        "headline": "UKRAINE HITS KERCH BRIDGE AGAIN",
        "body": "THIRD STRIKE ON THE RAIL SECTION IN FOUR DAYS. "
                "NEPTUN MISSILES HALT TRAIN TRAFFIC.",
        "source": "AP",
    },
    {
        "kicker": "TECHNOLOGY",
        "accent": (5, 150, 105),
        "headline": "ANTHROPIC'S RECORD $81.3B IPO",
        "body": "NASDAQ DEBUT. SHARES OPEN AT $111, 33% ABOVE THE "
                "$83 PRICE.",
        "source": "TECHCRUNCH - REUTERS",
    },
    {
        "kicker": "SOUTH ASIA",
        "accent": (190, 24, 93),
        "headline": "BANGLADESH BURNS",
        "body": "AWAMI LEAGUE LOCKDOWN BITES. YUNUS'S ANCESTRAL HOME "
                "TORCHED, FOUR KILLED, CLASHES IN 28 DISTRICTS.",
        "source": "PTI - REUTERS",
    },
]


def render():
    buf = new_canvas(WIDTH, HEIGHT, PAPER)
    # Masthead: dark band, title, then the date in gold.
    fill(buf, WIDTH, 0, 0, WIDTH, 168, NAVY)
    draw_centred(buf, WIDTH, 30, "THE WORLD IN ONE DAY", WHITE, 4)
    draw_centred(buf, WIDTH, 96, "THURSDAY, 19 NOVEMBER 2026", GOLD, 3)
    fill(buf, WIDTH, 0, 168, WIDTH, 4, GOLD)
    # Six cards: two columns, three rows.
    margin = 24
    gap = 16
    top = 188
    bottom = 976
    card_w = (WIDTH - 2 * margin - gap) // 2
    card_h = (bottom - top - 2 * gap) // 3
    for i, story in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x = margin + col * (card_w + gap)
        y = top + row * (card_h + gap)
        fill(buf, WIDTH, x, y, card_w, card_h, CARD)
        border(buf, WIDTH, x, y, card_w, card_h, LINE, 2)
        fill(buf, WIDTH, x, y, card_w, 10, story["accent"])
        draw_text(buf, WIDTH, x + 18, y + 26, story["kicker"],
                  story["accent"], 1)
        after_head = draw_wrapped(buf, WIDTH, x + 18, y + 52,
                                  story["headline"], INK, 2,
                                  (card_w - 36) // 12, 30)
        draw_wrapped(buf, WIDTH, x + 18, after_head + 14, story["body"],
                     INK, 1, (card_w - 36) // 6, 14)
        draw_text(buf, WIDTH, x + 18, y + card_h - 30, story["source"],
                  GREY, 1)
    draw_centred(buf, WIDTH, 988,
                 "SOURCES: REUTERS - AP - AFP - BBC - TECHCRUNCH - PTI",
                 GREY, 1)
    return buf


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "generated.png")
    buf = render()
    write_png(out, WIDTH, HEIGHT, buf)
    print("wrote %s (%dx%d)" % (out, WIDTH, HEIGHT))


if __name__ == "__main__":
    main()
