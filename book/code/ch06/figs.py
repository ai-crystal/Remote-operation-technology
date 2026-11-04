# -*- coding: utf-8 -*-
"""第 5 章插图：SSH 协议的三层结构。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

from matplotlib.patches import Rectangle

from figstyle import (ACCENT, ACCENT_L, GRAY, GRAY_L, GREEN, GREEN_L, INK, RED,
                      RED_L, WARM, WARM_L, WHITE, arrow, box, brace, canvas,
                      elb_arrow, label, lifeline, line, msg, note, save)


# ---------------------------------------------------------------- 图 5-1
fig, ax = canvas(7.0, 4.0, 100)
ax.set_ylim(0, 57)

layers = [
    ("连接协议", "RFC 4254", "通道：shell、exec、sftp、端口转发", ACCENT_L, ACCENT),
    ("用户认证协议", "RFC 4252", "password、publickey、keyboard-interactive",
     WARM_L, WARM),
    ("传输层协议", "RFC 4253", "版本交换、算法协商、密钥交换、加密与完整性",
     GREEN_L, GREEN),
    ("TCP 连接", "端口 22", "一条有序的字节流", GRAY_L, GRAY),
]
ys = [44.0, 32.0, 20.0, 7.0]
hs = [9.0, 9.0, 9.0, 8.6]
for (name, rfc, detail, fc, ec), y, h in zip(layers, ys, hs):
    box(ax, 3, y, 74, h, fc=fc, ec=ec, lw=1.1, radius=1.2)
    label(ax, 6, y + h / 2, name, fs=9.0, bold=True, ha="left")
    label(ax, 28, y + h / 2 + 1.7, rfc, fs=7.0, color=GRAY, ha="left")
    label(ax, 28, y + h / 2 - 1.9, detail, fs=7.4, ha="left")

# 上两层都在加密通道内
ax.plot([77.5, 79.5, 79.5, 77.5], [53, 53, 29, 29], color=GRAY, lw=0.9)
label(ax, 81.4, 41, "这两层\n都在加密\n通道内部", fs=7.2, color=GRAY, ha="left")
label(ax, 80.4, 24.5, "通道由它\n建起来", fs=7.2, color=GRAY, ha="left")
label(ax, 80.4, 11.3, "通道跑在\n字节流上", fs=7.2, color=GRAY, ha="left")

save(fig, "06/fig06_1.png")

# ---------------------------------------------------------------- 图 5-2
fig, ax = canvas(7.4, 2.96, 100)
ax.set_ylim(0, 40)

PY, PH = 25.0, 14.0
cells = [(2, 9, "包长度\n4 字节", ACCENT_L, ACCENT),
         (11, 6.5, "填充\n长度\n1 字节", ACCENT_L, ACCENT),
         (17.5, 43.5, "载荷\n消息类型 + 字段", WHITE, ACCENT),
         (61, 14, "随机填充\n至少 4 字节", GRAY_L, GRAY),
         (78, 20, "MAC\n32 字节", WARM_L, WARM)]
for x, w, t, fc, ec in cells:
    box(ax, x, PY, w, PH, t, fc=fc, ec=ec, fs=7.6, radius=0.6, lw=0.9)

brace(ax, 2, 75, PY - 2.2, "整个包先加密（ETM 下前 4 字节不加密）", height=1.6,
      upward=False, color=ACCENT, fs=7.2)
label(ax, 88, PY - 4.4, "MAC 覆盖\n加密后的内容", fs=7.0, color=WARM)

label(ax, 50, 11.2, "载荷首字节是消息类型编号（20 = SSH_MSG_KEXINIT）；接收方先验 MAC 再解密",
      fs=7.4)
label(ax, 50, 4.8, "整包（不含长度字段与 MAC）至少 16 字节；填充至少 4 字节，用来凑满整块",
      fs=7.4, color=GRAY)

save(fig, "06/fig06_2.png")

# ---------------------------------------------------------------- 图 5-3
fig, ax = canvas(7.0, 4.3, 100)
ax.set_ylim(0, 61.4)

label(ax, 3, 56.0, "客户端的列表（有先后）", fs=8.0, bold=True, color=ACCENT,
      ha="left")
label(ax, 55, 56.0, "服务端的列表（只是集合）", fs=8.0, bold=True, color=WARM,
      ha="left")

client = [("curve25519-sha256", True), ("ecdh-sha2-nistp256", False),
          ("diffie-hellman-group14-sha256", False),
          ("diffie-hellman-group1-sha1", None)]
server = [("curve25519-sha256", True), ("ecdh-sha2-nistp256", False),
          ("diffie-hellman-group14-sha256", False)]

for i, (name, hit) in enumerate(client):
    y = 44.0 - i * 9.4
    fc = GREEN_L if hit else (WHITE if hit is False else GRAY_L)
    ec = GREEN if hit else (ACCENT if hit is False else GRAY)
    box(ax, 4, y, 40, 7.4, name, fc=fc, ec=ec, fs=7.4, radius=0.6, lw=0.9,
        color=INK if hit is not None else GRAY)
    label(ax, 2.2, y + 3.7, "%d" % (i + 1), fs=7.0, color=GRAY, ha="right")

for i, (name, hit) in enumerate(server):
    y = 44.0 - i * 9.4
    fc = GREEN_L if hit else WHITE
    ec = GREEN if hit else WARM
    box(ax, 55, y, 40, 7.4, name, fc=fc, ec=ec, fs=7.4, radius=0.6, lw=0.9)

# 命中标记
label(ax, 49.6, 47.7, "匹配", fs=7.2, color=GREEN, bold=True)
label(ax, 49.6, 17.8, "服务端\n没有它", fs=6.6, color=GRAY)

label(ax, 50, 12.2, "从客户端列表的头开始，取第一个服务端也支持的算法",
      fs=7.6, color=INK)
label(ax, 50, 7.2, "两边没有交集时协商直接失败（no matching key exchange method）",
      fs=7.4, color=GRAY)

save(fig, "06/fig06_3.png")

# ---------------------------------------------------------------- 图 5-4
fig, ax = canvas(7.2, 4.9, 100)
ax.set_ylim(0, 68)

lifeline(ax, 24, 63, 22, "客户端", fs=9.2)
lifeline(ax, 76, 63, 22, "服务器", color=GREEN, fs=9.2)

msg(ax, 24, 76, 54, "KEXINIT（20）：我支持这些算法", color=ACCENT, fs=8.0)
msg(ax, 76, 24, 48, "KEXINIT（20）：这是我的列表", color=GREEN, fs=8.0)
msg(ax, 24, 76, 40, "KEX_ECDH_INIT（30）：临时公钥 Q_C", color=ACCENT, fs=8.0)
msg(ax, 76, 24, 32, "KEX_ECDH_REPLY（31）：K_S、Q_S、签名", color=GREEN, fs=8.0)
msg(ax, 24, 76, 24.5, "NEWKEYS（21）：下一条起换新密钥", color=ACCENT, fs=8.0)

# 交换哈希与派生
box(ax, 3, 2, 94, 14.5, fc=GRAY_L, ec=GRAY, lw=0.9, radius=1.2)
label(ax, 50, 12.8, "交换哈希 H = SHA256(V_C || V_S || I_C || I_S || K_S || Q_C || Q_S || K)",
      fs=7.4)
label(ax, 50, 8.5, "双方各自用临时私钥和对方的临时公钥算出 K；会话密钥全部由 K 与 H 派生",
      fs=7.4, color=GRAY)
label(ax, 50, 4.9, "IV、加密密钥、MAC 密钥各两个方向，客户端与服务器互不共用",
      fs=7.4, color=GRAY)

save(fig, "06/fig06_4.png")
