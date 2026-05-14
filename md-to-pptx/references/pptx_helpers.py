#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPTX Helper Functions Template
===============================
Reusable building blocks for generating professional PPTX presentations.
Designed for technical/statistical content with formulas, tables, code blocks,
and callout boxes.

Usage:
  1. Copy this file or import its functions into your gen_pptx.py
  2. Customize slide content using the helpers below
  3. Run: python gen_pptx.py

Dependencies: pip install python-pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ══════════════════════════════════════════════════════════════════════════════
# STYLE CONSTANTS — Customize these to change the visual theme
# ══════════════════════════════════════════════════════════════════════════════

# Fonts
FN = '微软雅黑'           # All non-code text
FN_CODE = 'Consolas'      # Code blocks and formulas

# Font Sizes (pt)
SZ_TITLE = 38             # Slide big title
SZ_SECTION = 32           # Section heading
SZ_SUBTITLE = 22          # Subtitle
SZ_H3 = 20                # Sub-heading (h3)
SZ_BODY = 17              # Body text
SZ_BODY_SM = 16           # Body small
SZ_LIST = 17              # List items
SZ_FORMULA = 16           # Formula text (Consolas)
SZ_CODE = 13              # Code text (Consolas)
SZ_CALLOUT_TITLE = 16     # Callout bold title
SZ_CALLOUT_BODY = 15      # Callout body
SZ_TABLE_HDR = 15         # Table header (white on green)
SZ_TABLE_CELL = 14        # Table cell
SZ_FLOW = 14              # Flow diagram boxes
SZ_SLIDE_NUM = 11         # Slide number
SZ_LABEL = 17             # Labels

# Colors
ACCENT      = RGBColor(0x2D, 0x6A, 0x4F)   # Dark green
ACCENT_LIGHT= RGBColor(0x40, 0x91, 0x6C)   # Medium green
ACCENT_BG   = RGBColor(0xD8, 0xF3, 0xDC)   # Light green background
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
BLACK       = RGBColor(0x1A, 0x1A, 0x2E)   # Near-black body text
GRAY        = RGBColor(0x6C, 0x75, 0x7D)   # Subtitles, slide numbers
RED         = RGBColor(0xD0, 0x00, 0x00)   # Warning accent
RED_BG      = RGBColor(0xFC, 0xE4, 0xE4)   # Warning background
CODE_BG     = RGBColor(0xF0, 0xF0, 0xF0)   # Code block background
BORDER      = RGBColor(0xDE, 0xE2, 0xE6)   # Borders
DARK_GREEN  = RGBColor(0x1B, 0x43, 0x32)   # Formula text
DARK_RED    = RGBColor(0x64, 0x12, 0x20)   # Warning text

# Slide Dimensions (16:9 widescreen)
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

# Layout Constants
LEFT_BAR_W = Inches(0.06)   # Accent bar width
CONTENT_LEFT = Inches(0.5)  # Main content left margin
CONTENT_WIDTH = Inches(12.3) # Main content usable width
COL_W = Inches(5.8)         # Single column width
COL_L_LEFT = Inches(0.5)    # Left column start
COL_R_LEFT = Inches(6.8)    # Right column start


# ══════════════════════════════════════════════════════════════════════════════
# PRESENTATION SETUP
# ══════════════════════════════════════════════════════════════════════════════

def create_presentation():
    """Create a new widescreen presentation and return (prs, blank_layout)."""
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    blank_layout = prs.slide_layouts[6]
    return prs, blank_layout


# ══════════════════════════════════════════════════════════════════════════════
# BASIC HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def add_slide(prs, blank_layout):
    """Add a new slide with left accent bar. Returns the slide object."""
    slide = prs.slides.add_slide(blank_layout)
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Emu(0), Emu(0), LEFT_BAR_W, SLIDE_H
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT
    bar.line.fill.background()
    return slide


def add_tb(slide, left, top, width, height):
    """Add a textbox at the specified position."""
    return slide.shapes.add_textbox(left, top, width, height)


def set_text(tf, text, sz=SZ_BODY, bold=False, color=BLACK, align=PP_ALIGN.LEFT):
    """Set text in a text frame (replaces existing content)."""
    tf.clear()
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = Pt(sz)
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.name = FN
    return r


