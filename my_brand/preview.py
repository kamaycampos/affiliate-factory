#!/usr/bin/env python3
"""Show the member their look BEFORE any clip exists (setup Step 3).

    python3 my_brand/preview.py ["Hook line one" "line two"] ["CAPTION WORDS" "ACCENT"]

Draws my_brand/style.json - hook card colour, bar, text colour, caption colour,
accent word, capitals, shadow, font - onto a real Kevin frame and writes
my_brand/LOOK_PREVIEW.jpg. Open it for them (and send it to the chat as an image).
Change style.json, run again, until they say "yes, that's me".
Close to the real render, not identical: the factory also places the words
around the speaker's face. Needs only Pillow (pip install pillow).
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
st = json.load(open(os.path.join(HERE, "style.json")))


def rgb(v, default):
    v = str(v or "").strip()
    named = {"white": (255, 255, 255), "black": (0, 0, 0), "yellow": (255, 229, 0)}
    if v.lower() in named:
        return named[v.lower()]
    v = v.lstrip("#")
    return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4)) if len(v) == 6 else default


font_file = st.get("font_file") or "factory/assets/mont_black.ttf"
font_path = font_file if os.path.isabs(font_file) else os.path.join(ROOT, font_file)
up = (lambda t: t.upper()) if st.get("uppercase", True) else (lambda t: t)
hook = sys.argv[1:3] if len(sys.argv) >= 3 else ["What 100 healthy", "90-year-olds all ate"]
cap_words, accent = (sys.argv[3], sys.argv[4]) if len(sys.argv) >= 5 else ("Read the", "label")

frame = Image.open(os.path.join(HERE, "sample_frame.jpg")).convert("RGBA")
W, H = frame.size

# The hook card: a rounded panel, a short bar under it, the hook in two lines.
lines = [up(l) for l in hook]
size = 70
fo = ImageFont.truetype(font_path, size)
probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
while max(probe.textlength(l, font=fo) for l in lines) > W - 240 and size > 40:
    size -= 2
    fo = ImageFont.truetype(font_path, size)
tw = max(probe.textlength(l, font=fo) for l in lines)
cw, ch = int(tw) + 80, len(lines) * (size + 22) + 56
card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
d = ImageDraw.Draw(card)
d.rounded_rectangle([0, 0, cw - 1, ch - 1], 24, fill=rgb(st.get("hook_card_color"), (10, 11, 14)) + (225,))
d.rounded_rectangle([34, ch - 16, 150, ch - 10], 3, fill=rgb(st.get("hook_bar_color"), (245, 197, 66)))
y = 28
for l in lines:
    d.text(((cw - probe.textlength(l, font=fo)) / 2, y), l, font=fo,
           fill=rgb(st.get("hook_text_color"), (255, 255, 255)))
    y += size + 22
frame.alpha_composite(card, ((W - cw) // 2, int(st.get("hook_bottom", 930)) - ch))

# One caption line: plain words + the accent word.
cs = int(st.get("caption_size", 72))
cf = ImageFont.truetype(font_path, cs)
words = [(up(cap_words) + " ", rgb(st.get("text_color"), (255, 255, 255))),
         (up(accent), rgb(st.get("accent_color") if st.get("accent_captions", True) else st.get("text_color"), (255, 229, 0)))]
x = (W - sum(probe.textlength(w, font=cf) for w, _ in words)) / 2
y = int(st.get("caption_y", 1050))
shadow = st.get("shadow", "heavy")
if shadow != "none":
    sh = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    xx = x
    for w, _ in words:
        if shadow == "outline":
            sd.text((xx, y), w, font=cf, fill=(0, 0, 0, 0), stroke_width=6, stroke_fill=(0, 0, 0, 230))
        else:
            sd.text((xx + 4, y + 6), w, font=cf, fill=(0, 0, 0, 220 if shadow == "heavy" else 140))
        xx += probe.textlength(w, font=cf)
    frame.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4 if shadow != "outline" else 1)))
d = ImageDraw.Draw(frame)
for w, col in words:
    d.text((x, y), w, font=cf, fill=col)
    x += probe.textlength(w, font=cf)

out = os.path.join(HERE, "LOOK_PREVIEW.jpg")
frame.convert("RGB").save(out, quality=88)
print(out)
