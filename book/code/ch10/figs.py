# -*- coding: utf-8 -*-
"""第 10 章插图：为什么需要堡垒机。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

from figstyle import (ACCENT, ACCENT_L, GRAY, GRAY_L, GREEN, GREEN_L, INK, RED,
                      RED_L, WARM, WARM_L, WHITE, arrow, box, canvas, elb_arrow,
                      label, lifeline, line, msg, note, save)


def tbox(ax, x, y, w, h, title, sub=None, fc=ACCENT_L, tfs=9.4, sfs=7.8,
         ec=INK, color=None):
    box(ax, x, y, w, h, fc=fc, ec=ec)
    if sub:
        label(ax, x + w / 2.0, y + h * 0.68, title, fs=tfs, bold=True, color=color)
        label(ax, x + w / 2.0, y + h * 0.28, sub, fs=sfs, color=GRAY)
    else:
        label(ax, x + w / 2.0, y + h / 2.0, title, fs=tfs, bold=True, color=color)


# ---------------------------------------------------------------- 图 10-1
fig, ax = canvas(7.4, 4.2, 100)

label(ax, 24, 54.6, "没有堡垒机", fs=10.4, bold=True)
label(ax, 76, 54.6, "有堡垒机", fs=10.4, bold=True)
label(ax, 6.5, 51.6, "6 台终端", fs=7.6, color=GRAY)
label(ax, 41.0, 51.6, "8 台服务器", fs=7.6, color=GRAY)
label(ax, 58.0, 51.6, "6 台终端", fs=7.6, color=GRAY)
label(ax, 93.0, 51.6, "8 台服务器", fs=7.6, color=GRAY)

line(ax, (50, 6), (50, 50), color=GRAY_L, lw=1.6)

# 左：终端与服务器两两相连
term_y = [43.0 - i * 7.4 for i in range(6)]
srv_y = [46.0 - i * 6.0 for i in range(8)]

for ty in term_y:
    for sy in srv_y:
        line(ax, (11, ty + 2.1), (36, sy + 2.1), color="#b7bcc2", lw=0.45)

for i, y in enumerate(term_y):
    box(ax, 2, y, 9, 4.2, fc=GRAY_L, ec=GRAY, lw=0.8)
    label(ax, 6.5, y + 2.1, "终端%d" % (i + 1), fs=6.8, color=INK)

for i, y in enumerate(srv_y):
    box(ax, 36, y, 10, 4.2, fc=GREEN_L, ec=GREEN, lw=0.8)
    label(ax, 41, y + 2.1, "服务器%d" % (i + 1), fs=6.8, color=INK)

# 右：终端先到堡垒机，堡垒机再到服务器
term_y2 = [43.0 - i * 7.4 for i in range(6)]
srv_y2 = [46.0 - i * 6.0 for i in range(8)]

for i, ty in enumerate(term_y2):
    line(ax, (63, ty + 2.1), (67.5, 31.0 - i * 2.1), color="#b7bcc2", lw=0.7)
for i, sy in enumerate(srv_y2):
    line(ax, (81.5, 31.5 - i * 1.55), (88, sy + 2.1), color="#b7bcc2", lw=0.7)

for i, y in enumerate(term_y2):
    box(ax, 54, y, 9, 4.2, fc=GRAY_L, ec=GRAY, lw=0.8)
    label(ax, 58.5, y + 2.1, "终端%d" % (i + 1), fs=6.8, color=INK)

for i, y in enumerate(srv_y2):
    box(ax, 88, y, 10, 4.2, fc=GREEN_L, ec=GREEN, lw=0.8)
    label(ax, 93, y + 2.1, "服务器%d" % (i + 1), fs=6.8, color=INK)

box(ax, 67.5, 18, 14, 18, fc=WARM_L, ec=WARM, lw=1.2)
label(ax, 74.5, 30.6, "堡垒机", fs=9.2, bold=True)
label(ax, 74.5, 26.4, "唯一入口", fs=7.4, color=GRAY)
label(ax, 74.5, 22.6, "账号统一", fs=7.4, color=GRAY)

label(ax, 50, 1.4, "左边每条线都要单独发密钥、单独查日志；右边所有流量经过同一个入口。",
      fs=8.2, color=GRAY)

save(fig, "10/fig10_1.png")

# ---------------------------------------------------------------- 图 10-2
fig, ax = canvas(7.0, 4.0, 100)

box(ax, 31, 21, 38, 14, fc=WHITE, ec=ACCENT, lw=1.2)
label(ax, 50, 28.0, "一次受控的\n运维会话", fs=9.6, bold=True, color=ACCENT)

tbox(ax, 3, 42, 38, 11, "认证 Authentication", "你是谁", fc=ACCENT_L, ec=ACCENT, tfs=9.0, sfs=7.8)
tbox(ax, 59, 42, 38, 11, "授权 Authorization", "你能做什么", fc=ACCENT_L, ec=ACCENT, tfs=9.0, sfs=7.8)
tbox(ax, 3, 4, 38, 11, "账号 Account", "用哪个身份去连", fc=GREEN_L, ec=GREEN, tfs=9.0, sfs=7.8)
tbox(ax, 59, 4, 38, 11, "审计 Audit", "事后可查可回放", fc=WARM_L, ec=WARM, tfs=9.0, sfs=7.8)

arrow(ax, (30, 42), (40, 35.5), color=ACCENT, lw=0.9)
arrow(ax, (70, 42), (60, 35.5), color=ACCENT, lw=0.9)
arrow(ax, (30, 15), (40, 21.0), color=GREEN, lw=0.9)
arrow(ax, (60, 21.0), (70, 15), color=WARM, lw=0.9)   # 会话产生审计记录

save(fig, "10/fig10_2.png")

# ---------------------------------------------------------------- 图 10-3
fig, ax = canvas(7.2, 4.8, 100)

lifeline(ax, 15, 60, 10, "运维人员", sub="浏览器或终端")
lifeline(ax, 50, 60, 10, "堡垒机", color=WARM, sub="认证、鉴权、录像")
lifeline(ax, 85, 60, 10, "目标机", color=GREEN, sub="sshd")

msg(ax, 15, 50, 48, "① 登录：密码 + MFA", color=ACCENT, fs=8.4)
msg(ax, 15, 50, 41, "② 选择资产与系统用户", color=ACCENT, fs=8.4)

box(ax, 41, 30, 18, 8, fc=WHITE, ec=WARM, lw=0.9)
label(ax, 50, 35.5, "③ 查授权", fs=8.4, bold=True, color=WARM)
label(ax, 50, 32.2, "有没有权限", fs=7.8, color=GRAY)

msg(ax, 50, 85, 24, "④ 用资产上的账号与密钥登录", color=GREEN, fs=8.4)
msg(ax, 15, 50, 17, "⑤ 键入命令", color=ACCENT, fs=8.4)
msg(ax, 50, 85, 17, "", color=GREEN, fs=8.0)
label(ax, 67.5, 18.0, "转发并记录", fs=7.8, color=GRAY)
msg(ax, 85, 50, 11, "输出回显", color=GREEN, fs=8.0, dash=True)

label(ax, 50, 2.6, "会话结束后，录像文件与命令记录一起入库，可按时间检索、回放。",
      fs=8.2, color=GRAY)

save(fig, "10/fig10_3.png")
