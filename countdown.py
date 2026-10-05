#!/usr/bin/env python3
"""countdown - 终端倒计时小工具。

用法：
    countdown 25m            # 倒计时 25 分钟
    countdown 1h30m          # 1 小时 30 分钟
    countdown 90s            # 90 秒
    countdown --until 18:00  # 倒计时到今天 18:00（已过则算明天）

纯标准库，纯本地。
"""

import argparse
import datetime as dt
import re
import sys
import time

DURATION_RE = re.compile(
    r"^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$", re.IGNORECASE
)


def parse_duration(text):
    """把 '25m' / '1h30m' / '90s' 解析为秒数。非法返回 None。"""
    text = text.strip()
    if not text:
        return None
    m = DURATION_RE.match(text)
    if not m:
        return None
    h, mi, s = m.group(1), m.group(2), m.group(3)
    if h is None and mi is None and s is None:
        return None
    total = (int(h or 0) * 3600) + (int(mi or 0) * 60) + int(s or 0)
    return total if total > 0 else None


def seconds_until(clock, now=None):
    """计算到下一个 clock（'HH:MM'）还有多少秒；已过则算明天。"""
    now = now or dt.datetime.now()
    try:
        hh, mm = clock.split(":")
        target = now.replace(hour=int(hh), minute=int(mm), second=0, microsecond=0)
    except (ValueError, AttributeError):
        return None
    delta = (target - now).total_seconds()
    if delta <= 0:
        delta += 24 * 3600
    return int(delta)


def fmt_hms(seconds):
    """秒数 -> 'HH:MM:SS' 或 'MM:SS'。"""
    seconds = max(0, int(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def run(total, message=None, bell=True, tick=0.2):
    """真正的倒计时循环。同行刷新 + 进度条。"""
    end = time.monotonic() + total
    bar_w = 20
    try:
        while True:
            remaining = end - time.monotonic()
            if remaining <= 0:
                break
            done = 1.0 - remaining / total
            filled = int(done * bar_w)
            bar = "█" * filled + "░" * (bar_w - filled)
            sys.stdout.write(f"\r⏳ {fmt_hms(remaining)}  [{bar}]")
            sys.stdout.flush()
            time.sleep(min(tick, remaining))
    except KeyboardInterrupt:
        sys.stdout.write("\n已取消。\n")
        return 130
    sys.stdout.write("\r" + " " * (bar_w + 20) + "\r")
    banner = "=" * 30
    print(banner)
    print("🔔 时间到！")
    if message:
        print(f"💬 {message}")
    print(banner)
    if bell:
        sys.stdout.write("\a")
        sys.stdout.flush()
    return 0


def cmd_main(argv=None):
    p = argparse.ArgumentParser(
        prog="countdown",
        description="终端倒计时：25m / 1h30m / 90s，或 --until 18:00。",
    )
    p.add_argument("duration", nargs="?",
                   help="时长，如 25m、1h30m、90s")
    p.add_argument("--until", metavar="HH:MM",
                   help="倒计时到某个钟点（今天已过则算明天）")
    p.add_argument("--message", default=None,
                   help="结束时显示的提示语")
    p.add_argument("--no-bell", action="store_true",
                   help="结束时不响终端铃声（默认会响 \\a）")
    p.add_argument("--version", action="version", version="countdown 0.1.0")
    args = p.parse_args(argv)

    if args.until:
        total = seconds_until(args.until)
        if total is None:
            print(f"error: 无法解析时间：{args.until}（请用 HH:MM，如 18:00）",
                  file=sys.stderr)
            return 1
    elif args.duration:
        total = parse_duration(args.duration)
        if total is None:
            print(f"error: 无法解析时长：{args.duration}"
                  f"（请用 25m / 1h30m / 90s 这样的格式）",
                  file=sys.stderr)
            return 1
    else:
        p.print_usage(sys.stderr)
        print("error: 请指定时长（如 25m）或 --until HH:MM",
              file=sys.stderr)
        return 2

    print(f"开始倒计时：{fmt_hms(total)}"
          + (f" —— {args.message}" if args.message else ""))
    return run(total, message=args.message, bell=not args.no_bell)


def main():
    sys.exit(cmd_main())


if __name__ == "__main__":
    main()
