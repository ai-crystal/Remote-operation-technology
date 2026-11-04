# -*- coding: utf-8 -*-
"""把 book/ 下的 Markdown 编译成一本书的 PDF。

用法（一般通过根目录 build.bat 调用）：
    python book/build/build.py            # 完整构建
    python book/build/build.py --no-opt   # 跳过图片压缩（调试用）
"""

import io
import json
import os
import sys
import time

from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, Image,
                                KeepTogether, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Spacer)
from reportlab.platypus.flowables import HRFlowable

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(HERE)
ROOT = os.path.dirname(BOOK)
OUTPUT = os.path.join(ROOT, "output")
IMAGES = os.path.join(BOOK, "images")
BUILD_TMP = os.path.join(HERE, "_tmp")

sys.path.insert(0, HERE)
import mdbook                                   # noqa: E402
import theme                                    # noqa: E402
from theme import (ACCENT, ACCENT_SOFT, BODY, BODY_B, BODY_I, CONTENT_W, GRAY,
                   GRAY_LIGHT, HEAD, INK, MARGIN_B, MARGIN_L, MARGIN_R, MARGIN_T,
                   PAGE_H, PAGE_W, RULE)  # noqa: E402

BOOK_TITLE = "远程之门"
BOOK_SUBTITLE = "SSH、堡垒机与对象存储的技术细节"
BOOK_AUTHOR = "Dr. Dezeming"
BOOK_YEAR = "2026"
OFFSET = 1          # 封面占 1 页，正文页码与阅读器页码对齐


# ---------------------------------------------------------------- 辅助部件

class PageKind(Flowable):
    """零尺寸标记，用来声明所在页面的类型（不排页眉 / 单独首页等）。"""

    def __init__(self, kind):
        Flowable.__init__(self)
        self.kind = kind
        self.width = 0
        self.height = 0

    def wrap(self, aw, ah):
        return (0, 0)

    def draw(self):
        pass


class RegionMark(Flowable):
    """零尺寸标记：在排版到该处时切换页眉与目录收录方式。"""

    def __init__(self, doc, toc_mode="h1h2", head=None):
        Flowable.__init__(self)
        self.doc = doc
        self.toc_mode = toc_mode
        self.head = head
        self.width = 0
        self.height = 0

    def wrap(self, aw, ah):
        return (0, 0)

    def draw(self):
        self.doc.toc_mode = self.toc_mode
        if self.head is not None:
            self.doc.running_head = self.head


class BookDoc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        BaseDocTemplate.__init__(
            self, filename,
            pagesize=(PAGE_W, PAGE_H),
            leftMargin=MARGIN_L, rightMargin=MARGIN_R,
            topMargin=MARGIN_T, bottomMargin=MARGIN_B,
            title=BOOK_TITLE + "：" + BOOK_SUBTITLE,
            author=BOOK_AUTHOR,
            subject="SSH 协议、堡垒机、VS Code 远程开发与对象存储",
            creator="book/build/build.py",
            **kw
        )
        frame = Frame(MARGIN_L, MARGIN_B, CONTENT_W, PAGE_H - MARGIN_T - MARGIN_B,
                      id="main", leftPadding=0, rightPadding=0,
                      topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id="main", frames=[frame],
                                            onPageEnd=self.decorate)])
        self.page_kind = {}
        self.running_head = ""
        self.toc_mode = "h1h2"
        self._bm = 0

    # 每页结束时画页眉页脚
    def decorate(self, canv, doc):
        kind = self.page_kind.get(doc.page, "normal")
        canv.saveState()
        if kind in ("normal", "chapter", "toc", "appendix"):
            canv.setFont(BODY, 8)
            canv.setFillColor(GRAY_LIGHT)
            canv.drawString(MARGIN_L, PAGE_H - MARGIN_T + 20, BOOK_TITLE)
            if self.running_head:
                canv.setFont(BODY, 8)
                canv.drawRightString(PAGE_W - MARGIN_R, PAGE_H - MARGIN_T + 20,
                                     self.running_head)
            canv.setStrokeColor(RULE)
            canv.setLineWidth(0.5)
            canv.line(MARGIN_L, PAGE_H - MARGIN_T + 13,
                      PAGE_W - MARGIN_R, PAGE_H - MARGIN_T + 13)

        if kind != "title":
            canv.setFont(BODY, 8.6)
            canv.setFillColor(GRAY)
            canv.drawCentredString(PAGE_W / 2.0, MARGIN_B - 30, str(doc.page + OFFSET))
        canv.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, PageKind):
            self.page_kind[self.page] = flowable.kind
            return
        if isinstance(flowable, mdbook.TaggedHeading):
            lvl = flowable.head_level
            text = getattr(flowable, "toc_text", flowable.head_text)
            show = self.toc_mode in ("h1", "h1h2")
            if show and lvl <= 1:
                self.notify("TOCEntry", (min(lvl, 1), text, self.page + OFFSET))
            if show:
                self._bm += 1
                key = "h%d_%d" % (self.page, self._bm)
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=min(lvl, 2), closed=(lvl > 0))


