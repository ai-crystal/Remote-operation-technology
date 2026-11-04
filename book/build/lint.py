# -*- coding: utf-8 -*-
"""稿件体检：在编译之前找出会让书出错的问题。

检查项：
  1. 代码块里出现中日韩字符（等宽字体没有这些字形，会渲染成空白）
  2. 图片路径不存在
  3. 代码块内部嵌套了代码围栏
  4. 标题里出现会干扰排版的字符
  5. 图、表编号是否连续
"""

import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(HERE)

CJK = re.compile(r"[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]")
BAD_HEAD = re.compile(r"[<>&]")
FENCE = re.compile(r"^```")


def files():
    out = []
    for pat in ("chapters/*.md", "front/*.md", "appendix/*.md"):
        out.extend(sorted(glob.glob(os.path.join(BOOK, pat))))
    return out


def check(path):
    errors, warns = [], []
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    rel = os.path.relpath(path, BOOK)

    in_code = False
    code_start = 0
    figs, tabs = [], []

    for i, line in enumerate(lines, 1):
        if line.startswith("```"):
            if in_code and line.strip() != "```":
                errors.append("%s:%d 代码块内部又出现围栏行" % (rel, i))
            in_code = not in_code
            if in_code:
                code_start = i
            continue
        if in_code:
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            title = m.group(2)
            if BAD_HEAD.search(title):
                errors.append("%s:%d 标题含 < > & 字符：%s" % (rel, i, title))
            if title.count("*") % 2 == 1:
                errors.append("%s:%d 标题里的粗体标记没有闭合" % (rel, i))

        for src in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", line):
            target = os.path.normpath(os.path.join(os.path.dirname(path), src))
            if not os.path.exists(target):
                errors.append("%s:%d 图片不存在：%s" % (rel, i, src))

        cap = re.match(r"^!\[(图\s*(\d+)-(\d+))", line)
        if cap:
            figs.append(int(cap.group(3)))
        cap = re.match(r"^表\s*(\d+)-(\d+)", line)
        if cap:
            tabs.append(int(cap.group(2)))

    if in_code:
        errors.append("%s:%d 代码块没有闭合" % (rel, code_start))

    for name, seq in (("图", figs), ("表", tabs)):
        for a, b in zip(seq, seq[1:]):
            if b != a + 1:
                warns.append("%s %s编号不连续：%d 之后是 %d" % (rel, name, a, b))

    return errors, warns


def main():
    all_err, all_warn = [], []
    for path in files():
        e, w = check(path)
        all_err.extend(e)
        all_warn.extend(w)

    for m in all_warn:
        print("  [注意] " + m)
    for m in all_err:
        print("  [错误] " + m)

    if all_err:
        print("体检发现 %d 个必须修的问题。" % len(all_err))
        return 1
    print("体检通过，%d 个文件。" % len(files()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
