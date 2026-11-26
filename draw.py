import os
from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
NAVY = (22, 35, 63)
RED = (163, 22, 33)
GOLD = (198, 158, 74)
SEA = (28, 68, 110)
SEA_DARK = (16, 44, 80)
GREY = (96, 96, 96)
LIGHT_LINE = (190, 182, 164)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_width):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def flame(draw, cx, base, size, palette):
    outer = [
        (cx - size * 0.55, base),
        (cx - size * 0.42, base - size * 0.55),
        (cx - size * 0.12, base - size * 0.42),
        (cx, base - size * 1.05),
        (cx + size * 0.18, base - size * 0.45),
        (cx + size * 0.5, base - size * 0.6),
        (cx + size * 0.55, base),
    ]
    draw.polygon(outer, fill=palette[0])
    inner = [
        (cx - size * 0.3, base),
        (cx - size * 0.22, base - size * 0.35),
        (cx, base - size * 0.62),
        (cx + size * 0.24, base - size * 0.3),
        (cx + size * 0.3, base),
    ]
    draw.polygon(inner, fill=palette[1])
    core = [
        (cx - size * 0.14, base),
        (cx - size * 0.1, base - size * 0.2),
        (cx, base - size * 0.34),
        (cx + size * 0.12, base - size * 0.18),
        (cx + size * 0.14, base),
    ]
    draw.polygon(core, fill=palette[2])


def smoke(draw, cx, cy, radius, colour):
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=colour)
    draw.ellipse(
        [cx - radius * 0.6, cy - radius * 1.5, cx + radius * 0.7, cy - radius * 0.2],
        fill=colour,
    )
    draw.ellipse(
        [cx - radius * 0.3, cy - radius * 2.1, cx + radius * 0.9, cy - radius * 0.9],
        fill=colour,
    )


def tanker(draw, x, y, length, hull, deck):
    draw.rectangle([x, y, x + length, y + hull], fill=(52, 52, 58))
    draw.rectangle([x + length * 0.62, y - hull * 1.15, x + length * 0.82, y], fill=(214, 214, 208))
    draw.rectangle([x + length * 0.66, y - hull * 1.55, x + length * 0.78, y - hull * 1.15], fill=(214, 214, 208))
    draw.rectangle([x + length * 0.1, y - hull * 0.5, x + length * 0.55, y], fill=deck)
    draw.rectangle([x + length * 0.86, y - hull * 0.9, x + length * 0.9, y], fill=(120, 30, 30))
    for i in range(3):
        wx = x + length * 0.66 + i * length * 0.05
        draw.rectangle([wx, y - hull * 1.05, wx + length * 0.03, y - hull * 0.85], fill=NAVY)


def mine_shape(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(20, 20, 20))
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7), (0.7, 0.7)]:
        x2 = cx + dx * r * 1.5
        y2 = cy + dy * r * 1.5
        draw.line([cx + dx * r * 0.7, cy + dy * r * 0.7, x2, y2], fill=(20, 20, 20), width=3)
        draw.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], fill=(20, 20, 20))


def refinery(draw, x, y, w, h):
    draw.rectangle([x, y + h * 0.35, x + w, y + h], fill=(74, 74, 78))
    draw.polygon(
        [(x + w * 0.08, y + h * 0.35), (x + w * 0.14, y), (x + w * 0.22, y), (x + w * 0.28, y + h * 0.35)],
        fill=(52, 52, 58),
    )
    draw.polygon(
        [(x + w * 0.55, y + h * 0.35), (x + w * 0.6, y + h * 0.1), (x + w * 0.68, y + h * 0.1), (x + w * 0.73, y + h * 0.35)],
        fill=(52, 52, 58),
    )
    draw.rectangle([x + w * 0.8, y + h * 0.45, x + w * 0.95, y + h], fill=(52, 52, 58))
    for i in range(4):
        wy = y + h * 0.5 + i * h * 0.12
        draw.rectangle([x + w * 0.05, wy, x + w * 0.95, wy + 3], fill=(214, 190, 120))


def skyline(draw, x, y, w, h):
    heights = [0.55, 0.8, 0.45, 0.95, 0.62, 0.75, 0.5]
    step = w / len(heights)
    for i, frac in enumerate(heights):
        bx = x + i * step
        bh = h * frac
        draw.rectangle([bx + 2, y + h - bh, bx + step - 2, y + h], fill=(52, 52, 58))
        for wy in range(3):
            for wx in range(2):
                lx = bx + 6 + wx * (step / 2 - 4)
                ly = y + h - bh + 8 + wy * 16
                draw.rectangle([lx, ly, lx + 6, ly + 8], fill=(232, 200, 90))


