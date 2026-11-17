# -*- coding: utf-8 -*-
"""第 4 章插图：服务器上发生了什么。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

from matplotlib.patches import Rectangle

from figstyle import (ACCENT, ACCENT_L, GRAY, GRAY_L, GREEN, GREEN_L, INK, RED,
                      RED_L, WARM, WARM_L, WHITE, arrow, box, brace, canvas,
                      elb_arrow, label, lifeline, line, msg, note, save)


# ---------------------------------------------------------------- 图 4-1
fig, ax = canvas(7.0, 5.6, 100)
ax.set_ylim(0, 80)

# sshd 主进程
box(ax, 18, 70, 64, 8.4, "sshd 主进程：一直监听 22 端口",
    fc=ACCENT_L, ec=ACCENT, fs=9.0, lw=1.1, radius=1.2)
arrow(ax, (50, 69.6), (50, 65.0), color=ACCENT)
label(ax, 51.6, 67.3, "认证通过，为这条连接 fork 一个子进程",
      fs=7.2, color=ACCENT, ha="left")

# sshd 子进程
box(ax, 18, 56, 64, 8.4, "sshd 子进程：只服务你这一条连接",
    fc=ACCENT_L, ec=ACCENT, fs=9.0, lw=1.1, radius=1.2)
arrow(ax, (50, 55.6), (50, 51.0), color=ACCENT)
label(ax, 51.6, 53.3, "申请一对伪终端", fs=7.2, color=ACCENT, ha="left")

# 伪终端：master / slave
box(ax, 6, 41, 40, 9.6, "伪终端 master\n留在 sshd 进程里",
    fc=WARM_L, ec=WARM, fs=8.0, lw=1.1, radius=1.2)
box(ax, 54, 41, 40, 9.6, "伪终端 slave\n就是 shell 眼里的终端",
    fc=WARM_L, ec=WARM, fs=8.0, lw=1.1, radius=1.2)
arrow(ax, (46.4, 46.9), (53.6, 46.9), color=WARM, lw=0.9)
arrow(ax, (53.6, 44.5), (46.4, 44.5), color=WARM, lw=0.9)

# slave → bash
arrow(ax, (74, 40.6), (74, 36.9), color=WARM)
label(ax, 77.2, 38.9, "把 slave 设成 fd 0/1/2", fs=7.2, color=WARM, ha="left")

# bash
box(ax, 44, 26, 44, 10.4, "bash（登录 shell）\n提示符、历史、行编辑",
    fc=GREEN_L, ec=GREEN, fs=8.2, lw=1.1, radius=1.2)
ax.add_patch(Rectangle((5, 28.6), 28, 9.4, facecolor=WHITE, edgecolor=GRAY,
                       lw=0.8, linestyle=(0, (4, 3)), zorder=2))
label(ax, 19, 33.3, "连接一断，整套\n进程与设备一起回收", fs=7.2, color=GRAY)
_ = 0

# bash fork：子进程执行命令，父进程继续等待
arrow(ax, (48, 25.6), (48, 21.4), color=GREEN)
label(ax, 46.4, 23.5, "fork", fs=7.2, color=GREEN, ha="right")
arrow(ax, (80, 25.6), (80, 21.4), color=GREEN)
label(ax, 81.6, 23.5, "父进程继续等", fs=7.2, color=GREEN, ha="left")

box(ax, 2, 11, 52, 9.6, "子进程：执行你敲的命令\n（vim、top、less …）",
    fc=WHITE, ec=GREEN, fs=8.0, lw=1.0, radius=1.2)
box(ax, 58, 11, 38, 9.6, "父进程 bash\n等它结束、再显示提示符",
    fc=WHITE, ec=GREEN, fs=8.0, lw=1.0, radius=1.2)

label(ax, 50, 5.6, "你看到的“终端”其实是内核里的一对设备：写 master，slave 那头就能读到",
      fs=7.2, color=GRAY)
label(ax, 50, 1.8, "标准输入、标准输出、标准错误（fd 0/1/2）全部指向 slave",
      fs=7.2, color=GRAY)

save(fig, "04/fig04_1.png")

# ---------------------------------------------------------------- 图 4-2
fig, ax = canvas(7.0, 3.08, 100)
ax.set_ylim(0, 44)

CW, CG, GG = 6.2, 0.6, 2.4      # 单元格宽、同组间隙、组间间隙
CH = 11.0
YT = 28.5                        # 字母行底边
WY = YT - 3.7                    # 权重行

# 类型格
box(ax, 3.0, YT, CW, CH, "-", fc=GRAY_L, ec=GRAY, fs=10.0, radius=0.5, lw=0.9)
label(ax, 3.0 + CW / 2, WY, "类型", fs=7.0, color=GRAY)

groups = [("属主 user", "rwx"), ("属组 group", "r-x"), ("其他人 other", "r--")]
sums = ["7", "5", "4"]
fcs = [ACCENT_L, WARM_L, GREEN_L]
ecs = [ACCENT, WARM, GREEN]
weights = [4, 2, 1]

x = 3.0 + CW + GG
for (gname, letters), s, fc, ec in zip(groups, sums, fcs, ecs):
    gx = x
    for i, ch in enumerate(letters):
        cx = gx + i * (CW + CG)
        on = ch != "-"
        box(ax, cx, YT, CW, CH, ch, fc=fc if on else WHITE,
            ec=ec if on else GRAY_L, fs=10.5, radius=0.5, lw=0.9,
            color=INK if on else GRAY_L)
        ax.text(cx + CW / 2, WY, str(weights[i]), ha="center", va="center",
                fontsize=7.0, color=ec if on else GRAY)
    gend = gx + 3 * CW + 2 * CG
    gc = (gx + gend) / 2.0
    label(ax, gc, YT + CH + 2.6, gname, fs=8.0, color=ec, bold=True)
    # 段内求和 → 一位八进制
    ax.plot([gc, gc], [WY - 3.0, 18.6], color=ec, lw=0.8, ls=(0, (3, 3)))
    box(ax, gc - 6.5, 9.8, 13, 8.2, s, fc=WHITE, ec=ec, fs=12.5,
        bold=True, radius=0.7, lw=1.0, color=ec)
    x = gend + GG

label(ax, 3.0, 13.9, "每段\n求和", fs=7.2, color=GRAY, ha="left")
label(ax, 42, 3.4, "三段连起来读，就是八进制的 754", fs=8.4, bold=True)

# 私钥卡片
box(ax, 82, 7, 17, 34.4, fc=WHITE, ec=RED, lw=1.1, radius=1.2)
label(ax, 90.5, 37.0, "私钥文件", fs=8.2, bold=True, color=RED)
label(ax, 90.5, 31.6, "-rw-------", fs=7.4)
label(ax, 90.5, 23.4, "600", fs=13.0, bold=True, color=RED)
label(ax, 90.5, 13.3, "只有属主\n能读能写", fs=7.2, color=GRAY)

save(fig, "04/fig04_2.png")

# ---------------------------------------------------------------- 图 4-3
fig, ax = canvas(7.2, 3.31, 100)
ax.set_ylim(0, 46)

steps = ["bash 读入\n一行命令",
         "在 PATH 里\n逐个目录查找",
         "fork 复制出\n一个子进程",
         "exec 换成\n那个程序",
         "结束，bash\n回到提示符"]
fcs = [ACCENT_L, ACCENT_L, WARM_L, WARM_L, GREEN_L]
ecs = [ACCENT, ACCENT, WARM, WARM, GREEN]

for i, (t, fc, ec) in enumerate(zip(steps, fcs, ecs)):
    bx = 2 + i * 20
    box(ax, bx, 26, 16, 14, t, fc=fc, ec=ec, fs=8.0, lw=1.0, radius=1.2)
    if i < 4:
        arrow(ax, (bx + 16.4, 33), (bx + 19.6, 33))

# PATH 细节
ax.plot([30, 30], [25.6, 20.6], color=GRAY, lw=0.8, ls=(0, (3, 3)), zorder=1)
ax.add_patch(Rectangle((6, 11), 60, 9, facecolor=GRAY_L, edgecolor=GRAY,
                       lw=0.9, linestyle=(0, (4, 3)), zorder=2))
label(ax, 36, 15.5, "按 PATH 顺序挨个目录试：/usr/local/bin、/usr/bin、/bin …",
      fs=7.4)
label(ax, 69, 15.5, "命中第一个就停下，\n后面的目录不会再看",
      fs=7.2, color=GRAY, ha="left")

label(ax, 50, 4.6, "“跑一个命令”＝找到文件、复制进程、换掉程序映像，这三件事分开发生",
      fs=7.4, color=GRAY)

save(fig, "04/fig04_3.png")
