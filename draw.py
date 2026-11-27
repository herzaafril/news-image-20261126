#!/usr/bin/env python3
"""Draw the news-image-20261126 entry: Thursday 26 November 2026 in one image.

Deterministic PIL render, 1024x1024. Stories verified in
~/workspace/makefun/work-news26/verified-stories.md (happened or first
reported Thu 26 Nov 2026 in any timezone). 40 stories: 31 verified + 9 soft
items worded honestly per the file. No Thursday Wall Street close exists:
US markets were shut for Thanksgiving.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (31, 58, 95)
RED = (179, 35, 27)
GOLD = (201, 150, 39)
CARD = (255, 253, 248)
LINE = (120, 112, 96)
SHADOW = (222, 216, 200)

FD = "/usr/share/fonts/truetype/dejavu/"
FN = "/usr/share/fonts/truetype/noto/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_R = lambda s: font("DejaVuSans.ttf", s)
F_CB = lambda s: ImageFont.truetype(FN + "NotoSans-CondensedBold.ttf", s)
F_C = lambda s: ImageFont.truetype(FN + "NotoSans-Condensed.ttf", s)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def wrap(text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(x, y, text, fnt, maxw, fill=INK, leading=None, max_lines=99):
    leading = leading or int(fnt.size * 1.18)
    lines = wrap(text, fnt, maxw)[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def tag_chip(x, y, label, color):
    f = F_CB(11)
    tw = d.textlength(label, font=f)
    d.rounded_rectangle([x, y, x + tw + 12, y + 17], radius=4, fill=color)
    d.text((x + 6, y + 2), label, font=f, fill=(255, 255, 255))
    return x + tw + 12


def diamond(cx, cy, r, fill=GOLD):
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=fill)


def star(cx, cy, r, fill=GOLD):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)


def person(cx, base_y, hgt, skin=(240, 210, 180), suit=(45, 50, 70)):
    """Small standing figure: head + body, base_y = feet."""
    hr = max(3, hgt // 6)
    d.ellipse([cx - hr, base_y - hgt, cx + hr, base_y - hgt + 2 * hr], fill=skin)
    d.polygon([(cx - hr - 2, base_y), (cx - hr, base_y - hgt + 2 * hr),
               (cx + hr, base_y - hgt + 2 * hr), (cx + hr + 2, base_y)], fill=suit)


# ---------------------------------------------------------------- masthead
title = "THE WORLD IN ONE DAY"
tf = F_SERIF_B(34)
tw = d.textlength(title, font=tf)
d.text((W // 2, 6), title, font=tf, fill=INK, anchor="ma")
# flanking rules + diamonds at title mid-height
ty = 24
d.line([(16, ty), (W // 2 - tw / 2 - 26, ty)], fill=NAVY, width=2)
d.line([(W // 2 + tw / 2 + 26, ty), (W - 16, ty)], fill=NAVY, width=2)
diamond(24, ty, 5)
diamond(W - 24, ty, 5)
star(W // 2 - tw / 2 - 16, ty, 6)
star(W // 2 + tw / 2 + 16, ty, 6)
d.text((W // 2, 42), "THURSDAY 26 NOVEMBER 2026", font=F_B(26), fill=RED, anchor="ma")
d.line([(16, 74), (W - 16, 74)], fill=INK, width=2)
d.line([(16, 78), (W - 16, 78)], fill=INK, width=1)
diamond(W // 2, 76, 4, fill=RED)
stats = "40 dated stories  ·  7 regions  ·  timeline in UTC below  ·  Thanksgiving Day — US markets CLOSED (no Thursday Wall Street close)"
d.text((W // 2, 82), stats, font=F_CB(12), fill=NAVY, anchor="ma")

# ---------------------------------------------------------------- timeline
TY = 118
d.line([(30, TY), (W - 30, TY)], fill=NAVY, width=2)
anchors = [
    ("00:20", "Ibiza tanker sinks"),
    ("01:43", "Bank of Korea +25bp"),
    ("03:17", "Flinders Is. fire"),
    ("06:00", "Kyiv drone tally"),
    ("07:45", "Bangkok blast"),
    ("12:10", "ISS robot docks"),
    ("16:11", "Mexico–SpaceX talks"),
    ("17:00", "Paris bowl auction"),
    ("evening", "US storm + NFL"),
]
for i, (t, lab) in enumerate(anchors):
    x = 46 + i * (W - 92) // (len(anchors) - 1)
    d.line([(x, TY - 5), (x, TY + 5)], fill=NAVY, width=2)
    d.ellipse([x - 4, TY - 4, x + 4, TY + 4], fill=RED)
    d.text((x, TY - 22), t, font=F_CB(11), fill=INK, anchor="ma")
    ly = TY + 7 if i % 2 == 0 else TY + 21
    d.text((x, ly), lab, font=F_C(10), fill=NAVY, anchor="ma")

# ---------------------------------------------------------------- scenes
def scene_eu(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 32, 96))
    # chandelier glints (kept clear of the stamp corner)
    for i in range(4):
        gx = x + 96 + i * (w - 130) // 3
        star(gx, y + 9, 3, fill=(255, 230, 150))
    # red NO DEAL stamp, top-left
    d.rounded_rectangle([x + 6, y + 5, x + 62, y + 21], radius=3, outline=(255, 90, 80), width=2)
    d.text((x + 34, y + 7), "NO DEAL", font=F_CB(11), fill=(255, 90, 80), anchor="ma")
    cx, cy, r = x + w // 2, y + h // 2 - 8, min(w, h) // 3 - 2
    for k in range(12):
        a = 2 * math.pi * k / 12
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        star(sx, sy, 6, fill=(255, 204, 0))
    d.text((cx, cy - 8), "€", font=F_B(16), fill=(255, 230, 150), anchor="ma")
    # summit table with papers + seated leaders
    tyy = y + h - 20
    d.rectangle([x + 10, tyy, x + w - 10, tyy + 10], fill=(110, 72, 36))
    d.rectangle([x + 10, tyy + 10, x + w - 10, tyy + 13], fill=(80, 52, 26))
    for i in range(7):
        hx = x + 26 + i * (w - 52) // 6
        person(hx, tyy + 2, 22, suit=(40 + (i % 3) * 12, 45, 75))
        px = hx - 7
        d.rectangle([px, tyy + 2, px + 14, tyy + 8], fill=(245, 245, 240))
        d.line([(px + 2, tyy + 5), (px + 12, tyy + 5)], fill=RED, width=1)


def scene_refinery(x, y, w, h, fire=True, blast=False):
    d.rectangle([x, y, x + w, y + h], fill=(255, 190, 120))
    d.ellipse([x + w - 34, y + 6, x + w - 14, y + 26], fill=(255, 240, 180))  # sun
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(205, 175, 120))  # sand
    d.rectangle([x, y + h - 6, x + w, y + h], fill=(150, 125, 85))
    # storage tanks
    for tx in (x + 10, x + w - 46):
        d.rectangle([tx, y + h - 44, tx + 34, y + h - 18], fill=(215, 215, 220), outline=(120, 120, 130))
        d.ellipse([tx, y + h - 50, tx + 34, y + h - 38], fill=(225, 225, 230), outline=(120, 120, 130))
        d.line([(tx, y + h - 31), (tx + 34, y + h - 31)], fill=(150, 150, 160), width=1)
    # towers + pipes
    for i, tw_ in enumerate((16, 12, 20, 10)):
        tx = x + 52 + i * ((w - 104) // 4)
        d.rectangle([tx, y + 24, tx + tw_, y + h - 18], fill=(70, 70, 80))
        d.rectangle([tx - 3, y + 18, tx + tw_ + 3, y + 26], fill=(50, 50, 60))
        for ly in range(y + 32, y + h - 24, 9):
            d.line([(tx + 2, ly), (tx + tw_ - 2, ly)], fill=(110, 110, 120), width=1)
    d.rectangle([x + 52, y + h - 34, x + w - 52, y + h - 30], fill=(90, 90, 100))
    if fire:
        fx, fy = x + w // 2, y + 28
        d.polygon([(fx - 18, fy + 28), (fx, fy - 16), (fx + 18, fy + 28)], fill=(210, 60, 15))
        d.polygon([(fx - 12, fy + 26), (fx, fy - 6), (fx + 12, fy + 26)], fill=(240, 110, 20))
        d.polygon([(fx - 6, fy + 24), (fx, fy + 4), (fx + 6, fy + 24)], fill=(255, 190, 50))
        for i in range(5):
            sx = fx + 8 + i * 11
            sy = fy - 20 - i * 6
            d.ellipse([sx, sy, sx + 18 - i, sy + 12 - i], fill=(105, 105, 105))
        if blast:
            for rr in (26, 36):
                d.ellipse([fx - rr, fy - rr // 2, fx + rr, fy + rr // 2], outline=(255, 240, 200), width=2)
            for dx, dy in ((-30, -8), (28, -14), (-22, 6), (24, 4), (0, -26)):
                d.ellipse([fx + dx - 2, fy + dy - 2, fx + dx + 2, fy + dy + 2], fill=(80, 60, 40))
    # worker with hard hat by the fence
    wx = x + 30
    person(wx, y + h - 8, 20, suit=(230, 120, 30))
    d.rectangle([wx - 5, y + h - 29, wx + 5, y + h - 25], fill=(255, 210, 40))
    d.line([(x + 4, y + h - 12), (x + w - 4, y + h - 12)], fill=(90, 75, 50), width=1)


def scene_bank(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 228, 245))
    for cx0, cy0 in ((x + 26, y + 12), (x + w - 70, y + 10)):
        d.ellipse([cx0, cy0, cx0 + 34, cy0 + 12], fill=(255, 255, 255))
        d.ellipse([cx0 + 8, cy0 - 5, cx0 + 26, cy0 + 7], fill=(255, 255, 255))
    bx, by = x + 12, y + h - 16
    bw = w - 24
    d.rectangle([bx, by - 36, bx + bw, by], fill=(240, 238, 230), outline=NAVY)
    d.polygon([(bx - 4, by - 36), (bx + bw // 2, by - 50), (bx + bw + 4, by - 36)], fill=NAVY)
    # flag on the pediment
    fx = bx + bw // 2
    d.line([(fx, by - 50), (fx, by - 62)], fill=(80, 80, 80), width=2)
    d.rectangle([fx, by - 62, fx + 13, by - 54], fill=(255, 255, 255), outline=(150, 150, 150))
    d.pieslice([fx + 3, by - 61, fx + 10, by - 55], 180, 360, fill=(205, 40, 50))
    d.pieslice([fx + 3, by - 61, fx + 10, by - 55], 0, 180, fill=(40, 70, 160))
    for i in range(5):
        cx = bx + 12 + i * (bw - 31) // 4
        d.rectangle([cx, by - 34, cx + 7, by - 4], fill=(165, 163, 152))
    d.rectangle([bx + bw // 2 - 6, by - 20, bx + bw // 2 + 6, by], fill=(90, 80, 60))  # door
    d.rectangle([bx - 4, by, bx + bw + 4, by + 5], fill=(150, 148, 138))
    # rising rate chart with grid
    gx0, gy0 = x + w - 96, y + 16
    for i in range(4):
        d.line([(gx0, gy0 + i * 12), (gx0 + 78, gy0 + i * 12)], fill=(170, 195, 220), width=1)
    pts = [(gx0, gy0 + 44), (gx0 + 24, gy0 + 30), (gx0 + 44, gy0 + 34), (gx0 + 72, gy0 + 12)]
    d.line(pts, fill=RED, width=3)
    d.polygon([(pts[-1][0] - 7, pts[-1][1] + 4), (pts[-1][0] + 3, pts[-1][1] - 4), (pts[-1][0] + 2, pts[-1][1] + 8)], fill=RED)
    d.text((x + w - 10, y + 2), "3.25%", font=F_B(17), fill=RED, anchor="ra")
    # coin stacks
    for sx, n in ((x + w - 30, 3), (x + w - 16, 2)):
        for i in range(n):
            d.ellipse([sx, y + h - 10 - i * 4, sx + 12, y + h - 4 - i * 4], fill=(240, 200, 80), outline=(180, 140, 40))


def scene_storm(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(140, 162, 190))
    for cx0, cy0, cw0 in ((x + 6, y + 2, 70), (x + w - 84, y + 0, 78), (x + w // 2 - 34, y + 6, 66)):
        d.ellipse([cx0, cy0, cx0 + cw0, cy0 + 18], fill=(105, 122, 150))
        d.ellipse([cx0 + 12, cy0 - 4, cx0 + cw0 - 14, cy0 + 10], fill=(120, 138, 165))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(240, 244, 248))
    # tilted power pole + broken wire + spark
    px = x + 16
    d.line([(px, y + h - 14), (px + 10, y + 14)], fill=(60, 55, 50), width=4)
    d.line([(px + 4, y + 20), (px + 20, y + 24)], fill=(60, 55, 50), width=3)
    d.line([(px + 18, y + 23), (x + w - 24, y + 34)], fill=(40, 40, 40), width=2)
    d.line([(x + w - 44, y + 31), (x + w - 38, y + h - 22)], fill=(40, 40, 40), width=2)
    star(x + w - 41, y + h - 24, 5, fill=(255, 220, 60))
    # bent tree
    tx = x + w // 2 - 6
    d.line([(tx, y + h - 14), (tx + 8, y + h // 2)], fill=(80, 60, 40), width=5)
    for i in range(5):
        d.line([(tx + 8, y + h // 2), (tx + 34 + i * 2, y + 6 + i * 4)], fill=(55, 85, 55), width=3)
    # house with snow roof
    hx = x + w - 52
    d.rectangle([hx, y + h - 34, hx + 34, y + h - 14], fill=(200, 120, 90))
    d.polygon([(hx - 3, y + h - 34), (hx + 17, y + h - 46), (hx + 37, y + h - 34)], fill=(250, 250, 250))
    d.rectangle([hx + 6, y + h - 28, hx + 14, y + h - 20], fill=(255, 220, 120))
    d.rectangle([hx + 20, y + h - 26, hx + 28, y + h - 14], fill=(90, 60, 40))
    # wind-driven rain streaks
    for i in range(9):
        sx = x + 8 + i * (w - 16) // 9
        sy = y + 16 + (i % 3) * 12
        d.line([(sx, sy), (sx + 16, sy - 6)], fill=(230, 240, 250), width=2)


def scene_barrage(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(25, 30, 55))
    # moon
    d.ellipse([x + w - 30, y + 6, x + w - 12, y + 24], fill=(240, 235, 200))
    d.ellipse([x + w - 36, y + 4, x + w - 20, y + 22], fill=(25, 30, 55))
    # searchlight beams
    d.polygon([(x + 14, y + h - 4), (x + 52, y + 8), (x + 66, y + 12)], fill=(70, 80, 110))
    d.polygon([(x + w - 16, y + h - 4), (x + w - 58, y + 10), (x + w - 44, y + 6)], fill=(70, 80, 110))
    for i in range(6):
        bx = x + 8 + i * (w // 6)
        bh = 24 + (i * 7) % 20
        d.rectangle([bx, y + h - bh, bx + w // 7, y + h], fill=(45, 50, 80))
        for wy in range(y + h - bh + 5, y + h - 6, 9):
            for wx in (bx + 4, bx + 10):
                if (wx + wy) % 3:
                    d.rectangle([wx, wy, wx + 4, wy + 4], fill=(255, 220, 120))
    # ground explosion glow
    ex, ey = x + w // 2 - 10, y + h - 10
    d.ellipse([ex - 16, ey - 8, ex + 16, ey + 6], fill=(240, 120, 30))
    d.ellipse([ex - 8, ey - 12, ex + 8, ey + 4], fill=(255, 190, 60))
    for i in range(4):
        dx, dy = x + 20 + i * (w // 4), y + 12 + (i % 2) * 10
        d.ellipse([dx - 5, dy - 3, dx + 5, dy + 3], fill=(200, 200, 210))
        d.ellipse([dx - 2, dy - 1, dx + 2, dy + 1], fill=(255, 60, 50))
        d.line([(dx, dy + 3), (dx - 12, dy + 16)], fill=(255, 150, 60), width=2)


def scene_ebola(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(230, 240, 225))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(195, 170, 130))
    # tree
    d.rectangle([x + w - 22, y + h - 30, x + w - 18, y + h - 12], fill=(100, 75, 45))
    d.ellipse([x + w - 36, y + h - 52, x + w - 4, y + h - 26], fill=(90, 140, 80))
    # two clinic tents
    for tx, tw_ in ((x + 8, 58), (x + 74, 48)):
        ty = y + h - 12
        d.polygon([(tx, ty), (tx + tw_ // 2, ty - 30), (tx + tw_, ty)], fill=(250, 250, 250), outline=RED)
        d.rectangle([tx + tw_ // 2 - 3, ty - 22, tx + tw_ // 2 + 3, ty - 8], fill=RED)
        d.rectangle([tx + tw_ // 2 - 7, ty - 18, tx + tw_ // 2 + 7, ty - 12], fill=RED)
    # red-cross flag
    fx = x + 66
    d.line([(fx, y + h - 12), (fx, y + 8)], fill=(90, 90, 90), width=2)
    d.rectangle([fx, y + 8, fx + 20, y + 20], fill=(255, 255, 255), outline=(180, 180, 180))
    d.rectangle([fx + 8, y + 10, fx + 12, y + 18], fill=RED)
    d.rectangle([fx + 5, y + 12, fx + 15, y + 16], fill=RED)
    # medic in PPE + patient queue
    person(x + 96, y + h - 12, 22, suit=(245, 220, 120))
    d.rectangle([x + 92, y + h - 34, x + 100, y + h - 30], fill=(255, 255, 255))
    for i, px in enumerate((x + 116, x + 130, x + 144)):
        person(px, y + h - 12, 18 - i, suit=(90 + i * 30, 90, 130))


def scene_iss(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 16, 40))
    for sx, sy in ((x + 12, y + 10), (x + w - 20, y + 14), (x + 30, y + 26), (x + w - 36, y + 30),
                   (x + 52, y + 8), (x + w - 58, y + 22), (x + 8, y + 30)):
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    star(x + w - 14, y + 10, 5, fill=(255, 240, 180))
    # Earth curve with land patches
    d.ellipse([x - 10, y + h - 16, x + w + 10, y + h + 14], fill=(50, 110, 200))
    d.ellipse([x + 30, y + h - 13, x + 70, y + h - 4], fill=(90, 160, 100))
    d.ellipse([x + w - 80, y + h - 12, x + w - 40, y + h - 3], fill=(90, 160, 100))
    d.arc([x - 10, y + h - 16, x + w + 10, y + h + 14], 180, 360, fill=(140, 200, 255), width=2)
    cx, cy = x + w // 2, y + h // 2 - 10
    # truss + solar arrays with grid
    d.line([(cx - 58, cy), (cx + 58, cy)], fill=(180, 185, 195), width=3)
    for px0 in (cx - 58, cx + 14):
        d.rectangle([px0, cy - 13, px0 + 44, cy + 13], fill=(60, 90, 180), outline=(150, 180, 230))
        for gx in range(px0 + 11, px0 + 44, 11):
            d.line([(gx, cy - 13), (gx, cy + 13)], fill=(120, 155, 220), width=1)
        d.line([(px0, cy), (px0 + 44, cy)], fill=(120, 155, 220), width=1)
    d.rectangle([cx - 10, cy - 7, cx + 10, cy + 7], fill=(220, 220, 225))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(90, 160, 220))
    # docked Progress capsule
    d.polygon([(cx - 7, cy + 7), (cx + 7, cy + 7), (cx + 4, cy + 18), (cx - 4, cy + 18)], fill=(200, 200, 210))
    d.rectangle([cx - 5, cy + 18, cx + 5, cy + 24], fill=(170, 170, 185))
    # two-armed robot: shoulder, upper arm, elbow, forearm, gripper
    d.line([(cx + 10, cy + 4), (cx + 26, cy + 14)], fill=(230, 230, 235), width=4)
    d.ellipse([cx + 23, cy + 11, cx + 29, cy + 17], fill=(240, 200, 90))
    d.line([(cx + 26, cy + 14), (cx + 22, cy + 28)], fill=(230, 230, 235), width=4)
    d.line([(cx + 22, cy + 28), (cx + 18, cy + 33)], fill=(240, 200, 90), width=2)
    d.line([(cx + 22, cy + 28), (cx + 26, cy + 33)], fill=(240, 200, 90), width=2)


TAG_COLORS = {"OFFICIAL": NAVY, "CONFIRMED": (30, 110, 60), "REPORTED": (120, 90, 20), "CLAIM": (150, 60, 120)}

leads = [
    (scene_eu, "1. EU SUMMIT DEADLOCK", "Leaders fail to agree €1.58tn budget + €45bn Ukraine loan; next summit 17–18 Dec.", "OFFICIAL", "Reuters/AP"),
    (scene_refinery, "2. JAZAN REFINERY HIT", "Projectile hits Aramco refinery; Nepali worker killed; Riyadh says 50 targets struck.", "CONFIRMED", "Reuters"),
    (scene_bank, "3. BANK OF KOREA +25BP TO 3.25%", "5–2 vote, highest since 2024; 2026 growth forecast lifted to 3.9%.", "OFFICIAL", "BOK"),
]

tier2 = [
    (scene_storm, "4. US THANKSGIVING NOR'EASTER", ">960,000 without power; 2,300+ flights delayed, 451 cancelled.", "REPORTED", "AP"),
    (lambda x, y, w, h: scene_refinery(x, y, w, h, True, True), "5. BANGKOK REFINERY BLAST", "Bangchak explosion injures 9, three critically; fire out in ~30 min.", "CONFIRMED", "AP/AFP"),
    (scene_barrage, "6. RUSSIA BARRAGE: KYIV + KHARKIV", "113 drones overnight, 87 downed; 2 killed Kharkiv, 7 wounded Kyiv.", "REPORTED", "Reuters"),
    (scene_ebola, "7. DR CONGO EBOLA >12,000", "12,021 cases, 5,904 dead; 2nd-largest outbreak on record.", "OFFICIAL", "AP/Reuters"),
    (scene_iss, "8. TELEDROID DOCKS AT ISS", "Progress MS-36 arrives with two-armed robot + 2.4t cargo.", "CONFIRMED", "NASA/TASS"),
]

LY = 152
cw = (W - 32 - 2 * 10) // 3
for i, (sc, head, summ, tg, src) in enumerate(leads):
    x = 16 + i * (cw + 10)
    d.rounded_rectangle([x + 3, LY + 3, x + cw + 3, LY + 175], radius=8, fill=SHADOW)
    d.rounded_rectangle([x, LY, x + cw, LY + 172], radius=8, fill=CARD, outline=LINE)
    sc(x + 6, LY + 6, cw - 12, 78)
    yy = text_block(x + 10, LY + 90, head, F_CB(15), cw - 20, max_lines=2)
    yy = text_block(x + 10, yy + 1, summ, F_C(12), cw - 20, max_lines=2)
    ex = tag_chip(x + 10, LY + 148, tg, TAG_COLORS[tg])
    d.text((ex + 6, LY + 151), src, font=F_C(11), fill=NAVY)

TY2 = 332
cw2 = (W - 32 - 4 * 8) // 5
for i, (sc, head, summ, tg, src) in enumerate(tier2):
    x = 16 + i * (cw2 + 8)
    d.rounded_rectangle([x + 3, TY2 + 3, x + cw2 + 3, TY2 + 151], radius=8, fill=SHADOW)
    d.rounded_rectangle([x, TY2, x + cw2, TY2 + 148], radius=8, fill=CARD, outline=LINE)
    sc(x + 5, TY2 + 5, cw2 - 10, 54)
    yy = text_block(x + 8, TY2 + 63, head, F_CB(12), cw2 - 16, max_lines=3)
    yy = text_block(x + 8, yy + 1, summ, F_C(10), cw2 - 16, max_lines=3)
    ex = tag_chip(x + 8, TY2 + 126, tg, TAG_COLORS[tg])
    d.text((ex + 5, TY2 + 129), src, font=F_C(10), fill=NAVY)

# ---------------------------------------------------------------- map band
MY = 488
d.rounded_rectangle([19, MY + 3, 659, MY + 137], radius=8, fill=SHADOW)
d.rounded_rectangle([16, MY, 656, MY + 134], radius=8, fill=(215, 230, 245), outline=LINE)
MX0, MY0, MW, MH = 20, MY + 4, 632, 126


def proj(lon, lat, x0=MX0, y0=MY0, w=MW, h=MH, lonr=(-180, 180), latr=(-60, 85)):
    return (x0 + (lon - lonr[0]) / (lonr[1] - lonr[0]) * w,
            y0 + (latr[1] - lat) / (latr[1] - latr[0]) * h)


# graticule (drawn first; land covers it, grid shows over oceans)
GRID = (180, 205, 230)
for lon in range(-150, 181, 30):
    gx, _ = proj(lon, 0)
    d.line([(gx, MY0), (gx, MY0 + MH)], fill=GRID, width=1)
for lat in range(-60, 86, 30):
    _, gy = proj(0, lat)
    if lat == 0:
        for sx in range(int(MX0), int(MX0 + MW), 10):
            d.line([(sx, gy), (sx + 5, gy)], fill=(150, 180, 215), width=1)
    else:
        d.line([(MX0, gy), (MX0 + MW, gy)], fill=GRID, width=1)

LAND = (120, 170, 110)
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 70), (-85, 66), (-80, 62), (-78, 58), (-65, 50), (-55, 47), (-60, 45), (-70, 42), (-74, 39), (-76, 35), (-80, 32), (-81, 25), (-84, 30), (-89, 29), (-94, 29), (-97, 26), (-97, 22), (-94, 18), (-90, 15), (-83, 9), (-79, 9), (-77, 7), (-80, 8), (-84, 12), (-87, 14), (-92, 15), (-97, 16), (-102, 18), (-105, 20), (-110, 23), (-114, 29), (-117, 33), (-122, 37), (-124, 42), (-124, 47), (-128, 51), (-133, 56), (-145, 60), (-155, 59), (-162, 61)],
    [(-77, 7), (-75, 10), (-72, 12), (-64, 10), (-60, 8), (-52, 5), (-50, 0), (-44, -3), (-35, -8), (-39, -13), (-40, -21), (-48, -26), (-52, -32), (-58, -38), (-62, -41), (-65, -45), (-67, -50), (-68, -54), (-71, -54), (-73, -50), (-74, -44), (-73, -37), (-71, -30), (-70, -20), (-70, -18), (-75, -15), (-79, -8), (-81, -4), (-80, 1), (-77, 4)],
    [(-9, 37), (-9, 43), (-2, 44), (-4, 48), (-1, 50), (1, 51), (5, 53), (8, 55), (10, 57), (18, 56), (24, 59), (30, 60), (28, 66), (32, 70), (45, 68), (60, 69), (75, 73), (90, 75), (105, 77), (120, 73), (135, 72), (150, 70), (165, 69), (178, 66), (178, 64), (170, 60), (162, 58), (158, 52), (156, 50), (150, 45), (142, 42), (140, 38), (135, 35), (129, 33), (122, 31), (120, 26), (114, 22), (108, 18), (109, 13), (106, 9), (103, 7), (100, 8), (98, 10), (97, 15), (94, 17), (92, 16), (89, 22), (86, 20), (80, 13), (77, 8), (73, 20), (70, 22), (66, 25), (61, 25), (57, 26), (52, 26), (50, 29), (48, 30), (47, 28), (44, 29), (43, 12), (40, 15), (38, 22), (35, 28), (34, 31), (36, 36), (30, 36), (27, 37), (23, 36), (19, 40), (12, 44), (8, 44), (3, 43), (3, 42), (0, 39), (-2, 37), (-6, 36)],
    [(-6, 35), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (35, 28), (37, 22), (38, 20), (40, 15), (43, 12), (48, 11), (51, 12), (51, 10), (48, 5), (42, -2), (40, -8), (38, -18), (36, -22), (33, -26), (31, -29), (28, -33), (20, -35), (17, -32), (14, -22), (12, -18), (13, -12), (9, -1), (9, 4), (6, 5), (3, 6), (-2, 5), (-8, 4), (-13, 8), (-17, 12), (-17, 15), (-16, 20), (-16, 24), (-15, 27), (-10, 29), (-9, 31)],
    [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (129, -32), (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (147, -38), (150, -37), (153, -32), (153, -27), (151, -24), (149, -20), (146, -19), (142, -11), (142, -14), (141, -17), (136, -15), (135, -12), (132, -11), (126, -14), (122, -17), (118, -20)],
    [(-45, 60), (-40, 63), (-32, 68), (-22, 70), (-20, 74), (-22, 77), (-30, 80), (-45, 80), (-55, 76), (-58, 70), (-55, 64), (-53, 60)],
    [(-5, 50), (-3, 53), (-5, 55), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (142, 44), (140, 43), (138, 38), (135, 34), (131, 32)],
    [(167, -45), (171, -42), (173, -39), (176, -37), (178, -37), (176, -40), (174, -41), (172, -43), (168, -46)],
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -9), (125, -9), (130, -3), (135, -2), (140, -3), (145, -5), (147, -7), (142, -8), (137, -7), (132, -4), (127, -8), (120, -10), (113, -10), (105, -8), (98, -2)],
]
for poly in CONTINENTS:
    d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND)

# compass rose over the empty South Pacific
ccx, ccy = proj(-148, -32)
d.ellipse([ccx - 15, ccy - 15, ccx + 15, ccy + 15], outline=NAVY, width=1)
for k in range(8):
    a = k * math.pi / 4
    rr = 14 if k % 2 == 0 else 8
    d.polygon([(ccx, ccy), (ccx + rr * math.cos(a - 0.18), ccy + rr * math.sin(a - 0.18)),
               (ccx + rr * math.cos(a), ccy + rr * math.sin(a)),
               (ccx + rr * math.cos(a + 0.18), ccy + rr * math.sin(a + 0.18))],
              fill=NAVY if k % 2 == 0 else (140, 170, 210))
d.text((ccx, ccy - 24), "N", font=F_CB(9), fill=NAVY, anchor="ma")

PINS = [(1, 4.35, 50.85), (2, 42.6, 16.9), (3, 127, 37.6), (4, -74, 40.7), (5, 100.5, 13.8),
        (6, 30.5, 50.4), (7, 23, -2), (10, -0.1, 51.5), (11, 19.4, 51.8), (13, 2.35, 48.85), (14, 1.4, 38.9)]
for n, lon, lat in PINS:
    px, py = proj(lon, lat)
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
    d.text((px, py - 6), str(n), font=F_CB(9), fill=(255, 255, 255), anchor="ma")
px, py = proj(150, 78)
d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=NAVY, outline=(255, 255, 255), width=1)
d.text((px, py - 6), "8", font=F_CB(9), fill=(255, 255, 255), anchor="ma")
d.text((px, py + 10), "ISS", font=F_CB(9), fill=NAVY, anchor="ma")
d.text((MX0 + 4, MY0 + 2), "WORLD MAP — pins = stories 1–8, 10, 11, 13, 14", font=F_CB(10), fill=NAVY)

# Europe inset
IX, IY, IW, IH = 470, MY + 48, 180, 80
d.rounded_rectangle([IX, IY, IX + IW, IY + IH], radius=6, fill=(225, 238, 250), outline=NAVY)
EU = [(-9, 37), (-9, 43), (-2, 44), (-4, 48), (-1, 50), (1, 51), (5, 53), (8, 55), (10, 57), (18, 56), (24, 59), (30, 60), (28, 66), (32, 62), (30, 55), (28, 50), (30, 46), (28, 41), (23, 36), (19, 40), (12, 44), (8, 44), (3, 43), (3, 42), (0, 39), (-2, 37), (-6, 36)]
d.polygon([proj(lon, lat, IX + 3, IY + 14, IW - 6, IH - 17, (-12, 32), (36, 62)) for lon, lat in EU], fill=LAND)
d.polygon([proj(lon, lat, IX + 3, IY + 14, IW - 6, IH - 17, (-12, 32), (36, 62)) for lon, lat in [(-5, 50), (-3, 53), (-5, 55), (-3, 58), (-1, 57), (0, 53), (1, 51)]], fill=LAND)
for n, lon, lat in [(1, 4.35, 50.85), (6, 30.5, 50.4), (10, -0.1, 51.5), (11, 19.4, 51.8), (13, 2.35, 48.85), (14, 1.4, 38.9)]:
    px, py = proj(lon, lat, IX + 3, IY + 14, IW - 6, IH - 17, (-12, 32), (36, 62))
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=1)
    d.text((px, py - 5), str(n), font=F_CB(8), fill=(255, 255, 255), anchor="ma")
d.text((IX + 5, IY + 2), "EUROPE ZOOM", font=F_CB(9), fill=NAVY)

# region key
KX = 666
d.rounded_rectangle([KX + 3, MY + 3, W - 13, MY + 137], radius=8, fill=SHADOW)
d.rounded_rectangle([KX, MY, W - 16, MY + 134], radius=8, fill=CARD, outline=LINE)
d.text((KX + 10, MY + 6), "REGIONS (40 stories)", font=F_CB(13), fill=NAVY)
regions = [("Europe", 10), ("Asia", 12), ("Americas", 6), ("Africa", 5), ("Middle East", 5), ("Oceania", 1), ("Global/Space", 1)]
ry = MY + 26
for name, cnt in regions:
    d.text((KX + 10, ry), name, font=F_C(12), fill=INK)
    d.text((W - 26, ry), str(cnt), font=F_CB(12), fill=RED, anchor="ra")
    ry += 13
d.text((KX + 10, ry + 2), "Tags: CONFIRMED / OFFICIAL / REPORTED / CLAIM", font=F_C(10), fill=NAVY)

# ---------------------------------------------------------------- list
LIST = [
    (9, "ECB chief: Hernández de Cos picked", "Reuters/AP"),
    (10, "UK net migration 77,000 — lowest since 1997", "ONS"),
    (11, "Poland takes two more F-35s — 12 in country", "Defence24"),
    (12, "UK train attacker guilty of 14 attempted murders", "CPS"),
    (13, "Depardieu ordered to stand trial for rape", "Reuters/AP"),
    (14, "Marie-Antoinette bowl sells for €2.9m in Paris", "France 24"),
    (15, "Diesel tanker sinks off Ibiza — 1 dead, 17 rescued", "Reuters"),
    (16, "Serbia presidential vote set for 27 Dec", "Reuters"),
    (17, "Two Italians killed in Kuwait drone strike", "Reuters/ANSA"),
    (18, "Israel kills Hamas official Abu Nada in Deir al-Balah", "Reuters"),
    (19, "Nvidia halts AI server shipments to 4 SE Asian nations", "FT"),
    (20, "Chess Game 3 drawn — Gukesh–Sindarov 1.5–1.5", "Chess.com"),
    (21, "India marks 18 years since 26/11 Mumbai attacks", "IANS"),
    (22, "Hong Kong marks 1st anniversary of Wang Fuk Court fire", "AP"),
    (23, "Beijing golf clampdown: 18+ courses closing", "AFP"),
    (24, "Bangladesh factories stay shut Thu after Wed wage rise", "Reuters"),
    (25, "Guinea-Bissau junta delays election to 2028", "Reuters/AP"),
    (26, "Sudan army says it downed FH-95 drone west of Kadugli", "SUNA"),
    (27, "Driver arrested Thu over Wed Cairo fire that killed 31", "AP"),
    (28, "Flinders Island fire >14,000 ha by Thu; 6 properties hit", "AAP"),
    (29, "Argentina Senate suspends PASO primaries 43–29", "Reuters"),
    (30, "Mexico seeks US talks on SpaceX debris/airspace", "Reuters"),
    (31, "NFL Thanksgiving: Bears 39–35 Lions", "Sports Illustrated"),
    (32, "Macy's 100th parade postponed — Wed decision, moved to Sat", "AP"),
    (33, "Iran says Thu two more tankers hit mines at Hormuz (CLAIM)", "Tasnim"),
    (34, "Kim Jong Un nuclear tour Wed, reported Thu", "KCNA/Reuters"),
    (35, "Phala Phala: parties say Thu they will appeal Wed ruling", "Business Day"),
    (36, "Myanmar defies ICJ Rohingya ruling (Wed remarks, reported Thu)", "Reuters"),
    (37, "Philadelphia parade cancelled Wed evening; TV special Thu", "NBC10"),
    (38, "Bogor mine rescue continues Thu; toll disputed (flooded Mon)", "AP"),
    (39, "Saudi–Turkey–Pakistan pact: ministers arrive Thu for Fri–Sat talks", "Reuters"),
    (40, "Beirut minibus drivers' shootout kills 2 Thu (local reports)", "Naharnet/LBCI"),
]
LY2 = 626
d.text((16, LY2), "ALSO ON THURSDAY", font=F_CB(13), fill=NAVY)
diamond(150, LY2 + 7, 4)
half = (len(LIST) + 1) // 2
colw = (W - 32 - 12) // 2
for ci, chunk in enumerate((LIST[:half], LIST[half:])):
    x = 16 + ci * (colw + 12)
    y = LY2 + 18
    for n, head, src in chunk:
        if (n % 2) == 0:
            d.rectangle([x - 2, y - 1, x + colw, y + 12], fill=(240, 236, 224))
        d.text((x, y), f"{n}.", font=F_CB(11), fill=RED)
        d.text((x + 24, y), head, font=F_C(11), fill=INK)
        d.text((x + colw, y), src, font=F_C(10), fill=NAVY, anchor="ra")
        y += 14
d.line([(W // 2 - 6, LY2 + 18), (W // 2 - 6, LY2 + 18 + half * 14 - 4)], fill=(205, 198, 180), width=1)

# ---------------------------------------------------------------- DATE CHECK footer
FY = 876
d.line([(16, FY), (W // 2 - 14, FY)], fill=INK, width=2)
d.line([(W // 2 + 14, FY), (W - 16, FY)], fill=INK, width=2)
diamond(W // 2, FY, 5, fill=RED)
star(16, FY + 12, 5)
d.text((28, FY + 6), "DATE CHECK — not Thursday, however often printed:", font=F_CB(13), fill=RED)
footer = ("US tariffs on 14 economies (Wed 25) · any Thursday Wall Street close (US markets shut for Thanksgiving — "
          "figures are Wednesday's) · Kospi −6.2% (Wed) · Eurostar strike (Wed) · FedEx Miami runway excursion (Wed) · "
          "jet-door incident (Wed) · Pacifica Pier collapse (Wed) · Venezuela $237.5bn debt (Tue) · FCC Starmind "
          "clearance (Wed) · NATO AWACS to Poland (Mon 23) · Hungary–Ukraine meeting (Tue) · Spain crypto-freeze "
          "decree (Wed) · Canary 1,990 arrivals (Tue) · Sinner surgery (Tue) · Guinea Conakry order (Wed) · Kuno "
          "cheetahs 62 (20 Nov) · Australia Digital Duty of Care (Wed) · NZ coalition result (Fri 27) · Cairo fire "
          "itself (Wed — Thu = driver arrested) · Bogor flood (Mon — Thu = rescue only) · Phala Phala ruling (Wed) · "
          "Kim tour (Wed) · Teledroid launch (Tue — Thu = docking).")
text_block(16, FY + 26, footer, F_C(11), W - 32, max_lines=5)
d.text((16, H - 26), "Sources beside each story. Day = events that happened, or were first reported, on Thu 26 Nov 2026 in any time zone.",
       font=F_C(11), fill=NAVY)
star(W - 24, H - 20, 5)

img.save("entry.png", "PNG", optimize=True)
print("wrote entry.png")
