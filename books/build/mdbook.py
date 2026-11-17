# -*- coding: utf-8 -*-
"""Markdown 到 reportlab flowable 的转换。

约定：
  * h1 为章标题，h2 为节标题，h3/h4 为更低层级
  * 图片的 alt 文字就是图注，图片下方居中排版
  * 以“表 ”开头的独立段落视为表题，排在表格上方
  * 代码块只放等宽可读的 ASCII 内容
"""

import os
import re
import xml.etree.ElementTree as ET

import markdown
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph,
                                Preformatted, Spacer, Table, TableStyle)
from reportlab.platypus.paragraph import Paragraph as _RLParagraph

from theme import (ACCENT, BODY, BODY_B, BODY_I, CODE_BG, CODE_LINE, CONTENT_W,
                   GRAY, HEAD, INK, MONO, MONO_CJK, TABLE_HEAD_BG, TABLE_LINE)

MAX_IMG_W = CONTENT_W

# ---------------------------------------------------------------- 避头尾
# reportlab 自带的 kinsokuShoriSplit 标着 "NOT USED OR FINISHED YET"，实际生效的是
# dumbSplit：纯按宽度切字，于是会出现以“。”“，”开头的行。这里在切分之后补两件事：
#   行首禁则：句号、逗号、右括号等不能出现在行首 —— 挂到上一行末尾（悬挂标点）
#   行尾禁则：左括号、左引号不能留在行尾 —— 挪到下一行开头
from reportlab.lib import textsplit as _ts
from reportlab.pdfbase.pdfmetrics import stringWidth as _sw
from reportlab.platypus import paragraph as _rlpara

NO_START = "。，、；：！？）】》」』”’"
NO_END = "（【《「『“‘"


def _kinsoku_split(word, maxWidths, fontName, fontSize, encoding="utf8"):
    if not isinstance(maxWidths, (list, tuple)):
        maxWidths = [maxWidths]
    if isinstance(word, bytes):
        word = word.decode(encoding)
    widths = _ts.getCharWidths(word, fontName, fontSize)
    lines = [[float(extra), text] for extra, text in _ts.dumbSplit(word, widths, maxWidths)]

    for i in range(1, len(lines)):
        text = lines[i][1]
        k = 0
        while k < len(text) - 1 and text[k] in NO_START:
            k += 1
        if k:
            hang = text[:k]
            lines[i - 1][1] += hang
            lines[i - 1][0] -= _sw(hang, fontName, fontSize)
            lines[i][1] = text[k:]

    for i in range(len(lines) - 1):
        text = lines[i][1]
        k = 0
        while k < len(text) - 1 and text[-1 - k] in NO_END:
            k += 1
        if k:
            moved = text[-k:]
            lines[i][1] = text[:-k]
            lines[i][0] += _sw(moved, fontName, fontSize)
            lines[i + 1][1] = moved + lines[i + 1][1]
            lines[i + 1][0] -= _sw(moved, fontName, fontSize)

    return lines


_rlpara.wordSplit = _kinsoku_split


def _repair_cjk_lines(para):
    """多 frag（含行内代码）的段落走 cjkFragSplit，需要在排好之后补救。"""
    lines = getattr(para, "lines", None)
    if not lines or getattr(para, "kind", 0) != 1:
        return
    for i in range(1, len(lines)):
        words = getattr(lines[i], "words", None)
        if not words:
            continue
        text = words[0].text or ""
        if len(text) > 1 and text[0] in NO_START:
            words[0].text = text[1:]
            prev = getattr(lines[i - 1], "words", None)
            if prev:
                prev[-1].text = (prev[-1].text or "") + text[0]
    for i in range(len(lines) - 1):
        words = getattr(lines[i], "words", None)
        if not words:
            continue
        text = words[-1].text or ""
        if len(text) > 1 and text[-1] in NO_END:
            words[-1].text = text[:-1]
            nxt = getattr(lines[i + 1], "words", None)
            if nxt:
                nxt[0].text = text[-1] + (nxt[0].text or "")


def _repair_cjk_para(para):
    """kind=1（多 frag）走 lines[i].words；kind=0（单 frag）走 lines[i][1][0]。"""
    lines = getattr(para, "lines", None)
    if not lines:
        return
    if getattr(para, "kind", 0) == 0:
        rows = [[extra, [text]] for extra, (text,) in
                ((ln[0], (ln[1][0],)) for ln in lines)]
        for i in range(1, len(rows)):
            text = rows[i][1][0]
            if len(text) > 1 and text[0] in NO_START:
                rows[i][1][0] = text[1:]
                rows[i - 1][1][0] += text[0]
        for i in range(len(rows) - 1):
            text = rows[i][1][0]
            if len(text) > 1 and text[-1] in NO_END:
                rows[i][1][0] = text[:-1]
                rows[i + 1][1][0] = text[-1] + rows[i + 1][1][0]
        para.lines = rows
        return
    _repair_cjk_lines(para)


