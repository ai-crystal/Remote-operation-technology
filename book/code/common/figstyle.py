# -*- coding: utf-8 -*-
"""全书插图共用的绘图工具。所有图都由代码生成，不放入 AI 生成图片。

约定
----
1. 画布坐标统一为 0..100（横）与 0..100*高/宽（纵），左下角为原点。
2. 图内不写标题，标题由图注承担（Markdown 里图片的 alt 文字）。
3. 文字与线框之间留出空白，宁可把框画大一点，也不要让文字压到边框。
"""

import io
import os
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (Circle, FancyArrowPatch, FancyBboxPatch,
                                Polygon, Rectangle)

# ------------------------------------------------------------------ 基础设置

INK = "#1b1b1b"
ACCENT = "#1f5e8c"
ACCENT_L = "#dce8f0"
WARM = "#a2613a"
WARM_L = "#f2e4d8"
GREEN = "#3f6b52"
GREEN_L = "#dfeae2"
GRAY = "#6f6f6f"
GRAY_L = "#e8ebee"
RED = "#9c3d3d"
RED_L = "#f0dddd"
WHITE = "#ffffff"

FONT_CANDIDATES = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC",
                   "Source Han Sans SC", "WenQuanYi Zen Hei"]

OUT_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "..", "..", "images"))


def setup():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": FONT_CANDIDATES,
        "axes.unicode_minus": False,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.dpi": 220,
        "text.color": INK,
        "font.size": 10,
    })


def canvas(width_in, height_in, xmax=100.0, ymax=None):
    """返回 (fig, ax)。ax 已关闭坐标轴，坐标范围 (0..xmax, 0..ymax)。"""
    setup()
    fig = plt.figure(figsize=(width_in, height_in))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax if ymax is not None else xmax * height_in / width_in)
    ax.set_axis_off()
    ax.set_aspect("equal")
    return fig, ax


def save(fig, relpath, pad=16):
    """保存并裁掉四周多余的空白，避免插图在版心里缩得太小。"""
    path = os.path.join(OUT_ROOT, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    buf.seek(0)

    from PIL import Image, ImageChops
    im = Image.open(buf).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 8 else 0)
    box = diff.getbbox()
    if box:
        left = max(box[0] - pad, 0)
        top = max(box[1] - pad, 0)
        right = min(box[2] + pad, im.width)
        bottom = min(box[3] + pad, im.height)
        im = im.crop((left, top, right, bottom))
    im.save(path, "PNG", optimize=True)
    print("saved", path, im.size)


# ------------------------------------------------------------------ 图形组件

def box(ax, x, y, w, h, text="", fc=WHITE, ec=INK, fs=9.5, bold=False,
        color=None, radius=1.2, lw=1.0, ha="center", va="center",
        align="center", pad=0.0, zorder=3):
    """圆角矩形。x,y 为左下角。"""
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle="round,pad=%s,rounding_size=%s" % (pad, radius),
                       linewidth=lw, edgecolor=ec, facecolor=fc, zorder=zorder)
    ax.add_patch(p)
    if text:
        tx = x + w / 2.0 if ha == "center" else x + 1.5
        ty = y + h / 2.0
        ax.text(tx, ty, text, ha=ha, va=va, fontsize=fs,
                fontweight="bold" if bold else "normal",
                color=color or INK, zorder=zorder + 1,
                linespacing=1.6)
    return p


def hbox(ax, x, y, w, h, text, **kw):
    return box(ax, x, y, w, h, text, **kw)


def arrow(ax, p1, p2=None, text=None, color=INK, lw=1.1, fs=8.8,
          style="-|>", rad=0.0, tpos=0.5, toff=(0, 1.6), zorder=2, ls="-"):
    if p2 is None:
        p1, p2 = (0, 0), p1
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=9,
                        linewidth=lw, color=color, zorder=zorder,
                        connectionstyle="arc3,rad=%s" % rad, linestyle=ls,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    if text:
        mx = p1[0] + (p2[0] - p1[0]) * tpos + toff[0]
        my = p1[1] + (p2[1] - p1[1]) * tpos + toff[1]
        ax.text(mx, my, text, ha="center", va="bottom", fontsize=fs,
                color=color, zorder=zorder + 1)


