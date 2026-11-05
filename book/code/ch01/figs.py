# -*- coding: utf-8 -*-
"""第 1 章插图：计算机之间怎么通信。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

from figstyle import (ACCENT, ACCENT_L, GRAY, GRAY_L, GREEN, GREEN_L, INK, RED,
                      RED_L, WARM, WARM_L, WHITE, arrow, box, canvas, label,
                      line, note, save)

# ---------------------------------------------------------------- 图 1-1
fig, ax = canvas(7.4, 3.2, 100)

box(ax, 1.5, 6.0, 55.0, 32.0, fc="#f7f9fb", ec="#c9d4dc", lw=1.0, radius=1.6)
label(ax, 29.0, 40.0, "局域网，地址都在 192.168.1.x 这一段", fs=8.4, color=GRAY)

pcs = [(27.5, "电脑 A", "192.168.1.23"), (16.5, "电脑 B", "192.168.1.24"),
       (8.0, "电脑 C", "192.168.1.25")]
for y, name, ip in pcs:
    box(ax, 5.0, y, 15.0, 7.6, fc=ACCENT_L, ec=ACCENT)
    label(ax, 12.5, y + 4.9, name, fs=8.2, bold=True)
    label(ax, 12.5, y + 2.2, ip, fs=6.9, color=GRAY)
    line(ax, (20.4, y + 3.8), (28.6, 21.0), color=INK, lw=0.9)
    arrow(ax, (28.6, 21.0), (30.4, 21.0), lw=0.9)

box(ax, 31.0, 16.8, 14.0, 8.4, fc=WHITE, ec=INK)
label(ax, 38.0, 22.4, "交换机", fs=9.2, bold=True)
label(ax, 38.0, 19.0, "按地址转发", fs=7.2, color=GRAY)

box(ax, 62.0, 16.8, 15.0, 8.4, fc=WARM_L, ec=WARM)
label(ax, 69.5, 22.4, "路由器", fs=9.2, bold=True)
label(ax, 69.5, 19.0, "网关 192.168.1.1", fs=7.0, color=GRAY)

arrow(ax, (45.4, 21.0), (61.6, 21.0), lw=0.9)
label(ax, 53.4, 22.8, "出网段", fs=7.4, color=GRAY)

box(ax, 82.0, 16.2, 16.0, 9.6, fc=GRAY_L, ec=GRAY)
label(ax, 90.0, 22.2, "互联网", fs=9.2, bold=True)
label(ax, 90.0, 18.6, "别的网络", fs=7.2, color=GRAY)

arrow(ax, (77.4, 21.0), (81.6, 21.0), lw=0.9)

label(ax, 50.0, 1.6, "同一网段内由交换机直接转发，出了网段交给网关",
      fs=8.0, color=GRAY)
save(fig, "01/fig01_1.png")

# ---------------------------------------------------------------- 图 1-2
fig, ax = canvas(7.4, 2.2, 100)

ys, h = 8.0, 11.0
box(ax, 1.5, ys, 17.0, h, "程序的数据", fc=GRAY_L, ec=GRAY, fs=8.6)
box(ax, 23.0, ys, 22.0, h, "切块，写上收发地址", fc=ACCENT_L, ec=ACCENT, fs=8.6)
box(ax, 49.5, ys, 13.0, h, "网卡", fc=WHITE, ec=INK, fs=8.6)
box(ax, 67.0, ys, 15.0, h, "线路上的信号", fc=WARM_L, ec=WARM, fs=8.6)
box(ax, 86.5, ys, 12.0, h, "对端网卡", fc=WHITE, ec=INK, fs=8.6)

for x1, x2 in ((18.9, 22.6), (45.4, 49.1), (62.9, 66.6), (82.4, 86.1)):
    arrow(ax, (x1, ys + h / 2), (x2, ys + h / 2), lw=0.9)

label(ax, 32.0, 22.4, "发送方", fs=8.4, color=GRAY)
label(ax, 92.5, 22.4, "接收方", fs=8.4, color=GRAY)
line(ax, (63.8, 4.6), (63.8, 24.6), color=GRAY, lw=0.6, ls=(0, (3, 3)))
line(ax, (84.0, 4.6), (84.0, 24.6), color=GRAY, lw=0.6, ls=(0, (3, 3)))

label(ax, 72.0, 2.2, "线路这一段只搬信号", fs=7.6, color=WARM)
label(ax, 50, 26.6, "线路上的设备只看地址，不看内容；到了对端再拼回原来的数据",
      fs=7.8, color=GRAY)
save(fig, "01/fig01_2.png")

# ---------------------------------------------------------------- 图 1-3
fig, ax = canvas(7.4, 2.6, 100)

ys, h = 9.0, 10.0
nodes = [
    (1.5, 15.0, "你的电脑", "192.168.1.23", ACCENT_L, ACCENT),
    (21.0, 17.0, "家用路由器", "网关，做地址转换", WARM_L, WARM),
    (43.0, 16.0, "运营商", "骨干网与光缆", GRAY_L, GRAY),
    (64.0, 16.0, "数据中心", "机房的路由器", GRAY_L, GRAY),
    (84.5, 14.0, "服务器", "198.51.100.17", GREEN_L, GREEN),
]
for x, w, title, sub, fc, ec in nodes:
    box(ax, x, ys, w, h, fc=fc, ec=ec)
    label(ax, x + w / 2, ys + h - 3.4, title, fs=8.4, bold=True)
    label(ax, x + w / 2, ys + 3.0, sub, fs=6.9, color=GRAY)

for x1, x2 in ((16.9, 20.6), (38.4, 42.6), (59.4, 63.6), (80.4, 84.1)):
    arrow(ax, (x1, ys + h / 2), (x2, ys + h / 2), lw=0.9)

label(ax, 50, 23.4, "包一站一站往目的地送，每一站只决定下一步交给谁",
      fs=7.9, color=GRAY)
label(ax, 50, 3.4, "内网地址在网关处换成公网地址，外部看不到你局域网里的设备",
      fs=7.9, color=GRAY)
save(fig, "01/fig01_3.png")
