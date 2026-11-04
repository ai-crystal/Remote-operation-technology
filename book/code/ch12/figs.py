# -*- coding: utf-8 -*-
"""第 12 章插图：签名与权限。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

from figstyle import (ACCENT, ACCENT_L, GRAY, GRAY_L, GREEN, GREEN_L, INK, RED,
                      RED_L, WARM, WARM_L, WHITE, arrow, box, brace, canvas,
                      dot, elb_arrow, label, lifeline, line, msg, note, save)
from matplotlib.patches import Polygon


def diamond(ax, cx, cy, w, h, text, fc=WHITE, ec=ACCENT, fs=8.4, lw=1.0):
    p = Polygon([[cx, cy + h / 2.0], [cx + w / 2.0, cy], [cx, cy - h / 2.0],
                 [cx - w / 2.0, cy]], closed=True, facecolor=fc, edgecolor=ec,
                linewidth=lw, zorder=3)
    ax.add_patch(p)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
            linespacing=1.5, zorder=4)


def mono(ax, x, y, text, fs=7.2, color=INK, ha="left"):
    ax.text(x, y, text, fontsize=fs, color=color, ha=ha, va="center",
            family="monospace", zorder=4)


# ---------------------------------------------------------------- 图 12-1
fig, ax = canvas(7.4, 3.9, 100)

parts = [
    ("① HTTP 方法", "GET"),
    ("② 规范化 URI", "/train/model.bin"),
    ("③ 规范化查询串", "按参数名排序后拼接"),
    ("④ 规范化头部", "小写名 + 单个冒号 + 值"),
    ("⑤ 签名头部列表", "host;x-amz-content-sha256;x-amz-date"),
]
for i, (t, v) in enumerate(parts):
    y = 38.4 - i * 7.9
    box(ax, 1.0, y, 30, 6.6, fc=WHITE, ec=GRAY, lw=0.9)
    label(ax, 16.0, y + 4.4, t, fs=8.5, bold=True)
    label(ax, 16.0, y + 1.9, v, fs=7.4, color=GRAY)

arrow(ax, (31.4, 27.4), (32.8, 27.4), color=GRAY)

# 拼起来的规范请求原文
box(ax, 33.0, 6.0, 45, 40.0, fc="#fbfcfd", ec=GRAY, lw=0.9)
label(ax, 55.5, 49.2, "CanonicalRequest：五段按固定顺序拼成一段文本", fs=8.6, bold=True)

rows = [
    ("GET", "方法"),
    ("/train/model.bin", "URI"),
    ("", "查询"),
    ("host:s3.example.com", "头部"),
    ("x-amz-date:20261104T040000Z", ""),
    ("x-amz-content-sha256:UNSIGNED-PAYLOAD", ""),
    ("host;x-amz-content-sha256;x-amz-date", "签名头"),
    ("UNSIGNED-PAYLOAD", "载荷"),
]
for i, (t, tag) in enumerate(rows):
    y = 40.0 - i * 4.0
    if t:
        mono(ax, 41.5, y, t, fs=7.6)
    else:
        label(ax, 41.5, y, "（没有查询参数时，这一行是空的）", fs=6.8,
              color="#b3b8bc", ha="left")
    if tag:
        label(ax, 39.5, y, tag, fs=7.0, color=GRAY, ha="right")

arrow(ax, (78.4, 25.0), (83.6, 25.0), color=GRAY)
label(ax, 81.0, 26.2, "哈希", fs=7.8, color=GRAY)
box(ax, 84.0, 17.0, 15, 16.0, fc=WARM_L, ec=WARM)
label(ax, 91.5, 28.6, "SHA-256", fs=8.2, bold=True, color=WARM)
label(ax, 91.5, 25.4, "得到摘要", fs=7.4, color=GRAY)
label(ax, 91.5, 21.4, "64 个\n十六进制字符", fs=7.2, color=GRAY)

save(fig, "12/fig12_1.png")

# ---------------------------------------------------------------- 图 12-2
fig, ax = canvas(7.2, 4.2, 100)

steps = [
    ('kDate = HMAC("AWS4" + SK, 20261104)', "掺入日期", ACCENT_L, ACCENT),
    ('kRegion = HMAC(kDate, "us-east-1")', "掺入区域名", WHITE, GRAY),
    ('kService = HMAC(kRegion, "s3")', "掺入服务名", WHITE, GRAY),
    ('kSigning = HMAC(kService, "aws4_request")', "掺入固定串", WHITE, GRAY),
    ('signature = HMAC(kSigning, StringToSign)', "最后签摘要", ACCENT_L, ACCENT),
]
for i, (f, tag, fc, ec) in enumerate(steps):
    x = 3.0 + i * 2.0
    y = 46.0 - i * 10.2
    box(ax, x, y, 46, 7.0, fc=fc, ec=ec, lw=1.0)
    mono(ax, x + 2.0, y + 3.5, f, fs=7.4)
    label(ax, x + 47.5, y + 3.5, tag, fs=7.6, color=GRAY, ha="left")
    if i < len(steps) - 1:
        arrow(ax, (x + 23, y), (x + 25, y - 3.2), color=GRAY)

box(ax, 69.0, 22.0, 29, 24.0, fc="#fbfcfd", ec=GRAY, lw=0.9)
label(ax, 83.5, 42.0, "为什么绕四级", fs=8.2, bold=True)
for k, t in enumerate(["SK 只有一把，", "每天、每个区域、", "每个服务各自派生，",
                       "一处泄露不牵连别处。"]):
    label(ax, 83.5, 37.4 - k * 4.0, t, fs=7.3, color=GRAY)

note(ax, 2.0, 1.8, "每一级都多掺一样东西，所以签名与「日期 + 区域 + 服务 + 密钥」全部绑定",
     fs=7.8, color=GRAY, ha="left")

save(fig, "12/fig12_2.png")

# ---------------------------------------------------------------- 图 12-3
fig, ax = canvas(7.2, 3.1, 100)

label(ax, 30.0, 39.8, "一整串 URL 拆开看：谁拿到都能用，所以每一段都得能解释", fs=8.2, color=GRAY)

url_rows = [
    ("https://bucket.oss.example.com", GRAY,
     "协议 + 域名（桶名在域名里）"),
    ("/datasets/train.bin", GRAY,
     "对象键：路径风格时桶名写在这里"),
    ("?X-Amz-Algorithm=AWS4-HMAC-SHA256", ACCENT,
     "签名算法，取值固定"),
    ("&X-Amz-Credential=AKID****/20261104/us-east-1/s3/aws4_request", WARM,
     "用哪把钥匙、哪天的、哪个区域与服务"),
    ("&X-Amz-Date=20261104T040000Z", INK,
     "签发时刻（UTC）"),
    ("&X-Amz-Expires=3600", INK,
     "多少秒之后失效"),
    ("&X-Amz-SignedHeaders=host", INK,
     "哪些请求头参与了签名"),
    ("&X-Amz-Signature=9f2c1b7e…", ACCENT,
     "最终签名：改动任何一段都会失效"),
]
for i, (t, c, lab) in enumerate(url_rows):
    y = 36.0 - i * 4.2
    mono(ax, 2.0, y, t, fs=6.8, color=c)
    endx = 2.0 + len(t) * 0.79 + 1.2
    line(ax, (endx, y), (54.0, y), color="#c8ccd0", lw=0.7, ls=(0, (1, 2)))
    label(ax, 55.5, y, lab, fs=7.6, color=INK, ha="left")

save(fig, "12/fig12_3.png")

# ---------------------------------------------------------------- 图 12-4
fig, ax = canvas(7.2, 4.2, 100)

box(ax, 28.0, 50.0, 34, 6.4, "一次请求：谁、想做什么、对哪个资源", fc=GRAY_L, ec=GRAY)
arrow(ax, (45, 50.0), (45, 46.6), color=GRAY)

box(ax, 2.0, 32.0, 24, 15.0, fc="#fbfcfd", ec=GRAY, lw=0.9)
label(ax, 14.0, 43.6, "参与判断的策略", fs=7.8, bold=True)
label(ax, 14.0, 39.4, "桶策略 / 身份策略", fs=7.3, color=GRAY)
label(ax, 14.0, 36.0, "ACL / 会话策略", fs=7.3, color=GRAY)
arrow(ax, (26.2, 40.0), (29.6, 40.0), color=GRAY)

diamond(ax, 45, 40, 30, 13, "任一处\n显式 Deny？")
arrow(ax, (60.0, 40.0), (71.5, 40.0))
label(ax, 65.5, 41.3, "是", fs=8.0)
box(ax, 72.0, 35.5, 26, 9.0, "直接拒绝", fc=RED_L, ec=RED, fs=9.2, bold=True)

arrow(ax, (45, 33.5), (45, 28.5))
label(ax, 46.4, 31.0, "否", fs=8.0, ha="left")

diamond(ax, 45, 22, 30, 13, "有显式\nAllow？")
arrow(ax, (60.0, 22.0), (71.5, 22.0))
label(ax, 65.5, 23.3, "否", fs=8.0)
box(ax, 72.0, 17.5, 26, 9.0, "仍然拒绝\n（默认拒绝）", fc=RED_L, ec=RED, fs=8.6)

arrow(ax, (45, 15.5), (45, 11.2))
label(ax, 46.4, 13.3, "是", fs=8.0, ha="left")
box(ax, 30.0, 4.0, 30, 7.2, "放行，请求被执行", fc=GREEN_L, ec=GREEN, fs=8.8, bold=True)

label(ax, 45.0, 1.2, "显式拒绝优先于任何允许，所以排权限时先找有没有 deny", fs=7.8, color=GRAY)

save(fig, "12/fig12_4.png")
