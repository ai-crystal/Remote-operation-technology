# 附录 A　入门速查

## A.1 登录

| 命令 | 作用 |
| --- | --- |
| `ssh alice@198.51.100.17` | 用当前账号登录远端 |
| `ssh -p 2222 alice@host` | 指定端口 |
| `ssh -i key alice@host` | 指定私钥 |
| `ssh host "uptime"` | 执行一条命令就退出 |
| `exit` | 退出登录 |

## A.2 钥匙

| 命令 | 作用 |
| --- | --- |
| `ssh-keygen -t ed25519 -C "note"` | 生成一对密钥 |
| `ssh-copy-id alice@host` | 把公钥装到服务器 |
| `ssh-keygen -l -f key.pub` | 查看指纹 |
| `ssh-keygen -R host` | 删掉某台主机的旧记录 |

## A.3 排查

| 命令 | 作用 |
| --- | --- |
| `nslookup host` | 名字能不能换成地址 |
| `ping host` | 机器活不活（不回应不代表死） |
| `nc -vz host port` | 端口开不开 |
| `ssh -v alice@host` | 看登录卡在哪一步 |
| `ls -l` | 看文件权限 |
| `chmod 600 key` | 把私钥权限收紧 |

## A.4 端口转发

| 命令 | 作用 |
| --- | --- |
| `ssh -L 3306:10.0.0.8:3306 alice@host` | 把远端 3306 搬到本地 |
| `ssh -L 8080:10.0.0.9:80 alice@host` | 把远端网页搬到本地 |

## A.5 服务

| 命令 / 概念 | 作用 |
| --- | --- |
| `ss -lntp` | 看本机在哪些端口监听 |
| `curl -v http://127.0.0.1:8000/health` | 测本机接口 |
| `systemctl status 服务名` | 看服务状态 |
| `journalctl -u 服务名 -f` | 跟服务日志 |
