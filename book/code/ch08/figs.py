# -*- coding: utf-8 -*-
"""第 7 章插图：端口转发。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

from figstyle import (ACCENT, ACCENT_L, GRAY, GRAY_L, GREEN, GREEN_L, INK, RED,
                      RED_L, WARM, WARM_L, WHITE, arrow, box, canvas, elb_arrow,
                      label, line, note, save)


def tbox(ax, x, y, w, h, title, sub=None, fc=ACCENT_L, tfs=9.2, sfs=7.6,
         ec=INK, color=None):
    box(ax, x, y, w, h, fc=fc, ec=ec)
    if sub:
        label(ax, x + w / 2.0, y + h * 0.66, title, fs=tfs, bold=True, color=color)
        label(ax, x + w / 2.0, y + h * 0.27, sub, fs=sfs, color=GRAY)
    else:
        label(ax, x + w / 2.0, y + h / 2.0, title, fs=tfs, bold=True, color=color)


def over_arrow(ax, x, y, text, fs=7.4, color=None, mono=False):
    """写在箭头上方的标签，宽度控制在框之间。"""
    ax.text(x, y + 2.2, text, ha="center", va="bottom", fontsize=fs,
            color=color or INK, zorder=7,
            family="monospace" if mono else None)


def cmdb(ax, x, y, w, text):
    box(ax, x, y, w, 7.2, fc=GRAY_L, ec=GRAY, lw=0.8)
    ax.text(x + w / 2.0, y + 3.6, text, ha="center", va="center", fontsize=8.6,
            family="monospace", color=INK, zorder=6)


def bracket(ax, x1, x2, y, text, color=GRAY):
    ax.plot([x1, x1, x2, x2], [y - 1.0, y, y, y - 1.0], color=color, lw=0.8, zorder=1)
    label(ax, (x1 + x2) / 2.0, y + 1.7, text, fs=7.9, color=color)


# ---------------------------------------------------------------- 图 7-1
fig, ax = canvas(7.4, 4.0, 100)

cmdb(ax, 10, 44, 80, "ssh -L 8080:10.0.0.5:80 user@server")
bracket(ax, 1, 43, 39.5, "你的电脑")
bracket(ax, 86.5, 99.5, 39.5, "服务器所在内网")

tbox(ax, 1, 24, 13, 11, "本地程序", "浏览器等", fc=GRAY_L, tfs=9.0)
tbox(ax, 30, 24, 13, 11, "SSH 客户端", "监听 :8080", fc=ACCENT_L, ec=ACCENT)
tbox(ax, 59, 24, 13, 11, "SSH 服务器", "sshd", fc=GREEN_L, ec=GREEN)
tbox(ax, 86.5, 24, 13, 11, "内网服务", "Web 服务", fc=WARM_L, ec=WARM, tfs=9.0)

arrow(ax, (14, 29.5), (30, 29.5), lw=1.0)
over_arrow(ax, 22, 29.5, "本地:8080")
arrow(ax, (43, 29.5), (59, 29.5), lw=1.7, color=ACCENT)
over_arrow(ax, 51, 29.5, "加密隧道", color=ACCENT)
arrow(ax, (72, 29.5), (86.5, 29.5), lw=1.0)
over_arrow(ax, 79.2, 29.5, "10.0.0.5:80", fs=6.9, mono=True)

label(ax, 8.4, 18.0, "以为在连本机", fs=7.6, color=GRAY)
label(ax, 36.5, 18.0, "在本机 8080 上监听", fs=7.6, color=GRAY)
label(ax, 65.5, 18.0, "由它真正连出去", fs=7.6, color=GRAY)
label(ax, 93.0, 18.0, "只有内网能访问", fs=7.6, color=GRAY)

label(ax, 50, 7.6, "监听的那一端在本地，真正去连服务的那一端在远端。",
      fs=8.4, color=GRAY)

save(fig, "08/fig08_1.png")

# ---------------------------------------------------------------- 图 7-2
fig, ax = canvas(7.4, 4.0, 100)

cmdb(ax, 10, 44, 80, "ssh -R 9000:127.0.0.1:3000 user@public-host")
bracket(ax, 1, 43, 39.5, "你的电脑")
bracket(ax, 86.5, 99.5, 39.5, "公网上的那台机器")

tbox(ax, 1, 24, 13, 11, "本地服务", "127.0.0.1:3000", fc=WARM_L, ec=WARM, tfs=9.0, sfs=6.8)
tbox(ax, 30, 24, 13, 11, "SSH 客户端", "ssh 进程", fc=ACCENT_L, ec=ACCENT)
tbox(ax, 59, 24, 13, 11, "SSH 服务器", "sshd", fc=GREEN_L, ec=GREEN)
tbox(ax, 86.5, 24, 13, 11, "外部访问者", "任何人", fc=GRAY_L, tfs=9.0)

arrow(ax, (86.5, 29.5), (72, 29.5), lw=1.0)
over_arrow(ax, 79.2, 29.5, "连 :9000")
arrow(ax, (59, 29.5), (43, 29.5), lw=1.7, color=ACCENT)
over_arrow(ax, 51, 29.5, "加密隧道", color=ACCENT)
arrow(ax, (30, 29.5), (14, 29.5), lw=1.0)
over_arrow(ax, 22, 29.5, ":3000", mono=True)

label(ax, 7.5, 18.0, "服务留在本地\n不开放到公网", fs=7.6, color=GRAY)
label(ax, 36.5, 18.0, "把收到的连接\n送回本机", fs=7.6, color=GRAY)
label(ax, 65.5, 18.0, "监听\n0.0.0.0:9000", fs=7.2, color=GRAY)
label(ax, 93.0, 18.0, "以为在连\n一台公网机器", fs=7.6, color=GRAY)

label(ax, 50, 7.6, "同样的隧道，反了个方向：监听放在远端，服务留在本地。",
      fs=8.4, color=GRAY)

save(fig, "08/fig08_2.png")

# ---------------------------------------------------------------- 图 7-3
fig, ax = canvas(7.4, 4.6, 100)

cmdb(ax, 16, 47, 68, "ssh -D 1080 user@server")

tbox(ax, 2, 26, 16, 11, "浏览器", "或其他程序", fc=GRAY_L, tfs=9.0)
tbox(ax, 27, 26, 20, 11, "SSH 客户端", "本机 SOCKS5 代理 :1080",
     fc=ACCENT_L, ec=ACCENT, sfs=7.2)
tbox(ax, 55, 26, 17, 11, "SSH 服务器", "按请求分别连出去",
     fc=GREEN_L, ec=GREEN, sfs=7.4)

targets = [
    (37, "example.com:443", "外部网站"),
    (27, "10.0.0.7:3306", "内网数据库"),
    (17, "wiki.intra:80", "内网知识库"),
]
for y, mono_txt, cn in targets:
    box(ax, 78, y, 21, 9, fc=WARM_L, ec=WARM)
    ax.text(88.5, y + 5.5, mono_txt, ha="center", va="center", fontsize=7.4,
            family="monospace", color=INK, zorder=6)
    label(ax, 88.5, y + 2.6, cn, fs=7.4, color=GRAY)

arrow(ax, (18, 31.5), (27, 31.5), lw=1.0)
over_arrow(ax, 22.5, 31.5, "请求", fs=7.2, color=GRAY)
arrow(ax, (47, 31.5), (55, 31.5), lw=1.5, color=ACCENT)
over_arrow(ax, 51, 31.5, "隧道", fs=7.0, color=ACCENT)

for y in (41.5, 31.5, 21.5):
    arrow(ax, (72, 31.5), (78, y), lw=1.0, color=WARM)

label(ax, 10, 20.0, "只把请求\n交给代理", fs=7.6, color=GRAY)
label(ax, 37, 20.0, "目标地址由它\n转告服务器", fs=7.5, color=GRAY)
label(ax, 74, 10.5, "同一条隧道\n通向多个目标", fs=7.5, color=GRAY)

label(ax, 50, 4.6, "连哪台机器、哪个端口，都写在运行时的请求里：隧道本身没有固定的目标。",
      fs=8.2, color=GRAY)

save(fig, "08/fig08_3.png")

# ---------------------------------------------------------------- 图 7-4
fig, ax = canvas(7.4, 3.8, 100)

cmdb(ax, 12, 41, 76, "ssh -J jump@bastion  alice@10.0.0.9")

tbox(ax, 2, 22, 20, 11, "你的电脑", "ssh 客户端", fc=ACCENT_L, ec=ACCENT, tfs=9.2)
tbox(ax, 37, 22, 22, 11, "跳板机", "bastion:22", fc=WARM_L, ec=WARM, tfs=9.2)
tbox(ax, 74, 22, 22, 11, "目标机", "10.0.0.9:22", fc=GREEN_L, ec=GREEN, tfs=9.2)

arrow(ax, (22, 27.5), (37, 27.5), lw=1.0)
over_arrow(ax, 29.5, 27.5, "SSH ①", fs=7.2)
arrow(ax, (59, 27.5), (74, 27.5), lw=1.0)
over_arrow(ax, 66.5, 27.5, "SSH ②", fs=7.2)

line(ax, (12, 33), (12, 37.2), color=ACCENT, lw=0.9, ls=(0, (4, 3)))
line(ax, (12, 37.2), (85, 37.2), color=ACCENT, lw=0.9, ls=(0, (4, 3)))
arrow(ax, (85, 37.2), (85, 33), color=ACCENT, lw=0.9, ls=(0, (4, 3)))
label(ax, 48.5, 38.4, "SSH 握手端到端：目标机看到的是你的凭据", fs=7.9, color=ACCENT)

label(ax, 12, 15.0, "对跳板机认证一次\n再穿过它连 ②", fs=7.6, color=GRAY)
label(ax, 48, 15.0, "只转发字节流\n不保存目标机凭据", fs=7.6, color=GRAY)
label(ax, 85, 15.0, "只认你的账号\n不认跳板机", fs=7.6, color=GRAY)

label(ax, 50, 4.8, "第二段 TCP 由跳板机代开，两段都是 22 端口；对目标机来说，来源是跳板机的地址。",
      fs=8.2, color=GRAY)

save(fig, "08/fig08_4.png")
