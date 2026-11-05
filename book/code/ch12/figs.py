# -*- coding: utf-8 -*-
"""第 12 章插图：VS Code Remote-SSH。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

from figstyle import (ACCENT, ACCENT_L, GRAY, GRAY_L, GREEN, GREEN_L, INK, RED,
                      RED_L, WARM, WARM_L, WHITE, arrow, box, brace, canvas,
                      dot, elb_arrow, label, lifeline, line, msg, note, save)


def region(ax, x, y, w, h, title, sub=None):
    """用虚线大框圈出一台机器。"""
    p = box(ax, x, y, w, h, fc="white", ec=GRAY, lw=0.9, radius=1.8, zorder=1)
    p.set_linestyle((0, (6, 4)))
    label(ax, x + w / 2.0, y + h - 3.2, title, fs=10.2, bold=True)
    if sub:
        label(ax, x + w / 2.0, y + h - 6.0, sub, fs=8.0, color=GRAY)


def vbox(ax, x, y, w, h, title, sub=None, fc=WHITE, ec=INK, fs=9.0, bold=False):
    box(ax, x, y, w, h, fc=fc, ec=ec)
    if sub:
        label(ax, x + w / 2.0, y + h * 0.63, title, fs=fs, bold=bold)
        label(ax, x + w / 2.0, y + h * 0.28, sub, fs=7.7, color=GRAY)
    else:
        label(ax, x + w / 2.0, y + h / 2.0, title, fs=fs, bold=bold)


# ---------------------------------------------------------------- 图 10-1
fig, ax = canvas(7.4, 4.2, 100)

region(ax, 1.5, 4.5, 36, 45.5, "本机", "你面前的这台电脑")
region(ax, 62.5, 4.5, 36, 45.5, "远程主机", "Linux 服务器")

vbox(ax, 4.5, 31.0, 30, 8.0, "界面进程", "窗口、编辑器、终端标签", fc=ACCENT_L, ec=ACCENT)
vbox(ax, 4.5, 20.0, 30, 8.0, "扩展宿主进程", "跑本地扩展", fc=WHITE)
vbox(ax, 4.5, 9.0, 30, 8.0, "ssh 子进程", "系统 ssh 客户端", fc=WHITE)

arrow(ax, (12, 31), (12, 28.2), style="<|-|>")
label(ax, 14.0, 29.6, "本地 IPC", fs=7.8, color=GRAY, ha="left")
arrow(ax, (25, 20), (25, 17.2), style="<|-|>")
label(ax, 27.8, 18.6, "管道", fs=7.8, color=GRAY, ha="left")

# 右侧：vscode-server 是一个常驻进程，内部带几个服务
box(ax, 65, 6.0, 31, 34.5, fc="#fbfcfd", ec=ACCENT, lw=1.0)
label(ax, 80.5, 37.2, "vscode-server", fs=9.4, bold=True, color=ACCENT)
label(ax, 80.5, 34.4, "远程常驻进程", fs=7.7, color=GRAY)
for y, t in [(26.8, "扩展宿主进程"), (18.3, "文件服务"), (9.8, "终端服务")]:
    vbox(ax, 67.5, y, 26, 6.4, t, fc=WHITE, ec=GRAY, fs=8.6)

# 中间的隧道
arrow(ax, (34.5, 13.0), (65, 13.0), style="<|-|>", color=ACCENT, lw=1.3)
label(ax, 50, 14.8, "SSH 隧道（加密）", fs=8.8, color=ACCENT, bold=True)
note(ax, 50, 11.2, "补全、终端输出、文件读写\n都走这条隧道", fs=8.2, color=GRAY,
     ha="center", va="top")

label(ax, 50, 1.6, "虚线圈出的每个矩形，都是一个独立的操作系统进程", fs=8.2, color=GRAY)

save(fig, "12/fig12_1.png")

# ---------------------------------------------------------------- 图 10-2
fig, ax = canvas(7.0, 4.3, 100)

lifeline(ax, 12, 59, 12.5, "本地 VS Code", sub="界面进程")
lifeline(ax, 37, 59, 12.5, "ssh 客户端", color=GRAY, sub="读 ~/.ssh/config")
lifeline(ax, 63, 59, 12.5, "目标机 sshd", color=GREEN, sub="认证与会话")
lifeline(ax, 88, 59, 12.5, "vscode-server", color=WARM, sub="远程扩展宿主")

steps = [
    (51.0, 12, 37, "① 启动 ssh 子进程", INK, False),
    (46.0, 37, 63, "② TCP 连接、协商算法、认证", INK, False),
    (41.0, 63, 37, "③ 认证通过", GRAY, True),
    (36.0, 37, 63, "④ 请求启动 server", INK, False),
    (31.0, 63, 88, "⑤ 没有就下载安装", INK, False),
    (26.0, 88, 63, "⑥ 报告端口与 token", GRAY, True),
    (21.0, 63, 37, "⑦ server 已就绪", GRAY, True),
    (16.0, 12, 37, "⑧ 界面连本地端口", INK, False),
]
for y, x1, x2, t, c, d in steps:
    msg(ax, x1, x2, y, t, color=c, dash=d, fs=8.5)

note(ax, 50, 5.2, "箭头方向就是发起方；排错时先确定卡在第几步", fs=8.2, color=GRAY, ha="center")

save(fig, "12/fig12_2.png")

# ---------------------------------------------------------------- 图 10-3
fig, ax = canvas(7.4, 3.5, 100)

label(ax, 17.0, 43.4, "① 你写的配置", fs=9.6, bold=True)
label(ax, 54.0, 43.4, "② ssh 展开成真实参数", fs=9.6, bold=True)
label(ax, 86.5, 43.4, "③ 实际走两跳", fs=9.6, bold=True)

box(ax, 1.0, 5.0, 32, 30.0, fc="#fbfcfd", ec=GRAY, lw=0.9)
label(ax, 3.0, 32.4, "C:/Users/alice/.ssh/config", fs=7.4, ha="left", color=GRAY)
cfg = [
    "Host l40-server",
    "    HostName 203.0.113.24",
    "    Port 58222",
    "    User alice@ubuntu@10.0.0.5",
    "    IdentityFile ~/.ssh/ssh.jumpserver.pem",
]
for i, t in enumerate(cfg):
    label(ax, 3.0, 29.0 - i * 4.7, t, fs=7.6, ha="left",
          color=ACCENT if i == 0 else GRAY, bold=(i == 0))

arrow(ax, (33.2, 24.7), (35.9, 24.7), color=GRAY)
arrow(ax, (72.4, 24.7), (75.7, 24.7), color=GRAY)

for y, t in [(29.0, "地址 203.0.113.24"),
             (21.5, "端口 58222"),
             (14.0, "用户 alice@ubuntu@10.0.0.5"),
             (6.5, "私钥 ~/.ssh/ssh.jumpserver.pem")]:
    vbox(ax, 36.5, y, 35, 6.4, t, fc=ACCENT_L, ec=ACCENT, fs=8.2)

vbox(ax, 76, 31.5, 22, 6.4, "本机", fc=WHITE, ec=GRAY, fs=8.6)
vbox(ax, 76, 20.0, 22, 8.6, "堡垒机", "203.0.113.24:58222", fc=WARM_L, ec=WARM, fs=8.8)
vbox(ax, 76, 7.5, 22, 8.6, "目标机", "10.0.0.5:22", fc=GREEN_L, ec=GREEN, fs=8.8)

arrow(ax, (87, 31.5), (87, 28.7))
label(ax, 88.2, 30.1, "第一跳", fs=7.6, color=GRAY, ha="left")
arrow(ax, (87, 20.0), (87, 16.2))
label(ax, 88.2, 18.1, "第二跳", fs=7.6, color=GRAY, ha="left")

note(ax, 50, 1.6, "把目标写进 User 字段是堡垒机的约定；用 ProxyJump 则拆成两行，一跳一段",
     fs=8.0, color=GRAY, ha="center")

save(fig, "12/fig12_4.png")

# ---------------------------------------------------------------- 图 10-4
fig, ax = canvas(7.4, 3.7, 100)

region(ax, 1.0, 4.0, 39, 43.0, "本机", "客户端侧")
region(ax, 60.0, 4.0, 39, 43.0, "远程主机", "服务端侧")

vbox(ax, 3.5, 30.0, 34, 8.0, "VS Code 界面进程", fc=ACCENT_L, ec=ACCENT, fs=8.8)
vbox(ax, 3.5, 19.0, 34, 8.6, "127.0.0.1:5xxxx", "本地监听端口（随机）", fc=WHITE, ec=ACCENT, fs=8.6)
vbox(ax, 3.5, 8.0, 34, 8.0, "ssh 客户端（-L）", fc=WHITE, ec=INK, fs=8.8)

arrow(ax, (13.5, 30.0), (13.5, 27.6))
label(ax, 14.8, 28.8, "http / ws", fs=7.8, color=GRAY, ha="left")
arrow(ax, (13.5, 19.0), (13.5, 16.0))
label(ax, 14.8, 17.4, "明文请求", fs=7.8, color=GRAY, ha="left")

vbox(ax, 62.5, 30.0, 34, 8.0, "vscode-server", fc=WARM_L, ec=WARM, fs=8.8)
vbox(ax, 62.5, 19.0, 34, 8.6, "/tmp/vscode-ipc-xxxx.sock", "远程 socket 监听", fc=WHITE, ec=WARM, fs=7.8)
vbox(ax, 62.5, 8.0, 34, 8.0, "sshd", fc=WHITE, ec=GREEN, fs=8.8)

arrow(ax, (79.5, 16.0), (79.5, 19.0))
label(ax, 80.8, 17.4, "connect", fs=7.8, color=GRAY, ha="left")
arrow(ax, (79.5, 27.6), (79.5, 30.0))
label(ax, 80.8, 28.8, "stdio", fs=7.8, color=GRAY, ha="left")

arrow(ax, (37.5, 12.0), (62.5, 12.0), style="<|-|>", color=ACCENT, lw=1.3)
label(ax, 50, 13.8, "SSH 隧道", fs=8.8, color=ACCENT, bold=True)
label(ax, 50, 10.2, "字节原样搬运", fs=7.8, color=GRAY)

note(ax, 50, 1.6, "远程也可能不用 socket，而是监听 127.0.0.1 的随机端口", fs=8.0, color=GRAY,
     ha="center")

save(fig, "12/fig12_3.png")
