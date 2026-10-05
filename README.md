# countdown

终端倒计时小工具：时长进，专注出。纯标准库、纯本地。

## 安装

零依赖，Python 3.10+ 直接跑：

```bash
cd countdown
python3 -m countdown 25m
```

## 用法

```bash
countdown 25m                 # 25 分钟
countdown 1h30m               # 1 小时 30 分钟
countdown 90s                 # 90 秒
countdown 25m --message "休息一下"   # 结束时显示提示语
countdown --until 18:00       # 倒计时到今天 18:00（已过则算明天）
countdown 25m --no-bell       # 结束时不响铃
```

倒计时过程中同行刷新 `MM:SS` + 进度条；结束时打印横幅并响终端铃声（`\a`）。

## 时长格式

`1h30m`、`25m`、`90s` 可组合，大小写不敏感。非法输入（`abc`、空串、`0s`）中文报错、exit 1。

## 诚实说明

- 只有终端铃声（`\a`），**没有图形界面通知**——终端不支持响铃的环境里结束时只显示横幅。
- `Ctrl-C` 可随时取消，exit 130。
- 计时基于 `time.monotonic()`，不受系统时间调整影响。
- `--until` 用的是本机本地时区。
