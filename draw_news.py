#!/usr/bin/env python3
"""Draw 'The World in One Day' - a 1024x1024 newspaper front page summing up
the world news of Wednesday 18 November 2026.

Everything is drawn in code with PIL: navy masthead, a 2x4 grid of story
cards, and a footer naming the sources and the date. No external images.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- canvas
W, H = 1024, 1024
PAPER = (246, 241, 229)      # warm off-white
NAVY = (20, 38, 63)          # masthead band
GOLD = (201, 162, 39)        # masthead rule + date line
CARD = (255, 255, 255)
CARD_BORDER = (216, 208, 190)
INK = (26, 26, 26)
SUMMARY_INK = (58, 58, 58)
FOOTER_GREY = (107, 107, 107)

SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- stories
# (tag, headline, summary, chip colour)
STORIES = [
    ("MIDDLE EAST",
     "U.S. sinks five Iranian tankers",
     "Iran fires missiles at a U.S. base in Jordan and ships near Hormuz; oil tops $100.",
     (139, 30, 30)),
    ("POLITICS",
     "Peltola wins Alaska Senate seat",
     "Democrat beats Dan Sullivan; Democrats take a 56\u201344 Senate majority.",
     (31, 78, 121)),
    ("RUSSIA",
     "Russian military plane crashes in Siberia",
     "An-12 transport goes down near Kemerovo; all 19 aboard killed.",
     (74, 85, 104)),
    ("WEATHER",
     "Category 5 Cyclone Xavier hits Cook Islands",
     "Gusts reach 315 km/h; wharves damaged on Manihiki, no deaths reported.",
     (14, 116, 144)),
    ("ASIA",
     "North Korea fires missile toward the sea",
     "Seoul says a ballistic missile flew toward the Sea of Japan amid border tensions.",
     (156, 66, 33)),
    ("EUROPE",
     "Deep 5.3 quake rattles Romania",
     "Felt in Bucharest and Ukraine; no major damage reported.",
     (91, 75, 138)),
    ("AMERICAS",
     "U.S. report traces $12bn in Venezuelan oil revenue",
     "53-page State Department report details funds handled since Maduro's capture.",
     (39, 103, 73)),
    ("DIPLOMACY",
     "Four nations urge Israel to let aid into Gaza",
     "Australia, Canada, Italy and the UK call for open aid access as floods worsen.",
     (140, 109, 31)),
]

FOOTER_SOURCES = ("Sources: Al Jazeera \u00b7 Reuters \u00b7 AP \u00b7 MetService "
                  "\u00b7 The Paris Eye \u00b7 The Munich Eye \u00b7 USGS")
FOOTER_DATE = "All events happened, or were first reported, on 18 November 2026."


# ---------------------------------------------------------------- helpers
def wrap_text(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def text_height(fnt, lines, spacing=0):
    """Pixel height of wrapped lines, using the font's own line height."""
    if not lines:
        return 0
    ascent, descent = fnt.getmetrics()
    line = ascent + descent
    return (len(lines) - 1) * (line + spacing) + line


# ---------------------------------------------------------------- layout
MASTHEAD_H = 160
GRID_TOP = 164
GRID_LEFT = 40
GRID_RIGHT = W - 40
GRID_GAP = 10
COLS, ROWS = 2, 4
CARD_H = 192
CARD_W = (GRID_RIGHT - GRID_LEFT - (COLS - 1) * GRID_GAP) // COLS
CARD_PAD = 10
CHIP_H = 24
CHIP_GAP = 5
HEADLINE_GAP = 4

FOOTER_Y1 = 972
FOOTER_Y2 = 992


