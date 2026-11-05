# 附录 A　命令速查

## A.1 客户端连接

| 命令 | 作用 |
| --- | --- |
| `ssh host` | 用配置文件里的别名连接 |
| `ssh -p 2222 user@host` | 指定端口连接 |
| `ssh -l user@asset@jump jump` | 指定用户名，用户名里含 at 符号时用它 |
| `ssh -i key.pem user@host` | 指定私钥 |
| `ssh -v host` | 打印调试信息，`-vv` `-vvv` 更详细 |
| `ssh -N -L 8080:10.0.0.9:80 jump` | 只做转发，不登录 shell |
| `ssh -J jump1,jump2 target` | 两级跳板 |
| `ssh -D 1080 jump` | 起一个 SOCKS5 代理 |
| `ssh -T host` | 不分配伪终端，适合脚本 |
| `ssh -t host cmd` | 强制分配伪终端 |
| `ssh -o Option=Value host` | 临时指定配置项 |
| `ssh -G host` | 打印最终生效的配置，不发起连接 |

## A.2 密钥管理

| 命令 | 作用 |
| --- | --- |
| `ssh-keygen -t ed25519 -C "note"` | 生成 Ed25519 密钥 |
| `ssh-keygen -t rsa -b 4096` | 生成 4096 位 RSA 密钥 |
| `ssh-keygen -l -f key.pub` | 查看公钥指纹 |
| `ssh-keygen -y -f key` | 从私钥导出公钥 |
| `ssh-keygen -p -f key` | 修改私钥口令 |
| `ssh-keygen -p -m PEM -f key` | 转换成 PEM 格式 |
| `ssh-keygen -R host` | 从 known_hosts 删除某主机的记录 |
| `ssh-keygen -F host` | 在 known_hosts 里查找记录 |
| `ssh-copy-id -i key.pub user@host` | 把公钥装到远端 |
| `ssh-keyscan -t ed25519 host` | 抓取主机公钥 |

## A.3 agent

| 命令 | 作用 |
| --- | --- |
| `eval "$(ssh-agent -s)"` | 启动 agent |
| `ssh-add key` | 把私钥加入 agent |
| `ssh-add -l` | 列出已加载的钥匙 |
| `ssh-add -D` | 清空所有钥匙 |
| `ssh-add -t 3600 key` | 加载并在一小时后自动移除 |

## A.4 诊断

| 命令 | 作用 |
| --- | --- |
| `ss -lntp` | 列出监听的 TCP 端口和进程 |
| `ss -tnp` | 列出已建立的连接 |
| `nc -vz host port` | 测试端口连通性 |
| `curl -v telnet://host:port` | 测试端口并看握手过程 |
| `traceroute host` | 逐跳显示路径 |
| `tcpdump -n -i any port 22` | 抓 SSH 流量 |
| `journalctl -u ssh -n 50` | 看 sshd 最近日志 |
| `sudo sshd -T` | 打印服务端生效配置 |

## A.5 服务端

| 命令 | 作用 |
| --- | --- |
| `systemctl status ssh` | 查看 sshd 状态 |
| `systemctl restart ssh` | 重启 sshd |
| `sshd -t` | 检查配置文件语法 |
| `chmod 700 ~/.ssh` | 修正目录权限 |
| `chmod 600 ~/.ssh/authorized_keys` | 修正公钥文件权限 |
| `chmod 600 ~/.ssh/id_ed25519` | 修正私钥权限 |

## A.6 对象存储

| 命令 | 作用 |
| --- | --- |
| `coscli ls cos://bucket/prefix/` | 列出对象 |
| `coscli cp local cos://bucket/key` | 上传单个文件 |
| `coscli cp cos://bucket/key local` | 下载单个文件 |
| `coscli cp dir/ cos://bucket/prefix/ -r` | 递归上传 |
| `coscli sync local/ cos://bucket/prefix/` | 增量同步 |
| `coscli rm cos://bucket/key` | 删除对象 |
| `coscli sign cos://bucket/key --expire 3600` | 生成预签名 URL |
| `curl -I "https://bucket.cos.region.myqcloud.com/key"` | 查看对象头部信息 |

## A.7 常用配置项

| 配置项 | 客户端或服务端 | 说明 |
| --- | --- | --- |
| `HostName` | 客户端 | 真实地址 |
| `Port` | 客户端 | 端口 |
| `User` | 客户端 | 登录名 |
| `IdentityFile` | 客户端 | 私钥路径 |
| `IdentitiesOnly` | 客户端 | 只用指定私钥 |
| `ProxyJump` | 客户端 | 跳板机 |
| `ServerAliveInterval` | 客户端 | 心跳间隔 |
| `LocalForward` | 客户端 | 等价于 `-L` |
| `RemoteForward` | 客户端 | 等价于 `-R` |
| `RequestTTY` | 客户端 | 是否分配伪终端 |
| `PasswordAuthentication` | 服务端 | 是否允许密码登录 |
| `PermitRootLogin` | 服务端 | 是否允许 root 登录 |
| `PubkeyAuthentication` | 服务端 | 是否允许公钥登录 |
| `AllowTcpForwarding` | 服务端 | 是否允许端口转发 |
| `GatewayPorts` | 服务端 | 远程转发能否绑定非回环地址 |
| `MaxSessions` | 服务端 | 单连接最大通道数 |
| `ClientAliveInterval` | 服务端 | 服务端心跳间隔 |
| `TrustedUserCAKeys` | 服务端 | 用户证书的 CA 公钥 |
