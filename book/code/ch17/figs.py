# -*- coding: utf-8 -*-
"""第 17 章插图：上传、下载与长任务。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

from figstyle import (ACCENT, ACCENT_L, GRAY, GRAY_L, GREEN, GREEN_L, INK, RED,
                      RED_L, WARM, WARM_L, WHITE, arrow, box, canvas, label,
                      lifeline, line, msg, note, save)


def tbox(ax, x, y, w, h, title, sub=None, fc=ACCENT_L, ec=INK, tfs=9.2, sfs=7.0):
    box(ax, x, y, w, h, fc=fc, ec=ec)
    if sub:
        label(ax, x + w / 2.0, y + h * 0.66, title, fs=tfs, bold=True)
        label(ax, x + w / 2.0, y + h * 0.26, sub, fs=sfs, color=GRAY)
    else:
        label(ax, x + w / 2.0, y + h / 2.0, title, fs=tfs, bold=True)


# ---------------------------------------------------------------- 图 17-1
fig, ax = canvas(7.4, 4.6, 100)
ax.set_ylim(0, 62)

label(ax, 2, 58.4, "同步：把三分钟的转换塞进一个请求", fs=9.0, bold=True, ha="left")
arrow(ax, (10, 50), (90, 50), lw=1.2)
label(ax, 30, 52.4, "POST /jobs，然后一直等", fs=7.8)
line(ax, (42, 46.5), (42, 54), color=RED, lw=1.0, ls=(0, (4, 3)))
label(ax, 43, 55.6, "代理 60 秒超时", fs=7.4, color=RED, ha="left")
label(ax, 66, 52.4, "请求已死，服务端还在跑", fs=7.4, color=GRAY)
label(ax, 10, 46.6, "请求开始", fs=7.0, color=GRAY)

label(ax, 2, 40.0, "异步：请求只负责下单，处理交给后台", fs=9.0, bold=True, ha="left")
tbox(ax, 2, 26, 15, 9, "POST /jobs", "立即返回", fc=ACCENT_L, ec=ACCENT, tfs=8.2, sfs=6.8)
tbox(ax, 21, 26, 15, 9, "202 + 任务号", "queued", fc=GRAY_L, ec=GRAY, tfs=8.0, sfs=6.8)
tbox(ax, 40, 26, 26, 9, "worker 在后台跑", "running，几分钟", fc=WARM_L, ec=WARM, tfs=8.2, sfs=6.8)
tbox(ax, 70, 26, 26, 9, "succeeded", "结果位置写进库", fc=GREEN_L, ec=GREEN, tfs=8.2, sfs=6.8)
for x1, x2 in ((17.4, 20.6), (36.4, 39.6), (66.4, 69.6)):
    arrow(ax, (x1, 30.5), (x2, 30.5), lw=1.0)

for x in (46.0, 52.0, 58.0):
    arrow(ax, (x, 20.8), (x, 25.4), lw=0.8, color=ACCENT, ls=(0, (2, 2)))
label(ax, 52.0, 17.6, "GET /jobs/42 轮询同一任务号", fs=7.2, color=ACCENT)
arrow(ax, (83.0, 25.4), (83.0, 20.6), lw=0.9, color=GREEN)
label(ax, 83.0, 17.8, "下载结果", fs=7.2, color=GREEN)

label(ax, 50, 8.0, "请求几毫秒就返回，任务状态存在库里，客户端随时可查、可重连。",
      fs=8.0, color=GRAY)

save(fig, "17/fig17_1.png")
# ---------------------------------------------------------------- 图 17-2
fig, ax = canvas(7.4, 4.6, 100)
ax.set_ylim(0, 62)

rows = [
    (48, "轮询", "客户端每隔一两秒问一次，实现最简单", ACCENT),
    (28, "SSE", "服务端在一条 HTTP 响应上持续推事件，断线自动重连", GREEN),
    (8, "WebSocket", "握手后升级成双向长连接，双方随时能发消息", WARM),
]
for y, name, desc, color in rows:
    box(ax, 2, y, 18, 9, fc=GRAY_L, ec=GRAY, lw=0.9)
    label(ax, 11, y + 5.6, "客户端", fs=8.4, bold=True)
    box(ax, 62, y, 18, 9, fc=WHITE, ec=color, lw=1.0)
    label(ax, 71, y + 5.6, "服务端", fs=8.4, bold=True)
    label(ax, 40, y + 13.0, name, fs=9.0, bold=True, color=color)
    label(ax, 40, y - 2.4, desc, fs=7.2, color=GRAY)

# 轮询：一次往返
arrow(ax, (20.4, 51.0), (61.6, 51.0), lw=0.9, color=ACCENT, ls=(0, (2, 2)))
arrow(ax, (61.6, 53.4), (20.4, 53.4), lw=0.9, color=ACCENT, ls=(0, (2, 2)))
label(ax, 41, 54.8, "问一次，答一次", fs=6.9, color=ACCENT)

# SSE：单向推
arrow(ax, (61.6, 32.5), (20.4, 32.5), lw=1.3, color=GREEN)
label(ax, 41, 33.9, "服务端单向推送", fs=6.9, color=GREEN)

# WebSocket：双向
arrow(ax, (20.4, 10.6), (61.6, 10.6), lw=1.1, color=WARM)
arrow(ax, (61.6, 14.0), (20.4, 14.0), lw=1.1, color=WARM)
label(ax, 41, 15.4, "两个方向都能发", fs=6.9, color=WARM)

label(ax, 50, 1.6, "任务少、进度慢就用轮询；只要推进度用 SSE；要交互才上 WebSocket。",
      fs=8.0, color=GRAY)

save(fig, "17/fig17_2.png")