def draw_card(draw, x, y, tag, headline, summary, chip_colour):
    """Draw one story card; returns nothing, asserts everything fits."""
    inner_x = x + CARD_PAD
    inner_w = CARD_W - 2 * CARD_PAD
    content_h = CARD_H - 2 * CARD_PAD  # vertical room inside the card

    # Shrink headline / summary fonts only if the worst case would overflow.
    head_size = 29
    summ_size = 20
    while True:
        head_fnt = font(SERIF_BOLD, head_size)
        summ_fnt = font(SANS_REG, summ_size)
        head_lines = wrap_text(draw, headline, head_fnt, inner_w)
        summ_lines = wrap_text(draw, summary, summ_fnt, inner_w)
        total = (CHIP_H + CHIP_GAP
                 + text_height(head_fnt, head_lines)
                 + HEADLINE_GAP
                 + text_height(summ_fnt, summ_lines))
        if total <= content_h or (head_size <= 22 and summ_size <= 18):
            break
        if head_size > 22:
            head_size -= 1
        elif summ_size > 18:
            summ_size -= 1

    assert len(head_lines) <= 3, f"headline too long ({len(head_lines)} lines): {headline}"
    assert len(summ_lines) <= 2, f"summary too long ({len(summ_lines)} lines): {summary}"
    assert total <= content_h, f"card content overflows: {total} > {content_h}"

    # Card body.
    draw.rounded_rectangle([x, y, x + CARD_W - 1, y + CARD_H - 1],
                           radius=10, fill=CARD, outline=CARD_BORDER, width=1)

    # Tag chip.
    tag_fnt = font(SANS_BOLD, 17)
    tag_w = draw.textlength(tag, font=tag_fnt)
    chip_w = int(tag_w) + 20
    chip_y = y + CARD_PAD
    draw.rounded_rectangle([inner_x, chip_y, inner_x + chip_w, chip_y + CHIP_H],
                           radius=6, fill=chip_colour)
    draw.text((inner_x + 10, chip_y + 1), tag, font=tag_fnt, fill=(255, 255, 255))

    # Headline.
    hy = chip_y + CHIP_H + CHIP_GAP
    draw.multiline_text((inner_x, hy), "\n".join(head_lines),
                        font=head_fnt, fill=INK, spacing=0)

    # Summary.
    sy = hy + text_height(head_fnt, head_lines) + HEADLINE_GAP
    draw.multiline_text((inner_x, sy), "\n".join(summ_lines),
                        font=summ_fnt, fill=SUMMARY_INK, spacing=0)

    return len(head_lines), len(summ_lines)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- masthead: navy band, title, date line, gold rule ----
    draw.rectangle([0, 0, W - 1, MASTHEAD_H - 1], fill=NAVY)
    title_fnt = font(SERIF_BOLD, 60)
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=title_fnt)
    draw.text(((W - tw) / 2, 22), title, font=title_fnt, fill=(255, 255, 255))
    date_fnt = font(SANS_BOLD, 28)
    date_line = "WEDNESDAY \u00b7 18 NOVEMBER 2026"
    dw = draw.textlength(date_line, font=date_fnt)
    draw.text(((W - dw) / 2, 100), date_line, font=date_fnt, fill=GOLD)
    draw.rectangle([0, MASTHEAD_H, W - 1, MASTHEAD_H + 3], fill=GOLD)

    # ---- story grid ----
    for i, (tag, headline, summary, colour) in enumerate(STORIES):
        row, col = divmod(i, COLS)
        cx = GRID_LEFT + col * (CARD_W + GRID_GAP)
        cy = GRID_TOP + row * (CARD_H + GRID_GAP)
        hl, sl = draw_card(draw, cx, cy, tag, headline, summary, colour)
        print(f"card {i + 1}: {tag}: headline {hl} lines, summary {sl} lines")

    grid_bottom = GRID_TOP + ROWS * CARD_H + (ROWS - 1) * GRID_GAP
    assert grid_bottom < FOOTER_Y1, "grid collides with footer"

    # ---- footer ----
    foot_fnt = font(SANS_REG, 15)
    for text, fy in ((FOOTER_SOURCES, FOOTER_Y1), (FOOTER_DATE, FOOTER_Y2)):
        fw = draw.textlength(text, font=foot_fnt)
        assert fw <= W - 2 * 40, f"footer line too wide: {text}"
        draw.text(((W - fw) / 2, fy), text, font=foot_fnt, fill=FOOTER_GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out}: {img.size[0]}x{img.size[1]}, {size} bytes")
    assert img.size == (1024, 1024)
    assert size <= 1048576, f"entry.png too big: {size} bytes"


if __name__ == "__main__":
    main()
