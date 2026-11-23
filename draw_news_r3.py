#!/usr/bin/env python3
"""Fresh R3/R4 rebuild of the news-image-20261123 front page.

Written from scratch for the judge-panel rebuild: same 7 verified stories
as the R2 entry, plus the panel's fixes — a drawn pictogram per story
(no more purely-typographic page) and a BY THE NUMBERS strip reusing only
figures already in those 7 stories (nothing invented).

Output: entry-r3.png (1024x1024). Never overwrites entry.png (the R2 entry).
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry-r3.png"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_IT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

NAVY = (16, 30, 67)
GOLD = (217, 164, 65)
INK = (17, 17, 17)
GRAY = (85, 85, 85)
RULE = (204, 204, 204)
WHITE = (255, 255, 255)

RED = (168, 50, 38)
GREEN = (30, 122, 70)
BLUE = (31, 78, 121)
ORANGE = (198, 122, 26)
PURPLE = (108, 52, 131)
TEAL = (17, 122, 101)
DARKRED = (140, 40, 30)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, text, f, max_w, max_lines, min_size, path):
    """Shrink font until text fits max_lines; returns (lines, font)."""
    size = f.size
    while size >= min_size:
        ff = font(path, size)
        lines = wrap(d, text, ff, max_w)
        if len(lines) <= max_lines:
            return lines, ff
        size -= 1
    raise SystemExit(f"OVERFLOW: cannot fit {text[:40]!r} in {max_lines} lines")


def tag(d, x, y, text, color, size=15):
    f = font(SANS_B, size)
    tw = d.textlength(text, font=f)
    pad_x, pad_y = 10, 5
    d.rounded_rectangle([x, y, x + tw + 2 * pad_x, y + size + 2 * pad_y + 4],
                        radius=5, fill=color)
    d.text((x + pad_x, y + pad_y), text, font=f, fill=WHITE)
    return tw + 2 * pad_x


def icon_tile(kind, color, size=48):
    """Draw a white pictogram on a color rounded square; returns RGBA tile."""
    tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=9, fill=color + (255,))
    w = (255, 255, 255, 255)
    s = size
    if kind == "globe":
        cx, cy, r = s / 2, s / 2, s * 0.32
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=w, width=3)
        d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=w, width=2)
        d.line([cx - r, cy, cx + r, cy], fill=w, width=2)
        d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 200, 340, fill=w, width=2)
    elif kind == "cricket":
        # bat: thick diagonal blade with handle; ball: red circle w/ seam
        d.polygon([(s * 0.52, s * 0.16), (s * 0.68, s * 0.28),
                   (s * 0.46, s * 0.60), (s * 0.32, s * 0.48)], fill=w)
        d.line([s * 0.30, s * 0.50, s * 0.16, s * 0.72], fill=w, width=6)
        d.ellipse([s * 0.60, s * 0.62, s * 0.86, s * 0.88], fill=(200, 40, 40, 255),
                  outline=w, width=2)
        d.arc([s * 0.62, s * 0.64, s * 0.84, s * 0.86], 300, 60, fill=w, width=2)
    elif kind == "train":
        d.rounded_rectangle([s * 0.18, s * 0.22, s * 0.82, s * 0.68], radius=6,
                            outline=w, width=3)
        d.rectangle([s * 0.30, s * 0.32, s * 0.46, s * 0.46], fill=w)
        d.rectangle([s * 0.54, s * 0.32, s * 0.70, s * 0.46], fill=w)
        d.line([s * 0.18, s * 0.56, s * 0.82, s * 0.56], fill=w, width=2)
        d.ellipse([s * 0.28, s * 0.68, s * 0.40, s * 0.80], fill=w)
        d.ellipse([s * 0.60, s * 0.68, s * 0.72, s * 0.80], fill=w)
    elif kind == "flame":
        # asymmetric flame with a flick curling left at the top
        d.polygon([(s * 0.56, s * 0.10), (s * 0.50, s * 0.26), (s * 0.68, s * 0.34),
                   (s * 0.78, s * 0.56), (s * 0.72, s * 0.76), (s * 0.52, s * 0.86),
                   (s * 0.32, s * 0.78), (s * 0.24, s * 0.58), (s * 0.34, s * 0.40),
                   (s * 0.42, s * 0.28)], fill=w)
        d.polygon([(s * 0.54, s * 0.42), (s * 0.64, s * 0.58), (s * 0.60, s * 0.74),
                   (s * 0.44, s * 0.74), (s * 0.40, s * 0.58)],
                  fill=color + (255,))
    elif kind == "warning":
        d.polygon([(s * 0.50, s * 0.16), (s * 0.86, s * 0.80), (s * 0.14, s * 0.80)],
                  fill=w)
        d.rectangle([s * 0.465, s * 0.38, s * 0.535, s * 0.60],
                    fill=color + (255,))
        d.ellipse([s * 0.45, s * 0.66, s * 0.55, s * 0.76], fill=color + (255,))
    elif kind == "scales":
        d.line([s * 0.50, s * 0.18, s * 0.50, s * 0.78], fill=w, width=3)
        d.line([s * 0.20, s * 0.30, s * 0.80, s * 0.30], fill=w, width=3)
        d.line([s * 0.50, s * 0.78, s * 0.32, s * 0.78], fill=w, width=3)
        d.line([s * 0.50, s * 0.78, s * 0.68, s * 0.78], fill=w, width=3)
        for cx in (s * 0.20, s * 0.80):
            d.line([cx, s * 0.30, cx - s * 0.10, s * 0.52], fill=w, width=2)
            d.line([cx, s * 0.30, cx + s * 0.10, s * 0.52], fill=w, width=2)
            d.arc([cx - s * 0.10, s * 0.42, cx + s * 0.10, s * 0.62], 0, 180,
                  fill=w, width=2)
    elif kind == "school":
        d.polygon([(s * 0.50, s * 0.16), (s * 0.84, s * 0.42), (s * 0.16, s * 0.42)],
                  fill=w)
        d.rectangle([s * 0.24, s * 0.42, s * 0.76, s * 0.80], outline=w, width=3)
        d.rectangle([s * 0.44, s * 0.58, s * 0.56, s * 0.80], fill=w)
        d.line([s * 0.50, s * 0.16, s * 0.50, s * 0.06], fill=w, width=2)
        d.polygon([(s * 0.50, s * 0.06), (s * 0.66, s * 0.11), (s * 0.50, s * 0.16)],
                  fill=w)
    return tile


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 104], fill=NAVY)
    f_title = font(SERIF, 58)
    d.text((W / 2, 8), "THE WORLD TODAY", font=f_title, fill=WHITE, anchor="ma")
    f_date = font(SANS_B, 25)
    d.text((W / 2, 68), "MONDAY 23 NOVEMBER 2026", font=f_date, fill=GOLD,
           anchor="ma")
    d.rectangle([0, 104, W, 108], fill=GOLD)

    # ---- lead: COP31 ----
    y = 124
    tag(d, 40, y, "CLIMATE  •  ANTALYA, TURKEY", RED)
    f_lead = font(SERIF, 46)
    d.text((40, y + 34), "COP31 ends with no deal", font=f_lead, fill=INK)
    lead_body = ("Two weeks of UN climate talks in Antalya collapse without a "
                 "political agreement; the final draft drops any mention of "
                 "fossil fuels. The UN chief voices 'profound frustration' "
                 "as the EU refuses to endorse the weak text.")
    f_body = font(SANS, 20)
    lines = wrap(d, lead_body, f_body, 660)
    assert len(lines) <= 4, f"lead body overflow: {len(lines)} lines"
    yy = y + 96
    for ln in lines:
        d.text((40, yy), ln, font=f_body, fill=(51, 51, 51))
        yy += 28
    # lead globe icon panel
    panel = Image.new("RGBA", (170, 170), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle([0, 0, 169, 169], radius=14, fill=NAVY + (255,))
    globe = icon_tile("globe", NAVY, 150)
    panel.alpha_composite(globe, (10, 6))
    pd.text((85, 138), "NO DEAL", font=font(SANS_B, 20), fill=GOLD, anchor="ma")
    img.paste(panel, (814, y + 30), panel)
    d = ImageDraw.Draw(img)

    d.line([40, 336, W - 40, 336], fill=RULE, width=1)

    # ---- grid: 6 stories, 2 cols x 3 rows ----
    stories = [
        ("SPORT  •  CRICKET", GREEN, "cricket",
         "India post record 720/9 — but NZ hold on for a draw",
         "Mitchell and Phillips bat out day five in Wellington as New "
         "Zealand finish 239/5 after India's record total."),
        ("DIPLOMACY  •  DELHI", BLUE, "train",
         "Modi gives Nepal Rs 24,000-crore package",
         "PM Modi announces a Rs 24,000-crore development package for "
         "Nepal, signs eight pacts, and flags a new Ayodhya–Janakpur train."),
        ("DISASTER  •  INDONESIA", ORANGE, "flame",
         "24 dead confirmed in Indonesia factory fire",
         "Rescuers search for about 30 people still missing after the "
         "weekend blaze at a candy factory in Banten."),
        ("WAR  •  US-IRAN", DARKRED, "warning",
         "Trump warns of Iran strikes after New Year",
         "Trump says he is inclined to resume major strikes if no deal is "
         "reached, and threatens vessels defying the Gulf blockade."),
        ("JUSTICE  •  THE HAGUE", PURPLE, "scales",
         "Tajikistan quits ICC on day of Putin visit",
         "Tajikistan becomes the fourth country to begin withdrawing from "
         "the court since the US push."),
        ("EUROPE  •  GERMANY", TEAL, "school",
         "450 German schools hit by emailed bomb threats",
         "Schools across Germany — and Denmark — receive emailed threats; "
         "police say there is no credible danger."),
    ]
    col_w = 460
    xs = [40, 524]
    ys = [348, 500, 652]
    for i, (tag_text, color, icon, head, body) in enumerate(stories):
        x = xs[i % 2]
        y = ys[i // 2]
        tag(d, x, y, tag_text, color, size=14)
        img.paste(icon_tile(icon, color, 48), (x + col_w - 48, y - 2),
                  icon_tile(icon, color, 48))
        d = ImageDraw.Draw(img)
        h_lines, h_font = fit_lines(d, head, font(SERIF, 25), col_w, 2, 20, SERIF)
        yy = y + 28
        for ln in h_lines:
            d.text((x, yy), ln, font=h_font, fill=INK)
            yy += 28
        b_lines, b_font = fit_lines(d, body, font(SANS, 17), col_w, 3, 14, SANS)
        yy += 2
        for ln in b_lines:
            d.text((x, yy), ln, font=b_font, fill=(51, 51, 51))
            yy += 20
        if i % 2 == 0:
            d.line([x + col_w + 12, y, x + col_w + 12, y + 140], fill=RULE, width=1)

    # ---- BY THE NUMBERS strip (figures already in the 7 stories) ----
    d.rectangle([0, 812, W, 908], fill=NAVY)
    d.text((40, 824), "BY THE NUMBERS", font=font(SANS_B, 16), fill=GOLD)
    stats = [
        ("720/9", "India's record total"),
        ("24 dead", "~30 missing in Banten"),
        ("450", "schools threatened"),
        ("Rs 24,000 cr", "Nepal package"),
    ]
    seg_w = (W - 80) // 4
    for i, (num, label) in enumerate(stats):
        cx = 40 + seg_w * i + seg_w // 2
        d.text((cx, 846), num, font=font(SERIF, 30), fill=GOLD, anchor="ma")
        d.text((cx, 882), label, font=font(SANS, 15), fill=WHITE, anchor="ma")

    # ---- footer ----
    d.line([40, 924, W - 40, 924], fill=RULE, width=1)
    d.text((W / 2, 936), "The news of Monday 23 November 2026",
           font=font(SERIF_IT, 21), fill=NAVY, anchor="ma")
    d.text((W / 2, 968),
           "Sources: Reuters  •  Al Jazeera  •  NDTV  •  The Hindu  •  "
           "CricTracker  •  Times of India  •  Fox News  •  Dawn",
           font=font(SANS, 14), fill=GRAY, anchor="ma")

    img.save(OUT)
    print(f"saved {OUT} {img.size}")


if __name__ == "__main__":
    main()
