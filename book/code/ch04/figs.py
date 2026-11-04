# -*- coding: utf-8 -*-
"""第 4 章插图：密码学。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

from matplotlib.patches import Circle, Rectangle

from figstyle import (ACCENT, ACCENT_L, GRAY, GRAY_L, GREEN, GREEN_L, INK, RED,
                      RED_L, WARM, WARM_L, WHITE, arrow, box, brace, canvas,
                      elb_arrow, label, lifeline, line, msg, note, save)


def key_icon(ax, x, y, color, scale=1.0, lw=1.4):
    """在 (x, y) 画一把横放的钥匙，y 是钥匙的中轴高度。"""
    r = 1.9 * scale
    ax.add_patch(Circle((x, y), r, facecolor=WHITE, edgecolor=color,
                        lw=lw, zorder=6))
    ax.plot([x + r, x + r + 7.5 * scale], [y, y], color=color, lw=lw + 0.4,
            zorder=6, solid_capstyle="round")
    for dx in (5.4, 6.6):
        ax.plot([x + dx * scale, x + dx * scale], [y, y - 2.2 * scale],
                color=color, lw=lw, zorder=6, solid_capstyle="round")


# ---------------------------------------------------------------- 图 4-1
fig, ax = canvas(7.2, 3.31, 100)
ax.set_ylim(0, 46)

by, bh = 17.0, 13.0
box(ax, 1, by, 14, bh, "明文", fc=GRAY_L, ec=GRAY, fs=8.6, lw=1.0)
box(ax, 19, by - 0.5, 16, bh + 1, "加密", fc=ACCENT_L, ec=ACCENT, fs=9.0,
    bold=True, lw=1.1)
box(ax, 38, by + 1.5, 26, bh - 3, "网络上\n只有密文", fc=GRAY_L, ec=GRAY,
    fs=8.0, lw=1.0)
box(ax, 67, by - 0.5, 16, bh + 1, "解密", fc=WARM_L, ec=WARM, fs=9.0,
    bold=True, lw=1.1)
box(ax, 86, by, 13, bh, "明文", fc=GRAY_L, ec=GRAY, fs=8.6, lw=1.0)

arrow(ax, (15.4, 23.5), (18.6, 23.5))
arrow(ax, (35.4, 23.5), (37.6, 23.5))
arrow(ax, (64.4, 23.5), (66.6, 23.5))
arrow(ax, (83.4, 23.5), (85.6, 23.5))

label(ax, 50, 40.2, "同一把密钥", fs=8.2, bold=True, color=ACCENT)
key_icon(ax, 44.5, 35.4, ACCENT, scale=1.0)
ax.plot([45.2, 27.0], [33.0, 31.0], color=ACCENT, lw=0.9, ls=(0, (3, 3)))
ax.plot([49.6, 75.0], [33.0, 31.0], color=ACCENT, lw=0.9, ls=(0, (3, 3)))

label(ax, 27, 14.2, "用它加密", fs=7.2, color=ACCENT)
label(ax, 75, 14.2, "还是用它解密", fs=7.2, color=WARM)

label(ax, 50, 8.2, "发送方和接收方必须先有同一个秘密", fs=7.6, color=GRAY)
label(ax, 50, 3.2, "于是问题变成：这把钥匙本身怎么安全地交到对方手里", fs=7.6,
      color=GRAY)

save(fig, "04/fig04_1.png")

# ---------------------------------------------------------------- 图 4-2
fig, ax = canvas(7.2, 5.04, 100)
ax.set_ylim(0, 70)

panels = [
    (2, "① 加密：把秘密送过去", "谁都能加密，只有收方能解开", ACCENT),
    (52, "② 签名：证明是我发的", "谁都能验证，只有本人能签", WARM),
]
steps = [
    [("明文", "会话密钥、文件内容", GRAY_L, GRAY),
     ("用收方的公钥加密", "公钥可以随便公开", ACCENT_L, ACCENT),
     ("密文", "经由网络送到对方", GRAY_L, GRAY),
     ("用收方自己的私钥解密", "私钥只有收方知道", WARM_L, WARM),
     ("明文", "", GRAY_L, GRAY)],
    [("消息", "谁都能读，不需要保密", GRAY_L, GRAY),
     ("用发送方自己的私钥签名", "私钥只有发送方知道", WARM_L, WARM),
     ("签名值", "和消息一起发出去", GRAY_L, GRAY),
     ("用发送方的公钥验证", "公钥可以随便公开", ACCENT_L, ACCENT),
     ("通过：确实是本人发的", "", GREEN_L, GREEN)],
]

ax.plot([49.5, 49.5], [6, 60], color=GRAY_L, lw=1.0, ls=(0, (2, 3)))

BH = 7.6
for (px, title, sub, tc), col in zip(panels, steps):
    label(ax, px + 23, 66.0, title, fs=9.2, bold=True, color=tc, ha="left")
    label(ax, px + 23, 61.4, sub, fs=7.2, color=GRAY, ha="left")
    y = 52.0
    for i, (t, s, fc, ec) in enumerate(col):
        box(ax, px + 3, y, 40, BH, fc=fc, ec=ec, lw=1.0)
        label(ax, px + 23, y + BH / 2 + (0.9 if s else 0), t, fs=8.4,
              bold=True, color=INK)
        if s:
            label(ax, px + 23, y + BH / 2 - 2.2, s, fs=6.8, color=GRAY)
        if i < 4:
            arrow(ax, (px + 23, y - 0.3), (px + 23, y - 3.3), color=tc, lw=1.0)
        y -= 11.2

# 钥匙颜色说明
key_icon(ax, 26, 3.4, ACCENT, scale=0.72, lw=1.2)
label(ax, 36.5, 3.4, "公钥：可以公开", fs=7.4, color=ACCENT, ha="left")
key_icon(ax, 60, 3.4, WARM, scale=0.72, lw=1.2)
label(ax, 70.5, 3.4, "私钥：只有自己知道", fs=7.4, color=WARM, ha="left")

save(fig, "04/fig04_2.png")

# ---------------------------------------------------------------- 图 4-3
fig, ax = canvas(7.2, 4.3, 100)
ax.set_ylim(0, 59.7)

label(ax, 2, 55.0, "阶段一　握手：用非对称把会话密钥送过去", fs=8.8, bold=True,
      color=ACCENT, ha="left")

row1 = [("服务器发出公钥", "连同证书一起", ACCENT_L, ACCENT),
        ("客户端生成会话密钥", "一串随机数", GRAY_L, GRAY),
        ("用公钥加密后发出", "网络上是密文", ACCENT_L, ACCENT),
        ("服务器用私钥解开", "双方都拿到密钥", WARM_L, WARM)]
for i, (t, s, fc, ec) in enumerate(row1):
    bx = 1 + i * 24.6
    box(ax, bx, 40, 21.2, 10.4, t + "\n" + s, fc=fc, ec=ec, fs=7.4, lw=1.0)
    if i < 3:
        arrow(ax, (bx + 21.5, 45.2), (bx + 24.2, 45.2))

ax.plot([2, 98], [33.5, 33.5], color=GRAY, lw=0.9, ls=(0, (4, 3)))
label(ax, 2, 35.4, "切换：此后不再用非对称，全部改用这把会话密钥", fs=7.4, color=GRAY,
      ha="left")

label(ax, 2, 28.0, "阶段二　传输：用会话密钥做对称加密", fs=8.8, bold=True,
      color=GREEN, ha="left")

row2 = [("双方都持有会话密钥", "只在这次连接里有效", GREEN_L, GREEN),
        ("数据用它加密", "速度比非对称快得多", GREEN_L, GREEN),
        ("抓包只能看到密文", "换一条连接就换一把", GRAY_L, GRAY)]
for i, (t, s, fc, ec) in enumerate(row2):
    bx = 1 + i * 33.0
    box(ax, bx, 13.0, 30, 10.4, t + "\n" + s, fc=fc, ec=ec, fs=7.4, lw=1.0)
    if i < 2:
        arrow(ax, (bx + 30.3, 18.2), (bx + 32.7, 18.2))

label(ax, 50, 5.6, "非对称解决“钥匙怎么送过去”，对称解决“数据够不够快”，各管一段",
      fs=7.6, color=GRAY)

save(fig, "04/fig04_3.png")

# ---------------------------------------------------------------- 图 4-4
fig, ax = canvas(7.2, 3.6, 100)
ax.set_ylim(0, 50)

box(ax, 2, 30, 24, 14, fc=ACCENT_L, ec=ACCENT, lw=1.1, radius=1.2)
label(ax, 14, 39.6, "甲", fs=9.4, bold=True)
label(ax, 14, 35.2, "自己选一个私钥 a", fs=7.4, color=ACCENT)

box(ax, 74, 30, 24, 14, fc=WARM_L, ec=WARM, lw=1.1, radius=1.2)
label(ax, 86, 39.6, "乙", fs=9.4, bold=True)
label(ax, 86, 35.2, "自己选一个私钥 b", fs=7.4, color=WARM)

arrow(ax, (26.4, 40.8), (73.6, 40.8), color=ACCENT)
label(ax, 50, 41.8, "发出 $g^a$（a 自己留着）", fs=7.6, color=ACCENT, va="bottom")
arrow(ax, (73.6, 33.6), (26.4, 33.6), color=WARM)
label(ax, 50, 34.6, "发出 $g^b$（b 自己留着）", fs=7.6, color=WARM, va="bottom")

box(ax, 2, 10, 24, 12, "算出 $g^{ba}$", fc=WHITE, ec=ACCENT, fs=9.2, lw=1.0,
    radius=1.2)
box(ax, 74, 10, 24, 12, "算出 $g^{ab}$", fc=WHITE, ec=WARM, fs=9.2, lw=1.0,
    radius=1.2)
arrow(ax, (14, 29.6), (14, 22.4), color=ACCENT)
arrow(ax, (86, 29.6), (86, 22.4), color=WARM)

label(ax, 50, 17.4, "两边算出同一个值", fs=8.4, bold=True)
label(ax, 50, 12.4, "$g^{ab} = g^{ba}$，这就是会话密钥", fs=8.0, color=GRAY)

label(ax, 50, 3.8, "窃听者看得到 g、$g^a$、$g^b$，但由它们反推出 a 或 b 极难",
      fs=7.6, color=GRAY)

save(fig, "04/fig04_4.png")
