#!/usr/bin/env python3
"""Evening redraw for make.fun news-image-20261123.

Newspaper front page for Monday 23 November 2026, drawn fresh from the
evening research brief (7 stories, all verified against live sources on
23 Nov 2026). Renders entry.png (1024x1024, RGB, <= 1 MiB) next to this
file. Uses only DejaVu system fonts; no rupee symbol anywhere.
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 40
CONTENT_W = W - 2 * MARGIN  # 944

NAVY = (16, 30, 67)
GOLD = (217, 164, 65)
INK = (20, 20, 20)
GREY = (74, 74, 74)
LIGHT_GREY = (204, 204, 204)
WHITE = (255, 255, 255)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w, draw):
    """Greedy word wrap by pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_text(text, path, start_size, min_size, max_lines, max_w, draw):
    """Largest font size (down to min_size) that wraps into max_lines."""
    size = start_size
    while size > min_size:
        fnt = font(path, size)
        lines = wrap(text, fnt, max_w, draw)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(path, min_size)
    return fnt, wrap(text, fnt, max_w, draw)


def draw_chip(draw, x, y, label, color, size=17):
    """Coloured rounded chip with white bold text; returns chip width."""
    fnt = font(SANS_BOLD, size)
    tw = draw.textlength(label, font=fnt)
    pad_x, h = 11, 28
    w = int(tw) + 2 * pad_x
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=color)
    draw.text((x + pad_x, y + h // 2), label, font=fnt, fill=WHITE, anchor="lm")
    return w


LEAD = {
    "chip": "CLIMATE \u2022 ANTALYA, TURKEY",
    "chip_color": (176, 58, 46),
    "headline": "COP31 ends with no deal",
    "deck": (
        "Two weeks of UN climate talks in Antalya collapse without a political "
        "agreement; the final draft drops any mention of fossil fuels. The UN "
        "chief voices 'profound frustration' as the EU refuses to endorse the "
        "weak text."
    ),
}

GRID = [
    {
        "chip": "SPORT \u2022 CRICKET",
        "chip_color": (30, 132, 73),
        "headline": "India post record 720/9 \u2014 but NZ hold on for a draw",
        "deck": (
            "Mitchell and Phillips bat out day five in Wellington as New "
            "Zealand finish 239/5 after India's record total."
        ),
    },
    {
        "chip": "DIPLOMACY \u2022 DELHI",
        "chip_color": (31, 56, 100),
        "headline": "Modi gives Nepal Rs 24,000-crore package",
        "deck": (
            "PM Modi announces a Rs 24,000-crore development package for "
            "Nepal, signs eight pacts, and flags a new Ayodhya\u2013Janakpur train."
        ),
    },
    {
        "chip": "DISASTER \u2022 INDONESIA",
        "chip_color": (202, 111, 30),
        "headline": "24 dead confirmed in Indonesia factory fire",
        "deck": (
            "Rescuers search for about 30 people still missing after the "
            "weekend blaze at a candy factory in Banten."
        ),
    },
    {
        "chip": "WAR \u2022 US-IRAN",
        "chip_color": (123, 36, 28),
        "headline": "Trump warns of Iran strikes after New Year",
        "deck": (
            "Trump says he is inclined to resume major strikes if no deal is "
            "reached, and threatens vessels defying the Gulf blockade."
        ),
    },
    {
        "chip": "JUSTICE \u2022 THE HAGUE",
        "chip_color": (108, 52, 131),
        "headline": "Tajikistan quits ICC on day of Putin visit",
        "deck": (
            "Tajikistan becomes the fourth country to begin withdrawing from "
            "the court since the US push."
        ),
    },
    {
        "chip": "EUROPE \u2022 GERMANY",
        "chip_color": (17, 122, 101),
        "headline": "450 German schools hit by emailed bomb threats",
        "deck": (
            "Schools across Germany \u2014 and Denmark \u2014 receive emailed "
            "threats; police say there is no credible danger."
        ),
    },
]

FOOTER_TITLE = "The news of Monday 23 November 2026"
FOOTER_SOURCES = (
    "Sources: Reuters \u2022 Al Jazeera \u2022 NDTV \u2022 The Hindu \u2022 "
    "CricTracker \u2022 Times of India \u2022 Fox News \u2022 Dawn"
)


def main():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # --- Masthead ---
    draw.rectangle([0, 0, W, 118], fill=NAVY)
    draw.text(
        (W // 2, 16),
        "THE WORLD TODAY",
        font=font(SERIF_BOLD, 56),
        fill=WHITE,
        anchor="mt",
    )
    draw.text(
        (W // 2, 78),
        "MONDAY 23 NOVEMBER 2026",
        font=font(SANS_BOLD, 25),
        fill=GOLD,
        anchor="mt",
    )
    draw.rectangle([0, 118, W, 122], fill=GOLD)

    # --- Lead story ---
    draw_chip(draw, MARGIN, 140, LEAD["chip"], LEAD["chip_color"], size=19)
    draw.text(
        (MARGIN, 178),
        LEAD["headline"],
        font=font(SERIF_BOLD, 52),
        fill=INK,
    )
    lead_deck_font = font(SANS, 23)
    lead_lines = wrap(LEAD["deck"], lead_deck_font, CONTENT_W, draw)
    y = 244
    for line in lead_lines:
        draw.text((MARGIN, y), line, font=lead_deck_font, fill=GREY)
        y += 30

    # --- Divider under lead ---
    draw.line([(MARGIN, 332), (W - MARGIN, 332)], fill=LIGHT_GREY, width=2)

    # --- Grid: 2 columns x 3 rows ---
    col_w = (CONTENT_W - 28) // 2  # 458
    row_h, row_gap = 176, 12
    grid_top = 352
    for i, story in enumerate(GRID):
        col = i % 2
        row = i // 2
        x0 = MARGIN + col * (col_w + 28)
        y0 = grid_top + row * (row_h + row_gap)

        draw_chip(draw, x0, y0, story["chip"], story["chip_color"], size=16)

        h_font, h_lines = fit_text(
            story["headline"], SERIF_BOLD, 26, 21, 2, col_w, draw
        )
        hy = y0 + 38
        for line in h_lines:
            draw.text((x0, hy), line, font=h_font, fill=INK)
            hy += 32

        d_font, d_lines = fit_text(
            story["deck"], SANS, 18, 15, 3, col_w, draw
        )
        dy = hy + 8
        for line in d_lines:
            draw.text((x0, dy), line, font=d_font, fill=GREY)
            dy += 23

    # --- Vertical hairline between columns ---
    grid_bottom = grid_top + 3 * row_h + 2 * row_gap
    draw.line(
        [(W // 2, grid_top + 4), (W // 2, grid_bottom - 4)],
        fill=(221, 221, 221),
        width=1,
    )

    # --- Footer ---
    draw.line([(MARGIN, 922), (W - MARGIN, 922)], fill=LIGHT_GREY, width=2)
    draw.text(
        (W // 2, 934),
        FOOTER_TITLE,
        font=font(SERIF_BOLD, 18),
        fill=NAVY,
        anchor="mt",
    )
    draw.text(
        (W // 2, 962),
        FOOTER_SOURCES,
        font=font(SANS, 14),
        fill=GREY,
        anchor="mt",
    )

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print("wrote", out)
    print("size:", size, "bytes (limit 1048576)")
    print("sha256:", sha)
    assert img.size == (1024, 1024)
    assert size <= 1048576, "entry.png exceeds 1 MiB"


if __name__ == "__main__":
    main()
