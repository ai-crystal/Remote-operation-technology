# 远程之门

> 远程操作的技术细节

从一条 `ssh` 登录到几百 TB 的对象存储，再到把程序做成别人能用的服务。

这个仓库是一套**三分册**的技术书：同一件事，三种深度。

## 三分册

### [入门册 · 网络这座城](books/beginner/README.md)

六篇二十三章，不讲公式，不要求会写代码。从“你家到服务器隔了几道门”讲到“怎么和 AI 一起干活”：地址与端口、域名、门禁与海关、ssh 与钥匙、进程与服务、上传与对象存储、隧道与远程开发、报错的读法与安全底线。

**适合**：靠 AI 写代码但一部署就卡住的人；第一次接触服务器、想把概念理顺的人。

### [进阶册 · 远程操作的技术细节](books/intermediate/README.md)

五篇十八章，系列的主干。完整讲链路、信任、控制、数据，以及把程序做成服务：协议细节、密码学工具、堡垒机与 JumpServer、VS Code 远程开发、对象存储与签名、上传与长任务、会员与权限。

**适合**：要在工作里真正用起来的人，或读完入门册想继续深入的人。

### [深入册 · 协议、密码学与实现细节](books/deep/README.md)

两篇六章。拆开 SSH 的线格式、密钥交换的数学、签名与证书链、SigV4 的完整推导，再谈性能、并发与安全边界。

**适合**：要写协议实现、做安全评估、排查疑难问题的工程师。

## 在线阅读

站点：<https://ai-crystal.github.io/Remote-operation-technology/>

- [入门册](https://ai-crystal.github.io/Remote-operation-technology/#/books/beginner/README)
- [进阶册](https://ai-crystal.github.io/Remote-operation-technology/#/books/intermediate/README)
- [深入册](https://ai-crystal.github.io/Remote-operation-technology/#/books/deep/README)

每一章都有独立地址，可以直接分享。

## 下载 PDF

- [入门册 PDF](output/remote-gate-beginner.pdf)（103 页）
- [进阶册 PDF](output/remote-access-book.pdf)（151 页）
- [深入册 PDF](output/remote-gate-deep.pdf)（31 页）

PDF 用脚本生成。每册一个入口，改哪本编哪本：

```text
build-beginner.bat      只构建入门册
build-intermediate.bat  只构建进阶册
build-deep.bat          只构建深入册
build.bat figures       只重画插图（进阶册的图，入门/深入用的是副本）
build.bat               三册全构建
```

每个入口都会先体检（`lint.py`）再排版；插图不重画，所以单册通常在 3 秒内完成。

## 关于插图

书里的图都由代码生成，脚本在 `book/code/` 下，共用 `book/code/common/figstyle.py`。改某张图，改对应的 `figs.py` 再跑一遍。

## 作者

Dr. Dezeming，2026 年。
