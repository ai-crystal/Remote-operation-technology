# -*- coding: utf-8 -*-
"""第 1 章插图。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

from figstyle import (ACCENT, ACCENT_L, GRAY, GRAY_L, GREEN, GREEN_L, INK, RED,
                      RED_L, WARM, WARM_L, WHITE, arrow, box, brace, canvas,
                      elb_arrow, label, lifeline, line, msg, note, save)

# ---------------------------------------------------------------- 图 1-1
fig, ax = canvas(7.4, 2.9, 100)
ax.set_ylim(0, 39)

ys, hh = 9.0, 13.0
boxes = [
    (1.5, 22.0, "你的电脑", "VS Code、终端、ssh.exe", ACCENT_L),
    (28.0, 20.0, "公网", "路由、NAT、防火墙", GRAY_L),
    (55.5, 21.0, "堡垒机", "JumpServer 的 SSH 网关", WARM_L),
    (83.5, 15.0, "目标服务器", "sshd 与你的账号", GREEN_L),
]
for x, w, title, sub, fc in boxes:
    box(ax, x, ys, w, hh, fc=fc)
    label(ax, x + w / 2, ys + hh - 4.0, title, fs=10.5, bold=True)
    label(ax, x + w / 2, ys + 4.2, sub, fs=8.2, color=GRAY)

arrow(ax, (23.8, 15.5), (27.6, 15.5))
label(ax, 25.7, 17.4, "TCP", fs=8.0, color=GRAY)

arrow(ax, (48.4, 15.5), (55.1, 15.5))
label(ax, 51.75, 17.4, "SSH", fs=8.0, color=GRAY)

arrow(ax, (76.9, 15.5), (83.1, 15.5))
label(ax, 80.0, 17.4, "SSH", fs=8.0, color=GRAY)

arrow(ax, (11.0, 22.4), (11.0, 35.6), style="-", color=ACCENT, lw=0.8, ls=(0, (3, 3)))
label(ax, 11.0, 37.0, "你看到的窗口", fs=8.4, color=ACCENT)

label(ax, 50, 2.4, "链路上流动的始终是加密后的字节流", fs=8.4, color=GRAY)

save(fig, "01/fig01_1.png")

# ---------------------------------------------------------------- 图 1-2
fig, ax = canvas(6.6, 3.4, 100)
ax.set_ylim(0, 51.5)

layers = [
    ("你的操作：在终端里敲下 ssh 命令", GRAY_L),
    ("应用层：终端程序、SSH 客户端", ACCENT_L),
    ("加密层：经过加密与完整性保护的字节流", ACCENT_L),
    ("传输层：TCP 连接，带端口号与序号", GRAY_L),
    ("网络层：IP 包，带源地址与目的地址", GRAY_L),
    ("链路层：以太网帧或无线帧，一跳一跳地转发", GRAY_L),
]
top, h = 44.5, 6.6
for i, (text, fc) in enumerate(layers):
    y = top - i * (h + 1.4)
    box(ax, 6, y, 88, h, fc=fc, radius=0.8)
    label(ax, 50, y + h / 2.0, text, fs=9.2)

label(ax, 50, 1.2, "越往下越靠近物理线路，越往上越接近人的意图", fs=8.6, color=GRAY)
arrow(ax, (95.5, 5.0), (95.5, 47.0), color=ACCENT, lw=0.9)
label(ax, 97.6, 26.0, "抽象", fs=8.2, color=ACCENT)
save(fig, "01/fig01_2.png")

# ---------------------------------------------------------------- 图 1-3
fig, ax = canvas(7.0, 4.6, 100)
ax.set_ylim(0, 65.7)

lifeline(ax, 18, 60, 6, "你的电脑", sub="ssh 客户端")
lifeline(ax, 82, 60, 6, "目标服务器", color=GREEN, sub="sshd")

steps = [
    (52.0, "TCP 三次握手，建立一条字节流", False),
    (45.5, "交换版本号：SSH-2.0-OpenSSH_9.6", False),
    (39.0, "各自列出支持的算法，商定一套", True),
    (32.5, "密钥交换：生成只有双方知道的会话密钥", True),
    (26.0, "NEWKEYS：此后所有内容都加密", False),
    (19.5, "身份认证：证明“我是那个用户”", True),
    (13.0, "打开会话通道，分配伪终端，启动 shell", False),
]
for y, text, dashed in steps:
    msg(ax, 18, 82, y, text, dash=dashed, fs=8.4)
    ax.text(84.5, y, "", fontsize=8)

label(ax, 50, 57.2, "这一段建立起一条可信的管道", fs=8.6, color=GRAY)
label(ax, 50, 3.2, "管道建好之后，才是你熟悉的命令行", fs=8.6, color=GRAY)
save(fig, "01/fig01_3.png")