def courthouse(draw, x, y, w, h):
    draw.polygon(
        [(x, y + h * 0.3), (x + w / 2, y), (x + w, y + h * 0.3)],
        fill=(96, 84, 66),
    )
    draw.rectangle([x, y + h * 0.3, x + w, y + h * 0.38], fill=(74, 66, 54))
    for i in range(5):
        cx = x + w * 0.1 + i * w * 0.2
        draw.rectangle([cx - 7, y + h * 0.38, cx + 7, y + h * 0.92], fill=(214, 208, 192))
    draw.rectangle([x, y + h * 0.92, x + w, y + h], fill=(74, 66, 54))


def chart(draw, x, y, w, h):
    pts = [
        (x, y + h * 0.25),
        (x + w * 0.2, y + h * 0.35),
        (x + w * 0.4, y + h * 0.6),
        (x + w * 0.6, y + h * 0.85),
        (x + w * 0.8, y + h * 0.55),
        (x + w, y + h * 0.3),
    ]
    draw.line(pts, fill=RED, width=5, joint="curve")
    for px, py in pts:
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED)
    draw.line([x, y + h * 0.85, x + w, y + h * 0.85], fill=GREY, width=2)


def draw_lead_scene(draw):
    px, py, pw, ph = 24, 224, 560, 246
    draw.rectangle([px, py, px + pw, py + ph], fill=SEA_DARK)
    draw.rectangle([px, py, px + pw, py + 62], fill=(232, 196, 120))
    draw.ellipse([px + 430, py + 6, px + 486, py + 62], fill=(240, 170, 60))
    draw.rectangle([px, py + 62, px + pw, py + 96], fill=(226, 178, 96))
    draw.rectangle([px, py + 96, px + pw, py + ph], fill=SEA)
    for i in range(4):
        wx = px + 30 + i * 120
        draw.arc([wx, py + 108, wx + 90, py + 132], 0, 180, fill=(140, 180, 220), width=3)
    tanker(draw, px + 40, py + 150, 250, 34, (150, 44, 44))
    tanker(draw, px + 320, py + 168, 220, 30, (44, 96, 60))
    flame(draw, px + 120, py + 150, 46, [(230, 90, 20), (245, 160, 40), (250, 220, 90)])
    flame(draw, px + 420, py + 168, 38, [(230, 90, 20), (245, 160, 40), (250, 220, 90)])
    smoke(draw, px + 120, py + 96, 22, (70, 70, 74))
    smoke(draw, px + 420, py + 112, 18, (70, 70, 74))
    mine_shape(draw, px + 545, py + 210, 11)
    mine_shape(draw, px + 300, py + 222, 9)
    draw.rectangle([px, py, px + pw, py + ph], outline=INK, width=2)


def draw_story(draw, x, y, w, kicker, headline, body, art):
    draw.text((x, y), kicker, font=font(SANS_BOLD, 15), fill=RED)
    hf = font(SERIF, 25)
    lines = wrap_text(draw, headline, hf, w)
    ly = y + 24
    for line in lines:
        draw.text((x, ly), line, font=hf, fill=INK)
        ly += 30
    ax, ay, ah = x, ly + 6, 96
    draw.rectangle([ax, ay, ax + w, ay + ah], fill=(232, 226, 210))
    draw.rectangle([ax, ay, ax + w, ay + ah], outline=INK, width=1)
    art(draw, ax + 8, ay + 8, w - 16, ah - 16)
    bf = font(SANS, 16)
    by = ay + ah + 10
    for line in wrap_text(draw, body, bf, w):
        draw.text((x, by), line, font=bf, fill=INK)
        by += 21


