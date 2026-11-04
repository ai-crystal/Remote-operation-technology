# 远程之门

> 远程操作的技术细节

从一条 `ssh` 登录到几百 TB 的对象存储，讲清远程操作这件事的四层机制。

## 这本书讲什么

远程操作看起来只是敲几条命令，底下其实叠着四层东西。这本书按这四层展开，每一层都从“它要解决什么问题”讲起。

第一层是链路。网卡、交换机、路由器、网关、地址、端口、域名、TCP，以及数据包怎么被一层层装进帧里。这一层回答“为什么连不上”。

第二层是信任。对称加密、非对称加密、哈希、密钥交换、证书，然后是 SSH 协议本身的三个子协议、密钥与指纹、端口转发。这一层回答“凭什么相信对面”。

第三层是控制。当连接从一个人扩展到一群人，凭据怎么收拢、操作怎么审计、开发环境怎么搬到远端。这一层讲堡垒机、JumpServer 与 VS Code 的远程开发。

第四层是数据。对象存储的模型、分片上传、签名算法、权限体系，以及为什么一个字节的差异就得到 403。

## 目录

### 第一篇　从一台机器到一条链路

1. [计算机之间怎么通信](book/chapters/ch01.md)
2. [SSH 是什么](book/chapters/ch02.md)
3. [地址、端口与那条看不见的路](book/chapters/ch03.md)
4. [服务器上发生了什么](book/chapters/ch04.md)

### 第二篇　信任是怎么建立的

5. [加密、哈希与密钥交换](book/chapters/ch05.md)
6. [SSH 协议的三层结构](book/chapters/ch06.md)
7. [密钥、指纹与信任](book/chapters/ch07.md)
8. [端口转发，把远方的服务搬到本地](book/chapters/ch08.md)

### 第三篇　从一个人到一群人

9. [为什么需要堡垒机](book/chapters/ch09.md)
10. [JumpServer 的内部构造](book/chapters/ch10.md)
11. [VS Code 远程开发的工作原理](book/chapters/ch11.md)

### 第四篇　数据的另一端

12. [对象存储的模型](book/chapters/ch12.md)
13. [签名、密钥与 403](book/chapters/ch13.md)
14. [从登录到数据存取](book/chapters/ch14.md)

### 附录

- [附录 A　命令速查](book/appendix/a-cheatsheet.md)
- [附录 B　术语表](book/appendix/b-glossary.md)
- [后记](book/front/90-epilogue.md)

## 在线阅读

本站用 docsify 搭建，每一章都有独立链接，可以直接分享：

```text
https://<你的用户名>.github.io/<仓库名>/#/book/chapters/ch06
```

左侧目录按篇分组，顶部可以搜索全书内容。

## 下载 PDF

- [整本 PDF（含封面、两级目录、PDF 书签）](output/remote-access-book.pdf ':ignore')
- [前言](book/front/20-preface.md)

PDF 用 `build.bat` 生成，插图已压缩，字体做了子集化，体积控制在 20 MB 以内。

## 关于插图

书里的每一张图都是代码画出来的，脚本在 `book/code/` 下，按章分目录。插图本身在 `book/images/`。想改某张图，改对应的 `figs.py` 再跑一遍即可。

## 作者

Dr. Dezeming，2026 年。
