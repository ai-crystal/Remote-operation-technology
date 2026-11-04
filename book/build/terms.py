# -*- coding: utf-8 -*-
"""术语体检：找出“第一次出现却没有解释”的专业词。

判定办法，在术语首次出现的段落里，往后 80 个字内应当出现
“指 / 叫 / 即 / 是一种 / 也就是 / 全称 / 简称 / 括号注释”之类的解释迹象。
没有就列出来，人工补一句再跑一次。
"""

import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(HERE)

TERMS = """
SSH sshd OpenSSH 终端 shell 伪终端 主机密钥 公钥 私钥 证书 CA 凭据
IPv4 IPv6 私有地址 公网地址 套接字 端口 NAT DNS 域名 TCP UDP SYN ACK TIME_WAIT 帧 分片 MTU MAC
UID GID 权限位 sudo PATH 环境变量 systemd 文件描述符 fork exec inode pty
对称加密 分组密码 流密码 AES ChaCha20 CTR GCM 哈希 SHA-256 HMAC 消息认证码
非对称加密 RSA 椭圆曲线 ECC Ed25519 密钥交换 ECDH Curve25519 前向保密 PKI TLS
载荷 padding ETM KEXINIT 交换哈希 会话标识 重密钥 通道 流控 keepalive
签名 指纹 TOFU ssh-agent PEM
端口转发 本地转发 远程转发 动态转发 SOCKS ProxyJump ProxyCommand GatewayPorts
堡垒机 4A 审计 会话录像 命令过滤 网关模式 等保
系统用户 账号 资产 授权 三合一
Electron 扩展宿主 vscode-server
对象存储 桶 元数据 ETag 分片上传 生命周期 一致性 持久性 纠删码 挂载 NFS SMB NAS
SigV4 规范化请求 预签名 临时密钥 STS 桶策略 ACL
""".split()

SIGNS = ("指", "叫", "即", "是一种", "也就是", "全称", "简称", "（", "(",
         "所谓", "意思是", "就是", "是一", "属于", "表示")


def paragraphs(path):
    """返回 [(起始行号, 段落文本)]，跳过代码块。"""
    lines = open(path, encoding="utf-8").read().split("\n")
    out, buf, start, in_code = [], [], 0, False
    for i, l in enumerate(lines, 1):
        if l.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not l.strip():
            if buf:
                out.append((start, "\n".join(buf)))
                buf = []
            continue
        if not buf:
            start = i
        buf.append(l)
    if buf:
        out.append((start, "\n".join(buf)))
    return out


def main():
    files = sorted(glob.glob(os.path.join(BOOK, "chapters", "ch*.md")))
    paras = [(p, paragraphs(p)) for p in files]
    missing = []

    for term in TERMS:
        done = False
        for path, plist in paras:
            if done:
                break
            for ln, text in plist:
                if text.lstrip().startswith("#"):
                    continue
                if term not in text:
                    continue
                idx = text.find(term)
                tail = text[idx + len(term): idx + len(term) + 80]
                head = text[max(0, idx - 30): idx]
                explained = any(s in tail for s in SIGNS) or any(
                    s in head for s in ("所谓", "叫做", "称为"))
                if not explained:
                    ctx = text[max(0, idx - 20): idx + 60].replace("\n", " ")
                    missing.append((term, os.path.basename(path), ln, ctx))
                done = True
                break
        if not done:
            missing.append((term, "-", 0, "未出现"))

    for term, f, ln, ctx in missing:
        print("%-14s %-12s %-4s %s" % (term, f, ln, ctx))
    print("\n共 %d 条待看" % len(missing))


if __name__ == "__main__":
    main()
