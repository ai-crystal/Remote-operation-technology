# -*- coding: utf-8 -*-
"""排版主题：字体注册、配色、段落样式。"""

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

WIN_FONTS = r"C:\Windows\Fonts"

# 版心尺寸（A4）
PAGE_W, PAGE_H = 595.28, 841.89
MARGIN_L = 80
MARGIN_R = 72
MARGIN_T = 78
MARGIN_B = 74
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R
CONTENT_H = PAGE_H - MARGIN_T - MARGIN_B

# 配色：低饱和的墨色与灰蓝
INK = colors.HexColor("#1b1b1b")
INK_SOFT = colors.HexColor("#333333")
GRAY = colors.HexColor("#6f6f6f")
GRAY_LIGHT = colors.HexColor("#9b9b9b")
ACCENT = colors.HexColor("#1f5e8c")
ACCENT_SOFT = colors.HexColor("#4a7fa5")
RULE = colors.HexColor("#ccd6dd")
CODE_BG = colors.HexColor("#f4f6f7")
CODE_LINE = colors.HexColor("#d9e0e5")
TABLE_HEAD_BG = colors.HexColor("#eef2f5")
TABLE_LINE = colors.HexColor("#c3ccd4")

BODY = "Song"        # 宋体，正文
BODY_B = "Hei"       # 黑体，粗体
BODY_I = "Kai"       # 楷体，斜体与引文
HEAD = "Hei"         # 标题
MONO = "Mono"
MONO_B = "MonoB"
MONO_CJK = "MonoCJK"

_FONT_FILES = [
    (BODY, "simsun.ttc", 0),
    (BODY_B, "simhei.ttf", 0),
    (BODY_I, "simkai.ttf", 0),
    (HEAD, "simhei.ttf", 0),
    (MONO, "consola.ttf", 0),
    (MONO_B, "consolab.ttf", 0),
    (MONO_CJK, "simsun.ttc", 1),
]


def register_fonts():
    for name, fname, idx in _FONT_FILES:
        path = os.path.join(WIN_FONTS, fname)
        if not os.path.exists(path):
            raise SystemExit("缺少字体文件：" + path)
        try:
            pdfmetrics.registerFont(TTFont(name, path, subfontIndex=idx))
        except Exception:
            pdfmetrics.registerFont(TTFont(name, path))
    pdfmetrics.registerFontFamily(BODY, normal=BODY, bold=BODY_B, italic=BODY_I, boldItalic=BODY_B)
    pdfmetrics.registerFontFamily(BODY_I, normal=BODY_I, bold=BODY_B, italic=BODY_I, boldItalic=BODY_B)
    pdfmetrics.registerFontFamily(MONO, normal=MONO, bold=MONO_B, italic=MONO, boldItalic=MONO_B)
    pdfmetrics.registerFontFamily(HEAD, normal=HEAD, bold=HEAD, italic=HEAD, boldItalic=HEAD)


