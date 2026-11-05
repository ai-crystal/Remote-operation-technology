# -*- coding: utf-8 -*-
"""第 9 章插图：VPN：把一整张内网搬到身边。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

from figstyle import (ACCENT, ACCENT_L, GRAY, GRAY_L, GREEN, GREEN_L, INK, RED,
                      RED_L, WARM, WARM_L, WHITE, arrow, box, canvas, label,
                      lifeline, line, msg, note, save)
from matplotlib.patches import Rectangle


def tbox(ax, x, y, w, h, title, sub=None, fc=ACCENT_L, ec=INK, tfs=9.2, sfs=7.4):
    box(ax, x, y, w, h, fc=fc, ec=ec)
    if sub:
        label(ax, x + w / 2.0, y + h * 0.66, title, fs=tfs, bold=True)
        label(ax, x + w / 2.0, y + h * 0.27, sub, fs=sfs, color=GRAY)
    else:
        label(ax, x + w / 2.0, y + h / 2.0, title, fs=tfs, bold=True)


def over(ax, x, y, text, fs=7.4, color=None, mono=False):
    ax.text(x, y + 2.0, text, ha="center", va="bottom", fontsize=fs,
            color=color or INK, zorder=7,
            family="monospace" if mono else None)


# ---------------------------------------------------------------- 图 9-1
fig, ax = canvas(7.4, 4.4, 100)

tbox(ax, 1, 30, 14, 12, "浏览器", "连 10.0.0.9", fc=GRAY_L, tfs=9.0, sfs=7.2)
tbox(ax, 22, 30, 17, 12, "虚拟网卡", "wg0  10.8.0.2", fc=ACCENT_L, ec=ACCENT, sfs=7.0)
tbox(ax, 46, 30, 15, 12, "物理网卡", "eth0", fc=WARM_L, ec=WARM, sfs=7.2)
tbox(ax, 68, 30, 15, 12, "VPN 网关", "203.0.113.61", fc=GREEN_L, ec=GREEN, sfs=6.6)
tbox(ax, 88, 30, 11, 12, "内网服务", "10.0.0.9", fc=WHITE, tfs=8.4, sfs=7.0)

arrow(ax, (15, 36), (22, 36), lw=1.0)
over(ax, 18.5, 36, "原包", fs=7.0, color=GRAY)
arrow(ax, (39, 36), (46, 36), lw=1.5, color=ACCENT)
over(ax, 42.5, 36, "加密", fs=7.0, color=ACCENT)
arrow(ax, (61, 36), (68, 36), lw=1.2, color=ACCENT)
over(ax, 64.5, 36, "隧道", fs=7.0, color=ACCENT)
arrow(ax, (83, 36), (88, 36), lw=1.0)
over(ax, 85.5, 36, "原包", fs=6.8, color=GRAY)

box(ax, 1, 14, 19, 9, fc=GRAY_L, ec=GRAY, lw=0.8)
label(ax, 10.5, 20.4, "路由表", fs=8.6, bold=True)
label(ax, 10.5, 16.6, "10.0.0.0/8 → wg0", fs=7.2)
ax.plot([10.5, 10.5], [23.0, 26.0], color=ACCENT, lw=0.9, ls=(0, (3, 2)))
ax.plot([10.5, 20.6], [26.0, 26.0], color=ACCENT, lw=0.9, ls=(0, (3, 2)))
arrow(ax, (19.2, 26.0), (22.0, 29.6), color=ACCENT, lw=0.9, ls=(0, (3, 2)))

label(ax, 30.5, 26.6, "② 加一块虚拟网卡", fs=8.0, color=ACCENT)
label(ax, 10.5, 10.6, "③ 改路由", fs=8.0, color=ACCENT)
label(ax, 64.5, 26.6, "① 建隧道", fs=8.0, color=ACCENT)

label(ax, 1, 5.2, "程序什么都没改：它仍然在连 10.0.0.9，包是操作系统和客户端替它改道的。",
      fs=8.4, color=GRAY, ha="left")

save(fig, "09/fig09_1.png")

# ---------------------------------------------------------------- 图 9-2
fig, ax = canvas(7.4, 3.9, 100)

def bar(ax, x, y, w, texts, fcs, h=9.0, fs=7.6):
    """一排相邻的字段块。texts 为空串的块不写字。"""
    cx = x
    for (t, wi, fc) in zip(texts, w, fcs):
        box(ax, cx, y, wi, h, fc=fc, radius=0.6, lw=0.8)
        if t:
            label(ax, cx + wi / 2.0, y + h / 2.0, t, fs=fs)
        cx += wi
    return cx


label(ax, 2, 45.2, "① 要发的包", fs=8.6, bold=True, ha="left")
bar(ax, 2, 34, [19, 11, 30],
    ["IP 头\n10.8.0.2 → 10.0.0.9", "TCP 头", "数据"],
    [GRAY_L, GRAY_L, WHITE], fs=7.4)

label(ax, 2, 30.2, "② 客户端把它整体加密", fs=8.6, bold=True, ha="left")
bar(ax, 2, 19, [60], ["密文：原包一个字节没少，只是看不见了"], [ACCENT_L], fs=7.6)

label(ax, 2, 15.2, "③ 再套上能上公网的头", fs=8.6, bold=True, ha="left")
bar(ax, 2, 4, [21, 10, 13, 16],
    ["新 IP 头\n你的地址 → 网关", "UDP", "隧道头", "密文"],
    [WARM_L, WARM_L, WARM_L, ACCENT_L], fs=7.0)

box(ax, 66, 28, 32, 13, fc=WHITE, ec=GRAY, lw=0.8)
label(ax, 82, 36.6, "每个包多出一段", fs=8.4, bold=True)
label(ax, 82, 31.8, "60～80 字节", fs=8.0, color=WARM)

box(ax, 66, 12, 32, 13, fc=WHITE, ec=GRAY, lw=0.8)
label(ax, 82, 20.6, "隧道 MTU 要调小", fs=8.4, bold=True)
label(ax, 82, 15.8, "1500 → 1400 左右", fs=8.0, color=WARM)

label(ax, 50, 1.2, "同一份数据，越往外走头越多；中间设备只看得见最外面那一层。",
      fs=8.0, color=GRAY)

save(fig, "09/fig09_2.png")

# ---------------------------------------------------------------- 图 9-3
fig, ax = canvas(7.4, 3.8, 100)

def routing(ax, x, w, title, rows, note_text, hi):
    label(ax, x + w / 2.0, 42.2, title, fs=9.2, bold=True)
    box(ax, x, 18.0, w, 21.5, fc=WHITE, ec=GRAY, lw=0.9, radius=0.8)
    ax.text(x + 3.0, 35.6, "目的网段", ha="left", va="center",
            fontsize=7.4, color=GRAY, zorder=6)
    ax.text(x + w - 3.0, 35.6, "出口", ha="right", va="center",
            fontsize=7.4, color=GRAY, zorder=6)
    ax.plot([x + 2.4, x + w - 2.4], [33.4, 33.4], color=GRAY_L, lw=0.8)
    y = 30.4
    for dest, dev, mark in rows:
        if mark and dest.startswith("0.0.0.0"):
            ax.add_patch(Rectangle((x + 1.2, y - 2.4), w - 2.4, 4.8,
                                   facecolor=ACCENT_L, edgecolor="none", zorder=5))
        ax.text(x + 3.0, y, dest, ha="left", va="center", fontsize=7.8,
                family="monospace", color=INK, zorder=6)
        ax.text(x + w - 3.0, y, dev, ha="right", va="center", fontsize=7.8,
                family="monospace", color=hi if mark else GRAY, zorder=6)
        y -= 5.3
    label(ax, x + w / 2.0, 13.4, note_text, fs=7.8, color=GRAY)

routing(ax, 3, 44, "全隧道", [
    ("10.0.0.0/8", "wg0", True),
    ("0.0.0.0/0", "wg0", True),
    ("192.168.1.0/24", "eth0", False),
], "所有流量绕公司出口\n审计完整，速度受限", ACCENT)

routing(ax, 53, 44, "拆分隧道", [
    ("10.0.0.0/8", "wg0", True),
    ("0.0.0.0/0", "eth0", False),
    ("192.168.1.0/24", "eth0", False),
], "只有内网走隧道\n速度快，审计有缺口", ACCENT)

label(ax, 50, 6.4, "决定流量走不走隧道的，不是客户端界面，而是这两张表里最长前缀匹配的结果。",
      fs=8.2, color=GRAY)

save(fig, "09/fig09_3.png")

# ---------------------------------------------------------------- 图 9-4
fig, ax = canvas(7.4, 4.8, 100)
ax.set_ylim(0, 65)

lifeline(ax, 18, 60, 8.0, "客户端 iNode", color=ACCENT, fs=9.0)
lifeline(ax, 52, 60, 8.0, "交换机", color=WARM, fs=9.0, sub="认证者")
lifeline(ax, 85, 60, 8.0, "RADIUS", color=GREEN, fs=9.0, sub="认证服务器")

label(ax, 50, 50.4, "端口未授权：只放行认证报文，其他一律丢弃", fs=8.2, color=RED)

steps = [
    (45.6, 18, 52, "EAPOL-Start", False),
    (41.0, 52, 18, "EAP-Request / Identity", True),
    (36.4, 18, 52, "EAP-Response / Identity（学号）", False),
    (31.8, 52, 85, "Access-Request", False),
    (27.2, 85, 18, "EAP 方法交互（口令、证书）", True),
    (22.6, 52, 85, "Access-Request（结果）", False),
    (18.0, 85, 52, "Access-Accept", True),
]
for y, x1, x2, text, dash in steps:
    msg(ax, x1, x2, y, text, fs=8.2, dash=dash)

label(ax, 55.5, 13.6, "端口改为授权，必要时下发 VLAN", fs=8.0, color=ACCENT, ha="left")
label(ax, 30, 10.4, "此时 DHCP 才拿到地址", fs=8.0, color=GRAY)

save(fig, "09/fig09_4.png")
