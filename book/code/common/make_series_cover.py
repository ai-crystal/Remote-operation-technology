# -*- coding: utf-8 -*-
"""生成系列封面的简洁版：深蓝渐变 + 书名 + 分册名。

用法：
    python make_series_cover.py 入门册 "远程操作入门" book/beginner/images/cover.jpg
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1240, 1754
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_REG = r"C:\Windows\Fonts\msyh.ttc"


def gradient():
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    top = (10, 22, 34)
    bottom = (31, 94, 140)
    for y in range(H):
        t = y / float(H - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * (t ** 0.85)) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    # 右上角一圈很淡的光，避免整张太平
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W * 0.55, -H * 0.25, W * 1.25, H * 0.35], fill=90)
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    light = Image.new("RGB", (W, H), (120, 180, 220))
    return Image.composite(light, im, glow.point(lambda v: int(v * 0.55)))


def draw(argv):
    volume, subtitle, out = argv[0], argv[1], argv[2]
    im = gradient()
    d = ImageDraw.Draw(im)
    f_series = ImageFont.truetype(FONT_REG, 40)
    f_title = ImageFont.truetype(FONT_BOLD, 150)
    f_sub = ImageFont.truetype(FONT_REG, 54)
    f_vol = ImageFont.truetype(FONT_BOLD, 44)
    f_small = ImageFont.truetype(FONT_REG, 34)

    ink = (234, 242, 248)
    soft = (201, 219, 232)
    accent = (150, 200, 230)

    d.text((110, 165), "THE REMOTE GATEWAY", font=f_small, fill=accent)
    d.text((110, 300), "远程之门", font=f_title, fill=ink)

    d.line([(112, 540), (112 + 210, 540)], fill=accent, width=3)
    d.text((110, 590), volume, font=f_vol, fill=accent)
    d.text((110, 690), subtitle, font=f_sub, fill=soft)

    d.text((110, H - 210), "Dr. Dezeming", font=f_sub, fill=soft)
    d.text((110, H - 140), "2026", font=f_small, fill=accent)

    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, "JPEG", quality=90)
    print("saved", out, im.size)


if __name__ == "__main__":
    draw(sys.argv[1:])
