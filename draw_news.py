#!/usr/bin/env python3
"""Draw entry.png: a newspaper front page summing up the world news of
Monday 23 November 2026. Rendered with PIL so every letter is exact.
Run: python3 draw_news.py  -> writes entry.png next to this script."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (16, 16, 20)
NAVY = (16, 30, 67)
GOLD = (217, 164, 65)
RED = (178, 34, 34)
GREY = (90, 88, 82)
RULE = (200, 192, 172)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_block(draw, x, y, w, chip, chip_color, headline, deck,
               head_size=27, deck_size=19, head_font=SANS_B):
    """One story block: coloured category chip, bold headline, deck."""
    f_chip = font(SANS_B, 16)
    f_head = font(head_font, head_size)
    f_deck = font(SANS, deck_size)
    # chip
    tw = draw.textlength(chip, font=f_chip)
    pad = 10
    draw.rounded_rectangle([x, y, x + tw + 2 * pad, y + 28], radius=4,
                           fill=chip_color)
    draw.text((x + pad, y + 5), chip, font=f_chip, fill=(255, 255, 255))
    y += 38
    for line in wrap(draw, headline, f_head, w):
        draw.text((x, y), line, font=f_head, fill=INK)
        y += head_size + 6
    y += 2
    for line in wrap(draw, deck, f_deck, w):
        draw.text((x, y), line, font=f_deck, fill=(60, 58, 52))
        y += deck_size + 5
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 38  # margin

    # ---- Masthead ----
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((W // 2, 18), "THE WORLD TODAY", font=font(SERIF_B, 58),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 92), "MONDAY  23  NOVEMBER  2026", font=font(SANS_B, 34),
           fill=GOLD, anchor="ma")
    d.rectangle([0, 148, W, 154], fill=GOLD)

    y = 172

    # ---- Lead story: COP31 ----
    y = draw_block(
        d, M, y, W - 2 * M,
        "CLIMATE  •  ANTALYA, TURKEY", RED,
        "COP31 ends with no deal",
        "Two weeks of UN climate talks collapse without a political "
        "agreement, and the final draft drops any mention of fossil fuels.",
        head_size=46, deck_size=23, head_font=SERIF_B)
    y += 14
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    y += 16

    # ---- Grid: 2 columns x 3 rows ----
    col_w = (W - 2 * M - 28) // 2
    x2 = M + col_w + 28
    row_h = 196
    stories = [
        ("DIPLOMACY  •  NEW DELHI", NAVY,
         "Modi meets Nepal's PM in Delhi",
         "Balendra Shah holds talks on energy, hydropower and rail links "
         "on a two-day state visit to India."),
        ("ENERGY  •  STRAIT OF HORMUZ", (120, 72, 20),
         "Two tankers hit in the Strait of Hormuz",
         "British monitors report two tankers struck by projectiles near "
         "Oman; Iran says a tanker hit a naval mine."),
        ("WAR  •  BALTIC SEA", (90, 40, 90),
         "Russian cargo ship still burning off Finland",
         "The Sparta II, hit by drones on Saturday, drifts into Finnish "
         "waters; all 16 crew are evacuated."),
        ("DISASTER  •  INDONESIA", (140, 40, 40),
         "3 dead, dozens missing in factory fire",
         "A blaze at a candy factory near Jakarta leaves at least 36 "
         "workers unaccounted for; the search goes on."),
        ("SPORT  •  CRICKET", (20, 100, 60),
         "India smash record 720/9 in Wellington",
         "Rahul hits 136 and Pant 128 as India post the highest Test total "
         "ever scored in New Zealand."),
        ("EDUCATION  •  SOUTH KOREA", (40, 80, 140),
         "Minister quits over AI cheating row",
         "Education chief Choi Kyo-jin resigns after last-minute exam "
         "rules to stop AI cheating cause chaos."),
    ]
    for i, (chip, color, head, deck) in enumerate(stories):
        cx = M if i % 2 == 0 else x2
        cy = y + (i // 2) * row_h
        draw_block(d, cx, cy, col_w, chip, color, head, deck)
        # vertical divider between columns
        if i % 2 == 0:
            d.line([(M + col_w + 14, cy + 4),
                    (M + col_w + 14, cy + row_h - 14)], fill=RULE, width=1)

    y = y + 3 * row_h + 6
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    y += 12
    d.text((W // 2, y),
           "The news of Monday 23 November 2026",
           font=font(SERIF_B, 20), fill=INK, anchor="ma")
    y += 30
    d.text((W // 2, y),
           "Sources: Reuters  •  Al Jazeera  •  Yonhap  •  ESPNcricinfo  •  Channel News Asia",
           font=font(SANS, 15), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