def styles():
    s = {}

    s["body"] = ParagraphStyle(
        "body", fontName=BODY, fontSize=10.5, leading=18.4,
        alignment=TA_JUSTIFY, firstLineIndent=21, spaceBefore=0, spaceAfter=3.2,
        wordWrap="CJK", textColor=INK, allowWidows=1, allowOrphans=1,
    )
    # 段首不缩进：用于紧接标题的第一段、列表续段、图注后段落等
    s["body_ni"] = ParagraphStyle("body_ni", parent=s["body"], firstLineIndent=0)

    s["ch_num"] = ParagraphStyle(
        "ch_num", fontName=HEAD, fontSize=9.5, leading=14, textColor=ACCENT,
        spaceBefore=0, spaceAfter=8, alignment=TA_LEFT, wordWrap="CJK",
    )
    s["h1"] = ParagraphStyle(
        "h1", fontName=HEAD, fontSize=22, leading=31, textColor=INK,
        spaceBefore=2, spaceAfter=16, alignment=TA_LEFT, wordWrap="CJK",
    )
    s["h2"] = ParagraphStyle(
        "h2", fontName=HEAD, fontSize=14, leading=21, textColor=INK,
        spaceBefore=17, spaceAfter=7, alignment=TA_LEFT, wordWrap="CJK",
        keepWithNext=1,
    )
    s["h3"] = ParagraphStyle(
        "h3", fontName=HEAD, fontSize=11.5, leading=18, textColor=INK_SOFT,
        spaceBefore=12, spaceAfter=5, alignment=TA_LEFT, wordWrap="CJK",
        keepWithNext=1,
    )
    s["h4"] = ParagraphStyle(
        "h4", fontName=BODY_B, fontSize=10.5, leading=17, textColor=INK_SOFT,
        spaceBefore=9, spaceAfter=3, alignment=TA_LEFT, wordWrap="CJK",
        keepWithNext=1,
    )

    s["caption"] = ParagraphStyle(
        "caption", fontName=BODY, fontSize=9, leading=14.5, textColor=GRAY,
        alignment=TA_CENTER, spaceBefore=5, spaceAfter=12, wordWrap="CJK",
    )
    s["table_caption"] = ParagraphStyle(
        "table_caption", fontName=BODY, fontSize=9, leading=14.5, textColor=GRAY,
        alignment=TA_CENTER, spaceBefore=10, spaceAfter=4, wordWrap="CJK",
        keepWithNext=1,
    )

    s["code"] = ParagraphStyle(
        "code", fontName=MONO, fontSize=8.5, leading=12.6, textColor=colors.HexColor("#20262b"),
        spaceBefore=0, spaceAfter=0, wordWrap="CJK",
    )
    # 含中文注释的代码块改用等宽的宋体，保证列能对齐
    s["code_cjk"] = ParagraphStyle(
        "code_cjk", parent=s["code"], fontName=MONO_CJK, fontSize=9.0, leading=13.4,
    )
    s["icode"] = ParagraphStyle(
        "icode", fontName=MONO, fontSize=9, leading=13, textColor=colors.HexColor("#31556b"),
        wordWrap="CJK",
    )

    s["quote"] = ParagraphStyle(
        "quote", fontName=BODY_I, fontSize=10, leading=17.5, textColor=colors.HexColor("#4a4a4a"),
        leftIndent=16, rightIndent=8, spaceBefore=6, spaceAfter=10, wordWrap="CJK",
        alignment=TA_JUSTIFY,
    )

    s["bullet"] = ParagraphStyle(
        "bullet", parent=s["body"], firstLineIndent=0, leftIndent=20, bulletIndent=8,
        spaceAfter=2.6,
    )

    s["cell"] = ParagraphStyle(
        "cell", fontName=BODY, fontSize=9, leading=14, textColor=INK,
        wordWrap="CJK", alignment=TA_LEFT,
    )
    s["cell_head"] = ParagraphStyle(
        "cell_head", fontName=BODY_B, fontSize=9, leading=14, textColor=INK,
        wordWrap="CJK", alignment=TA_LEFT,
    )

    s["part_kicker"] = ParagraphStyle(
        "part_kicker", fontName=HEAD, fontSize=10, leading=16, textColor=ACCENT_SOFT,
        alignment=TA_LEFT, spaceAfter=10, wordWrap="CJK",
    )
    s["part_title"] = ParagraphStyle(
        "part_title", fontName=HEAD, fontSize=27, leading=40, textColor=INK,
        alignment=TA_LEFT, spaceAfter=14, wordWrap="CJK",
    )
    s["part_lead"] = ParagraphStyle(
        "part_lead", fontName=BODY, fontSize=10.5, leading=19.5, textColor=colors.HexColor("#3d3d3d"),
        alignment=TA_JUSTIFY, wordWrap="CJK", spaceBefore=8,
    )

    s["toc_title"] = ParagraphStyle(
        "toc_title", fontName=HEAD, fontSize=19, leading=28, textColor=INK,
        alignment=TA_CENTER, spaceAfter=22,
    )
    s["toc0"] = ParagraphStyle(
        "toc0", fontName=HEAD, fontSize=10.5, leading=15, textColor=INK,
        leftIndent=0, firstLineIndent=0, spaceBefore=7, wordWrap="CJK",
    )
    s["toc1"] = ParagraphStyle(
        "toc1", fontName=BODY, fontSize=9.6, leading=14, textColor=colors.HexColor("#3f3f3f"),
        leftIndent=20, firstLineIndent=0, spaceBefore=1.5, wordWrap="CJK",
    )

    s["title_main"] = ParagraphStyle(
        "title_main", fontName=HEAD, fontSize=30, leading=44, textColor=INK,
        alignment=TA_CENTER, wordWrap="CJK",
    )
    s["title_sub"] = ParagraphStyle(
        "title_sub", fontName=BODY, fontSize=13, leading=22, textColor=colors.HexColor("#444444"),
        alignment=TA_CENTER, wordWrap="CJK",
    )
    s["title_meta"] = ParagraphStyle(
        "title_meta", fontName=BODY, fontSize=10.5, leading=20, textColor=GRAY,
        alignment=TA_CENTER, wordWrap="CJK",
    )
    s["copy"] = ParagraphStyle(
        "copy", fontName=BODY, fontSize=8.8, leading=17, textColor=colors.HexColor("#3a3a3a"),
        alignment=TA_LEFT, wordWrap="CJK", firstLineIndent=0,
    )
    return s