class KinsokuParagraph(_rlpara.Paragraph):
    """在 reportlab 排完一段之后补上避头尾处理。"""

    def breakLinesCJK(self, maxWidths):
        para = _rlpara.Paragraph.breakLinesCJK(self, maxWidths)
        try:
            _repair_cjk_para(para)
        except Exception:
            pass
        return para


# 全书统一用这个子类，正文、图注、表格单元格都享受避头尾
Paragraph = KinsokuParagraph
MAX_IMG_H = 520
IMAGE_RESOLVER = None      # 由构建脚本注入，用于替换压缩后的图片


# ---------------------------------------------------------------- 文字工具

def dlen(text):
    """按显示宽度计长：CJK 记 2，其余记 1。"""
    n = 0
    for ch in text:
        n += 2 if ord(ch) > 0x2E7F else 1
    return n


def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


CJK_RE = re.compile(r"[　-〿㐀-鿿＀-￯]")

# 真正的图题/表题是“表 3-1　标题”：编号后面跟的是全角空格。
# 正文里的引导句“表 3-1 列出……”用的是半角空格，不能被当成题注。
CAPTION_RE = re.compile(r"^(图|表)\s*\d+(?:-\d+)?　")


def is_caption(text):
    return bool(CAPTION_RE.match(text.strip())) and len(text.strip()) < 120


# ---------------------------------------------------------------- 行内标记

def inline(node, styles, extra=""):
    """把 HTML 元素的内容转成 reportlab 段落标记。"""
    out = []
    if extra:
        out.append(extra)
    if node.text:
        out.append(esc(node.text))
    for ch in node:
        if ch.tag == "br":
            out.append("<br/>")
            if ch.tail:
                out.append(esc(ch.tail))
            continue
        if ch.tag == "img":
            out.append(esc(ch.get("alt", "")))
            if ch.tail:
                out.append(esc(ch.tail))
            continue
        out.append(inline_chunk(ch, styles))
        if ch.tail:
            out.append(esc(ch.tail))
    return "".join(out)


def inline_chunk(ch, styles):
    """把单个子元素（code、b、a 等）连同它的标记一起转出来。"""
    tag = ch.tag
    opener = ""
    closer = ""
    if tag in ("strong", "b"):
        opener, closer = "<b>", "</b>"
    elif tag in ("em", "i"):
        opener, closer = "<i>", "</i>"
    elif tag == "code":
        raw = "".join(ch.itertext())
        face = MONO_CJK if CJK_RE.search(raw) else MONO
        opener, closer = '<font face="%s" size="9" color="#31556b">' % face, "</font>"
    elif tag == "a":
        href = ch.get("href", "")
        opener, closer = '<a href="%s" color="#1f5e8c">' % href.replace("&", "&amp;"), "</a>"
    elif tag == "sup":
        opener, closer = "<super>", "</super>"
    elif tag == "sub":
        opener, closer = "<sub>", "</sub>"
    return opener + inline(ch, styles) + closer


def plain(node):
    return "".join(node.itertext()).strip()


# ---------------------------------------------------------------- 代码块

def wrap_code(text, limit=88, cont_indent=4):
    lines = []
    for line in text.split("\n"):
        if dlen(line) <= limit:
            lines.append(line)
            continue
        buf, w = "", 0
        indent = len(line) - len(line.lstrip(" "))
        cont = " " * min(indent + cont_indent, 20)
        lead = line[:indent]
        for ch in line[indent:]:
            cw = 2 if ord(ch) > 0x2E7F else 1
            if w + cw > limit:
                buf += "\\"
                lines.append(lead + buf)
                lead = cont
                buf, w = "", 0
            buf += ch
            w += cw
        lines.append(lead + buf)
    return "\n".join(lines)