def add_para(tf, text, sz=SZ_BODY, bold=False, color=BLACK,
             align=PP_ALIGN.LEFT, sb=Pt(5)):
    """Append a new paragraph to a text frame."""
    p = tf.add_paragraph()
    p.alignment = align
    p.space_before = sb
    r = p.add_run()
    r.text = text
    r.font.size = Pt(sz)
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.name = FN
    return r


def add_bg(slide, left, top, w, h, fill, border_color=None):
    """Add a rounded rectangle background shape."""
    s = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h
    )
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if border_color:
        s.line.color.rgb = border_color
        s.line.width = Pt(1)
    else:
        s.line.fill.background()
    return s


# ══════════════════════════════════════════════════════════════════════════════
# COMPOSITE ELEMENTS
# ══════════════════════════════════════════════════════════════════════════════

def add_slide_num(slide, num, total):
    """Add slide number (bottom-right corner)."""
    tb = add_tb(slide, Inches(12.4), Inches(7.0), Inches(0.8), Inches(0.4))
    set_text(tb.text_frame, f'{num} / {total}',
             sz=SZ_SLIDE_NUM, color=GRAY, align=PP_ALIGN.RIGHT)


def add_title(slide, text, top=Inches(0.4)):
    """Add large slide title."""
    tb = add_tb(slide, CONTENT_LEFT, top, CONTENT_WIDTH, Inches(0.8))
    set_text(tb.text_frame, text, sz=SZ_TITLE, bold=True, color=ACCENT)


def add_subtitle(slide, text, top=Inches(1.1)):
    """Add subtitle text."""
    tb = add_tb(slide, CONTENT_LEFT, top, CONTENT_WIDTH, Inches(0.6))
    set_text(tb.text_frame, text, sz=SZ_SUBTITLE, color=GRAY)


def add_section(slide, text, top=Inches(0.25)):
    """Add section heading with green underline bar."""
    tb = add_tb(slide, CONTENT_LEFT, top, CONTENT_WIDTH, Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = text
    r.font.size = Pt(SZ_SECTION)
    r.font.bold = True
    r.font.color.rgb = BLACK
    r.font.name = FN
    # Green underline bar
    ln = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        CONTENT_LEFT, top + Inches(0.72),
        Inches(3), Inches(0.04)
    )
    ln.fill.solid()
    ln.fill.fore_color.rgb = ACCENT
    ln.line.fill.background()


def add_formula(slide, text, left, top, width, height):
    """
    Add a formula box with green background and left accent bar.

    text: multi-line string (each line becomes a paragraph)
    """
    add_bg(slide, left, top, width, height, ACCENT_BG, ACCENT_LIGHT)
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, Inches(0.05), height
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT
    bar.line.fill.background()

    tb = add_tb(slide, left + Inches(0.25), top + Inches(0.12),
                width - Inches(0.4), height - Inches(0.18))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(text.strip().split('\n')):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_before = Pt(2)
        r = p.add_run()
        r.text = line
        r.font.size = Pt(SZ_FORMULA)
        r.font.name = FN_CODE
        r.font.color.rgb = DARK_GREEN


def add_callout(slide, title, body, left, top, width, height, warn=False):
    """
    Add a callout box (info or warning style).

    title: bold heading text
    body: multi-line string body text
    warn: True for red warning style, False for green info style
    """
    if warn:
        bg_c, bd_c, tx_c = RED_BG, RED, DARK_RED
    else:
        bg_c, bd_c, tx_c = ACCENT_BG, ACCENT_LIGHT, DARK_GREEN

    add_bg(slide, left, top, width, height, bg_c, bd_c)
    tb = add_tb(slide, left + Inches(0.2), top + Inches(0.1),
                width - Inches(0.4), height - Inches(0.18))
    tf = tb.text_frame
    tf.word_wrap = True

    # Title
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = title
    r.font.size = Pt(SZ_CALLOUT_TITLE)
    r.font.bold = True
    r.font.color.rgb = tx_c
    r.font.name = FN

    # Body lines
    for line in body.strip().split('\n'):
        p2 = tf.add_paragraph()
        p2.space_before = Pt(3)
        r2 = p2.add_run()
        r2.text = line
        r2.font.size = Pt(SZ_CALLOUT_BODY)
        r2.font.color.rgb = tx_c
        r2.font.name = FN