def elb_arrow(ax, p1, p2, text=None, color=INK, lw=1.1, fs=8.6, first="h",
              toff=(0, 1.4), zorder=2):
    """正交折线箭头，first 指定先水平还是先垂直。"""
    x1, y1 = p1
    x2, y2 = p2
    if first == "h":
        mid = (x2, y1)
    else:
        mid = (x1, y2)
    ax.plot([x1, mid[0]], [y1, mid[1]], color=color, lw=lw, zorder=zorder,
            solid_capstyle="butt")
    a = FancyArrowPatch(mid, (x2, y2), arrowstyle="-|>", mutation_scale=9,
                        linewidth=lw, color=color, zorder=zorder,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    if text:
        ax.text((x1 + x2) / 2.0 + toff[0], (y1 + y2) / 2.0 + toff[1], text,
                ha="center", va="bottom", fontsize=fs, color=color, zorder=zorder + 1)


def label(ax, x, y, text, fs=9.5, color=None, ha="center", va="center",
          bold=False, wrap=None, ha_align="center", style="normal", zorder=5):
    if wrap:
        text = "\n".join(textwrap.wrap(text, wrap))
    ax.text(x, y, text, fontsize=fs, ha=ha, va=va, color=color or INK,
            fontweight="bold" if bold else "normal", style=style,
            linespacing=1.55, zorder=zorder)


def dot(ax, x, y, r=0.9, color=INK, zorder=4):
    ax.add_patch(Circle((x, y), r, color=color, zorder=zorder))


def line(ax, p1, p2, color=GRAY, lw=1.0, ls="-", zorder=1):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=lw, ls=ls,
            zorder=zorder, solid_capstyle="round")


def brace(ax, x1, x2, y, text, color=GRAY, fs=8.6, height=1.6, upward=True):
    """水平花括号，用于标注一段范围。"""
    s = 1 if upward else -1
    ax.plot([x1, x1, (x1 + x2) / 2.0], [y, y + s * height, y + s * height],
            color=color, lw=0.9)
    ax.plot([x2, x2, (x1 + x2) / 2.0], [y, y + s * height, y + s * height],
            color=color, lw=0.9)
    ax.text((x1 + x2) / 2.0, y + s * (height + 1.6), text, ha="center",
            va="bottom" if upward else "top", fontsize=fs, color=color)


def lifeline(ax, x, top, bottom, name, color=ACCENT, fs=9.5, sub=None):
    """时序图的角色竖线。"""
    box(ax, x - 8.5, top - 5.2, 17, 5.2, name, fc=ACCENT_L, ec=color, fs=fs, bold=True)
    ax.plot([x, x], [top - 5.6, bottom], color=color, lw=0.8, ls=(0, (4, 3)))
    if sub:
        ax.text(x, bottom - 1.6, sub, ha="center", va="top", fontsize=8.2, color=GRAY)


def msg(ax, x1, x2, y, text, color=INK, fs=8.6, dash=False, above=True,
        ha="center", bold=False):
    """时序图消息：水平箭头 + 上方文字。"""
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.0,
                                shrinkA=3, shrinkB=3,
                                linestyle="--" if dash else "-"),
                zorder=3)
    ax.text((x1 + x2) / 2.0 if ha == "center" else (x1 + x2) / 2.0, y + 0.9,
            text, ha=ha, va="bottom", fontsize=fs, color=color,
            fontweight="bold" if bold else "normal", zorder=4)


def note(ax, x, y, text, fs=8.4, color=GRAY, ha="left", va="center", wrap=None):
    if wrap:
        text = "\n".join(textwrap.wrap(text, wrap))
    ax.text(x, y, text, fontsize=fs, color=color, ha=ha, va=va, linespacing=1.5)
