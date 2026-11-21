#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026.

Produces entry.png, 1024x1024, deterministic: same bytes on every run.
Run: python3 draw.py  (writes entry.png next to this script)
"""

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 30
CW = W - 2 * MARGIN  # 964, content width

PAPER = (247, 243, 232)
INK = (22, 22, 22)
RED = (163, 22, 33)
GREY = (96, 92, 82)
CARD_BG = (255, 253, 246)
CARD_EDGE = (198, 190, 168)
NIGHT_TOP = (13, 24, 43)
NIGHT_BOTTOM = (35, 63, 104)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap, returns a list of lines."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_rich_para(draw, x, y, width, parts, line_height):
    """Draw a wrapped paragraph. parts is a list of (text, font) runs,
    so a bold lead-in can share a line with regular text. Returns the
    y just below the last line."""
    words = []
    for text, fnt in parts:
        for w in text.split(" "):
            if w:
                words.append((w, fnt))
    lines, cur, cur_w = [], [], 0
    for w, fnt in words:
        ww = draw.textlength(w, font=fnt)
        space = draw.textlength(" ", font=fnt) if cur else 0
        if cur and cur_w + space + ww > width:
            lines.append(cur)
            cur, cur_w = [(w, fnt)], ww
        else:
            cur.append((w, fnt))
            cur_w += space + ww
    if cur:
        lines.append(cur)
    yy = y
    for line in lines:
        xx = x
        for i, (w, fnt) in enumerate(line):
            if i:
                xx += draw.textlength(" ", font=fnt)
            draw.text((xx, yy), w, font=fnt, fill=INK)
            xx += draw.textlength(w, font=fnt)
        yy += line_height
    return yy


def draw_rule(draw, y, thick=1):
    draw.rectangle([MARGIN, y, W - MARGIN, y + thick - 1], fill=INK)


def draw_night_panel(draw, x, y, w, h):
    """Night sky over a city skyline, with interceptor arcs and bursts."""
    for i in range(h):
        t = i / max(h - 1, 1)
        r = int(NIGHT_TOP[0] + (NIGHT_BOTTOM[0] - NIGHT_TOP[0]) * t)
        g = int(NIGHT_TOP[1] + (NIGHT_BOTTOM[1] - NIGHT_TOP[1]) * t)
        b = int(NIGHT_TOP[2] + (NIGHT_BOTTOM[2] - NIGHT_TOP[2]) * t)
        draw.line([(x, y + i), (x + w - 1, y + i)], fill=(r, g, b))
    rng = random.Random(7)
    for _ in range(46):
        sx = x + rng.randint(4, w - 5)
        sy = y + rng.randint(4, int(h * 0.55))
        draw.point((sx, sy), fill=(220, 226, 240))
    horizon = y + h - 6
    skyline = [46, 30, 58, 38, 72, 44, 34, 64, 52, 40, 78, 36, 56, 30, 48, 66]
    bx = x + 6
    bw = (w - 12) // len(skyline)
    for j, bh in enumerate(skyline):
        draw.rectangle([bx, horizon - bh, bx + bw - 3, horizon], fill=(8, 14, 26))
        for _ in range(3):
            wx = bx + rng.randint(2, max(3, bw - 7))
            wy = horizon - rng.randint(6, max(7, bh - 4))
            draw.rectangle([wx, wy, wx + 2, wy + 3], fill=(255, 205, 110))
        bx += bw
    tx = x + int(w * 0.68)
    tw = 26
    draw.polygon(
        [(tx, horizon), (tx + 4, horizon - 96), (tx + tw - 4, horizon - 96),
         (tx + tw, horizon)],
        fill=(8, 14, 26),
    )
    draw.rectangle([tx + 10, horizon - 108, tx + 14, horizon - 96],
                   fill=(8, 14, 26))
    for _ in range(6):
        wy = horizon - rng.randint(10, 92)
        draw.rectangle([tx + 6, wy, tx + 8, wy + 2], fill=(255, 205, 110))
        draw.rectangle([tx + 16, wy, tx + 18, wy + 2], fill=(255, 205, 110))

    def arc(x0, y0, x1, y1, lift, color, width_px=3):
        pts = []
        steps = 40
        for s in range(steps + 1):
            t = s / steps
            px = x0 + (x1 - x0) * t
            py = y0 + (y1 - y0) * t - lift * 4 * t * (1 - t)
            pts.append((px, py))
        draw.line(pts, fill=color, width=width_px, joint="curve")

    def burst(cx, cy, radius, color):
        for k in range(12):
            ang = k * 30
            import math
            dx = radius * math.cos(math.radians(ang))
            dy = radius * math.sin(math.radians(ang))
            draw.line([(cx, cy), (cx + dx, cy + dy)], fill=color, width=2)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255))

    arc(x + 40, horizon - 10, x + int(w * 0.42), y + 26, 34,
        (255, 214, 130))
    arc(x + w - 60, horizon - 8, x + int(w * 0.60), y + 34, 30,
        (255, 214, 130))
    burst(x + int(w * 0.42), y + 26, 15, (255, 236, 180))
    burst(x + int(w * 0.60), y + 34, 12, (255, 236, 180))
    draw.ellipse([x + int(w * 0.30), y + 58, x + int(w * 0.30) + 5,
                  y + 63], fill=(255, 255, 255))
    draw.rectangle([x, y + h - 24, x + w, y + h], fill=(8, 14, 26))
    cap = font(SANS, 15)
    draw.text((x + 10, y + h - 21),
              "Interceptor fire over Riyadh in the early hours of Saturday.",
              font=cap, fill=(232, 234, 238))


def draw_card(draw, x, y, w, h, kicker, headline, dek):
    draw.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=CARD_EDGE,
                   width=1)
    draw.rectangle([x, y, x + 4, y + h], fill=RED)
    pad = 12
    kx, ky = x + pad + 4, y + 8
    draw.text((kx, ky), kicker, font=font(SANS_BOLD, 14), fill=RED)
    hy = ky + 20
    inner = w - 2 * pad - 4
    for line in wrap(draw, headline, font(SERIF_BOLD, 20), inner)[:2]:
        draw.text((kx, hy), line, font=font(SERIF_BOLD, 20), fill=INK)
        hy += 24
    for line in wrap(draw, dek, font(SANS, 15), inner)[:1]:
        draw.text((kx, hy + 3), line, font=font(SANS, 15), fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    y = 20
    draw.rectangle([MARGIN, y, W - MARGIN, y + 2], fill=INK)
    draw.rectangle([MARGIN, y + 6, W - MARGIN, y + 6], fill=INK)

    name = "THE WORLD TODAY"
    nf = font(SERIF_BOLD, 72)
    nw = draw.textlength(name, font=nf)
    draw.text(((W - nw) / 2, 30), name, font=nf, fill=INK)

    df = font(SANS_BOLD, 25)
    date = "SATURDAY, 21 NOVEMBER 2026"
    dw = draw.textlength(date, font=df)
    draw.text(((W - dw) / 2, 102), date, font=df, fill=INK)
    sf = font(SANS, 15)
    draw.text((MARGIN, 108), "SATURDAY EDITION", font=sf, fill=GREY)
    right = "ONE DAY IN ONE PAGE"
    draw.text((W - MARGIN - draw.textlength(right, font=sf), 108),
              right, font=sf, fill=GREY)

    draw_rule(draw, 134)
    draw.text((MARGIN, 144), "LEAD STORY: MIDDLE EAST",
              font=font(SANS_BOLD, 19), fill=RED)

    hf = font(SERIF_BOLD, 62)
    head = "MISSILES OVER RIYADH"
    hw = draw.textlength(head, font=hf)
    draw.text(((W - hw) / 2, 168), head, font=hf, fill=INK)

    sub = ("Saudi defences intercept three ballistic missiles aimed at the "
           "capital in the early hours, the second attack on Riyadh in days")
    sy = 236
    for line in wrap(draw, sub, font(SERIF_ITALIC, 25), 900):
        lw = draw.textlength(line, font=font(SERIF_ITALIC, 25))
        draw.text(((W - lw) / 2, sy), line, font=font(SERIF_ITALIC, 25),
                  fill=INK)
        sy += 29

    draw_night_panel(draw, MARGIN, 300, CW, 100)

    lead_left = ("Civil Defense sounded the alert at 1:53 a.m.; interceptions "
                 "followed shortly after 2 a.m. Two explosions were heard in "
                 "the capital before the alert was lifted. Pakistan's prime "
                 "minister condemned the attack on the King Abdullah "
                 "Financial District.")
    lead_right = ("A Houthi drone aimed at southern Saudi Arabia was also "
                  "intercepted, and Civil Defense issued 8 emergency alerts "
                  "in 24 hours. It is the second attack on the capital in "
                  "days, after Thursday's strike damaged the Public "
                  "Investment Fund tower, Riyadh's tallest skyscraper.")
    col_w = (CW - 20) // 2
    lf = font(SERIF, 19)
    y1 = draw_rich_para(draw, MARGIN, 410, col_w, [(lead_left, lf)], 24)
    y2 = draw_rich_para(draw, MARGIN + col_w + 20, 410, col_w,
                        [(lead_right, lf)], 24)
    lead_bottom = max(y1, y2)

    draw_rule(draw, lead_bottom + 8)
    gy = lead_bottom + 16
    draw.text((MARGIN, gy), "AROUND THE WORLD",
              font=font(SANS_BOLD, 19), fill=RED)
    gy += 28

    gap = 10
    card_w3 = (CW - 2 * gap) // 3
    grid_top = [
        ("IRAN", "Iran says it downed a 58th US drone",
         "IRGC claims another MQ-9 over Hormuz."),
        ("PERU", "Magnitude 6.7 quake shakes central Peru",
         "Strong tremor rattles the centre."),
        ("EUROPE", "Gen Z protests spread to 25 countries",
         "Youth-led demos reach across Europe."),
    ]
    for i, (kick, hd, dk) in enumerate(grid_top):
        draw_card(draw, MARGIN + i * (card_w3 + gap), gy, card_w3, 106,
                  kick, hd, dk)
    gy += 106 + gap
    card_w2 = (CW - gap) // 2
    grid_bottom = [
        ("UNITED STATES", "FBI criminal database reportedly hacked",
         "Breach reported as outages continue across the US."),
        ("DENMARK", "Denmark says it foiled a Russian assassination plot",
         "Target was a US-Ukrainian rapper, intelligence says."),
    ]
    for i, (kick, hd, dk) in enumerate(grid_bottom):
        draw_card(draw, MARGIN + i * (card_w2 + gap), gy, card_w2, 88,
                  kick, hd, dk)
    gy += 88

    draw_rule(draw, gy + 8)
    by = gy + 16
    draw.text((MARGIN, by), "IN BRIEF", font=font(SANS_BOLD, 19), fill=RED)
    by += 28

    briefs = [
        ("NEW YORK:", "Mayor-elect Mamdani plans to close Rikers Island "
         "jail by 2032."),
        ("TBILISI:", "A suspected gas blast partly collapses a block of "
         "flats, killing 6, including a young child."),
        ("LOS ANGELES:", "A man is convicted of starting the deadly "
         "Palisades fire."),
        ("SEOUL:", "The Supreme Court overturns ex-PM Han Duck-soo's "
         "15-year sentence over the martial law attempt."),
        ("SAN SALVADOR:", "President Bukele registers for a third "
         "consecutive term."),
        ("WASHINGTON:", "An appeals court lets the Trump administration end "
         "protected status for about 600,000 Venezuelans."),
    ]
    bf_bold = font(SANS_BOLD, 17)
    bf = font(SANS, 17)
    row_y = by
    for r in range(3):
        bottom = row_y
        for c in range(2):
            kick, text = briefs[r * 2 + c]
            end = draw_rich_para(
                draw, MARGIN + c * (col_w + 20), row_y, col_w,
                [(kick, bf_bold), (text, bf)], 21)
            bottom = max(bottom, end)
        row_y = bottom + 2

    draw_rule(draw, row_y + 6)
    foot = ("Every story above happened, or was first reported, on "
            "Saturday 21 November 2026.")
    ff = font(SERIF_ITALIC, 15)
    fw = draw.textlength(foot, font=ff)
    draw.text(((W - fw) / 2, row_y + 12), foot, font=ff, fill=GREY)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, out.stat().st_size, "bytes",
          "final y:", row_y + 30)


if __name__ == "__main__":
    main()