def add_code(slide, text, left, top, width, height):
    """
    Add a code block with gray background.

    text: multi-line string code content
    """
    add_bg(slide, left, top, width, height, CODE_BG, BORDER)
    tb = add_tb(slide, left + Inches(0.2), top + Inches(0.1),
                width - Inches(0.4), height - Inches(0.18))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(text.strip().split('\n')):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_before = Pt(0)
        r = p.add_run()
        r.text = line
        r.font.size = Pt(SZ_CODE)
        r.font.name = FN_CODE
        r.font.color.rgb = BLACK


def add_table(slide, headers, rows, left, top, width, height):
    """
    Add a formatted table with green header row.

    headers: list of column header strings
    rows: list of lists (each inner list = one data row)
    """
    if not headers:
        raise ValueError("headers cannot be empty")
    if not rows:
        raise ValueError("rows cannot be empty — use add_bg for empty placeholders")
    n_rows = len(rows) + 1
    n_cols = len(headers)
    tbl_shape = slide.shapes.add_table(n_rows, n_cols, left, top, width, height)
    tbl = tbl_shape.table

    # Header row
    for j, h in enumerate(headers):
        c = tbl.cell(0, j)
        c.text = h
        for p in c.text_frame.paragraphs:
            p.font.size = Pt(SZ_TABLE_HDR)
            p.font.bold = True
            p.font.color.rgb = WHITE
            p.font.name = FN
        c.fill.solid()
        c.fill.fore_color.rgb = ACCENT

    # Data rows
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = tbl.cell(i + 1, j)
            c.text = str(val)
            for p in c.text_frame.paragraphs:
                p.font.size = Pt(SZ_TABLE_CELL)
                p.font.color.rgb = BLACK
                p.font.name = FN
            if i % 2 == 1:
                c.fill.solid()
                c.fill.fore_color.rgb = RGBColor(0xF8, 0xF9, 0xFA)


