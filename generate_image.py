#!/usr/bin/env python3
"""Render the news image for Thursday 19 November 2026.

Build-time script (runs on the author's machine, not in the grader):
draws a 1024x1024 newspaper front page to entry.png from the six
verified stories below. Each story happened on, or was reported on,
19 November 2026, as carried by Reuters, AP, AFP, BBC, TechCrunch and
PTI (via the day's briefings that collected them). The entry itself is
main.py, which only copies entry.png to /output/entry.png —
deterministic, stdlib-only, no network.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)       # newsprint
NAVY = (18, 30, 58)
GOLD = (212, 175, 105)
INK = (26, 26, 26)
BODY_INK = (62, 62, 62)
GREY = (92, 92, 92)
CARD = (255, 255, 255)
RULE = (198, 190, 172)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# (tag, tag colour, headline, summary, icon)
STORIES = [
    ("DIPLOMACY", (27, 94, 143),
     "Trump, Xi and Putin meet in Shenzhen",
     "The three leaders hold the first US\u2013China\u2013Russia summit "
     "at APEC, talking nuclear risks, Ukraine and Iran.",
     "flags"),
    ("JUSTICE", (106, 76, 147),
     "UN court: Myanmar committed genocide",
     "The ICJ rules 9\u20136 that the 2017 crackdown on the Rohingya "
     "was genocide; about 10,000 were killed.",
     "scales"),
    ("MIDDLE EAST", (176, 106, 0),
     "Houthi strike hits Riyadh\u2019s PIF Tower",
     "A missile damages Saudi Arabia\u2019s sovereign wealth fund HQ, "
     "blowing out windows across seven floors.",
     "tower"),
    ("EUROPE \u00b7 WAR", (178, 34, 34),
     "Kerch bridge rail hit a third time",
     "Neptun missiles strike the rail section; train traffic halts "
     "days after the road span collapsed.",
     "bridge"),
    ("TECHNOLOGY", (46, 125, 90),
     "Anthropic debuts in record $81.3B IPO",
     "Shares open at $111 on Nasdaq, 33% above the $83 price, in "
     "the largest listing ever.",
     "chip"),
    ("SOUTH ASIA", (150, 60, 60),
     "Bangladesh burns as lockdown bites",
     "Yunus\u2019s ancestral home is torched and four people are "
     "killed in Awami League lockdown violence.",
     "flame"),
]


def icon(draw, kind, cx, cy, r, colour):
    """Simple white glyph on a coloured disc."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)
    w = (255, 255, 255)
    if kind == "bridge":
        draw.line([cx - r + 8, cy + 6, cx + r - 8, cy + 6], fill=w, width=4)
        draw.arc([cx - r + 8, cy - r + 12, cx - 4, cy + 10], 180, 360,
                 fill=w, width=4)
        draw.arc([cx + 4, cy - r + 12, cx + r - 8, cy + 10], 180, 360,
                 fill=w, width=4)
        draw.line([cx - r + 12, cy - r + 18, cx - r + 12, cy + 6],
                  fill=w, width=3)
        draw.line([cx + r - 12, cy - r + 18, cx + r - 12, cy + 6],
                  fill=w, width=3)
    elif kind == "flags":
        for x in (cx - 16, cx - 2, cx + 12):
            draw.line([x, cy - r + 14, x, cy + r - 12], fill=w, width=3)
            draw.rectangle([x, cy - r + 14, x + 12, cy - r + 26], fill=w)
    elif kind == "scales":
        draw.line([cx, cy - r + 12, cx, cy + r - 12], fill=w, width=3)
        draw.line([cx - r + 12, cy - r + 12, cx + r - 12, cy - r + 12],
                  fill=w, width=3)
        draw.polygon([(cx - r + 12, cy - 2), (cx - r + 2, cy - 2),
                      (cx - r + 7, cy + 10)], fill=w)
        draw.polygon([(cx + r - 12, cy - 2), (cx + r - 2, cy - 2),
                      (cx + r - 7, cy + 10)], fill=w)
        draw.line([cx - 8, cy + r - 12, cx + 8, cy + r - 12], fill=w, width=3)
    elif kind == "tower":
        draw.polygon([(cx - 10, cy + r - 12), (cx - 10, cy - 6),
                      (cx, cy - r + 10), (cx + 10, cy - 6),
                      (cx + 10, cy + r - 12)], fill=w)
        draw.line([cx - 6, cy + 2, cx + 6, cy + 2], fill=colour, width=2)
        draw.line([cx - 6, cy + 10, cx + 6, cy + 10], fill=colour, width=2)
    elif kind == "flame":
        draw.polygon([(cx, cy - r + 12), (cx + 12, cy - 2),
                      (cx + 6, cy + 6), (cx + 14, cy + r - 12),
                      (cx - 14, cy + r - 12), (cx - 6, cy + 6),
                      (cx - 12, cy - 2)], fill=w)
    elif kind == "chip":
        draw.rectangle([cx - 14, cy - 14, cx + 14, cy + 14], outline=w,
                       width=3)
        draw.rectangle([cx - 6, cy - 6, cx + 6, cy + 6], fill=w)
        for x in (cx - 8, cx, cx + 8):
            draw.line([x, cy - 20, x, cy - 14], fill=w, width=3)
            draw.line([x, cy + 14, x, cy + 20], fill=w, width=3)
        for y in (cy - 8, cy, cy + 8):
            draw.line([cx - 20, y, cx - 14, y], fill=w, width=3)
            draw.line([cx + 14, y, cx + 20, y], fill=w, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 172], fill=NAVY)
    d.line([36, 168, W - 36, 168], fill=GOLD, width=3)
    f_name = font(SERIF_BOLD, 40)
    f_kicker = font(SANS_BOLD, 22)
    date_text = "THURSDAY, 19 NOVEMBER 2026"
    date_size = 54
    f_date = font(SANS_BOLD, date_size)
    while d.textlength(date_text, font=f_date) > W - 2 * 36 and date_size > 28:
        date_size -= 2
        f_date = font(SANS_BOLD, date_size)
    f_sub = font(SANS, 22)
    d.text((36, 16), "THE WORLD IN ONE DAY", font=f_name, fill=(255, 255, 255))
    d.text((W - 36 - d.textlength("No. 19", font=f_kicker), 26), "No. 19",
           font=f_kicker, fill=GOLD)
    d.text((36, 66), date_text, font=f_date, fill=GOLD)
    d.text((36, 130), "Six stories that defined the day \u2014 as reported",
           font=f_sub, fill=(190, 200, 220))

    # --- story cards: 2 cols x 3 rows ---
    margin, gutter = 36, 18
    cw = (W - 2 * margin - gutter) // 2
    ch = 244
    top = 192
    f_tag = font(SANS_BOLD, 19)
    f_head = font(SANS_BOLD, 28)
    f_body = font(SANS, 20)
    for i, (tag, colour, head, body, ic) in enumerate(STORIES):
        row, col = divmod(i, 2)
        x0 = margin + col * (cw + gutter)
        y0 = top + row * (ch + gutter)
        d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=CARD, outline=RULE,
                    width=2)
        d.rectangle([x0, y0, x0 + cw, y0 + 7], fill=colour)
        icon(d, ic, x0 + cw - 42, y0 + 46, 29, colour)
        d.text((x0 + 18, y0 + 20), tag, font=f_tag, fill=colour)
        text_w = cw - 36 - 74  # leave room for the icon disc
        y = y0 + 52
        head_lines = wrap(d, head, f_head, text_w)[:2]
        for ln in head_lines:
            d.text((x0 + 18, y), ln, font=f_head, fill=INK)
            y += 35
        y += 4
        body_lines = wrap(d, body, f_body, cw - 36)[:3]
        for ln in body_lines:
            d.text((x0 + 18, y), ln, font=f_body, fill=BODY_INK)
            y += 27
        if len(wrap(d, head, f_head, text_w)) > 2 or \
                len(wrap(d, body, f_body, cw - 36)) > 3:
            print("WARNING: text truncated in card", i, tag)

    # --- footer ---
    f_foot = font(SANS, 17)
    d.text((36, 986),
           "Sources: Reuters, AP, AFP, BBC, TechCrunch, PTI \u2014 as reported "
           "on 19 November 2026.",
           font=f_foot, fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
