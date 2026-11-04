# -*- coding: utf-8 -*-
"""第 6 章插图：密钥、指纹与信任。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

from figstyle import (ACCENT, ACCENT_L, GRAY, GRAY_L, GREEN, GREEN_L, INK, RED,
                      RED_L, WARM, WARM_L, WHITE, arrow, box, canvas, elb_arrow,
                      label, lifeline, line, msg, note, save)


def tbox(ax, x, y, w, h, title, sub=None, fc=ACCENT_L, tfs=9.6, sfs=8.0,
         ec=INK, color=None):
    """带标题（可选副标题）的方框。"""
    box(ax, x, y, w, h, fc=fc, ec=ec)
    if sub:
        label(ax, x + w / 2.0, y + h * 0.66, title, fs=tfs, bold=True, color=color)
        label(ax, x + w / 2.0, y + h * 0.28, sub, fs=sfs, color=GRAY)
    else:
        label(ax, x + w / 2.0, y + h / 2.0, title, fs=tfs, bold=True, color=color)


# ---------------------------------------------------------------- 图 6-1
fig, ax = canvas(7.2, 4.2, 100)

lifeline(ax, 19, 54, 14, "客户端", sub="手里有私钥")
lifeline(ax, 81, 54, 14, "服务器", color=GREEN, sub="读 authorized_keys")

msg(ax, 19, 81, 45, "① 我想用这把公钥登录（算法 + 指纹）", color=ACCENT, fs=8.6)
msg(ax, 81, 19, 37, "② PK_OK：这把公钥可用，请签名", color=GREEN, fs=8.6)
msg(ax, 19, 81, 28, "③ 用私钥签名：会话标识 + 本次认证请求", color=ACCENT, fs=8.6)
msg(ax, 81, 19, 19, "④ 验签通过，认证成功", color=GREEN, fs=8.6)

label(ax, 50, 32.0, "服务器到 authorized_keys 里核对这把公钥",
      fs=8.0, color=GRAY)
label(ax, 50, 4.6, "私钥始终留在客户端：发出的只有签名，私钥本身从不传输",
      fs=8.4, color=GRAY)

save(fig, "07/fig07_1.png")

# ---------------------------------------------------------------- 图 6-2
fig, ax = canvas(7.4, 4.8, 100)

# 两个虚框代表两种情形
box(ax, 2, 11, 44, 45, fc="none", ec=GRAY, lw=0.9, radius=1.6)
box(ax, 54, 11, 44, 45, fc="none", ec=GRAY, lw=0.9, radius=1.6)
label(ax, 24, 58.6, "第一次连接", fs=10.2, bold=True)
label(ax, 76, 58.6, "再次连接", fs=10.2, bold=True)

# 左侧：首次连接
tbox(ax, 6, 47, 36, 7.5, "① 发起连接", fc=GRAY_L)
tbox(ax, 6, 36.5, 36, 7.5, "② 服务器出示主机公钥", "SHA256:9f2c…（指纹）", fc=ACCENT_L)
tbox(ax, 6, 26, 36, 7.5, "③ 与可信来源核对指纹", "运维给的、官网、控制台", fc=ACCENT_L)
tbox(ax, 6, 15.5, 36, 7.5, "④ 写入 known_hosts", fc=GREEN_L, ec=GREEN)

for y0, y1 in [(47, 44), (36.5, 33.5), (26, 23)]:
    arrow(ax, (24, y0), (24, y1), lw=0.9)

# 右侧：再次连接
tbox(ax, 58, 47, 36, 7.5, "① 发起连接", fc=GRAY_L)
tbox(ax, 58, 36.5, 36, 7.5, "② 取出 known_hosts 里的记录", fc=ACCENT_L)
tbox(ax, 58, 26, 36, 7.5, "③ 与出示的指纹比对", fc=ACCENT_L)
tbox(ax, 58, 15.5, 17, 8, "一致", "直接通过", fc=GREEN_L, ec=GREEN)
tbox(ax, 77, 15.5, 17, 8, "不一致", "拒绝连接", fc=RED_L, ec=RED)

for y0, y1 in [(47, 44), (36.5, 33.5)]:
    arrow(ax, (76, y0), (76, y1), lw=0.9)
arrow(ax, (66.5, 26), (66.5, 23.5), lw=0.9)
arrow(ax, (85.5, 26), (85.5, 23.5), lw=0.9)

label(ax, 50, 5.2, "指纹对不上：可能是中间人，也可能是服务器重装了系统。先核实，再决定是否删掉旧记录。",
      fs=8.2, color=GRAY)

save(fig, "07/fig07_3.png")

# ---------------------------------------------------------------- 图 6-3
fig, ax = canvas(7.4, 4.0, 100)

# 可选选项位
box(ax, 6, 46, 52, 6.6, fc=WARM_L, ec=WARM)
ax.text(32, 49.3, 'no-pty,command="/usr/bin/uptime"', ha="center", va="center",
        fontsize=8.0, family="monospace", color=INK, zorder=6)
label(ax, 60.5, 49.3, "选项位：可以整段省略", fs=8.2, color=WARM, ha="left")
arrow(ax, (11, 46), (11, 41.2), color=WARM, lw=0.8)
label(ax, 13.5, 43.6, "写在最前面", fs=7.9, color=WARM, ha="left")

# 主行三段
segs = [
    (6, 24, "ssh-ed25519"),
    (28, 62, "AAAAC3NzaC1lZDI1NTE5…"),
    (66, 92, "alice@laptop"),
]
fcs = [ACCENT_L, WARM_L, GREEN_L]
ecs = [ACCENT, WARM, GREEN]
for (x, w, txt), fc, ec in zip(segs, fcs, ecs):
    box(ax, x, 33, w - x, 7.6, fc=fc, ec=ec)
    ax.text((x + w) / 2.0, 36.8, txt, ha="center", va="center", fontsize=8.4,
            family="monospace", color=INK, zorder=6)

# 说明框
exp = [
    (6, 24, "算法名", "ed25519、rsa、ecdsa", ACCENT),
    (28, 62, "公钥本体（base64）", "这一段才是公开的那把钥匙", WARM),
    (66, 92, "注释", "只给人看，不影响登录", GREEN),
]
for x, w, title, sub, col in exp:
    box(ax, x, 18, w - x, 9.5, fc=WHITE, ec=col, lw=0.9)
    label(ax, (x + w) / 2.0, 24.4, title, fs=8.8, bold=True, color=col)
    label(ax, (x + w) / 2.0, 20.4, sub, fs=7.9, color=GRAY)

for x, w, _, _, col in exp:
    line(ax, ((x + w) / 2.0, 33), ((x + w) / 2.0, 27.5), color=col, lw=0.7,
         ls=(0, (3, 2)))

label(ax, 50, 10.6, "三段只用空格隔开，一行就是一条公钥；匹配到哪一行，那一行的选项跟着生效。",
      fs=8.2, color=GRAY)

save(fig, "07/fig07_2.png")

# ---------------------------------------------------------------- 图 6-4
fig, ax = canvas(7.2, 4.0, 100)

tbox(ax, 30, 41, 40, 10, "CA（签名密钥）", "用它签发的证书里写明：身份 + 公钥 + 有效期",
     fc=WARM_L, tfs=10.0, sfs=8.0)

tbox(ax, 4, 18, 30, 11, "服务器", "主机证书", fc=GREEN_L, ec=GREEN)
tbox(ax, 66, 18, 30, 11, "客户端", "用户证书", fc=ACCENT_L, ec=ACCENT)

arrow(ax, (44, 41), (22, 29.4), color=WARM, lw=1.0)
label(ax, 26.5, 34.0, "签发主机证书", fs=8.2, color=WARM, ha="right")
arrow(ax, (56, 41), (78, 29.4), color=WARM, lw=1.0)
label(ax, 73.5, 34.0, "签发用户证书", fs=8.2, color=WARM, ha="left")

arrow(ax, (34, 26.0), (66, 26.0), color=ACCENT, lw=0.9)
label(ax, 50, 27.8, "① 主机证书，客户端验签", fs=8.2, color=ACCENT)
arrow(ax, (66, 21.0), (34, 21.0), color=GREEN, lw=0.9)
label(ax, 50, 18.0, "② 用户证书，服务器验签", fs=8.2, color=GREEN)

label(ax, 50, 11.0, "双方只在本地预置同一个 CA 公钥：不再逐个核对主机指纹，也不再逐台分发 authorized_keys。",
      fs=8.2, color=GRAY)
label(ax, 50, 6.2, "证书里还写着有效期与用途，过期即失效，可以按时换发。",
      fs=8.2, color=GRAY)

save(fig, "07/fig07_4.png")
