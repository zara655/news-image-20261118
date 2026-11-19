#!/usr/bin/env python3
"""Draw entry.png: a one-image summary of world news on Wednesday 18 November 2026.

Run locally (needs Pillow); the grader only runs main.py, which copies the
committed entry.png. Layout: masthead with the date, one lead story, eight
story cards with hand-drawn icons, footer. 1024x1024, deterministic.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
INK = (14, 22, 38)        # deep navy background
PAPER = (246, 241, 231)   # warm off-white panels
RED = (198, 40, 49)
GOLD = (232, 176, 32)
TEAL = (23, 133, 140)
GREEN = (46, 140, 84)
PURPLE = (108, 74, 160)
ORANGE = (222, 116, 28)
SKY = (58, 124, 196)
SLATE = (52, 64, 84)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def flag_us(d, x, y, w, h):
    stripe = h / 7
    for i in range(7):
        c = (179, 34, 52) if i % 2 == 0 else WHITE
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=c)
    d.rectangle([x, y, x + w * 0.42, y + stripe * 4], fill=(60, 59, 110))
    for r in range(3):
        for c in range(4):
            cx = x + 6 + c * (w * 0.42 - 10) / 3
            cy = y + 5 + r * (stripe * 4 - 8) / 2
            d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=WHITE)
    d.rectangle([x, y, x + w, y + h], outline=BLACK, width=2)


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=BLACK, width=2)
    cx, cy, r = x + w * 0.22, y + h * 0.3, h * 0.16
    pts = []
    import math
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 222, 0))


def flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=WHITE)
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 43, 30))
    d.rectangle([x, y, x + w, y + h], outline=BLACK, width=2)


def icon_barrel(d, cx, cy, s, c):
    w, h = s * 0.62, s * 0.85
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=8, fill=c, outline=BLACK, width=3)
    for f in (0.28, 0.5, 0.72):
        d.line([cx - w / 2, cy - h / 2 + h * f, cx + w / 2, cy - h / 2 + h * f], fill=BLACK, width=3)
    d.ellipse([cx - w * 0.32, cy - h / 2 - 6, cx + w * 0.32, cy - h / 2 + 8], fill=c, outline=BLACK, width=3)


def icon_bridge(d, cx, cy, s, c):
    x0, x1 = cx - s * 0.48, cx + s * 0.48
    deck = cy - s * 0.05
    d.line([x0, deck, x1, deck], fill=c, width=7)
    for fx in (0.18, 0.5, 0.82):
        px = x0 + (x1 - x0) * fx
        d.line([px, deck - s * 0.34, px, deck + s * 0.3], fill=c, width=6)
    d.arc([x0, deck - s * 0.36, cx, deck + s * 0.1], 180, 360, fill=c, width=4)
    d.arc([cx, deck - s * 0.36, x1, deck + s * 0.1], 180, 360, fill=c, width=4)
    for i in range(3):
        wy = cy + s * (0.22 + i * 0.11)
        d.arc([cx - s * 0.4, wy - 8, cx - s * 0.05, wy + 8], 0, 180, fill=SKY, width=3)
        d.arc([cx + s * 0.05, wy - 8, cx + s * 0.4, wy + 8], 0, 180, fill=SKY, width=3)


def icon_chip(d, cx, cy, s, c):
    w = s * 0.58
    d.rounded_rectangle([cx - w / 2, cy - w / 2, cx + w / 2, cy + w / 2], radius=8, fill=c, outline=BLACK, width=3)
    d.rounded_rectangle([cx - w * 0.26, cy - w * 0.26, cx + w * 0.26, cy + w * 0.26], radius=5, outline=WHITE, width=3)
    for i in range(4):
        t = -w * 0.36 + i * w * 0.24
        d.line([cx + t, cy - w / 2, cx + t, cy - w / 2 - s * 0.14], fill=c, width=5)
        d.line([cx + t, cy + w / 2, cx + t, cy + w / 2 + s * 0.14], fill=c, width=5)
        d.line([cx - w / 2, cy + t, cx - w / 2 - s * 0.14, cy + t], fill=c, width=5)
        d.line([cx + w / 2, cy + t, cx + w / 2 + s * 0.14, cy + t], fill=c, width=5)


def icon_leaf(d, cx, cy, s, c):
    import math
    # leaf outline: two sine curves from bottom-left tip to top-right tip
    x0, y0 = cx - s * 0.42, cy + s * 0.36
    x1, y1 = cx + s * 0.42, cy - s * 0.36
    upper, lower = [], []
    for i in range(41):
        t = i / 40
        bx = x0 + (x1 - x0) * t
        by = y0 + (y1 - y0) * t
        off = s * 0.3 * math.sin(t * math.pi)
        upper.append((bx - off * 0.7, by - off * 0.7))
        lower.append((bx + off * 0.7, by + off * 0.7))
    d.polygon(upper + lower[::-1], fill=c, outline=BLACK)
    d.line([x0, y0, x1, y1], fill=BLACK, width=4)
    d.line([cx - s * 0.12, cy + s * 0.1, cx - s * 0.2, cy - s * 0.08], fill=BLACK, width=3)
    d.line([cx + s * 0.1, cy - s * 0.08, cx + s * 0.02, cy - s * 0.26], fill=BLACK, width=3)


def icon_cyclone(d, cx, cy, s, c):
    import math
    pts = []
    for i in range(140):
        t = i / 140 * math.pi * 5.2
        r = s * 0.05 + (i / 140) * s * 0.4
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t) * 0.82))
    d.line(pts, fill=c, width=7, joint="curve")
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=BLACK)


def icon_scales(d, cx, cy, s, c):
    top = cy - s * 0.42
    d.line([cx, top, cx, cy + s * 0.3], fill=c, width=6)
    d.line([cx - s * 0.38, top + s * 0.1, cx + s * 0.38, top + s * 0.1], fill=c, width=6)
    d.ellipse([cx - 6, top - 6, cx + 6, top + 6], fill=c, outline=BLACK, width=2)
    for sx in (cx - s * 0.38, cx + s * 0.38):
        d.line([sx, top + s * 0.1, sx - s * 0.13, cy + s * 0.08], fill=c, width=3)
        d.line([sx, top + s * 0.1, sx + s * 0.13, cy + s * 0.08], fill=c, width=3)
        d.arc([sx - s * 0.15, cy - s * 0.02, sx + s * 0.15, cy + s * 0.2], 0, 180, fill=c, width=5)
    d.line([cx - s * 0.2, cy + s * 0.36, cx + s * 0.2, cy + s * 0.36], fill=c, width=7)


def icon_capitol(d, cx, cy, s, c):
    base = cy + s * 0.36
    d.arc([cx - s * 0.3, cy - s * 0.42, cx + s * 0.3, cy + s * 0.18], 180, 360, fill=c, width=8)
    d.line([cx, cy - s * 0.42, cx, cy - s * 0.52], fill=c, width=5)
    d.line([cx - s * 0.34, cy - s * 0.08, cx + s * 0.34, cy - s * 0.08], fill=c, width=6)
    for i in range(5):
        px = cx - s * 0.28 + i * s * 0.14
        d.line([px, cy - s * 0.02, px, base - s * 0.08], fill=c, width=5)
    d.line([cx - s * 0.4, base, cx + s * 0.4, base], fill=c, width=8)


def icon_rocket(d, cx, cy, s, c):
    import math
    body = [(cx, cy - s * 0.46), (cx + s * 0.2, cy - s * 0.05), (cx + s * 0.16, cy + s * 0.22),
            (cx - s * 0.16, cy + s * 0.22), (cx - s * 0.2, cy - s * 0.05)]
    d.polygon(body, fill=c, outline=BLACK)
    d.ellipse([cx - s * 0.09, cy - s * 0.22, cx + s * 0.09, cy - s * 0.04], fill=WHITE, outline=BLACK, width=3)
    d.polygon([(cx - s * 0.16, cy + s * 0.1), (cx - s * 0.34, cy + s * 0.36), (cx - s * 0.1, cy + s * 0.36)], fill=RED, outline=BLACK)
    d.polygon([(cx + s * 0.16, cy + s * 0.1), (cx + s * 0.34, cy + s * 0.36), (cx + s * 0.1, cy + s * 0.36)], fill=RED, outline=BLACK)
    d.polygon([(cx - s * 0.09, cy + s * 0.24), (cx + s * 0.09, cy + s * 0.24), (cx, cy + s * 0.48)], fill=ORANGE, outline=BLACK)
    for r in (0.3, 0.42):
        d.arc([cx + s * r, cy - s * 0.5, cx + s * (r + 0.2), cy - s * 0.1], 300, 60, fill=GOLD, width=4)


CARDS = [
    ("MIDDLE EAST", RED, icon_barrel, "US–Iran strikes spread in the Gulf; oil ~$93"),
    ("EUROPE", SKY, icon_bridge, "Ukraine hits Kerch Bridge a second night"),
    ("TECHNOLOGY", GREEN, icon_chip, "Nvidia: no Huang return; revenue doubles"),
    ("CLIMATE", TEAL, icon_leaf, "COP31: phaseout draft splits climate talks"),
    ("SOUTH ASIA", ORANGE, icon_cyclone, "Cyclone Akvan: evacuations in Odisha"),
    ("JUSTICE", PURPLE, icon_scales, "ICJ: Myanmar genocide against Rohingya"),
    ("UNITED STATES", SLATE, icon_capitol, "Alaska flips; Democrats 56–44 in Senate"),
    ("SPACE", GOLD, icon_rocket, "Voyager 1: one light-day from Earth"),
]


def main():
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)

    # faint dotted world grid
    for gy in range(0, H, 46):
        for gx in range(0, W, 46):
            d.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(30, 44, 66))

    # masthead
    d.text((48, 30), "THE WORLD IN ONE DAY", font=font(BOLD, 28), fill=GOLD)
    d.text((48, 66), "Wednesday 18 November 2026", font=font(SERIFB, 50), fill=WHITE)
    d.rectangle([48, 134, W - 48, 142], fill=RED)

    # lead story panel
    ly0, ly1 = 160, 424
    d.rounded_rectangle([48, ly0, W - 48, ly1], radius=16, fill=PAPER)
    d.rectangle([48, ly0, 62, ly1], fill=RED)
    d.text((84, ly0 + 18), "LEAD STORY · DIPLOMACY", font=font(BOLD, 22), fill=RED)
    lead = "Trump, Xi and Putin hold first trilateral summit in Shenzhen"
    y = ly0 + 52
    for line in wrap(d, lead, font(BOLD, 40), 560):
        d.text((84, y), line, font=font(BOLD, 40), fill=BLACK)
        y += 48
    sub = "Xi–Putin talks open the APEC week; Ukraine, Iran and nuclear risks top the agenda"
    y += 2
    for line in wrap(d, sub, font(REG, 22), 560):
        d.text((84, y), line, font=font(REG, 22), fill=SLATE)
        y += 28
    fx, fy = 700, ly0 + 34
    flag_us(d, fx, fy, 108, 72)
    flag_cn(d, fx + 122, fy, 108, 72)
    flag_ru(d, fx + 61, fy + 86, 108, 72)
    d.text((fx + 40, fy + 168), "Shenzhen · APEC", font=font(BOLD, 20), fill=SLATE)

    # story cards, 2 rows x 4
    mx, gap = 48, 14
    cw = (W - 2 * mx - 3 * gap) // 4
    ch = 248
    y0 = 440
    for i, (tag, color, icon, head) in enumerate(CARDS):
        r, c = divmod(i, 4)
        x = mx + c * (cw + gap)
        yy = y0 + r * (ch + gap)
        d.rounded_rectangle([x, yy, x + cw, yy + ch], radius=14, fill=PAPER)
        d.rounded_rectangle([x, yy, x + cw, yy + 38], radius=14, fill=color)
        d.rectangle([x, yy + 24, x + cw, yy + 38], fill=color)
        d.text((x + 14, yy + 8), tag, font=font(BOLD, 19), fill=WHITE)
        icon(d, x + cw // 2, yy + 88, 80, color)
        ty = yy + 134
        for line in wrap(d, head, font(BOLD, 20), cw - 24):
            d.text((x + 12, ty), line, font=font(BOLD, 20), fill=BLACK)
            ty += 25

    # footer
    fy = y0 + 2 * ch + gap + 16
    d.rectangle([48, fy, W - 48, fy + 6], fill=GOLD)
    d.text((48, fy + 14), "World news summary · Wednesday 18 November 2026 · one day, every region",
           font=font(REG, 21), fill=(190, 200, 215))

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
