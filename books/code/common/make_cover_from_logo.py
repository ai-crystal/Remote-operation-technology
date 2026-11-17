# -*- coding: utf-8 -*-
"""用 E:/Study/0-logo 里的背景图合成系列封面与封底。

用法：
    python make_cover_from_logo.py <背景图> <分册名> <副标题> <强调色> <卷号> <输出.jpg>

设计要点：
  * 竖版 1240×1754，背景按“铺满 + 居中裁切”处理
  * 下半部压一层由透明到深色的渐变，保证文字可读
  * 统一版式：英文系列名 → 书名 → 分隔线 → 分册名 → 副标题 → 作者
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1240, 1754
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_REG = r"C:\Windows\Fonts\msyh.ttc"


def load_cover(bg_path, anchor=0.45):
    im = Image.open(bg_path).convert("RGB")
    scale = max(W / im.width, H / im.height)
    im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))),
                   Image.LANCZOS)
    left = (im.width - W) // 2
    top = int((im.height - H) * anchor)
    top = max(0, min(top, im.height - H))
    return im.crop((left, top, left + W, top + H))


def grade(im):
    """压一点亮度、加一层冷色，让画面和文字更贴。"""
    im = im.point(lambda v: int(v * 0.82))
    tint = Image.new("RGB", (W, H), (12, 26, 40))
    return Image.blend(im, tint, 0.22)


def scrim(im):
    """下方渐变遮罩：底部最暗，到画面中部完全透明。"""
    mask = Image.new("L", (1, H), 0)
    px = mask.load()
    start = int(H * 0.34)
    for y in range(H):
        if y < start:
            v = 0
        else:
            t = (y - start) / float(H - start)
            v = int(255 * (t ** 1.35))
        px[0, y] = v
    mask = mask.resize((W, H))
    dark = Image.new("RGB", (W, H), (5, 11, 18))
    return Image.composite(dark, im, mask)


def hex2rgb(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def text(d, xy, s, font, fill):
    d.text(xy, s, font=font, fill=fill)


def make_cover(bg, volume, subtitle, accent, number, out, anchor=0.45):
    im = scrim(grade(load_cover(bg, anchor)))
    d = ImageDraw.Draw(im, "RGBA")
    accent = hex2rgb(accent)

    f_en = ImageFont.truetype(FONT_REG, 32)
    f_title = ImageFont.truetype(FONT_BOLD, 148)
    f_vol = ImageFont.truetype(FONT_BOLD, 46)
    f_sub = ImageFont.truetype(FONT_REG, 48)
    f_small = ImageFont.truetype(FONT_REG, 30)

    left = 112
    # 顶部系列标识
    text(d, (left, 132), "THE REMOTE GATEWAY", f_en, (214, 232, 244, 210))
    d.line([(left, 190), (left + 88, 190)], fill=(214, 232, 244, 120), width=2)

    # 书名
    text(d, (left - 6, H - 760), "远程之门", f_title, (245, 250, 254, 255))

    # 分隔线 + 分册
    d.line([(left, H - 560), (left + 176, H - 560)], fill=accent + (235,), width=4)
    text(d, (left, H - 536), volume, f_vol, accent + (255,))
    text(d, (left, H - 462), subtitle, f_sub, (226, 238, 248, 235))

    # 卷号（右上角）
    text(d, (W - 240, 132), "%02d / 03" % number, f_small, (214, 232, 244, 190))

    # 作者
    text(d, (left, H - 250), "Dr. Dezeming", f_sub, (226, 238, 248, 220))
    text(d, (left, H - 178), "2026", f_small, (200, 220, 235, 190))

    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, "JPEG", quality=90)
    print("saved", out, im.size)


def make_back(bg, out, quote):
    im = load_cover(bg, 0.5).filter(ImageFilter.GaussianBlur(10))
    im = im.point(lambda v: int(v * 0.78))
    mask = Image.new("L", (1, H), 0)
    px = mask.load()
    for y in range(H):
        t = y / float(H - 1)
        px[0, y] = int(120 + 95 * (1 - abs(t - 0.5) * 2))
    mask = mask.resize((W, H))
    dark = Image.new("RGB", (W, H), (5, 11, 18))
    im = Image.composite(dark, im, mask)
    d = ImageDraw.Draw(im, "RGBA")
    f_q = ImageFont.truetype(FONT_REG, 40)
    f_s = ImageFont.truetype(FONT_REG, 28)
    f_t = ImageFont.truetype(FONT_BOLD, 64)
    text(d, (120, 150), "远程之门", f_t, (238, 246, 252, 235))
    d.line([(120, 240), (120 + 96, 240)], fill=(200, 220, 235, 150), width=3)
    text(d, (120, H - 380), quote, f_q, (232, 242, 250, 240))
    text(d, (120, H - 260), "远程之门 · 三册丛书", f_s, (200, 220, 235, 180))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, "JPEG", quality=88)
    print("saved", out, im.size)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[0] == "back":
        make_back(args[1], args[2], args[3])
    else:
        bg, volume, subtitle, accent, number, out = args
        make_cover(bg, volume, subtitle, accent, int(number), out)