# ---------------------------------------------------------------- 图片处理

def optimize_images(enable=True):
    """把过大的 PNG 转成体积更小的 JPEG 副本，供 PDF 内嵌。"""
    tmp = os.path.join(BUILD_TMP, "img")
    os.makedirs(tmp, exist_ok=True)
    mapping = {}
    if not enable:
        return mapping
    try:
        from PIL import Image as PILImage
    except ImportError:
        return mapping
    for dirpath, _, files in os.walk(IMAGES):
        for name in files:
            if not name.lower().endswith(".png"):
                continue
            src = os.path.join(dirpath, name)
            if os.path.getsize(src) < 260 * 1024:
                continue
            rel = os.path.relpath(src, IMAGES).replace(os.sep, "_")
            dst = os.path.join(tmp, os.path.splitext(rel)[0] + ".jpg")
            im = PILImage.open(src)
            if im.mode in ("RGBA", "LA", "P"):
                bg = PILImage.new("RGB", im.size, (255, 255, 255))
                im = im.convert("RGBA")
                bg.paste(im, mask=im.split()[-1])
                im = bg
            else:
                im = im.convert("RGB")
            if im.width > 1500:
                im = im.resize((1500, int(im.height * 1500 / im.width)),
                               PILImage.LANCZOS)
            im.save(dst, "JPEG", quality=87, optimize=True, progressive=True)
            if os.path.getsize(dst) < os.path.getsize(src):
                mapping[src] = dst
    return mapping


_IMG_MAP = {}


def _img_flow(path, width, height):
    real = _IMG_MAP.get(path, path)
    img = Image(real, width=width, height=height)
    img.hAlign = "CENTER"
    return img


def resolve_image(path):
    return _IMG_MAP.get(path, path)


# ---------------------------------------------------------------- 各类页面

