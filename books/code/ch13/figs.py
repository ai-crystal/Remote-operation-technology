# -*- coding: utf-8 -*-
"""第 13 章插图：对象存储的模型。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

from figstyle import (ACCENT, ACCENT_L, GRAY, GRAY_L, GREEN, GREEN_L, INK, RED,
                      RED_L, WARM, WARM_L, WHITE, arrow, box, brace, canvas,
                      dot, elb_arrow, label, lifeline, line, msg, note, save)


def card(ax, x, y, w, h, key, meta, hl=False):
    """一个对象卡片：键在上，元数据在下。"""
    box(ax, x, y, w, h, fc=ACCENT_L if hl else WHITE,
        ec=ACCENT if hl else GRAY, lw=1.0 if hl else 0.9)
    label(ax, x + 2.4, y + h * 0.68, key, fs=8.3, ha="left",
          color=ACCENT if hl else INK, bold=hl)
    label(ax, x + 2.4, y + h * 0.26, meta, fs=7.4, ha="left", color=GRAY)


# ---------------------------------------------------------------- 图 13-1
fig, ax = canvas(7.4, 4.25, 100)

# 左：账号里的桶清单
box(ax, 1.0, 6.0, 34, 44.0, fc="#fbfcfd", ec=GRAY, lw=0.9)
label(ax, 18.0, 46.3, "账号（Account）", fs=9.8, bold=True)
label(ax, 18.0, 43.0, "谁在调用：一对 AK/SK", fs=7.8, color=GRAY)
for y, t, hl in [(32.0, "bucket-training", True),
                 (21.5, "bucket-data", False),
                 (11.0, "bucket-backup", False)]:
    box(ax, 4.0, y, 28, 8.0, fc=ACCENT_L if hl else WHITE,
        ec=ACCENT if hl else GRAY, lw=1.0 if hl else 0.9)
    label(ax, 18.0, y + 4.0, t, fs=8.4, bold=hl, color=ACCENT if hl else INK)

arrow(ax, (35.4, 26.0), (43.8, 26.0), color=GRAY)
label(ax, 39.6, 27.4, "展开", fs=7.8, color=GRAY)

# 右：桶里的对象
box(ax, 44.0, 6.0, 55, 44.0, fc=WHITE, ec=ACCENT, lw=1.1)
label(ax, 46.5, 46.3, "桶（Bucket）bucket-training", fs=9.6, bold=True,
      color=ACCENT, ha="left")
label(ax, 46.5, 42.9, "每个对象 = 键 + 元数据 + 数据", fs=7.8, color=GRAY, ha="left")

card(ax, 47.0, 29.0, 49, 9.4, "datasets/2026/train-0001.parquet",
     "size 128 MB · etag 5d41c9… · 标准存储", hl=True)
card(ax, 47.0, 18.2, 49, 9.4, "datasets/2026/train-0002.parquet",
     "size 131 MB · etag 7a2e40… · 标准存储")
card(ax, 47.0, 7.4, 49, 9.4, "models/ckpt-epoch-10.pt",
     "size 2.4 GB · etag c19b83… · 低频访问")

note(ax, 50, 2.2, "键里的斜杠只是名字的一部分：没有目录，也没有 mkdir；列对象时可以用前缀筛选",
     fs=8.0, color=GRAY, ha="center")

save(fig, "13/fig13_1.png")

# ---------------------------------------------------------------- 图 13-2
fig, ax = canvas(7.4, 3.6, 100)

cols = [(1.0, "块存储", "Block Storage"), (34.5, "文件存储", "File Storage"),
        (68.0, "对象存储", "Object Storage")]
for c, t, sub in cols:
    label(ax, c + 15.5, 45.2, t, fs=10.2, bold=True)
    label(ax, c + 15.5, 42.0, sub, fs=7.8, color=GRAY)

# 块存储
c = 1.0
box(ax, c + 2, 31.0, 27, 7.0, "一台服务器", fc=WHITE, ec=INK, fs=8.8)
arrow(ax, (c + 15.5, 31.0), (c + 15.5, 27.0))
label(ax, c + 17.0, 28.4, "挂载", fs=7.8, color=GRAY, ha="left")

box(ax, c + 2.4, 20.6, 26.0, 6.3, fc=ACCENT_L, ec=ACCENT, lw=1.1, radius=0.9)
for k in range(1, 5):
    line(ax, (c + 2.4 + k * 5.2, 20.6), (c + 2.4 + k * 5.2, 26.9), color=ACCENT, lw=0.8, zorder=4)
label(ax, c + 15.5, 18.4, "固定大小的块（/dev/vdb）", fs=7.6, color=GRAY)

# 文件存储：用线条画一棵目录树
c = 34.5
label(ax, c + 7.6, 34.0, "/", fs=9.4, bold=True, ha="right")
line(ax, (c + 8.2, 33.6), (c + 8.2, 20.6), color=GRAY, lw=0.9)
for yb, name in [(30.4, "data/"), (21.6, "code/")]:
    line(ax, (c + 8.2, yb), (c + 11.0, yb), color=GRAY, lw=0.9)
    label(ax, c + 11.6, yb, name, fs=8.4, ha="left", bold=True)
    line(ax, (c + 12.9, yb - 0.6), (c + 12.9, yb - 4.4), color=GRAY, lw=0.9)
    line(ax, (c + 12.9, yb - 4.4), (c + 14.2, yb - 4.4), color=GRAY, lw=0.9)
label(ax, c + 14.8, 26.0, "train.bin", fs=8.0, ha="left", color=GRAY)
label(ax, c + 14.8, 17.2, "fig.py", fs=8.0, ha="left", color=GRAY)

# 对象存储
c = 68.0
box(ax, c + 2, 31.0, 27, 7.0, "客户端", fc=WHITE, ec=INK, fs=8.8)
arrow(ax, (c + 15.5, 31.0), (c + 15.5, 28.0))
label(ax, c + 17.0, 29.2, "HTTP", fs=7.8, color=GRAY, ha="left")
box(ax, c + 2, 16.0, 27, 11.6, fc=WHITE, ec=ACCENT, lw=1.0)
for i, t in enumerate(["datasets/train.bin", "models/ckpt.pt", "logs/run.json"]):
    label(ax, c + 4.0, 24.6 - i * 3.5, t, fs=7.4, ha="left", color=GRAY)

traits = [
    "按固定大小的块读写\n像一块本地硬盘",
    "目录树与文件句柄\n多台机器可同时挂载",
    "扁平键值 + HTTP 接口\n整个对象读、整个对象写",
]
for (c, _, _), t in zip(cols, traits):
    label(ax, c + 15.5, 11.6, t, fs=8.2)

label(ax, 50, 3.4, "三种形态对应三种用法：系统盘、共享协作目录、海量非结构化数据",
      fs=8.2, color=GRAY)

save(fig, "13/fig13_2.png")

# ---------------------------------------------------------------- 图 13-3
fig, ax = canvas(6.8, 4.4, 100)

lifeline(ax, 16, 60, 8.5, "客户端", sub="你的程序或 CLI")
lifeline(ax, 78, 60, 8.5, "对象存储", color=ACCENT, sub="按 HTTP 接口应答")

steps = [
    (52.0, 16, 78, "① InitiateMultipartUpload", INK, False),
    (46.5, 78, 16, "返回 UploadId", GRAY, True),
    (40.5, 16, 78, "② UploadPart #1", INK, False),
    (36.0, 16, 78, "② UploadPart #2", INK, False),
    (31.5, 16, 78, "② UploadPart #N", INK, False),
    (22.0, 16, 78, "③ CompleteMultipartUpload（交 part 号与 ETag）", INK, False),
    (16.5, 78, 16, "返回最终 ETag", GRAY, True),
    (11.0, 16, 78, "中途放弃：AbortMultipartUpload", GRAY, True),
]
for y, x1, x2, t, c, d in steps:
    msg(ax, x1, x2, y, t, color=c, dash=d, fs=8.4)

note(ax, 47, 26.8, "单片 5 MiB–5 GiB，最多 10000 片；各片可并发、可单独重传", fs=8.0,
     color=WARM, ha="center")

save(fig, "13/fig13_3.png")
