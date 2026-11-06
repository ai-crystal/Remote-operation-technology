# -*- coding: utf-8 -*-
"""第 16 章插图：端口、监听与 HTTP。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

from figstyle import (ACCENT, ACCENT_L, GRAY, GRAY_L, GREEN, GREEN_L, INK, RED,
                      RED_L, WARM, WARM_L, WHITE, arrow, box, canvas, label,
                      line, note, save)


def tbox(ax, x, y, w, h, title, sub=None, fc=ACCENT_L, ec=INK, tfs=9.2, sfs=7.2):
    box(ax, x, y, w, h, fc=fc, ec=ec)
    if sub:
        label(ax, x + w / 2.0, y + h * 0.66, title, fs=tfs, bold=True)
        label(ax, x + w / 2.0, y + h * 0.26, sub, fs=sfs, color=GRAY)
    else:
        label(ax, x + w / 2.0, y + h / 2.0, title, fs=tfs, bold=True)


# ---------------------------------------------------------------- 图 16-1
fig, ax = canvas(7.4, 4.0, 100)

tbox(ax, 3, 33, 30, 12, "监听套接字", "0.0.0.0:8000", fc=ACCENT_L, ec=ACCENT, sfs=7.0)
label(ax, 18, 28.6, "只接客，不传数据", fs=7.6, color=GRAY)
label(ax, 18, 25.2, "内核替它排队", fs=7.6, color=GRAY)

conns = [(43, "连接 A", "accept 得到的新套接字"),
         (25, "连接 B", "各有一条，互不干扰"),
         (7, "连接 C", "客户端断开发起新连接")]
for y, name, sub in conns:
    tbox(ax, 55, y, 26, 10, name, None, fc=GREEN_L, ec=GREEN, tfs=8.8)
    label(ax, 68, y + 3.2, sub, fs=6.9, color=GRAY)
    arrow(ax, (33.4, 39), (54.6, y + 5), lw=1.0, color=ACCENT)
    label(ax, 44, y + 6.0, "accept", fs=6.8, color=ACCENT)

tbox(ax, 86, 24, 13, 11, "客户端们", "各自一条", fc=WHITE, tfs=8.4, sfs=6.8)
for y in (43, 25, 7):
    arrow(ax, (85.6, 30), (81.2, y + 5), lw=0.9, color=GRAY)

label(ax, 50, 1.8, "一个监听套接字可以接受很多条连接；数据只在各自那条连接上跑。",
      fs=8.2, color=GRAY)

save(fig, "16/fig16_1.png")

# ---------------------------------------------------------------- 图 16-2
fig, ax = canvas(7.4, 3.6, 100)

nodes = [
    (1.0, 15, "客户端", "curl / 播放器", GRAY_L, GRAY),
    (20.0, 15, "公网入口", "IP 与端口", GRAY_L, GRAY),
    (39.0, 17, "安全组 / 防火墙", "放不放行", RED_L, RED),
    (60.0, 16, "反向代理", "TLS 终止 443", ACCENT_L, ACCENT),
    (80.0, 18, "应用进程", "127.0.0.1:8000", GREEN_L, GREEN),
]
for x, w, title, sub, fc, ec in nodes:
    tbox(ax, x, 20, w, 12, title, sub, fc=fc, ec=ec, tfs=8.6, sfs=6.9)

for x1, x2 in ((16.2, 19.8), (35.2, 38.8), (56.2, 59.8), (76.2, 79.8)):
    arrow(ax, (x1, 26), (x2, 26), lw=1.0)

label(ax, 8.5, 15.5, "发起连接", fs=7.2, color=GRAY)
label(ax, 27.5, 15.5, "找得到这台机器", fs=7.2, color=GRAY)
label(ax, 47.5, 15.5, "挡在这里最常见", fs=7.2, color=RED)
label(ax, 68.0, 15.5, "证书、转发、限流", fs=7.2, color=ACCENT)
label(ax, 89.0, 15.5, "只监听回环", fs=7.2, color=GREEN)

box(ax, 80.0, 5.0, 18, 8.0, fc=WHITE, ec=GREEN, lw=0.9)
label(ax, 89.0, 10.6, "数据库 / 队列", fs=7.6)
label(ax, 89.0, 7.2, "任务与状态", fs=6.9, color=GRAY)
arrow(ax, (89.0, 19.6), (89.0, 13.4), lw=0.9, color=GREEN)

label(ax, 50, 1.6, "任何一层不通，外面看到的现象都一样：连不上。所以要一层一层验证。",
      fs=8.2, color=GRAY)

save(fig, "16/fig16_2.png")
