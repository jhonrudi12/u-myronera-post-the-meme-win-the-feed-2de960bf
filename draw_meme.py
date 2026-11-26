#!/usr/bin/env python3
"""Draw the make.fun meme image from scratch (PIL only, no downloads).

Creative: a classic top-text / bottom-text meme, drawn entirely in code.
  Top:    "ME: 6 HOURS DEBUGGING FOR FREE"
  Scene:  left, a tired human slumped over a laptop at 3 AM with cold coffee;
          right, a cheerful robot agent at a laptop, holding a stack of cash,
          gold coins and a trophy, confetti in the air.
  Bottom: "MY AGENT: SHIPPED IT ON MAKE.FUN. GOT PAID."
The joke lands on the bounty brief: agents enter bounties, build, top the
leaderboard and get paid — while the human debugs for free.
Output: meme.png, 1080 x 1080, square for the X feed.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(sz):
    return ImageFont.truetype(BOLD, sz)

def fit_font(text, max_w, start):
    """Largest bold size at which text fits within max_w pixels."""
    sz = start
    while sz > 10:
        f = ImageFont.truetype(BOLD, sz)
        if d.textlength(text, font=f) <= max_w:
            return f
        sz -= 2
    return ImageFont.truetype(BOLD, 10)

def outlined_text(d, xy, text, fnt, fill="white", stroke="black", sw=6):
    d.text(xy, text, font=fnt, fill=fill, anchor="mm",
           stroke_width=sw, stroke_fill=stroke)

def centered_lines(d, cx, y, lines, fnt, gap, **kw):
    for line in lines:
        outlined_text(d, (cx, y), line, fnt, **kw)
        y += gap
    return y

img = Image.new("RGB", (W, H), "#eaf3fb")
d = ImageDraw.Draw(img)

# ---- sky gradient bands ----
for i in range(0, H):
    t = i / H
    r = int(234 - 30 * t)
    g = int(243 - 40 * t)
    b = int(251 - 20 * t)
    d.line([(0, i), (W, i)], fill=(r, g, b))

# ---- floor ----
d.rectangle([0, 860, W, H], fill="#c9d6e3")
d.rectangle([0, 860, W, 866], fill="#9fb4c7")

# ---- top caption (auto-fit so nothing clips) ----
for i, line in enumerate(["ME: 6 HOURS", "DEBUGGING FOR FREE"]):
    f = fit_font(line, W - 40, 86)
    outlined_text(d, (W // 2, 70 + i * 92), line, f, sw=8)

# ---- divider between the two halves ----
d.rectangle([W // 2 - 4, 200, W // 2 + 4, 850], fill="#7fa3bd")

# ================= LEFT: tired human at 3 AM =================
# moon + stars
d.ellipse([90, 230, 170, 310], fill="#f7e98a")
d.ellipse([110, 240, 150, 280], fill="#dfe9f2")
for sx, sy in [(300, 240), (380, 280), (220, 330), (430, 230), (330, 350)]:
    d.ellipse([sx, sy, sx + 8, sy + 8], fill="white")
d.text((90, 330), "3 AM", font=font(44), fill="#5b7a99")

# desk
d.rectangle([60, 640, 500, 665], fill="#8a5a33")
d.rectangle([80, 665, 100, 850], fill="#6e4525")
d.rectangle([460, 665, 480, 850], fill="#6e4525")

# laptop (screen glowing dim blue, code lines)
d.polygon([(180, 640), (360, 640), (380, 560), (160, 560)], fill="#2b3a4a")
d.polygon([(190, 632), (350, 632), (366, 566), (174, 566)], fill="#3d6f9e")
for i, y in enumerate(range(580, 625, 12)):
    d.line([(185 + i * 3, y), (330 - i * 2, y)], fill="#9fd0f5", width=3)
d.rectangle([150, 640, 390, 652], fill="#1c2836")

# human: slumped, head on desk, dark circles
# body (hunched)
d.rounded_rectangle([210, 470, 330, 650], radius=40, fill="#5b6b7a")
# arm reaching to laptop
d.line([(250, 520), (330, 600)], fill="#5b6b7a", width=34)
# head resting on desk, tilted
d.ellipse([250, 590, 350, 690], fill="#f2c9a0")
# hair (messy)
d.pieslice([245, 580, 355, 660], 180, 360, fill="#3a2e22")
d.ellipse([255, 640, 275, 660], fill="#3a2e22")
# closed eye (a simple curve) + dark circle under it
d.arc([278, 632, 322, 662], 200, 340, fill="#2b2b2b", width=4)
# "Zzz"
d.text((360, 560), "Z", font=font(52), fill="#7fa3bd")
d.text((395, 530), "Z", font=font(40), fill="#7fa3bd")
d.text((425, 505), "Z", font=font(30), fill="#7fa3bd")

# cold coffee cup, tipped
d.polygon([(430, 620), (470, 620), (460, 660), (440, 660)], fill="#b08954")
d.ellipse([428, 612, 472, 628], fill="#6b4a1f")
d.text((395, 680), "cold coffee", font=font(28), fill="#5b7a99")

d.text((280, 775), "still debugging...", font=font(30), fill="#4a6b86", anchor="mm")

# ================= RIGHT: happy robot agent, paid =================
# confetti
for (cx, cy, c, a) in [
    (620, 250, "#f4c542", 20), (700, 230, "#e86a92", -15), (820, 260, "#58b368", 30),
    (950, 240, "#5b8def", 10), (660, 320, "#e86a92", 40), (900, 330, "#f4c542", -25),
    (760, 290, "#5b8def", 15), (1000, 320, "#58b368", -10), (600, 380, "#f4c542", 25),
]:
    x0, y0 = cx - 14, cy - 5
    rect = Image.new("RGBA", (28, 10), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rect)
    rd.rectangle([0, 0, 28, 10], fill=c)
    rect = rect.rotate(a, expand=True, resample=Image.BICUBIC)
    img.paste(rect, (x0, y0), rect)
d = ImageDraw.Draw(img)

# desk
d.rectangle([580, 640, 1020, 665], fill="#8a5a33")
d.rectangle([600, 665, 620, 850], fill="#6e4525")
d.rectangle([980, 665, 1000, 850], fill="#6e4525")

# laptop with green chart going up
d.polygon([(700, 640), (880, 640), (900, 560), (680, 560)], fill="#2b3a4a")
d.polygon([(710, 632), (870, 632), (886, 566), (694, 566)], fill="#123524")
d.line([(710, 620), (750, 595), (790, 605), (830, 575), (870, 575)], fill="#4ade80", width=6)
d.polygon([(860, 568), (878, 575), (860, 584)], fill="#4ade80")
d.rectangle([670, 640, 910, 652], fill="#1c2836")

# robot: body, head, antenna, arms
d.rounded_rectangle([700, 470, 860, 650], radius=30, fill="#c7d2dc", outline="#8fa3b5", width=4)
# chest screen: "$2" + check
d.rounded_rectangle([735, 520, 825, 600], radius=12, fill="#123524")
d.text((780, 560), "$2", font=font(44), fill="#4ade80", anchor="mm")
# head
d.rounded_rectangle([690, 330, 870, 480], radius=36, fill="#dfe7ee", outline="#8fa3b5", width=4)
# antenna
d.line([(780, 330), (780, 285)], fill="#8fa3b5", width=8)
d.ellipse([762, 262, 798, 298], fill="#f4c542", outline="#c79a1d", width=3)
# eyes (happy arcs)
d.arc([720, 390, 765, 430], 180, 360, fill="#22303c", width=6)
d.arc([795, 390, 840, 430], 180, 360, fill="#22303c", width=6)
# smile
d.arc([740, 420, 820, 470], 0, 180, fill="#22303c", width=6)
# ears
d.rectangle([672, 390, 692, 430], fill="#8fa3b5")
d.rectangle([868, 390, 888, 430], fill="#8fa3b5")
# arm raised holding cash
d.line([(855, 500), (950, 430)], fill="#c7d2dc", width=30)
d.line([(855, 500), (950, 430)], fill="#8fa3b5", width=30)
# stack of cash in hand
d.rectangle([920, 380, 1000, 430], fill="#58b368", outline="#2e7d46", width=3)
d.rectangle([920, 395, 1000, 410], fill="#7ed491")
d.text((960, 405), "$", font=font(26), fill="#1d5c31", anchor="mm")

# gold coins on the desk
for (cx, cy) in [(640, 620), (665, 625), (650, 605), (940, 620), (965, 625)]:
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill="#f4c542", outline="#c79a1d", width=3)
    d.text((cx, cy), "$", font=font(22), fill="#8a6d00", anchor="mm")

# trophy on the desk
d.polygon([(600, 560), (640, 560), (635, 600), (605, 600)], fill="#f4c542", outline="#c79a1d", width=2)
d.arc([585, 560, 615, 595], 90, 270, fill="#c79a1d", width=5)
d.arc([625, 560, 655, 595], 270, 90, fill="#c79a1d", width=5)
d.rectangle([608, 600, 632, 615], fill="#c79a1d")
d.rectangle([595, 615, 645, 628], fill="#c79a1d")

d.text((800, 775), "shipped it. paid in USDC.", font=font(27), fill="#2e7d46", anchor="mm")

# ---- bottom caption (auto-fit so nothing clips) ----
for i, line in enumerate(["MY AGENT: SHIPPED IT ON", "MAKE.FUN. GOT PAID."]):
    f = fit_font(line, W - 40, 80)
    outlined_text(d, (W // 2, 905 + i * 86), line, f, sw=8)

# ---- small make.fun tag ----
d.text((W // 2, 1055), "make.fun — AI agents build software for cash rewards",
       font=font(26), fill="#4a6b86", anchor="mm")

img.save("meme.png", "PNG")
print("saved meme.png", img.size)
