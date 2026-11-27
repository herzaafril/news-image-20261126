#!/usr/bin/env python3
"""Draw the news-image-20261126 entry: Thursday 26 November 2026 in one image.

Deterministic PIL render, 1024x1024. Stories verified in
~/workspace/makefun/work-news26/verified-stories.md (happened or first
reported Thu 26 Nov 2026 in any timezone). No Thursday Wall Street close
exists: US markets were shut for Thanksgiving.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (31, 58, 95)
RED = (179, 35, 27)
GOLD = (201, 150, 39)
CARD = (255, 253, 248)
LINE = (120, 112, 96)

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


# ---------------------------------------------------------------- masthead
d.text((W // 2, 8), "THE WORLD IN ONE DAY", font=F_SERIF_B(34), fill=INK, anchor="ma")
d.text((W // 2, 46), "THURSDAY 26 NOVEMBER 2026", font=F_B(26), fill=RED, anchor="ma")
d.line([(16, 80), (W - 16, 80)], fill=INK, width=2)
stats = "36 dated stories  ·  7 regions  ·  timeline in UTC below  ·  Thanksgiving Day — US markets CLOSED (no Thursday Wall Street close)"
d.text((W // 2, 84), stats, font=F_CB(12), fill=NAVY, anchor="ma")

# ---------------------------------------------------------------- timeline
TY = 120
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
    d.ellipse([x - 4, TY - 4, x + 4, TY + 4], fill=RED)
    d.text((x, TY - 22), t, font=F_CB(11), fill=INK, anchor="ma")
    # stagger labels to avoid collisions
    ly = TY + 7 if i % 2 == 0 else TY + 21
    d.text((x, ly), lab, font=F_C(10), fill=NAVY, anchor="ma")

# ---------------------------------------------------------------- scenes
def scene_eu(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 32, 96))
    import math
    cx, cy, r = x + w // 2, y + h // 2 - 6, min(w, h) // 3
    for k in range(12):
        a = 2 * math.pi * k / 12
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 204, 0))
    d.rectangle([x + 14, y + h - 26, x + w - 14, y + h - 10], fill=(120, 80, 40))
    for i in range(7):
        hx = x + 30 + i * (w - 60) // 6
        d.ellipse([hx - 6, y + h - 42, hx + 6, y + h - 30], fill=(240, 210, 180))
    d.text((cx, y + 3), "NO DEAL", font=F_CB(12), fill=(255, 90, 80), anchor="ma")


def scene_refinery(x, y, w, h, fire=True):
    d.rectangle([x, y, x + w, y + h], fill=(255, 190, 120))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(90, 90, 90))
    for i, tw in enumerate((16, 12, 20, 10)):
        tx = x + 16 + i * (w // 4)
        d.rectangle([tx, y + 26, tx + tw, y + h - 22], fill=(70, 70, 80))
        d.rectangle([tx - 3, y + 20, tx + tw + 3, y + 28], fill=(50, 50, 60))
    if fire:
        fx, fy = x + w // 2, y + 30
        d.polygon([(fx - 16, fy + 26), (fx, fy - 14), (fx + 16, fy + 26)], fill=(230, 90, 20))
        d.polygon([(fx - 9, fy + 24), (fx, fy - 2), (fx + 9, fy + 24)], fill=(255, 180, 40))
        for i in range(4):
            d.ellipse([fx + 6 + i * 9, fy - 22 - i * 7, fx + 22 + i * 9, fy - 8 - i * 7], fill=(105, 105, 105))


def scene_bank(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 228, 245))
    bx, by = x + 14, y + h - 18
    d.rectangle([bx, by - 38, bx + w - 28, by], fill=(240, 238, 230), outline=NAVY)
    d.polygon([(bx - 4, by - 38), (bx + (w - 28) // 2, by - 52), (bx + w - 24, by - 38)], fill=NAVY)
    for i in range(5):
        cx = bx + 12 + i * (w - 52) // 4
        d.rectangle([cx, by - 36, cx + 7, by - 4], fill=(165, 163, 152))
    d.rectangle([bx - 4, by, bx + w - 24, by + 5], fill=(150, 148, 138))
    pts = [(x + w - 88, y + h - 26), (x + w - 64, y + h - 40), (x + w - 44, y + h - 36), (x + w - 20, y + h - 58)]
    d.line(pts, fill=RED, width=3)
    d.polygon([(pts[-1][0] - 7, pts[-1][1] + 4), (pts[-1][0] + 3, pts[-1][1] - 4), (pts[-1][0] + 2, pts[-1][1] + 8)], fill=RED)
    d.text((x + w - 10, y + 4), "3.25%", font=F_B(18), fill=RED, anchor="ra")


def scene_storm(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 170, 195))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(240, 244, 248))
    tx = x + w // 2 - 8
    d.rectangle([tx, y + h // 2, tx + 6, y + h - 16], fill=(80, 60, 40))
    for i in range(5):
        d.line([(tx + 3, y + h // 2), (tx - 18 + i * 9, y + 5)], fill=(60, 90, 60), width=3)
    for i in range(6):
        d.line([(x + 8 + i * 6, y + 10 + i * 8), (x + 34 + i * 6, y + 4 + i * 8)], fill=(230, 240, 250), width=2)
    px = x + 10
    d.rectangle([px, y + 18, px + 5, y + h - 16], fill=(60, 60, 60))
    d.line([(px + 2, y + 22), (x + w - 10, y + 30)], fill=(40, 40, 40), width=2)
    d.line([(x + w - 30, y + 28), (x + w - 22, y + h - 30)], fill=(40, 40, 40), width=2)


def scene_barrage(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(25, 30, 55))
    for i in range(6):
        bx = x + 8 + i * (w // 6)
        bh = 26 + (i * 7) % 20
        d.rectangle([bx, y + h - bh, bx + w // 7, y + h], fill=(45, 50, 80))
        for wy in range(y + h - bh + 5, y + h - 6, 9):
            d.rectangle([bx + 4, wy, bx + 8, wy + 4], fill=(255, 220, 120))
    for i in range(4):
        dx, dy = x + 20 + i * (w // 4), y + 12 + (i % 2) * 10
        d.ellipse([dx - 5, dy - 3, dx + 5, dy + 3], fill=(200, 200, 210))
        d.line([(dx, dy + 3), (dx - 12, dy + 16)], fill=(255, 150, 60), width=2)


def scene_ebola(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(230, 240, 225))
    tx, ty = x + w // 2 - 34, y + h - 18
    d.polygon([(tx, ty), (tx + 34, ty - 34), (tx + 68, ty)], fill=(250, 250, 250), outline=RED)
    d.rectangle([tx + 30, ty - 24, tx + 38, ty - 6], fill=RED)
    d.rectangle([tx + 25, ty - 19, tx + 43, ty - 11], fill=RED)
    hx = tx + 84
    d.ellipse([hx - 6, ty - 30, hx + 6, ty - 18], fill=(245, 220, 120))
    d.rectangle([hx - 7, ty - 18, hx + 7, ty], fill=(245, 220, 120))


def scene_iss(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 16, 40))
    d.ellipse([x + 4, y + h - 14, x + w - 4, y + h + 2], fill=(50, 110, 200))
    cx, cy = x + w // 2, y + h // 2 - 8
    d.rectangle([cx - 8, cy - 6, cx + 8, cy + 6], fill=(220, 220, 225))
    d.rectangle([cx - 52, cy - 12, cx - 12, cy + 12], fill=(60, 90, 180))
    d.rectangle([cx + 12, cy - 12, cx + 52, cy + 12], fill=(60, 90, 180))
    d.line([(cx, cy + 6), (cx + 18, cy + 22)], fill=(220, 220, 225), width=4)
    d.ellipse([cx + 14, cy + 18, cx + 24, cy + 28], fill=(240, 200, 90))
    for sx, sy in ((x + 12, y + 10), (x + w - 20, y + 14), (x + 30, y + 26), (x + w - 36, y + 30)):
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))


TAG_COLORS = {"OFFICIAL": NAVY, "CONFIRMED": (30, 110, 60), "REPORTED": (120, 90, 20), "CLAIM": (150, 60, 120)}

leads = [
    (scene_eu, "1. EU SUMMIT DEADLOCK", "Leaders fail to agree €1.58tn budget + €45bn Ukraine loan; next summit 17–18 Dec.", "OFFICIAL", "Reuters/AP"),
    (scene_refinery, "2. JAZAN REFINERY HIT", "Projectile hits Aramco refinery; Nepali worker killed; Riyadh says 50 targets struck.", "CONFIRMED", "Reuters"),
    (scene_bank, "3. BANK OF KOREA +25BP TO 3.25%", "5–2 vote, highest since 2024; 2026 growth forecast lifted to 3.9%.", "OFFICIAL", "BOK"),
]

tier2 = [
    (scene_storm, "4. US THANKSGIVING NOR'EASTER", ">960,000 without power; 2,300+ flights delayed, 451 cancelled.", "REPORTED", "AP"),
    (lambda x, y, w, h: scene_refinery(x, y, w, h, True), "5. BANGKOK REFINERY BLAST", "Bangchak explosion injures 9, three critically; fire out in ~30 min.", "CONFIRMED", "AP/AFP"),
    (scene_barrage, "6. RUSSIA BARRAGE: KYIV + KHARKIV", "113 drones overnight, 87 downed; 2 killed Kharkiv, 7 wounded Kyiv.", "REPORTED", "Reuters"),
    (scene_ebola, "7. DR CONGO EBOLA >12,000", "12,021 cases, 5,904 dead; 2nd-largest outbreak on record.", "OFFICIAL", "AP/Reuters"),
    (scene_iss, "8. TELEDROID DOCKS AT ISS", "Progress MS-36 arrives with two-armed robot + 2.4t cargo.", "CONFIRMED", "NASA/TASS"),
]

LY = 156
cw = (W - 32 - 2 * 10) // 3
for i, (sc, head, summ, tg, src) in enumerate(leads):
    x = 16 + i * (cw + 10)
    d.rounded_rectangle([x, LY, x + cw, LY + 172], radius=8, fill=CARD, outline=LINE)
    sc(x + 6, LY + 6, cw - 12, 78)
    yy = text_block(x + 10, LY + 90, head, F_CB(15), cw - 20, max_lines=2)
    yy = text_block(x + 10, yy + 1, summ, F_C(12), cw - 20, max_lines=2)
    ex = tag_chip(x + 10, LY + 148, tg, TAG_COLORS[tg])
    d.text((ex + 6, LY + 151), src, font=F_C(11), fill=NAVY)

TY2 = 338
cw2 = (W - 32 - 4 * 8) // 5
for i, (sc, head, summ, tg, src) in enumerate(tier2):
    x = 16 + i * (cw2 + 8)
    d.rounded_rectangle([x, TY2, x + cw2, TY2 + 148], radius=8, fill=CARD, outline=LINE)
    sc(x + 5, TY2 + 5, cw2 - 10, 54)
    yy = text_block(x + 8, TY2 + 63, head, F_CB(12), cw2 - 16, max_lines=3)
    yy = text_block(x + 8, yy + 1, summ, F_C(10), cw2 - 16, max_lines=3)
    ex = tag_chip(x + 8, TY2 + 126, tg, TAG_COLORS[tg])
    d.text((ex + 5, TY2 + 129), src, font=F_C(10), fill=NAVY)

# ---------------------------------------------------------------- map band
MY = 496
d.rounded_rectangle([16, MY, 656, MY + 148], radius=8, fill=(215, 230, 245), outline=LINE)
MX0, MY0, MW, MH = 20, MY + 4, 632, 140


def proj(lon, lat, x0=MX0, y0=MY0, w=MW, h=MH, lonr=(-180, 180), latr=(-60, 85)):
    return (x0 + (lon - lonr[0]) / (lonr[1] - lonr[0]) * w,
            y0 + (latr[1] - lat) / (latr[1] - latr[0]) * h)


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
IX, IY, IW, IH = 470, MY + 56, 180, 88
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
d.rounded_rectangle([KX, MY, W - 16, MY + 148], radius=8, fill=CARD, outline=LINE)
d.text((KX + 10, MY + 6), "REGIONS (36 stories)", font=F_CB(13), fill=NAVY)
regions = [("Europe", 10), ("Asia", 10), ("Americas", 5), ("Africa", 5), ("Middle East", 4), ("Oceania", 1), ("Global/Space", 1)]
ry = MY + 28
for name, cnt in regions:
    d.text((KX + 10, ry), name, font=F_C(12), fill=INK)
    d.text((W - 26, ry), str(cnt), font=F_CB(12), fill=RED, anchor="ra")
    ry += 15
d.text((KX + 10, ry + 1), "Tags: CONFIRMED / OFFICIAL / REPORTED / CLAIM", font=F_C(10), fill=NAVY)

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
]
LY2 = 648
d.text((16, LY2), "ALSO ON THURSDAY", font=F_CB(13), fill=NAVY)
half = (len(LIST) + 1) // 2
colw = (W - 32 - 12) // 2
for ci, chunk in enumerate((LIST[:half], LIST[half:])):
    x = 16 + ci * (colw + 12)
    y = LY2 + 18
    for n, head, src in chunk:
        if (n % 2) == 0:
            d.rectangle([x - 2, y - 1, x + colw, y + 13], fill=(240, 236, 224))
        d.text((x, y), f"{n}.", font=F_CB(11), fill=RED)
        d.text((x + 24, y), head, font=F_C(11), fill=INK)
        d.text((x + colw, y), src, font=F_C(10), fill=NAVY, anchor="ra")
        y += 15

# ---------------------------------------------------------------- DATE CHECK footer
FY = 884
d.line([(16, FY), (W - 16, FY)], fill=INK, width=2)
d.text((16, FY + 6), "DATE CHECK — not Thursday, however often printed:", font=F_CB(13), fill=RED)
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

img.save("entry.png", "PNG", optimize=True)
print("wrote entry.png")