def build_title_page(story, st):
    story.append(PageBreak())
    story.append(PageKind("title"))
    for _ in range(3):
        story.append(Spacer(1, 24))
    story.append(Paragraph(BOOK_TITLE, st["title_main"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(BOOK_SUBTITLE, st["title_sub"]))
    story.append(Spacer(1, 24))
    story.append(HRFlowable(width="26%", thickness=1.1, color=ACCENT,
                            spaceBefore=0, spaceAfter=26, hAlign="CENTER"))
    for _ in range(7):
        story.append(Spacer(1, 24))
    story.append(Paragraph(BOOK_AUTHOR, st["title_meta"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(BOOK_YEAR, st["title_meta"]))


def content_section(story, st, doc, entry, conv, kind, kicker, toc_prefix):
    """章 / 附录 / 前言 / 后记：统一的版式入口。"""
    path = os.path.join(BOOK, entry["file"])
    flows = conv.convert_file(path)
    if not flows:
        return
    head = flows[0]
    body = flows[1:]
    if not isinstance(head, mdbook.TaggedHeading):
        body = flows
        head = None
    story.append(PageBreak())
    story.append(PageKind(kind))
    story.append(RegionMark(doc, "h1h2" if kind in ("chapter", "appendix") else "h1",
                            head.head_text if head else ""))
    if kicker:
        story.append(Paragraph(kicker, st["ch_num"]))
    if head is not None:
        head.style = st["h1"]
        head.toc_text = ((toc_prefix + "　") if toc_prefix else "") + head.head_text
        head.head_level = 0
        story.append(head)
    story.append(HRFlowable(width="16%", thickness=1.3, color=ACCENT,
                            spaceBefore=0, spaceAfter=16, hAlign="LEFT"))
    story.extend(body)


def part_section(story, st, doc, entry, conv):
    path = os.path.join(BOOK, entry["file"])
    flows = conv.convert_file(path)
    head = None
    rest = flows
    if flows and isinstance(flows[0], mdbook.TaggedHeading):
        head = flows[0]
        rest = flows[1:]
    story.append(PageBreak())
    story.append(PageKind("part"))
    story.append(RegionMark(doc, "off", ""))
    story.append(Spacer(1, 120))
    story.append(Paragraph(entry["kicker"], st["part_kicker"]))
    if head:
        story.append(Paragraph(mdbook.esc(head.head_text), st["part_title"]))
    story.append(HRFlowable(width="100%", thickness=0.9, color=ACCENT_SOFT,
                            spaceBefore=6, spaceAfter=20))
    for fl in rest:
        if isinstance(fl, Paragraph):
            fl.style = st["part_lead"]
        story.append(fl)


def toc_section(story, st, toc, doc=None):
    story.append(PageBreak())
    story.append(PageKind("toc"))
    if doc is not None:
        story.append(RegionMark(doc, "off", ""))
    story.append(Paragraph("目　录", st["toc_title"]))
    story.append(toc)


# ---------------------------------------------------------------- 主流程

def patch_reportlab():
    """修掉 reportlab 在 CJK 段落被拆分后重排时的 kind 标记错误。

    拆分产生的片段已经带了 FragLine 行对象，但重新换行时被标成 kind=0，
    绘制阶段就会按“单一样式行”去取字段，触发 TypeError。
    """
    from reportlab.platypus import paragraph as _rp

    orig = _rp.Paragraph.breakLinesCJK

    def breakLinesCJK(self, maxWidths):
        bl = orig(self, maxWidths)
        try:
            if getattr(bl, "kind", None) == 0 and bl.lines                     and isinstance(bl.lines[0], _rp.FragLine):
                bl.kind = 1
        except Exception:
            pass
        return bl

    _rp.Paragraph.breakLinesCJK = breakLinesCJK


def patch_kinsoku():
    """补上中文标点的避头尾规则。

    reportlab 自带的 CANNOT_START_LINE 只覆盖日文标点，全角逗号、冒号、问号这些
    中文常用符号不在其中，断行时会被推到行首，排出来很难看。
    """
    from reportlab.lib import textsplit
    from reportlab.platypus import paragraph as _rp

    cannot_start = "，、。；：？！）】》」』”’｝］〉·…—～％"
    for mod in (textsplit, _rp):
        mod.ALL_CANNOT_START = mod.ALL_CANNOT_START + cannot_start
    textsplit.ALL_CANNOT_END = textsplit.ALL_CANNOT_END + "“‘（【《「『〈［｛"


def main():
    opt = "--no-opt" not in sys.argv
    t0 = time.time()
    patch_reportlab()
    patch_kinsoku()
    theme.register_fonts()
    st = theme.styles()

    global _IMG_MAP
    _IMG_MAP = optimize_images(opt)
    mdbook.IMAGE_RESOLVER = resolve_image

    os.makedirs(OUTPUT, exist_ok=True)
    os.makedirs(BUILD_TMP, exist_ok=True)

    with open(os.path.join(HERE, "structure.json"), encoding="utf-8") as f:
        struct = json.load(f)

    from reportlab.platypus.tableofcontents import TableOfContents
    toc = TableOfContents()
    toc.levelStyles = [st["toc0"], st["toc1"]]
    toc.dotsMinLevel = 0
    toc.tableStyle = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]

    body_pdf = os.path.join(BUILD_TMP, "body.pdf")
    doc = BookDoc(body_pdf)
    story = []
    conv = mdbook.Converter(st, os.path.join(BOOK, "chapters"))

    for entry in struct:
        kind = entry["kind"]
        if kind == "title":
            build_title_page(story, st)
        elif kind == "toc":
            toc_section(story, st, toc, doc)
        elif kind == "part":
            part_section(story, st, doc, entry, conv)
        elif kind in ("chapter", "appendix", "preface", "epilogue"):
            kicker = entry.get("kicker", "")
            prefix = entry.get("toc_prefix", "")
            content_section(story, st, doc, entry, conv, kind, kicker, prefix)
        elif kind == "md":
            path = os.path.join(BOOK, entry["file"])
            story.append(PageBreak())
            story.append(PageKind(entry.get("page_kind", "normal")))
            story.append(RegionMark(doc, "off", entry.get("head", "")))
            story.extend(conv.convert_file(path))
        else:
            raise SystemExit("未知的结构条目：" + str(entry))

    doc.multiBuild(story)
    body_pages = doc.page

    final = os.path.join(OUTPUT, "remote-access-book.pdf")
    staged = os.path.join(BUILD_TMP, "final.pdf")
    assemble(staged, body_pdf, body_pages)
    final = install_pdf(staged, final)
    size = os.path.getsize(final) / 1024.0 / 1024.0
    print("PDF: %s" % final)
    print("页数: %d 页（含封面封底），体积 %.2f MB，用时 %.1f s"
          % (body_pages + 2, size, time.time() - t0))
    if size > 19.5:
        print("警告：超过 19.5 MB，请检查插图体积。")
    return final


def install_pdf(staged, final):
    """把合成好的 PDF 放到 output/。文件被阅读器占用时退让一步，不覆盖失败。"""
    import time as _t

    os.makedirs(os.path.dirname(final), exist_ok=True)
    for i in range(8):
        try:
            os.replace(staged, final)
            return final
        except PermissionError:
            _t.sleep(0.4)
    alt = final.replace(".pdf", "-new.pdf")
    os.replace(staged, alt)
    print("提示：%s 正被其他程序占用（可能在阅读器中打开），本次输出到 %s"
          % (os.path.basename(final), os.path.basename(alt)))
    return alt


def assemble(final, body_pdf, body_pages):
    """用页面级拼装把封面、正文、封底合成一本 PDF。"""
    try:
        import pymupdf as fitz
    except ImportError:                                   # 兼容旧版本
        import fitz

    cover = os.path.join(BOOK, "images", "cover.jpg")
    back = os.path.join(BOOK, "images", "backcover.jpg")
    out = fitz.open()
    if os.path.exists(cover):
        page = out.new_page(width=PAGE_W, height=PAGE_H)
        page.insert_image(fitz.Rect(0, 0, PAGE_W, PAGE_H), filename=cover)
    body = fitz.open(body_pdf)
    offset = out.page_count
    toc = body.get_toc()
    out.insert_pdf(body)
    if toc:
        out.set_toc([[lvl, title, page + offset] for lvl, title, page in toc])
    if os.path.exists(back):
        page = out.new_page(width=PAGE_W, height=PAGE_H)
        page.insert_image(fitz.Rect(0, 0, PAGE_W, PAGE_H), filename=back)
    out.set_metadata({
        "title": "%s：%s" % (BOOK_TITLE, BOOK_SUBTITLE),
        "author": BOOK_AUTHOR,
        "subject": "SSH、堡垒机、VS Code 远程开发、对象存储",
        "keywords": "SSH, JumpServer, 堡垒机, COS, S3, Remote-SSH, 对象存储",
        "creator": "book/build/build.py",
    })
    out.save(final, garbage=4, deflate=True, clean=True)
    out.close()


if __name__ == "__main__":
    main()
