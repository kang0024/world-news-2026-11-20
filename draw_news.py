#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news poster for make.fun news-image-20261120.

Renders entry.png (1024x1024 PNG) from a fixed set of verified headlines.
Everything is drawn with the standard library + Pillow so the poster is
reproducible byte for byte on every run.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = Path(__file__).resolve().parent / "entry.png"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

INK = (16, 20, 30)
PAPER = (247, 244, 236)
ACCENT = (196, 42, 48)
NAVY = (24, 42, 78)

# Each card: (title lines, region line, colour, icon kind)
CARDS = [
    (["CYCLONE", "AKVAN LANDFALL"], "INDIA · ODISHA/ANDHRA", (22, 96, 170), "cyclone"),
    (["TRILATERAL", "SUMMIT"], "USA · CHINA · RUSSIA / SHENZHEN", ACCENT, "summit"),
    (["ICJ: MYANMAR", "GUILTY"], "ROHINGYA GENOCIDE VERDICT", (120, 60, 150), "scales"),
    (["ANTHROPIC", "IPO DEBUT"], "BIGGEST IPO EVER · +17%", (16, 120, 90), "rocket"),
    (["COP31 CLOSES", "ANTALYA"], "FOSSIL-FUEL LANGUAGE DROPPED", (30, 130, 130), "globe"),
    (["EU–UK SUMMIT", "BRUSSELS"], "BURNHAM · COSTA · VON DER LEYEN", (40, 70, 160), "stars"),
    (["AI RALLY", "UNWINDS"], "GLOBAL STOCKS · LONGEST SLIDE", (190, 90, 30), "chart"),
    (["HOUTHIS HIT", "RIYADH"], "SAUDI CONFIRMS 4 STRIKES", (140, 45, 60), "blast"),
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
        for sx, sy in ((-0.55, -0.35), (0.55, -0.35), (0.0, 0.45)):
            pts = []
            for k in range(10):
                a = -1.5708 + k * 0.6283
                rr = r * (0.42 if k % 2 == 0 else 0.18)
                pts.append((cx + sx * r + rr * __import__("math").cos(a),
                            cy + sy * r + rr * __import__("math").sin(a)))
            d.polygon(pts, fill=col)
    elif kind == "chart":
        d.line((cx - r, cy + r * 0.8, cx + r, cy + r * 0.8), fill=col, width=max(3, int(r * 0.12)))
        pts = [(cx - r * 0.85, cy - r * 0.55), (cx - r * 0.25, cy + r * 0.05),
               (cx + r * 0.2, cy - r * 0.2), (cx + r * 0.85, cy + r * 0.75)]
        d.line(pts, fill=col, width=max(4, int(r * 0.16)), joint="curve")
        d.polygon([(cx + r * 0.85, cy + r * 0.75), (cx + r * 0.45, cy + r * 0.68),
                   (cx + r * 0.82, cy + r * 0.3)], fill=col)
    elif kind == "blast":
        d.ellipse((cx - r * 0.35, cy - r * 0.35, cx + r * 0.35, cy + r * 0.35), fill=col)
        for ang in range(0, 360, 45):
            import math
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
    icon(d, kind, x + 48, y + 62, 30, col)
    tx = x + 92
    ty = y + 26
    for t in titles:
        f = fit(d, t, FONT_BOLD, cw - 108, 25)
        d.text((tx, ty), t, font=f, fill=INK)
        ty += f.size + 3
    fr = font(FONT_REG, 13)
    for line in wrap(d, region, fr, cw - 30):
        d.text((x + 15, y + ch - 42), line, font=fr, fill=(90, 96, 110))
        break


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    d.rectangle((0, 0, W, 150), fill=NAVY)
    d.rectangle((0, 150, W, 158), fill=ACCENT)
    f_date = font(FONT_BOLD, 62)
    d.text((34, 22), "20 NOVEMBER 2026", font=f_date, fill=(255, 255, 255))
    f_sub = font(FONT_BOLD, 25)
    d.text((36, 96), "FRIDAY  ·  THE WORLD'S NEWS IN ONE IMAGE", font=f_sub,
           fill=(255, 214, 120))
    d.rectangle((760, 30, 990, 120), outline=(255, 255, 255), width=3)
    f_bd = font(FONT_BOLD, 40)
    d.text((790, 40), "20.11", font=f_bd, fill=(255, 255, 255))
    f_bd2 = font(FONT_BOLD, 40)
    d.text((856, 40), "2026", font=f_bd2, fill=(255, 255, 255))

    cols, rows = 3, 3
    m, gap = 26, 16
    top = 182
    cw = (W - 2 * m - (cols - 1) * gap) // cols
    ch = (H - top - m - (rows - 1) * gap) // rows
    for i, card in enumerate(CARDS):
        r, c = divmod(i, cols)
        draw_card(d, card, m + c * (cw + gap), top + r * (ch + gap), cw, ch)

    f_foot = font(FONT_REG, 14)
    d.text((m, H - 24), "Compiled from wire reports: Kyodo · AP · Guardian · Reuters · The Hindu · UN · Consilium",
           font=f_foot, fill=(120, 124, 136))
    return img


def main():
    img = build()
    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
