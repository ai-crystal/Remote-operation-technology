# -*- coding: utf-8 -*-
"""第 18 章插图：会员、登录与权限。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

from figstyle import (ACCENT, ACCENT_L, GRAY, GRAY_L, GREEN, GREEN_L, INK, RED,
                      RED_L, WARM, WARM_L, WHITE, arrow, box, canvas, label,
                      lifeline, line, msg, note, save)


def tbox(ax, x, y, w, h, title, sub=None, fc=ACCENT_L, ec=INK, tfs=9.0, sfs=6.9):
    box(ax, x, y, w, h, fc=fc, ec=ec)
    if sub:
        label(ax, x + w / 2.0, y + h * 0.66, title, fs=tfs, bold=True)
        label(ax, x + w / 2.0, y + h * 0.26, sub, fs=sfs, color=GRAY)
    else:
        label(ax, x + w / 2.0, y + h / 2.0, title, fs=tfs, bold=True)


# ---------------------------------------------------------------- 图 18-1
fig, ax = canvas(7.4, 4.8, 100)
ax.set_ylim(0, 65)

lifeline(ax, 20, 60, 10.0, "浏览器", color=GRAY, fs=9.0)
lifeline(ax, 50, 60, 10.0, "你的服务端", color=ACCENT, fs=9.0)
lifeline(ax, 82, 60, 10.0, "GitHub", color=GREEN, fs=9.0)

steps = [
    (49.2, 20, 50, "① 点“用 GitHub 登录”", False),
    (45.0, 50, 20, "② 302 到授权页", True),
    (40.8, 20, 82, "③ 用户同意授权", False),
    (36.6, 82, 20, "④ 302 回调，带一次性 code", True),
    (32.4, 20, 50, "⑤ 把 code 交给服务端", False),
    (28.2, 50, 82, "⑥ code + 应用密钥换 token", False),
    (24.0, 82, 50, "⑦ access_token + 用户资料", True),
    (19.8, 50, 20, "⑧ 签发本站会话（Cookie）", True),
]
for y, x1, x2, text, dash in steps:
    msg(ax, x1, x2, y, text, fs=8.0, dash=dash)

label(ax, 50, 14.4, "第 ⑥ 步必须由服务端做：应用密钥不能出现在浏览器里。",
      fs=7.8, color=ACCENT)
label(ax, 50, 6.4, "回调地址要严格校验，否则授权码会被骗到别人的站点。", fs=7.6, color=GRAY)

save(fig, "18/fig18_1.png")

# ---------------------------------------------------------------- 图 18-2
fig, ax = canvas(7.4, 3.4, 100)

tbox(ax, 1, 22, 14, 10, "上传请求", "带凭证", fc=GRAY_L, ec=GRAY, tfs=8.4, sfs=6.8)
gates = [
    (19, 15, "认证", "你是谁", ACCENT_L, ACCENT),
    (38, 15, "会员等级", "能用什么", WARM_L, WARM),
    (57, 15, "额度", "还能用几次", RED_L, RED),
]
for x, w, name, sub, fc, ec in gates:
    tbox(ax, x, 22, w, 10, name, sub, fc=fc, ec=ec, tfs=8.4, sfs=6.8)

tbox(ax, 76, 22, 14, 10, "落盘", "写临时文件", fc=GREEN_L, ec=GREEN, tfs=8.4, sfs=6.8)
tbox(ax, 76, 6, 14, 9, "入队", "返回任务号", fc=GREEN_L, ec=GREEN, tfs=8.4, sfs=6.8)

for x1, x2 in ((15.4, 18.6), (34.4, 37.6), (53.4, 56.6), (72.4, 75.6)):
    arrow(ax, (x1, 27), (x2, 27), lw=1.0)
arrow(ax, (83, 21.6), (83, 15.4), lw=1.0, color=GREEN)

for x, code in ((26.5, "401"), (45.5, "403"), (64.5, "429")):
    arrow(ax, (x, 21.6), (x, 15.4), lw=0.9, color=RED, ls=(0, (2, 2)))
    label(ax, x, 12.0, code, fs=8.2, bold=True, color=RED)

label(ax, 26.5, 8.2, "去登录", fs=6.8, color=GRAY)
label(ax, 45.5, 8.2, "升级会员", fs=6.8, color=GRAY)
label(ax, 64.5, 8.2, "等一会儿", fs=6.8, color=GRAY)

label(ax, 50, 1.4, "顺序不能反：未认证、没额度的请求，不该有机会写磁盘、占队列。",
      fs=8.0, color=GRAY)

save(fig, "18/fig18_2.png")
