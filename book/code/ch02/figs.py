# -*- coding: utf-8 -*-
"""第 2 章插图：网络地基。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

from matplotlib.patches import Rectangle

from figstyle import (ACCENT, ACCENT_L, GRAY, GRAY_L, GREEN, GREEN_L, INK, RED,
                      RED_L, WARM, WARM_L, WHITE, arrow, box, brace, canvas,
                      elb_arrow, label, lifeline, line, msg, note, save)


def cell_col(ax, x, y, w, h, title, cells, ec, fc, fs=7.4, title_fs=7.8):
    """一列头部字段：顶部标题 + 若干等高分格。x,y 为左下角。"""
    th = 9.0
    box(ax, x, y + h - th, w, th, title, fc=fc, ec=ec, fs=title_fs,
        bold=True, radius=0.7, lw=0.9)
    gap = 1.5
    n = len(cells)
    ch = (h - th - gap - gap * (n - 1)) / n
    for i, t in enumerate(cells):
        cy = y + h - th - gap - (i + 1) * ch - i * gap
        box(ax, x + 1.2, cy, w - 2.4, ch, t, fc=WHITE, ec=ec, fs=fs,
            radius=0.5, lw=0.7, color=INK)


# ---------------------------------------------------------------- 图 2-1
fig, ax = canvas(7.4, 3.63, 200)
ax.set_ylim(0, 98)

# 从外到内：以太网帧 → IP 包 → TCP 段 → 应用数据
box(ax, 6, 8, 188, 88, fc=WHITE, ec=GRAY, lw=1.3, radius=2.2)
box(ax, 44, 14, 128, 76, fc=WHITE, ec=ACCENT, lw=1.3, radius=2.0)
box(ax, 84, 20, 84, 64, fc=WHITE, ec=WARM, lw=1.3, radius=1.8)
box(ax, 124, 26, 40, 52, "应用数据\nSSH 字节流", fc=GREEN_L, ec=GREEN,
    fs=8.2, radius=1.2, lw=1.1)

# 以太网头：目的 MAC / 源 MAC / 类型
cell_col(ax, 10, 29, 32, 46, "以太网头 14 B",
         ["目的 MAC", "源 MAC", "类型"], GRAY, GRAY_L)
# 帧尾校验
box(ax, 178, 38, 14, 28, "尾部\n校验\n4 B", fc=GRAY_L, ec=GRAY, fs=7.4,
    radius=0.8, lw=0.9)
# IPv4 头：版本 / 源 IP / 目的 IP
cell_col(ax, 48, 24, 32, 63, "IPv4 头 20 B",
         ["版本、头长", "源 IP", "目的 IP", "…"], ACCENT, ACCENT_L)
# TCP 头：源端口 / 目的端口 / 序号
cell_col(ax, 88, 28, 32, 52, "TCP 头 20 B",
         ["源端口", "目的端口", "序号", "…"], WARM, WARM_L)

# 层名称：贴在各矩形内左下角
label(ax, 8.5, 12.6, "以太网帧", fs=7.6, color=GRAY, ha="left")
label(ax, 46.5, 18.6, "IP 包", fs=7.6, color=ACCENT, ha="left")
label(ax, 86.5, 23.6, "TCP 段", fs=7.6, color=WARM, ha="left")

label(ax, 100, 3.2,
      "从外到内依次套住：以太网帧、IP 包、TCP 段、应用数据；"
      "每层只在前方加一个头部，帧尾再加 4 字节校验",
      fs=7.4, color=GRAY)

save(fig, "02/fig02_3.png")

# ---------------------------------------------------------------- 图 2-2
fig, ax = canvas(7.0, 5.0, 100)
ax.set_ylim(0, 71.4)

# 三个角色
box(ax, 2, 42, 24, 24, fc=ACCENT_L, ec=ACCENT, lw=1.1, radius=1.4)
label(ax, 14, 60.0, "内网主机", fs=9.2, bold=True)
label(ax, 14, 54.4, "192.168.1.23", fs=7.8)
label(ax, 14, 49.6, "端口 51544", fs=7.8)
label(ax, 14, 45.2, "私有地址", fs=6.8, color=GRAY)

box(ax, 36, 42, 28, 24, fc=WARM_L, ec=WARM, lw=1.1, radius=1.4)
label(ax, 50, 60.0, "路由器 / 云网关", fs=8.8, bold=True)
label(ax, 50, 54.6, "改写地址与端口", fs=7.6, color=WARM)
label(ax, 50, 50.2, "并记住这条映射", fs=7.6, color=WARM)
label(ax, 50, 45.8, "回包时再换回去", fs=7.6, color=WARM)

box(ax, 74, 42, 25, 24, fc=GREEN_L, ec=GREEN, lw=1.1, radius=1.4)
label(ax, 86.5, 60.0, "JumpServer", fs=9.0, bold=True)
label(ax, 86.5, 54.4, "124.221.133.165", fs=7.0)
label(ax, 86.5, 49.6, "端口 58222", fs=7.0)
label(ax, 86.5, 45.2, "公网地址", fs=6.8, color=GRAY)

# 出方向（实线，深蓝）
arrow(ax, (26.2, 58), (35.7, 58), color=ACCENT, lw=1.2)
label(ax, 31.0, 59.0, "源端口\n51544", fs=6.8, color=ACCENT, va="bottom")
arrow(ax, (64.3, 58), (73.7, 58), color=ACCENT, lw=1.2)
label(ax, 69.0, 59.0, "源端口\n40001", fs=6.8, color=ACCENT, va="bottom")

# 回方向（虚线，绿色）
arrow(ax, (73.7, 48), (64.3, 48), color=GREEN, lw=1.2, ls="--")
label(ax, 69.0, 49.0, "目的端口\n40001", fs=6.8, color=GREEN, va="bottom")
arrow(ax, (35.7, 48), (26.2, 48), color=GREEN, lw=1.2, ls="--")
label(ax, 31.0, 49.0, "目的端口\n51544", fs=6.8, color=GREEN, va="bottom")

# 图例
line(ax, (4, 69.4), (10, 69.4), color=ACCENT, lw=1.3)
label(ax, 11.2, 69.4, "出方向：改写源地址与源端口", fs=7.0, color=ACCENT, ha="left")
line(ax, (47, 69.4), (53, 69.4), color=GREEN, lw=1.3, ls="--")
label(ax, 54.2, 69.4, "回方向：按表改写目的地址与端口", fs=7.0, color=GREEN, ha="left")

# 网关向下连到表
arrow(ax, (50, 41.4), (50, 33.0), color=WARM, lw=1.0)
label(ax, 51.4, 37.0, "每条连接一条记录", fs=7.2, color=WARM, ha="left")

# NAT 表：直角表格，逐格着色
cols = [(2, 32), (34, 28), (62, 37)]
heads = ["内网侧看到的", "公网侧看到的", "对端 JumpServer"]
bodies = ["192.168.1.23\n端口 51544", "203.0.113.7\n端口 40001",
          "124.221.133.165\n端口 58222"]
fcs = [ACCENT_L, WARM_L, GREEN_L]
ecs = [ACCENT, WARM, GREEN]

for (x, w), head, body, fc, ec in zip(cols, heads, bodies, fcs, ecs):
    ax.add_patch(Rectangle((x, 24), w, 8, facecolor=fc, edgecolor=ec,
                           lw=1.0, zorder=3))
    ax.add_patch(Rectangle((x, 10), w, 14, facecolor=WHITE, edgecolor=ec,
                           lw=1.0, zorder=3))
    ax.text(x + w / 2.0, 28, head, ha="center", va="center", fontsize=7.4,
            fontweight="bold", zorder=4)
    ax.text(x + w / 2.0, 17, body, ha="center", va="center", fontsize=8.2,
            linespacing=1.7, zorder=4)

label(ax, 50, 5.4, "网关为这条连接分配了公网端口 40001：出方向改源、回方向改目的",
      fs=7.4, color=GRAY)
label(ax, 50, 1.6, "对外只有 203.0.113.7 这一个地址，内网主机并不直接暴露",
      fs=7.4, color=GRAY)

save(fig, "02/fig02_1.png")

# ---------------------------------------------------------------- 图 2-3
fig, ax = canvas(7.0, 5.2, 100)
ax.set_ylim(0, 74.3)

lifeline(ax, 20, 70, 6, "客户端", sub="你的 ssh")
lifeline(ax, 80, 70, 6, "服务器", color=GREEN, sub="sshd")

label(ax, 2.5, 66.5, "建立连接", fs=9.4, bold=True, color=ACCENT, ha="left")

msg(ax, 20, 80, 60, "SYN，seq = x", color=ACCENT)
msg(ax, 80, 20, 53.5, "SYN + ACK，seq = y，ack = x + 1", color=ACCENT)
msg(ax, 20, 80, 47, "ACK，seq = x + 1，ack = y + 1", color=ACCENT)

label(ax, 2.5, 39.0, "断开连接", fs=9.4, bold=True, color=WARM, ha="left")

msg(ax, 20, 80, 33, "FIN，seq = u", color=WARM)
msg(ax, 80, 20, 26.5, "ACK，ack = u + 1", color=WARM)
msg(ax, 80, 20, 20, "FIN，seq = v", color=WARM)
msg(ax, 20, 80, 13.5, "ACK，ack = v + 1", color=WARM)

# TIME_WAIT 标注：贴在客户端 lifeline 下方右侧
line(ax, (17.4, 12.6), (17.4, 5.2), color=WARM, lw=0.9)
label(ax, 18.6, 9.6, "TIME_WAIT：等 2×MSL 才真正关闭", fs=7.0, color=WARM, ha="left")
label(ax, 50, 1.4, "握手三步确认双方的收发都正常；挥手四步是各自关掉自己这个方向",
      fs=7.4, color=GRAY)

save(fig, "02/fig02_2.png")
