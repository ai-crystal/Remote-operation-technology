# -*- coding: utf-8 -*-
"""用 PIL 从背景图合成封面与封底。背景图来自 E:/Study/logo。"""

import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.normpath(os.path.join(HERE, "..", ".."))
IMAGES = os.path.join(BOOK, "images")
# 背景图放在本地目录，用环境变量 COVER_BG_DIR 指定；找不到就跳过，
# 直接使用仓库里已经生成好的 cover.jpg / backcover.jpg。
LOGO_DIR = os.environ.get("COVER_BG_DIR", os.path.join(BOOK, "images", "_source"))

W, H = 1240, 1754
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_REG = r"C:\Windows\Fonts\msyh.ttc"

TITLE = "远程之门"
SUBTITLE = "SSH、堡垒机与对象存储的技术细节"
EN_TITLE = "THE REMOTE GATEWAY"
AUTHOR = "Dr. Dezeming"
YEAR = "2026"


def load_bg(name, blur=2.0):
    path = os.path.join(LOGO_DIR, name)
    if not os.path.exists(path):
        raise SystemExit("缺少背景图 %s，请设置环境变量 COVER_BG_DIR 指向存放背景图的目录。" % path)
    im = Image.open(path).convert("RGB")
    # 等比裁剪铺满画布
    scale = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * scale) + 1, int(im.height * scale) + 1),
                   Image.LANCZOS)
    left = (im.width - W) // 2
    top = (im.height - H) // 2
    im = im.crop((left, top, left + W, top + H))
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    return im


def vertical_gradient(size, top_alpha, bottom_alpha, color=(6, 12, 20)):
    w, h = size
    grad = Image.new("L", (1, h))
    px = grad.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        a = int(top_alpha + (bottom_alpha - top_alpha) * t)
        px[0, y] = max(0, min(255, a))
    grad = grad.resize((w, h))
    layer = Image.new("RGB", (w, h), color)
    return layer, grad


def overlay(im, top_a, bottom_a, color=(6, 12, 20)):
    layer, mask = vertical_gradient(im.size, top_a, bottom_a, color)
    im.paste(layer, (0, 0), mask)
    return im


def draw_spaced(draw, xy, text, font, fill, spacing=10, anchor_center_x=None):
    """带字间距的绘制，返回总宽度。"""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = xy[0] - total / 2 if anchor_center_x else xy[0]
    y = xy[1]
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + spacing
    return total


def make_cover():
    im = load_bg("logo3.png", blur=1.4)
    im = overlay(im, 40, 190, (4, 10, 18))
    # 标题区压一层暗色，保证白字在亮背景上也清楚
    band = Image.new("RGB", (W, 420), (3, 8, 14))
    mask = Image.new("L", (W, 420), 0)
    md = ImageDraw.Draw(mask)
    for i in range(420):
        t = i / 419.0
        a = int(120 * (1 - abs(t - 0.5) * 1.6))
        md.line([(0, i), (W, i)], fill=max(a, 0))
    im.paste(band, (0, 500), mask)

    d = ImageDraw.Draw(im)

    f_title = ImageFont.truetype(FONT_BOLD, 132)
    f_sub = ImageFont.truetype(FONT_REG, 38)
    f_en = ImageFont.truetype(FONT_REG, 22)
    f_author = ImageFont.truetype(FONT_BOLD, 34)
    f_small = ImageFont.truetype(FONT_REG, 24)

    # 顶部小字，作为丛书的标记
    draw_spaced(d, (90, 118), "REMOTE  &  CLOUD", ImageFont.truetype(FONT_REG, 20),
                (200, 216, 230), spacing=4)

    # 主标题
    ty = 560
    draw_spaced(d, (W / 2, ty), TITLE, f_title, (255, 255, 255),
                spacing=26, anchor_center_x=True)

    # 主标题下的细线
    d.line([(W / 2 - 190, ty + 210), (W / 2 + 190, ty + 210)],
           fill=(150, 200, 230), width=3)

    # 副标题
    sub_w = d.textlength(SUBTITLE, font=f_sub)
    d.text(((W - sub_w) / 2, ty + 246), SUBTITLE, font=f_sub,
           fill=(226, 236, 244))

    en_w = d.textlength(EN_TITLE, font=f_en)
    d.text(((W - en_w) / 2, ty + 314), EN_TITLE, font=f_en, fill=(160, 190, 214))

    # 底部信息
    d.line([(90, H - 226), (W - 90, H - 226)], fill=(120, 150, 175), width=2)
    d.text((90, H - 196), AUTHOR, font=f_author, fill=(240, 245, 250))
    d.text((90, H - 140), YEAR, font=f_small, fill=(190, 205, 220))
    tail = "从一次 ssh 登录，到云端的数据存取"
    tw = d.textlength(tail, font=f_small)
    d.text((W - 90 - tw, H - 142), tail, font=f_small, fill=(190, 205, 220))

    path = os.path.join(IMAGES, "cover.jpg")
    im.save(path, "JPEG", quality=88, optimize=True, progressive=True)
    print("cover ->", path, im.size)


def make_back():
    im = load_bg("logo15.png", blur=2.2)
    im = overlay(im, 150, 215, (5, 10, 16))
    d = ImageDraw.Draw(im)

    f_head = ImageFont.truetype(FONT_BOLD, 44)
    f_body = ImageFont.truetype(FONT_REG, 30)
    f_quote = ImageFont.truetype(r"C:\Windows\Fonts\simkai.ttf", 34)
    f_small = ImageFont.truetype(FONT_REG, 24)

    y = 300
    d.text((110, y), "这本书讲什么", font=f_head, fill=(255, 255, 255))
    y += 96

    lines = [
        "一条 ssh 命令背后有多少层协议，为什么要先加密再认证，",
        "堡垒机的“用户@系统用户@资产”是怎么被解析的，",
        "VS Code 在你和目标机之间架了什么，",
        "对象存储的签名为什么总是对不上。",
    ]
    for ln in lines:
        d.text((110, y), ln, font=f_body, fill=(226, 234, 242))
        y += 58

    y += 46
    d.line([(110, y), (330, y)], fill=(150, 190, 215), width=3)
    y += 60

    quote = [
        "知道为什么这么做，配置错了能自己看出来，",
        "报错信息能自己读懂，别人给的指南也能自己判断。",
    ]
    for ln in quote:
        d.text((110, y), ln, font=f_quote, fill=(210, 224, 235))
        y += 62

    y = H - 250
    d.line([(110, y), (W - 110, y)], fill=(120, 150, 175), width=2)
    d.text((110, y + 34), AUTHOR, font=ImageFont.truetype(FONT_BOLD, 30),
           fill=(240, 245, 250))
    tail = "远程之门 · " + YEAR
    tw = d.textlength(tail, font=f_small)
    d.text((W - 110 - tw, y + 40), tail, font=f_small, fill=(190, 205, 220))

    path = os.path.join(IMAGES, "backcover.jpg")
    im.save(path, "JPEG", quality=88, optimize=True, progressive=True)
    print("backcover ->", path, im.size)


if __name__ == "__main__":
    if not os.path.isdir(LOGO_DIR):
        print("跳过封面渲染：未找到背景图目录 %s（可设置 COVER_BG_DIR）" % LOGO_DIR)
    else:
        make_cover()
        make_back()
