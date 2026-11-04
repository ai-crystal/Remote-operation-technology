# 远程之门

> SSH、堡垒机与对象存储的技术细节

一本写给“会用但不知道为什么”的工程师的书。

## 这本书解决什么问题

你每天都在用这些工具。终端里敲 `ssh` 能进服务器，VS Code 里点一下能连上远端项目，浏览器里能上传下载存储桶里的文件，公司要求所有运维必须经过堡垒机。工具都能用，但配置文件里那一行 `User alice@ubuntu@10.0.0.9` 是什么意思，`.pem` 和 `id_rsa` 有什么区别，为什么上传文件总是 403，都说不清楚。

这本书从一条 `ssh` 命令出发，把网络分层、密码学、SSH 协议、堡垒机的权限模型、VS Code 的远程架构、对象存储的签名算法依次讲开。读完你应该能做到三件事：看懂别人给的配置，读懂报错信息，判断一份方案是否合理。

## 目录

### 第一篇　把远方接到手边

1. [你按下回车之后](book/chapters/ch01.md)
2. [地址、端口与那条看不见的路](book/chapters/ch02.md)
3. [服务器上发生了什么](book/chapters/ch03.md)

### 第二篇　信任是怎么建立的

4. [把话藏起来](book/chapters/ch04.md)
5. [SSH 协议的三层结构](book/chapters/ch05.md)
6. [密钥、指纹与信任](book/chapters/ch06.md)
7. [端口转发，把远方的服务搬到本地](book/chapters/ch07.md)

### 第三篇　从一个人到一群人

8. [为什么需要堡垒机](book/chapters/ch08.md)
9. [JumpServer 的内部构造](book/chapters/ch09.md)
10. [VS Code 是怎么连过去的](book/chapters/ch10.md)

### 第四篇　数据的另一端

11. [对象存储的模型](book/chapters/ch11.md)
12. [签名、密钥与 403](book/chapters/ch12.md)
13. [把四件事串成一条链路](book/chapters/ch13.md)

### 附录

- [附录 A　命令速查](book/appendix/a-cheatsheet.md)
- [附录 B　术语表](book/appendix/b-glossary.md)
- [后记](book/front/90-epilogue.md)

## 在线阅读

本站用 docsify 搭建，每一章都有独立链接，可以直接分享：

```text
https://<你的用户名>.github.io/<仓库名>/#/book/chapters/ch05
```

左侧目录按篇分组，右上角可以搜索全书内容。

## 下载 PDF

- [整本 PDF（含封面、目录、书签）](output/remote-access-book.pdf)
- [前言](book/front/20-preface.md)

PDF 用 `build.bat` 生成，带两级目录与书签，插图已压缩，体积控制在 20 MB 以内。

## 关于插图

书里的每一张图都是代码画出来的，脚本在 `book/code/` 下，按章分目录。插图本身在 `book/images/`。想改某张图，改对应的 `figs.py` 再跑一遍即可，不需要动排版。

## 作者

Dr. Dezeming，2026 年。
