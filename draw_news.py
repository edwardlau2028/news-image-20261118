#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news summary image (1024x1024 PNG).

All headlines and summaries are my own wording of stories reported on
18 November 2026 by the sources listed in the footer. No AI image
generator is used: every glyph is rendered from system fonts with PIL,
so the text is pixel-accurate.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 248, 241)      # warm off-white
INK = (26, 26, 26)           # near-black
MUTED = (74, 68, 60)         # warm grey for summaries
NAVY = (15, 42, 74)          # masthead
GOLD = (232, 184, 75)        # date line + rule
RED = (176, 48, 48)
CARD = (255, 255, 255)
CARD_EDGE = (227, 220, 203)
FOOT = (110, 104, 94)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

f_title = ImageFont.truetype(SERIF_B, 56)
f_date = ImageFont.truetype(SANS_B, 30)
f_tag = ImageFont.truetype(SANS_B, 17)
f_head = ImageFont.truetype(SERIF_B, 29)
f_sum = ImageFont.truetype(SANS_R, 21)
f_foot = ImageFont.truetype(SANS_R, 18)

# (tag, tag colour, headline, one-line summary)
STORIES = [
    ("MIDDLE EAST", (142, 43, 43),
     "U.S. sinks five Iranian tankers",
     "Iran fires missiles at a U.S. base in Jordan and ships near Hormuz; oil tops $100."),
    ("POLITICS", (43, 95, 142),
     "Peltola wins Alaska Senate seat",
     "Democrat beats Dan Sullivan; Democrats take a 56\u201344 Senate majority."),
    ("RUSSIA", (55, 71, 79),
     "Russian military plane crashes in Siberia",
     "An-12 transport goes down near Kemerovo; all 19 aboard killed."),
    ("WEATHER", (74, 124, 46),
     "Category 5 Cyclone Xavier hits Cook Islands",
     "Gusts reach 315 km/h; wharves damaged on Manihiki, no deaths reported."),
    ("ASIA", (14, 124, 123),
     "North Korea fires missile toward the sea",
     "Seoul says a ballistic missile flew toward the Sea of Japan amid border tensions."),
    ("EUROPE", (91, 58, 142),
     "Deep 5.3 quake rattles Romania",
     "Felt in Bucharest and Ukraine; no major damage reported."),
    ("AMERICAS", (156, 107, 30),
     "U.S. report traces $12bn in Venezuelan oil revenue",
     "53-page State Department report details funds handled since Maduro's capture."),
    ("DIPLOMACY", (176, 58, 107),
     "Four nations urge Israel to let aid into Gaza",
     "Australia, Canada, Italy and the UK call for open aid access as floods worsen."),
]


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, cx, y, text, font, fill):
    draw.text((cx - draw.textlength(text, font=font) / 2, y), text, font=font, fill=fill)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Masthead ---
    d.rectangle([0, 0, W, 160], fill=NAVY)
    draw_center(d, W / 2, 30, "THE WORLD IN ONE DAY", f_title, (255, 255, 255))
    draw_center(d, W / 2, 104, "WEDNESDAY  \u00b7  18 NOVEMBER 2026", f_date, GOLD)
    d.rectangle([0, 160, W, 166], fill=GOLD)

    # --- Story grid: 2 columns x 4 rows ---
    margin, gap = 40, 40
    col_w = (W - 2 * margin - gap) // 2          # 462
    top, row_h, row_gap = 186, 182, 12
    for i, (tag, colour, head, summ) in enumerate(STORIES):
        r, c = divmod(i, 2)
        x0 = margin + c * (col_w + gap)
        y0 = top + r * (row_h + row_gap)
        x1, y1 = x0 + col_w, y0 + row_h

        d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD, outline=CARD_EDGE, width=2)

        # tag chip
        tw = d.textlength(tag, font=f_tag)
        d.rounded_rectangle([x0 + 16, y0 + 12, x0 + 16 + tw + 22, y0 + 38], radius=6, fill=colour)
        d.text((x0 + 27, y0 + 16), tag, font=f_tag, fill=(255, 255, 255))

        # headline, max 3 lines
        hlines = wrap(d, head, f_head, col_w - 32)
        assert len(hlines) <= 3, f"headline too long: {head!r} -> {hlines}"
        hy = y0 + 46
        for ln in hlines:
            d.text((x0 + 16, hy), ln, font=f_head, fill=INK)
            hy += 33

        # summary, max 2 lines, placed just below the headline block
        slines = wrap(d, summ, f_sum, col_w - 32)
        assert len(slines) <= 2, f"summary too long: {summ!r} -> {slines}"
        sy = hy + 6
        for ln in slines:
            d.text((x0 + 16, sy), ln, font=f_sum, fill=MUTED)
            sy += 26
        assert sy - 26 + 21 <= y0 + row_h - 8, f"summary overflows card: {summ!r}"

    # --- Footer ---
    fy = 962
    draw_center(d, W / 2, fy,
                "Sources: Al Jazeera \u00b7 Reuters \u00b7 AP \u00b7 MetService \u00b7 The Paris Eye \u00b7 The Munich Eye \u00b7 USGS",
                f_foot, FOOT)
    draw_center(d, W / 2, fy + 26,
                "All events happened, or were first reported, on 18 November 2026.",
                f_foot, FOOT)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
