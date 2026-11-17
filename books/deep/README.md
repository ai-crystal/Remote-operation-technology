# 远程之门 · 深入

> 协议线格式、密码学推导与系统边界

这一册不再讲“怎么用”，而是拆开三样东西：SSH 在线上到底是什么形状、密码学里那些数字从哪来、系统在压力与攻击面前会怎么表现。

## 这一册适合谁

- 读过进阶册，想知道“为什么这样设计”的人
- 要写协议实现、做安全评估、排查疑难问题的工程师
- 想弄懂 `ssh -vv` 每一行、`SignatureDoesNotMatch` 每个字节的人

## 目录

### 第一部　协议与密码

1. [抓一个 SSH 连接：从版本串到 NEWKEYS](books/deep/chapters/ch01.md)
2. [密钥交换的数学：DH、ECDH 与前向保密](books/deep/chapters/ch02.md)
3. [签名与证书链：从 Ed25519 到 CA 签发](books/deep/chapters/ch03.md)
4. [SigV4：一次签名的完整推导](books/deep/chapters/ch04.md)

### 第二部　系统与安全

5. [性能与并发：加密开销、连接复用与背压](books/deep/chapters/ch05.md)
6. [安全边界：中间人、越权与最小权限](books/deep/chapters/ch06.md)

## 前置

需要读过[进阶册](books/intermediate/README.md)，或者已经熟悉 SSH 的基本使用与对象存储的签名流程。数学只保留理解原理必需的部分，读不懂可以先看结论。

## 下载

- [深入册 PDF](output/remote-gate-deep.pdf)