def draw_brief(draw, x, y, w, kicker, body):
    draw.text((x, y), kicker, font=font(SANS_BOLD, 15), fill=GOLD)
    bf = font(SANS, 15)
    by = y + 24
    for line in wrap_text(draw, body, bf, w):
        draw.text((x, by), line, font=bf, fill=(238, 236, 228))
        by += 20


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 112], fill=NAVY)
    draw.rectangle([0, 112, W, 116], fill=GOLD)
    title = "THE WORLD TODAY"
    tf = font(SERIF, 58)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 12), title, font=tf, fill=(247, 242, 231))
    sub = "WEDNESDAY  ·  25 NOVEMBER 2026  ·  ONE DAY, ONE PAGE"
    sf = font(SANS_BOLD, 18)
    sw = draw.textlength(sub, font=sf)
    draw.text(((W - sw) / 2, 80), sub, font=sf, fill=GOLD)
    draw.rectangle([24, 128, 1000, 132], fill=RED)
    lead_head = "TANKERS ABLAZE IN HORMUZ STRAIT"
    lhf = font(SERIF, 36)
    ly = 142
    for line in wrap_text(draw, lead_head, lhf, 976):
        draw.text((24, ly), line, font=lhf, fill=INK)
        ly += 46
    draw_lead_scene(draw)
    tx = 608
    ty = 224
    draw.text((tx, ty), "IRAN WAR  ·  ENERGY", font=font(SANS_BOLD, 15), fill=RED)
    lead_body = (
        "Iran's Revolutionary Guard said two oil tankers struck naval mines "
        "in the Strait of Hormuz and caught fire. The vessels were on an "
        "unauthorised route, it said, as fears grow for shipping and oil supplies."
    )
    bf = font(SANS, 18)
    by = ty + 30
    for line in wrap_text(draw, lead_body, bf, 392):
        draw.text((tx, by), line, font=bf, fill=INK)
        by += 25
    by += 8
    draw.rectangle([tx, by, tx + 392, by + 2], fill=LIGHT_LINE)
    by += 12
    second = (
        "Yemen's Houthis said they also hit Saudi Arabia's Ras Tanura oil refinery."
    )
    for line in wrap_text(draw, second, bf, 392):
        draw.text((tx, by), line, font=bf, fill=INK)
        by += 25
    draw.rectangle([24, 486, 1000, 488], fill=INK)
    col_w = 309
    gap = 14
    stories = [
        (
            "GAZA  ·  ISRAEL-HAMAS WAR",
            "Hamas security chief killed in Gaza strike",
            "Israel killed Mohammad Abuelouf, a Hamas colonel who ran its internal security service, with his wife and two children, medics said.",
            lambda d, x, y, w, h: skyline(d, x, y, w, h),
        ),
        (
            "UKRAINE  ·  RUSSIA-UKRAINE WAR",
            "Two Russian refineries set ablaze",
            "Ukrainian drones hit two Rosneft refineries in Samara overnight; leaked Russian figures put its military deaths since 2022 at 490,334.",
            lambda d, x, y, w, h: refinery(d, x, y, w, h),
        ),
        (
            "UNITED STATES  ·  TECH",
            "Huawei convicted of stealing trade secrets",
            "A Brooklyn jury found Huawei guilty of trade-secret theft and bank fraud, but cleared it of racketeering, after a two-month trial.",
            lambda d, x, y, w, h: courthouse(d, x, y, w, h),
        ),
    ]
    for i, (kicker, headline, body, art) in enumerate(stories):
        x = 24 + i * (col_w + gap)
        draw_story(draw, x, 502, col_w, kicker, headline, body, art)
    draw.rectangle([24, 776, 1000, 780], fill=INK)
    draw.rectangle([0, 792, W, 968], fill=NAVY)
    draw.text((24, 806), "ALSO TODAY", font=font(SANS_BOLD, 16), fill=GOLD)
    briefs = [
        ("MARKETS", "Asia tumbled: Seoul's KOSPI fell 6.16%, Tokyo's Nikkei 2.78%. The Dow closed above 50,000 for the first time."),
        ("RIYADH", "A Houthi strike on a Riyadh skyscraper injured 11 people, Saudi civil defence said."),
        ("PACIFIC", "Australia and Solomon Islands signed a treaty barring any foreign military base on the islands."),
        ("SPACE", "China's Shenzhou-24 docked with Tiangong, carrying Pakistan's first astronaut into orbit."),
    ]
    bw = 226
    bgap = 12
    for i, (kicker, body) in enumerate(briefs):
        x = 24 + i * (bw + bgap)
        draw_brief(draw, x, 836, bw, kicker, body)
    foot = "Also: COP31 climate talks end without a deal  ·  Trump gives Giuliani the Medal of Freedom  ·  Drawn from wire reports of Wednesday 25 November 2026"
    ff = font(SANS, 13)
    fw = draw.textlength(foot, font=ff)
    draw.text(((W - fw) / 2, 984), foot, font=ff, fill=GREY)
    return img


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    build().save(out, format="PNG", optimize=True)
    print("wrote " + out)