def add_flow_boxes(slide, items, top, box_height=Inches(0.9)):
    """
    Add horizontal flow boxes with arrows between them.

    items: list of (text, left_position) tuples
    top: vertical position for the row
    """
    if not items:
        raise ValueError("items cannot be empty")
    box_w = Inches(2.6)
    for text, left in items:
        add_bg(slide, left, top, box_w, box_height, ACCENT_BG, ACCENT_LIGHT)
        tb = add_tb(slide, left + Inches(0.1), top + Inches(0.05),
                    box_w - Inches(0.2), box_height - Inches(0.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = text
        r.font.size = Pt(SZ_FLOW)
        r.font.bold = True
        r.font.color.rgb = ACCENT
        r.font.name = FN

    # Arrows between boxes
    for i in range(len(items) - 1):
        _, left_current = items[i]
        arrow_left = left_current + box_w + Inches(0.05)
        a = slide.shapes.add_shape(
            MSO_SHAPE.RIGHT_ARROW,
            arrow_left, top + Inches(0.22),
            Inches(0.35), Inches(0.35)
        )
        a.fill.solid()
        a.fill.fore_color.rgb = ACCENT
        a.line.fill.background()


def add_comparison(slide, left_title, left_items, right_title, right_items,
                   left_pos=COL_L_LEFT, right_pos=COL_R_LEFT,
                   top=Inches(4.9), width=COL_W, height=Inches(2.0),
                   left_warn=True):
    """
    Add side-by-side comparison boxes (red vs green).

    left_title: left box heading
    left_items: list of bullet point strings for left box
    right_title: right box heading
    right_items: list of bullet point strings for right box
    left_warn: True = left box is warning (red), False = left box is info (green)
    """
    # Left box
    left_bg = RED_BG if left_warn else ACCENT_BG
    left_bd = RED if left_warn else ACCENT_LIGHT
    left_tx = DARK_RED if left_warn else DARK_GREEN
    left_hd = RED if left_warn else ACCENT
    add_bg(slide, left_pos, top, width, height, left_bg, left_bd)
    tb_l = add_tb(slide, left_pos + Inches(0.2), top + Inches(0.1),
                  width - Inches(0.4), height - Inches(0.18))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    r = tf_l.paragraphs[0].add_run()
    r.text = left_title
    r.font.size = Pt(SZ_H3)
    r.font.bold = True
    r.font.color.rgb = left_hd
    r.font.name = FN
    for item in left_items:
        p = tf_l.add_paragraph()
        p.space_before = Pt(4)
        r = p.add_run()
        r.text = '• ' + item
        r.font.size = Pt(SZ_BODY_SM)
        r.font.color.rgb = left_tx
        r.font.name = FN

    # Right box
    right_bg = ACCENT_BG if left_warn else RED_BG
    right_bd = ACCENT_LIGHT if left_warn else RED
    right_tx = DARK_GREEN if left_warn else DARK_RED
    right_hd = ACCENT if left_warn else RED
    add_bg(slide, right_pos, top, width, height, right_bg, right_bd)
    tb_r = add_tb(slide, right_pos + Inches(0.2), top + Inches(0.1),
                  width - Inches(0.4), height - Inches(0.18))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    r = tf_r.paragraphs[0].add_run()
    r.text = right_title
    r.font.size = Pt(SZ_H3)
    r.font.bold = True
    r.font.color.rgb = right_hd
    r.font.name = FN
    for item in right_items:
        p = tf_r.add_paragraph()
        p.space_before = Pt(4)
        r = p.add_run()
        r.text = '• ' + item
        r.font.size = Pt(SZ_BODY_SM)
        r.font.color.rgb = right_tx
        r.font.name = FN

    # "vs." label
    vs_left = left_pos + width + Inches(0.05)
    tb_vs = add_tb(slide, vs_left, top + Inches(0.5), Inches(0.6), Inches(0.5))
    set_text(tb_vs.text_frame, 'vs.', sz=24, bold=True,
             color=GRAY, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════════════════
# BULLET LIST HELPER
# ══════════════════════════════════════════════════════════════════════════════

def add_bullet_list(slide, items, left, top, width, height,
                    sz=SZ_LIST, color=BLACK, bullet='• '):
    """Add a simple bullet list."""
    if not items:
        raise ValueError("items cannot be empty")
    tb = add_tb(slide, left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
            p.space_before = Pt(6)
        r = p.add_run()
        r.text = bullet + item
        r.font.size = Pt(sz)
        r.font.color.rgb = color
        r.font.name = FN


# ══════════════════════════════════════════════════════════════════════════════
# EXAMPLE USAGE
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import os

    prs, layout = create_presentation()
    total = 3

    # Slide 1: Title
    s = add_slide(prs, layout)
    add_title(s, 'Presentation Title', top=Inches(2.0))
    add_subtitle(s, 'Subtitle text here', top=Inches(2.8))
    add_slide_num(s, 1, total)

    # Slide 2: Section with content
    s = add_slide(prs, layout)
    add_section(s, 'Section Title')
    add_formula(s, 'Z = (d - delta) / sqrt(V)', Inches(0.5), Inches(1.15), Inches(12.3), Inches(0.75))
    add_callout(s, 'Key Insight', 'This is an important callout box.',
                Inches(0.5), Inches(2.2), Inches(12.3), Inches(1.0))
    add_slide_num(s, 2, total)

    # Slide 3: Table + Code
    s = add_slide(prs, layout)
    add_section(s, 'Comparison')
    add_table(s,
        ['Method', 'MI Variance', 'CI Type'],
        [['Wald-Rubin', 'Rubin', 'Wald'],
         ['Proposed Score', 'Rubin', 'Score inversion']],
        Inches(0.5), Inches(1.15), Inches(7.0), Inches(1.5))
    add_code(s, 'x <- rnorm(100)\nmean(x)', Inches(8.0), Inches(1.15), Inches(4.8), Inches(1.2))
    add_slide_num(s, 3, total)

    # Save
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example_output.pptx')
    prs.save(out)
    print(f'Saved: {out}')