def code_block(text, styles, width=CONTENT_W):
    text = text.rstrip()
    has_cjk = bool(CJK_RE.search(text))
    style = styles["code_cjk"] if has_cjk else styles["code"]
    text = wrap_code(text, limit=84 if has_cjk else 88)
    pre = Preformatted(text, style)
    t = Table([[pre]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
        ("LINEBEFORE", (0, 0), (0, -1), 2.0, colors.HexColor("#9fb4c4")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return [t, Spacer(1, 9)]


# ---------------------------------------------------------------- 图片

def figure(elem, styles, base_dir):
    src = elem.get("src", "")
    alt = elem.get("alt", "").strip()
    path = src if os.path.isabs(src) else os.path.normpath(os.path.join(base_dir, src))
    if not os.path.exists(path):
        p = Paragraph("[缺图 %s]" % esc(src), styles["caption"])
        return [p]
    iw, ih = ImageReader(path).getSize()
    w = MAX_IMG_W
    h = w * ih / iw
    if h > MAX_IMG_H:
        h = MAX_IMG_H
        w = h * iw / ih
    img = Image(path if IMAGE_RESOLVER is None else IMAGE_RESOLVER(path),
                width=w, height=h)
    img.hAlign = "CENTER"
    out = [Spacer(1, 6), img]
    if alt:
        cap = Paragraph(esc(alt), styles["caption"])
        out = [KeepTogether([Spacer(1, 6), img, cap])]
    return out


# ---------------------------------------------------------------- 表格

def table_block(elem, styles):
    rows, head_rows = [], 0
    for tr in elem.iter("tr"):
        cells = []
        for cell in tr:
            if cell.tag not in ("td", "th"):
                continue
            txt = cell_text(cell, styles)
            cells.append(txt)
        if not cells:
            continue
        rows.append(cells)
        if all(c.tag == "th" for c in tr if c.tag in ("td", "th")):
            head_rows += 1
    if not rows:
        return []
    ncol = max(len(r) for r in rows)
    for r in rows:
        while len(r) < ncol:
            r.append("")

    data = []
    for i, r in enumerate(rows):
        st = styles["cell_head"] if i < max(head_rows, 0) else styles["cell"]
        data.append([Paragraph(c, st) for c in r])

    # 按内容宽度分配列宽
    weights = []
    for c in range(ncol):
        wmax = 0
        for r in rows:
            wmax = max(wmax, min(dlen(strip_tags(r[c])), 26))
        weights.append(max(wmax, 6))
    total = float(sum(weights))
    widths = [CONTENT_W * w / total for w in weights]

    t = Table(data, colWidths=widths, repeatRows=head_rows if head_rows else 0)
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, TABLE_LINE),
        ("LINEBELOW", (0, 0), (-1, max(head_rows - 1, 0)), 1.0, colors.HexColor("#5f7484")),
    ]
    if head_rows:
        cmds.append(("BACKGROUND", (0, 0), (-1, head_rows - 1), TABLE_HEAD_BG))
    t.setStyle(TableStyle(cmds))
    return [Spacer(1, 6), t, Spacer(1, 12)]


def strip_tags(text):
    return re.sub(r"<[^>]+>", "", text)


def cell_text(cell, styles):
    parts = []
    if cell.text:
        parts.append(esc(cell.text))
    for ch in cell:
        if ch.tag == "code":
            parts.append('<font face="%s" size="8.4" color="#8d3a2f">%s</font>'
                         % (MONO, esc(plain(ch))))
        elif ch.tag in ("strong", "b"):
            parts.append("<b>%s</b>" % esc(plain(ch)))
        elif ch.tag in ("em", "i"):
            parts.append("<i>%s</i>" % esc(plain(ch)))
        elif ch.tag == "br":
            parts.append("<br/>")
        else:
            parts.append(inline(ch, styles))
        if ch.tail:
            parts.append(esc(ch.tail))
    return "".join(parts).strip()


# ---------------------------------------------------------------- 列表

def list_block(elem, styles, level=0, ordered=False, start=1):
    out = []
    items = [c for c in elem if c.tag == "li"]
    n = start
    base = 20 + level * 17
    for li in items:
        marker = ("%d." % n) if ordered else "•"
        n += 1
        paras, nested, cur = [], [], []
        if li.text and li.text.strip():
            # 只去掉换行，保留行内标记两侧的空格，否则“换成 `ls`”会粘成“换成ls”
            cur.append(esc(li.text.lstrip().rstrip(chr(10))))
        for ch in li:
            if ch.tag in ("ul", "ol"):
                if cur:
                    paras.append("".join(cur))
                    cur = []
                nested.append(ch)
                continue
            frag = inline_chunk(ch, styles)
            if frag.strip():
                cur.append(frag)
            if ch.tail and ch.tail.strip():
                cur.append(esc(ch.tail))
        if cur:
            paras.append("".join(cur))

        for i, text in enumerate(paras):
            if i == 0:
                st = ParagraphStyle("li%d" % level, parent=styles["bullet"],
                                    leftIndent=base, bulletIndent=base - 11,
                                    firstLineIndent=0)
                out.append(Paragraph(text, st, bulletText=marker))
            else:
                st = ParagraphStyle("li_c%d_%d" % (level, i), parent=styles["bullet"],
                                    leftIndent=base, bulletIndent=base - 11,
                                    firstLineIndent=0)
                out.append(Paragraph(text, st))
        for ch in nested:
            sub_ordered = ch.tag == "ol"
            sub_start = int(ch.get("start", 1) or 1) if sub_ordered else 1
            out.extend(list_block(ch, styles, level + 1, sub_ordered, sub_start))
    out.append(Spacer(1, 4))
    return out


# ---------------------------------------------------------------- 主转换

class Converter:
    def __init__(self, styles, base_dir):
        self.styles = styles
        self.base_dir = base_dir
        self.headings = []          # (level, text) 供外部建立目录

    def convert_file(self, path):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        return self.convert_text(text, path)

    def convert_text(self, text, path):
        md = markdown.Markdown(
            extensions=["tables", "fenced_code", "sane_lists", "attr_list"],
            output_format="xhtml",
        )
        html = md.convert(text)
        root = ET.fromstring("<root>" + html + "</root>")
        base = os.path.dirname(os.path.abspath(path))
        return self.emit_children(root, base)

    def emit_children(self, node, path):
        out = []
        kids = list(node)
        for i, ch in enumerate(kids):
            flows = self.emit(ch, path)
            # 引导句不要和它引出的代码块分到两页
            nxt = kids[i + 1] if i + 1 < len(kids) else None
            if (nxt is not None and nxt.tag == "pre" and len(flows) == 1
                    and isinstance(flows[0], Paragraph)):
                flows[0].keepWithNext = 1
            out.extend(flows)
        return out

    def emit(self, elem, path):
        st = self.styles
        tag = elem.tag
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            return self.heading(elem)
        if tag == "p":
            return self.paragraph(elem, path)
        if tag in ("ul", "ol"):
            return list_block(elem, st, 0, tag == "ol", int(elem.get("start", 1) or 1))
        if tag == "pre":
            return code_block(plain(elem), st)
        if tag == "blockquote":
            return self.quote(elem, path)
        if tag == "table":
            return table_block(elem, st)
        if tag == "hr":
            return [Paragraph("· · ·", ParagraphStyle(
                "orn", parent=st["caption"], textColor=GRAY, spaceBefore=10, spaceAfter=12))]
        if tag in ("div", "section", "article", "html", "body", "root"):
            return self.emit_children(elem, path)
        return []

    def heading(self, elem):
        tag = elem.tag
        txt = plain(elem)
        st = self.styles
        key = {"h1": "h1", "h2": "h2", "h3": "h3", "h4": "h4"}.get(tag, "h4")
        p = TaggedHeading(txt, st[key], level=int(tag[1]) - 1)
        return [p]

    def paragraph(self, elem, path):
        st = self.styles
        imgs = [c for c in elem if c.tag == "img"]
        if imgs and not (elem.text or "").strip() and len(elem) == len(imgs):
            out = []
            for im in imgs:
                out.extend(figure(im, st, path))
            return out
        txt = inline(elem, st).strip()
        if not txt:
            return []
        plain_txt = plain(elem)
        if is_caption(plain_txt) and len(txt) < 200:
            style = st["table_caption"] if plain_txt.startswith("表") else st["caption"]
            if plain_txt.startswith("表"):
                return [Paragraph(txt, style)]
            return [Paragraph(txt, style)]
        return [Paragraph(txt, st["body"])]

    def quote(self, elem, path):
        out = []
        for ch in elem:
            txt = inline(ch, self.styles).strip()
            if txt:
                out.append(Paragraph(txt, self.styles["quote"]))
        if elem.text and elem.text.strip():
            out.insert(0, Paragraph(esc(elem.text.strip()), self.styles["quote"]))
        return out


class TaggedHeading(Paragraph):
    """带层级信息的标题段落，供 afterFlowable 建目录与书签。"""

    def __init__(self, text, style, level=0):
        Paragraph.__init__(self, esc(text) if "<" not in text else text, style)
        self.head_text = text
        self.head_level = level


def md_flowables(path, styles):
    conv = Converter(styles, os.path.dirname(os.path.abspath(path)))
    flows = conv.convert_file(path)
    return flows, conv.headings
