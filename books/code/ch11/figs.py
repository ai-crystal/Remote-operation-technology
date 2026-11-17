# -*- coding: utf-8 -*-
"""第 11 章插图：JumpServer 的内部构造。"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

from figstyle import (ACCENT, ACCENT_L, GRAY, GRAY_L, GREEN, GREEN_L, INK, RED,
                      RED_L, WARM, WARM_L, WHITE, arrow, box, canvas, elb_arrow,
                      label, line, note, save)


def tbox(ax, x, y, w, h, title, sub=None, fc=ACCENT_L, tfs=9.4, sfs=7.8,
         ec=INK, color=None, sub_color=None):
    box(ax, x, y, w, h, fc=fc, ec=ec)
    if sub:
        label(ax, x + w / 2.0, y + h * 0.68, title, fs=tfs, bold=True, color=color)
        label(ax, x + w / 2.0, y + h * 0.29, sub, fs=sfs, color=sub_color or GRAY)
    else:
        label(ax, x + w / 2.0, y + h / 2.0, title, fs=tfs, bold=True, color=color)


# ---------------------------------------------------------------- 图 11-1
fig, ax = canvas(7.4, 4.3, 100)

CORE = (50.0, 31.0)
nodes = [
    ("Luna", "Web 前端", 19, 47),
    ("Chen", "编排与任务", 81, 47),
    ("Koko", "SSH / SFTP 网关", 13, 30),
    ("Razor", "远程应用发布", 87, 30),
    ("Lion", "RDP / VNC 网关", 19, 12),
    ("Magnus", "数据库代理", 81, 12),
]
for name, role, cx, cy in nodes:
    line(ax, (cx, cy), CORE, color="#c3c8ce", lw=0.9, zorder=1)

for name, role, cx, cy in nodes:
    fc, ec = (ACCENT_L, ACCENT) if name in ("Luna",) else (WARM_L, WARM)
    box(ax, cx - 12, cy - 4.2, 24, 8.4, fc=fc, ec=ec, zorder=3)
    label(ax, cx, cy + 1.7, name, fs=8.8, bold=True)
    label(ax, cx, cy - 1.9, role, fs=7.2, color=GRAY)

line(ax, CORE, (50, 18.5), color="#c3c8ce", lw=0.9, zorder=1)
box(ax, 37, 26.0, 26, 10.5, fc=ACCENT_L, ec=ACCENT, lw=1.2, zorder=3)
label(ax, 50, 33.4, "Core", fs=9.6, bold=True, color=ACCENT)
label(ax, 50, 29.0, "API 与业务逻辑", fs=7.4, color=GRAY)

box(ax, 37, 8.5, 26, 9.0, fc=WHITE, ec=ACCENT, lw=1.2, zorder=3)
label(ax, 50, 14.2, "数据库与缓存", fs=8.4, bold=True)
label(ax, 50, 10.4, "MySQL / Redis", fs=7.2, color=GRAY)

label(ax, 50, 2.6, "各组件都通过 Core 读写元数据，资产、账号、授权、会话记录集中在一处",
      fs=7.8, color=GRAY)

save(fig, "11/fig11_1.png")

# ---------------------------------------------------------------- 图 11-2
fig, ax = canvas(7.2, 3.9, 100)

tbox(ax, 4, 42, 24, 9, "资产 Asset", "一台机器：地址 + 端口", fc=GREEN_L, ec=GREEN)
tbox(ax, 36, 42, 24, 9, "账号 Account", "机器上真实的用户名/密钥", fc=WARM_L, ec=WARM)
tbox(ax, 68, 42, 24, 9, "系统用户 SystemUser", "登录时用哪组账号", fc=ACCENT_L, ec=ACCENT,
     tfs=8.4)
tbox(ax, 14, 19, 34, 9, "授权 AssetPermission", "资产 + 系统用户 → 授给谁",
     fc=WHITE, ec=ACCENT, tfs=8.6)
tbox(ax, 58, 19, 34, 9, "用户 / 用户组", "谁来登录", fc=GRAY_L, ec=GRAY)

arrow(ax, (28, 46.5), (36, 46.5), lw=0.9)
label(ax, 32, 48.6, "多对多", fs=7.6, color=ACCENT)
arrow(ax, (60, 46.5), (68, 46.5), lw=0.9)
label(ax, 64, 48.6, "多对多", fs=7.6, color=ACCENT)

arrow(ax, (20, 28), (20, 42), lw=0.9)
label(ax, 21.2, 34.1, "描述的对象", fs=7.4, color=GRAY, ha="left")
line(ax, (44, 28), (44, 34.4), color=INK, lw=0.9)
line(ax, (44, 34.4), (80, 34.4), color=INK, lw=0.9)
arrow(ax, (80, 34.4), (80, 42), lw=0.9)

arrow(ax, (48, 23.5), (58, 23.5), lw=0.9)
label(ax, 53, 25.2, "授给", fs=7.4, color=GRAY)

label(ax, 50, 11.6, "多对多：一个账号可以被多个系统用户引用，一个系统用户也可以包多个账号。",
      fs=8.0, color=GRAY)
label(ax, 50, 5.2, "系统用户不是某台机器上的账号，而是一组账号的组合；授权把这组账号指定给谁，才决定谁能登进去。",
      fs=8.0, color=GRAY)

save(fig, "11/fig11_2.png")

# ---------------------------------------------------------------- 图 11-3
fig, ax = canvas(7.2, 4.0, 100)

segs = [
    (11, 33, "alice", ACCENT_L, ACCENT),
    (36, 58, "ubuntu", WARM_L, WARM),
    (61, 89, "10.0.0.5", GREEN_L, GREEN),
]
for x1, x2, txt, fc, ec in segs:
    box(ax, x1, 44, x2 - x1, 8, fc=fc, ec=ec)
    ax.text((x1 + x2) / 2.0, 48, txt, ha="center", va="center", fontsize=10.0,
            family="monospace", color=INK, zorder=6)

label(ax, 34.5, 48, "@", fs=11, bold=True, color=GRAY)
label(ax, 59.5, 48, "@", fs=11, bold=True, color=GRAY)

exp = [
    (2, 34, "JumpServer 用户名", "你在堡垒机上的登录名", ACCENT),
    (36, 64, "系统用户名", "堡垒机里的凭据模板", WARM),
    (66, 96, "目标资产地址", "唯一确定一台机器", GREEN),
]
for x1, x2, title, sub, col in exp:
    box(ax, x1, 20, x2 - x1, 10, fc=WHITE, ec=col, lw=0.9)
    label(ax, (x1 + x2) / 2.0, 26.6, title, fs=8.6, bold=True, color=col)
    label(ax, (x1 + x2) / 2.0, 22.8, sub, fs=7.6, color=GRAY)

for (s1, s2, _t, _f, _e), (x1, x2, _, _, col) in zip(segs, exp):
    line(ax, ((s1 + s2) / 2.0, 44), ((x1 + x2) / 2.0, 30),
         color=col, lw=0.7, ls=(0, (3, 2)))

for x1, x2, _, _, col in exp:
    arrow(ax, ((x1 + x2) / 2.0, 20), ((x1 + x2) / 2.0, 14), color=col, lw=0.8)

box(ax, 2, 5, 94, 9, fc=GRAY_L, ec=GRAY)
label(ax, 49, 9.5, "Koko 据此查授权、取凭据，建立到目标机的 SSH 连接", fs=8.4)

save(fig, "11/fig11_3.png")

# ---------------------------------------------------------------- 图 11-4
fig, ax = canvas(6.2, 2.4, 100)

AX = 33.0
line(ax, (4, AX), (97, AX), color=INK, lw=1.0)
arrow(ax, (95, AX), (99, AX), lw=1.0)
label(ax, 96.0, AX + 2.6, "时间", fs=7.4, color=GRAY)

events = [
    (26, "登录成功"),
    (44, "执行 ls"),
    (64, "执行 rm -rf"),
    (88, "退出"),
]
for x, txt in events:
    ax.add_patch(__import__("matplotlib").patches.Circle((x, AX), 0.7, color=INK, zorder=4))
    label(ax, x, AX + 2.6, txt, fs=8.2)
    line(ax, (x, AX - 0.8), (x, 18.2), color="#c9ced4", lw=0.7, ls=(0, (2, 3)), zorder=1)

# 命令记录
box(ax, 4, 22.5, 92, 5.6, fc=GRAY_L, ec=GRAY, lw=0.8)
label(ax, 6, 25.3, "命令记录", fs=7.8, bold=True, color=INK, ha="left")
recs = [
    (26, 12, "登录", GRAY_L, GRAY),
    (44, 9, "ls", GRAY_L, GRAY),
    (64, 27, "rm -rf 被规则拦截", RED_L, RED),
    (88, 11, "退出", GRAY_L, GRAY),
]
for x, w, txt, fc, ec in recs:
    box(ax, x - w / 2.0, 23.1, w, 4.4, fc=fc, ec=ec, lw=0.7, radius=0.8)
    label(ax, x, 25.3, txt, fs=7.6, color=INK)

# 录像
box(ax, 4, 13, 92, 5.6, fc=GREEN_L, ec=GREEN, lw=0.8)
label(ax, 6, 15.8, "录像", fs=7.8, bold=True, color=INK, ha="left")
box(ax, 13, 13.6, 76, 4.4, fc=WHITE, ec=GREEN, lw=0.7, radius=0.8)
label(ax, 51, 15.8, "从登录到退出持续写入，会话结束才封存", fs=7.4, color=GREEN)

label(ax, 4, 7.0, "命令记录实时落库，方便检索；录像只在会话结束后封存，用于还原当时到底看到了什么。",
      fs=8.0, color=GRAY, ha="left")

save(fig, "11/fig11_4.png")
