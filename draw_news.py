#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news poster for make.fun news-image-20261120.

Renders entry.png (1024x1024 PNG) from a fixed set of verified headlines.
Everything is drawn with the standard library + Pillow so the poster is
reproducible byte for byte on every run.
"""

from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = Path(__file__).resolve().parent / "entry.png"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

INK = (16, 20, 30)
PAPER = (247, 244, 236)
ACCENT = (196, 42, 48)
NAVY = (24, 42, 78)

# Each card: (title lines, detail line, colour, icon kind)
CARDS = [
    (["CYCLONE", "AKVAN HITS"], "INDIA · ODISHA/ANDHRA", (22, 96, 170), "cyclone"),
    (["TRUMP · XI ·", "PUTIN MEET"], "FIRST TRILATERAL SUMMIT · SHENZHEN", ACCENT, "summit"),
    (["MYANMAR", "GUILTY"], "ICJ: ROHINGYA GENOCIDE VERDICT", (120, 60, 150), "scales"),
    (["ANTHROPIC", "IPO DEBUT"], "CLAUDE · BIGGEST IPO EVER · +17%", (16, 120, 90), "rocket"),
    (["COP31 ENDS", "IN ANTALYA"], "FOSSIL-FUEL LANGUAGE DROPPED", (30, 130, 130), "globe"),
    (["EU–UK", "SUMMIT"], "BRUSSELS · BURNHAM · VON DER LEYEN", (40, 70, 160), "stars"),
    (["GLOBAL", "SELLOFF"], "DOW BELOW 50K · GOLD BELOW $3,600", (190, 90, 30), "chart"),
    (["HOUTHIS HIT", "RIYADH"], "SAUDI CONFIRMS 4 ATTACKS", (140, 45, 60), "blast"),
    (["JAPAN–INDIA", "TIE DEEPENS"], "SDF LIVE-FIRE AT INDIAN RANGES", (60, 55, 110), "missile"),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, max_w, start):
    """Largest font size at which text fits max_w."""
    size = start
    while size > 8:
        f = font(path, size)
        if draw.textbbox((0, 0), text, font=f)[2] <= max_w:
            return f
        size -= 1
    return font(path, 9)


def wrap(draw, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textbbox((0, 0), trial, font=f)[2] <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def icon(d, kind, cx, cy, r, col):
    """Simple bold pictograms, legible at small size."""
    if kind == "cyclone":
        for i, rr in enumerate((r, r * 0.72, r * 0.44)):
            d.arc((cx - rr, cy - rr, cx + rr, cy + rr), 200 + i * 40, 520 + i * 40,
                  fill=col, width=max(3, int(r * 0.16)))
        d.ellipse((cx - r * 0.13, cy - r * 0.13, cx + r * 0.13, cy + r * 0.13), fill=col)
    elif kind == "summit":
        d.line((cx - r, cy + r * 0.55, cx, cy - r * 0.75, cx + r, cy + r * 0.55),
               fill=col, width=max(4, int(r * 0.18)))
        d.ellipse((cx - r * 0.28, cy - r * 1.05, cx + r * 0.28, cy - r * 0.5), fill=col)
    elif kind == "scales":
        d.line((cx, cy - r, cx, cy + r), fill=col, width=max(4, int(r * 0.16)))
        d.line((cx - r * 0.9, cy - r * 0.5, cx + r * 0.9, cy - r * 0.5), fill=col,
               width=max(4, int(r * 0.16)))
        for s in (-1, 1):
            d.pieslice((cx + s * r * 0.9 - r * 0.42, cy - r * 0.5,
                        cx + s * r * 0.9 + r * 0.42, cy + r * 0.3),
                       0, 180, fill=col)
        d.line((cx - r * 0.5, cy + r, cx + r * 0.5, cy + r), fill=col,
               width=max(4, int(r * 0.16)))
    elif kind == "rocket":
        d.polygon([(cx, cy - r), (cx + r * 0.42, cy + r * 0.35),
                   (cx, cy + r * 0.1), (cx - r * 0.42, cy + r * 0.35)], fill=col)
        d.polygon([(cx - r * 0.42, cy + r * 0.3), (cx - r * 0.05, cy + r * 0.05),
                   (cx - r * 0.05, cy + r * 0.95)], fill=col)
        d.polygon([(cx + r * 0.42, cy + r * 0.3), (cx + r * 0.05, cy + r * 0.05),
                   (cx + r * 0.05, cy + r * 0.95)], fill=col)
    elif kind == "globe":
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=max(4, int(r * 0.16)))
        d.ellipse((cx - r * 0.42, cy - r, cx + r * 0.42, cy + r), outline=col,
                  width=max(3, int(r * 0.12)))
        d.line((cx - r, cy, cx + r, cy), fill=col, width=max(3, int(r * 0.12)))
        d.arc((cx - r, cy - r * 0.55, cx + r, cy + r * 0.55), 0, 180, fill=col,
              width=max(3, int(r * 0.12)))
        d.arc((cx - r, cy - r * 0.55, cx + r, cy + r * 0.55), 180, 360, fill=col,
              width=max(3, int(r * 0.12)))
    elif kind == "stars":
        for star in range(12):
            angle = -math.pi / 2 + star * math.tau / 12
            sx = cx + r * 0.78 * math.cos(angle)
            sy = cy + r * 0.78 * math.sin(angle)
            pts = []
            for k in range(10):
                a = -math.pi / 2 + k * math.pi / 5
                rr = r * (0.17 if k % 2 == 0 else 0.075)
                pts.append((sx + rr * math.cos(a), sy + rr * math.sin(a)))
            d.polygon(pts, fill=col)
    elif kind == "chart":
        d.line((cx - r, cy + r * 0.8, cx + r, cy + r * 0.8), fill=col, width=max(3, int(r * 0.12)))
        pts = [(cx - r * 0.85, cy - r * 0.8), (cx - r * 0.25, cy - r * 0.15),
               (cx + r * 0.2, cy - r * 0.35), (cx + r * 0.7, cy + r * 0.35)]
        d.line(pts, fill=col, width=max(4, int(r * 0.16)), joint="curve")
        d.line((cx + r * 0.7, cy + r * 0.2, cx + r * 0.7, cy + r * 0.55), fill=col, width=5)
        d.polygon([(cx + r * 0.7, cy + r * 0.75), (cx + r * 0.38, cy + r * 0.3),
                   (cx + r * 1.0, cy + r * 0.3)], fill=col)
    elif kind == "blast":
        d.ellipse((cx - r * 0.35, cy - r * 0.35, cx + r * 0.35, cy + r * 0.35), fill=col)
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            d.line((cx + r * 0.45 * math.cos(a), cy + r * 0.45 * math.sin(a),
                    cx + r * 1.0 * math.cos(a), cy + r * 1.0 * math.sin(a)),
                   fill=col, width=max(4, int(r * 0.16)))
    elif kind == "missile":
        d.polygon([(cx, cy - r), (cx + r * 0.3, cy - r * 0.2), (cx + r * 0.3, cy + r * 0.6),
                   (cx - r * 0.3, cy + r * 0.6), (cx - r * 0.3, cy - r * 0.2)], fill=col)
        d.polygon([(cx - r * 0.3, cy + r * 0.1), (cx - r * 0.75, cy + r * 0.65),
                   (cx - r * 0.3, cy + r * 0.6)], fill=col)


def draw_card(d, card, x, y, cw, ch):
    titles, region, col, kind = card
    d.rounded_rectangle((x, y, x + cw, y + ch), radius=14, fill=(255, 255, 255),
                        outline=col, width=3)
    d.rounded_rectangle((x, y, x + cw, y + 10), radius=5, fill=col)
    icon(d, kind, x + 52, y + 66, 33, col)
    tx = x + 100
    ty = y + 30
    for t in titles:
        f = fit(d, t, FONT_BOLD, cw - 116, 30)
        d.text((tx, ty), t, font=f, fill=INK)
        ty += f.size + 4
    fr = font(FONT_BOLD, 15)
    for line_no, line in enumerate(wrap(d, region, fr, cw - 32)):
        d.text((x + 16, y + ch - 68 + line_no * 20), line, font=fr, fill=col)
    d.line((x + 16, y + ch - 76, x + cw - 16, y + ch - 76), fill=(228, 226, 218), width=2)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    d.rectangle((0, 0, W, 172), fill=NAVY)
    d.rectangle((0, 172, W, 180), fill=ACCENT)
    f_date = font(FONT_BOLD, 64)
    d.text((32, 20), "20 NOVEMBER 2026", font=f_date, fill=(255, 255, 255))
    f_sub = font(FONT_BOLD, 24)
    d.text((34, 100), "FRIDAY · THE WORLD'S NEWS IN ONE IMAGE", font=f_sub,
           fill=(255, 206, 92))
    f_sub2 = font(FONT_REG, 16)
    d.text((34, 136), "Everything that happened on this one day, across regions and beats",
           font=f_sub2, fill=(196, 206, 228))

    # date badge with a small globe, so the day reads at a glance
    bx = 770
    d.rounded_rectangle((bx, 26, 992, 146), radius=16, outline=(255, 255, 255), width=4)
    f_bd = font(FONT_BOLD, 26)
    d.text((bx + 16, 44), "NOV 20", font=f_bd, fill=(255, 255, 255))
    d.text((bx + 22, 96), "2026", font=font(FONT_BOLD, 30), fill=(255, 206, 92))
    gx, gy, gr = 940, 86, 32
    d.ellipse((gx - gr, gy - gr, gx + gr, gy + gr), outline=(255, 255, 255),
              width=4)
    d.ellipse((gx - gr * 0.42, gy - gr, gx + gr * 0.42, gy + gr), outline=(255, 255, 255),
              width=3)
    d.line((gx - gr, gy, gx + gr, gy), fill=(255, 255, 255), width=3)
    d.arc((gx - gr, gy - gr * 0.55, gx + gr, gy + gr * 0.55), 0, 180, fill=(255, 255, 255), width=3)
    d.arc((gx - gr, gy - gr * 0.55, gx + gr, gy + gr * 0.55), 180, 360, fill=(255, 255, 255), width=3)

    cols, rows = 3, 3
    m, gap = 26, 16
    top = 202
    cw = (W - 2 * m - (cols - 1) * gap) // cols
    ch = (H - top - m - (rows - 1) * gap) // rows
    for i, card in enumerate(CARDS):
        r, c = divmod(i, cols)
        draw_card(d, card, m + c * (cw + gap), top + r * (ch + gap), cw, ch)

    f_foot = font(FONT_REG, 14)
    d.text((m, H - 26), "Sources: Kyodo · AP · Reuters · Guardian · The Hindu · UN News · Consilium",
           font=f_foot, fill=(118, 122, 134))
    return img


def main():
    img = build()
    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
