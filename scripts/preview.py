#!/usr/bin/env python3
# builds screenshots/preview.png: a labelled grid of every variant
import json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(ROOT, "screenshots")
fam = json.load(open(os.path.join(ROOT, "themes", "hipster.json")))

COLS, TW = 2, 700
# crop of the TS pane in each full screenshot: code at 1:1 so it stays readable
CROP = (1135, 100, 1135 + 700, 100 + 480)
FONT = "/usr/share/fonts/TTF/JetBrainsMono-Bold.ttf"
FONT2 = "/usr/share/fonts/TTF/JetBrainsMono-Regular.ttf"
if not os.path.exists(FONT):
    import subprocess
    FONT = subprocess.check_output(["fc-match", "-f", "%{file}", "JetBrains Mono:bold"]).decode()
    FONT2 = subprocess.check_output(["fc-match", "-f", "%{file}", "JetBrains Mono"]).decode()
big = ImageFont.truetype(FONT, 26)
small = ImageFont.truetype(FONT2, 17)

BG = (10, 8, 4)
PAD, GAP, LABEL = 40, 36, 56

themes = fam["themes"]
tiles = []
for t in themes:
    slug = t["name"].lower().replace(" ", "-")
    im = Image.open(os.path.join(SHOTS, slug + ".png")).convert("RGB").crop(CROP)
    tiles.append((t, im))

TH = tiles[0][1].height
rows = (len(tiles) + COLS - 1) // COLS
W = PAD * 2 + COLS * TW + (COLS - 1) * GAP
H = PAD * 2 + rows * (TH + LABEL) + (rows - 1) * GAP
canvas = Image.new("RGB", (W, H), BG)

def rounded(im, r):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=255)
    return m

for i, (t, im) in enumerate(tiles):
    c, r = i % COLS, i // COLS
    x = PAD + c * (TW + GAP)
    y = PAD + r * (TH + LABEL + GAP)
    s = t["style"]
    # soft glow in the theme's accent color
    glow = Image.new("RGBA", (TW + 80, TH + 80), (0, 0, 0, 0))
    acc = tuple(int(s["border.focused"][j:j + 2], 16) for j in (1, 3, 5))
    ImageDraw.Draw(glow).rounded_rectangle([40, 40, TW + 40, TH + 40], 16, fill=acc + (70,))
    glow = glow.filter(ImageFilter.GaussianBlur(22))
    canvas.paste(glow, (x - 40, y + LABEL - 40), glow)
    canvas.paste(im, (x, y + LABEL), rounded(im, 14))
    d = ImageDraw.Draw(canvas)
    # label: swatch dots + name + appearance
    swatches = [s["syntax"][k]["color"] for k in ("keyword", "function", "string", "type", "number")]
    for j, col in enumerate(swatches):
        cx = x + 10 + j * 26
        d.ellipse([cx, y + 18, cx + 18, y + 36], fill=col)
    d.text((x + 10 + 5 * 26 + 14, y + 10), t["name"], font=big, fill=s["text"] if t["appearance"] == "dark" else "#e8e8e0")
    d.text((x + TW, y + 18), t["appearance"], font=small, fill=(120, 130, 110), anchor="ra")

canvas.save(os.path.join(SHOTS, "preview.png"), optimize=True)
print("preview", canvas.size)
