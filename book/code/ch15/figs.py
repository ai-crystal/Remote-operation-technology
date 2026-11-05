# -*- coding: utf-8 -*-
"""第 15 章插图：从登录到数据存取。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

from figstyle import (ACCENT, ACCENT_L, GRAY, GRAY_L, GREEN, GREEN_L, INK, RED,
                      RED_L, WARM, WARM_L, WHITE, arrow, box, brace, canvas,
                      dot, elb_arrow, label, lifeline, line, msg, note, save)
from matplotlib.patches import Polygon


def diamond(ax, cx, cy, w, h, text, fc=WHITE, ec=ACCENT, fs=8.2, lw=1.0):
    p = Polygon([[cx, cy + h / 2.0], [cx + w / 2.0, cy], [cx, cy - h / 2.0],
                 [cx - w / 2.0, cy]], closed=True, facecolor=fc, edgecolor=ec,
                linewidth=lw, zorder=3)
    ax.add_patch(p)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
            linespacing=1.5, zorder=4)


def node(ax, x, y, w, h, title, lines, fc, ec):
    box(ax, x, y, w, h, fc=fc, ec=ec, lw=1.1)
    label(ax, x + w / 2.0, y + h - 3.6, title, fs=9.2, bold=True,
          color=ec if ec != GRAY else INK)
    for i, t in enumerate(lines):
        label(ax, x + w / 2.0, y + h - 7.6 - i * 3.0, t, fs=7.6, color=GRAY)


# ---------------------------------------------------------------- 图 15-1
fig, ax = canvas(7.2, 4.6, 100)

node(ax, 2.0, 44.0, 34, 17.0, "Windows 本机", ["VS Code Remote-SSH",
                                             "OpenSSH 客户端", "coscli"],
     ACCENT_L, ACCENT)
node(ax, 56.0, 44.0, 42, 17.0, "JumpServer（堡垒机）",
     ["SSH 网关：认证、授权、审计", "记录每一条命令与文件传输"], WARM_L, WARM)
node(ax, 50.0, 22.0, 48, 16.0, "训练服务器（GPU 机）",
     ["跑训练脚本、读训练数据", "把 checkpoint 写出去"], GREEN_L, GREEN)
node(ax, 26.0, 4.0, 72, 11.0, "对象存储",
     ["训练数据与模型 checkpoint 都放在这里"], GRAY_L, GRAY)

arrow(ax, (36.2, 52.5), (55.6, 52.5), lw=1.2)
label(ax, 46.0, 54.1, "SSH", fs=8.4, bold=True)
label(ax, 46.0, 50.7, "公网", fs=7.6, color=GRAY)

arrow(ax, (74.0, 44.0), (74.0, 38.4), lw=1.2)
label(ax, 75.6, 42.6, "SSH：由堡垒机代你登录", fs=7.6, color=GRAY, ha="left")
label(ax, 75.6, 40.4, "你不再直接持有目标机的私钥", fs=7.4, color=GRAY, ha="left")

arrow(ax, (74.0, 22.0), (74.0, 15.4), lw=1.2)
label(ax, 75.6, 17.4, "HTTPS + AK/SK", fs=7.6, color=GRAY, ha="left")

line(ax, (4.5, 44.0), (4.5, 9.5), color=GRAY, lw=1.0)
arrow(ax, (4.5, 9.5), (25.6, 9.5), color=GRAY, lw=1.0)
label(ax, 6.5, 36.4, "coscli 直连对象存储", fs=7.6, color=GRAY, ha="left")
label(ax, 6.5, 33.2, "HTTPS + AK/SK 签名", fs=7.4, color=GRAY, ha="left")
for k, t in enumerate(["SSH 与对象存储互不依赖：", "堡垒机不可用时，", "coscli 仍能读写对象存储。"]):
    label(ax, 9.0, 29.6 - k * 3.2, t, fs=7.4, color=GRAY, ha="left")

label(ax, 50, 1.4, "两条路都要过认证：堡垒机认你，对象存储认那把 AK/SK", fs=7.8, color=GRAY)

save(fig, "15/fig15_1.png")

# ---------------------------------------------------------------- 图 15-2
fig, ax = canvas(7.2, 5.4, 100)

checks = [
    ("① DNS 解析与\n网络可达？", "ping / nslookup 主机名", "Could not resolve hostname"),
    ("② 端口\n开放？", "nc -vz 主机 端口", "Connection timed out / refused"),
    ("③ 免密认证\n通过？", "ssh -v 看用了哪把钥匙", "Permission denied (publickey)"),
    ("④ 主机指纹\n没变？", "核对指纹来源，换机后清旧记录", "Host key verification failed"),
    ("⑤ 堡垒机已\n授权？", "在 JumpServer 查授权单与绑定", "网关直接断开连接"),
    ("⑥ server 已\n装上？", "看 ~/.vscode-server 日志与配额", "Failed to parse remote port"),
]

for i, (q, act, sym) in enumerate(checks):
    y = 69.0 - i * 10.2
    diamond(ax, 26, y, 30, 8.2, q)
    arrow(ax, (41.2, y), (57.4, y))
    label(ax, 49.3, y + 1.0, "否", fs=7.6, color=GRAY)
    box(ax, 58.0, y - 4.1, 40, 8.2, fc=WHITE, ec=GRAY, lw=0.9)
    label(ax, 78.0, y + 1.3, act, fs=7.5)
    label(ax, 78.0, y - 1.9, sym, fs=6.6, color=GRAY)
    if i < len(checks) - 1:
        arrow(ax, (26, y - 4.1), (26, y - 6.1))
        label(ax, 27.4, y - 5.1, "是", fs=7.6, color=GRAY, ha="left")

arrow(ax, (26, 13.9), (26, 12.2))
label(ax, 27.4, 13.0, "是", fs=7.6, color=GRAY, ha="left")
box(ax, 11.0, 4.5, 30, 7.4, "还是慢或断：抓完整日志", fc=GRAY_L, ec=GRAY, fs=7.8, bold=True)

label(ax, 50.0, 1.4, "按顺序问下去，第一个答「否」的地方就是问题所在", fs=7.8, color=GRAY)

save(fig, "15/fig15_2.png")
