---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: MD to PPTX/HTML
description: "Convert structured Markdown documents to professional HTML or PPTX presentations with formulas, tables, code blocks, and callout boxes"
version: "1.0"
author: damonl525
license: MIT

# Categorization
category: document-conversion
tags:
  - markdown
  - pptx
  - html
  - presentation
  - formula
  - table
  - code-blocks
department: Biostatistics

# AI Model Compatibility
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

# Skill Capabilities
capabilities:
  - md-to-pptx
  - md-to-html
  - formula-rendering
  - table-generation
  - code-block-rendering
  - callout-boxes

# Language Support
languages:
  - en
  - zh
---

# MD to PPTX/HTML Presentation

Convert structured Markdown documents into professional presentations. Optimized for technical/statistical content with formulas, comparison tables, code blocks, and callout boxes.

## Design Philosophy

**Dense technical content, not marketing fluff.**

This skill targets internal knowledge sharing (stats team meetings, methodology reviews, journal club presentations). The style is:
- Clean, minimal, no animations
- Information-dense slides (not one sentence per slide)
- Formula boxes with green accent background
- Tables with green headers, alternating row shading
- Code blocks in monospace with light gray background
- Callout boxes (green for info, red for warnings)
- Left accent bar on every slide

## Visual Style Constants

These constants define the Damon style. Use them consistently across all output formats.

### Color Palette

```
ACCENT       = #2D6A4F  (dark green — headers, bars, section dividers)
ACCENT_LIGHT = #40916C  (medium green — borders, sub-headers)
ACCENT_BG    = #D8F3DC  (light green — formula backgrounds, callout fills)
WHITE        = #FFFFFF
BLACK        = #1A1A2E  (near-black — body text)
GRAY         = #6C757D  (slide numbers, subtitles)
RED          = #D00000  (warning callout accent)
RED_BG       = #FCE4E4  (warning callout background)
CODE_BG      = #F0F0F0  (code block background)
BORDER       = #DEE2E6  (code/table borders)
DARK_GREEN   = #1B4332  (formula text color)
DARK_RED     = #641220  (warning callout text)
```

### Typography (PPTX)

```
FONT_MAIN    = 微软雅黑      (all non-code text)
FONT_CODE    = Consolas      (code blocks, formulas)

SZ_TITLE     = 38pt  (slide big title)
SZ_SECTION   = 32pt  (section heading)
SZ_SUBTITLE  = 22pt  (subtitle)
SZ_H3        = 20pt  (sub-heading)
SZ_BODY      = 17pt  (body text)
SZ_BODY_SM   = 16pt  (body small)
SZ_LIST      = 17pt  (list items)
SZ_FORMULA   = 16pt  (formula text (Consolas))
SZ_CODE      = 13pt  (code text (Consolas))
SZ_CALLOUT_T = 16pt  (callout bold title)
SZ_CALLOUT_B = 15pt  (callout body)
SZ_TABLE_HDR = 15pt  (table header (white on green))
SZ_TABLE_CELL= 14pt  (table cell
SZ_SLIDE_NUM = 11pt  (slide number)
```

### Typography (HTML)

```css
--font-main: '微软雅黑', 'Segoe UI', sans-serif;
--font-mono: 'Consolas', 'JetBrains Mono', monospace;
--accent: #2D6A4F;
--accent-light: #40916C;
--accent-bg: #D8F3DC;
```

### Slide Layout

- **Dimensions**: 13.333" x 7.5" (16:9 widescreen)
- **Left accent bar**: 0.06" wide, full height, ACCENT color
- **Content area**: 0.5" left margin, 12.3" usable width
- **Slide number**: bottom-right, "N / total" format
- **Section heading**: 32pt bold + 3" green underline bar below

### Layout Constants (for positioning)

```
CONTENT_LEFT = 0.5"      # Main content left margin
CONTENT_WIDTH = 12.3"    # Main content usable width
COL_L_LEFT   = 0.5"      # Left column start
COL_R_LEFT   = 6.8"      # Right column start
COL_W        = 5.8"      # Single column width
```

## PPTX Helper API Reference

When generating gen_pptx.py, import helpers from `references/pptx_helpers.py`. Available functions:

```python
# Setup
create_presentation()          → (prs, blank_layout)

# Slide creation
add_slide(prs, layout)         → slide

# Text elements
add_title(slide, text, top=0.4")
add_subtitle(slide, text, top=1.1")
add_section(slide, text, top=0.25")
add_slide_num(slide, num, total)

# Rich elements
add_formula(slide, text, left, top, width, height)
add_code(slide, text, left, top, width, height)
add_callout(slide, title, body, left, top, width, height, warn=False)
add_table(slide, headers, rows, left, top, width, height)
add_bullet_list(slide, items, left, top, width, height, ...)

# Composite elements
add_flow_boxes(slide, items, top, box_height=0.9")
add_comparison(slide, left_title, left_items, right_title, right_items, ...)

# Low-level helpers
add_bg(slide, left, top, w, h, fill, border_color=None)
set_text(tf, text, sz, bold, color, align)
add_para(tf, text, sz, bold, color, align, sb)
```

## Slide Element Types

### 1. Title Slide
- Large title (38pt, ACCENT, bold)
- Subtitle (22pt, GRAY)
- Optional: reference citation in italic, goal list

### 2. Section Slide (divider)
- Section title (32pt bold, BLACK)
- Green underline bar (3" wide)
- Start of a new topic section

### 3. Content Slide with Two Columns
- Left column: 0.5" to 6.3" (width 5.8")
- Right column: 6.8" to 12.6" (width 5.8")
- Each column has its own heading (H3, ACCENT_LIGHT) + body

### 4. Formula Box
- Rounded rectangle with ACCENT_BG fill + ACCENT_LIGHT border
- Left green accent bar (0.05" wide)
- Consolas font, DARK_GREEN color
- Multi-line formulas supported

### 5. Code Block
- Rounded rectangle with CODE_BG fill + BORDER border
- Consolas font, BLACK color
- 0pt line spacing for dense code display

### 6. Table
- Header row: ACCENT background, white bold text
- Data rows: alternating white / #F8F9FA
- SZ_TABLE_HDR for headers, SZ_TABLE_CELL for data

### 7. Callout Box (Info)
- ACCENT_BG background, ACCENT_LIGHT border
- Bold title (ACCENT color) + body text (DARK_GREEN)

### 8. Callout Box (Warning)
- RED_BG background, RED border
- Bold title (DARK_RED) + body text (DARK_RED)

### 9. Flow Diagram
- Rounded rectangles (ACCENT_BG) with ACCENT bold text
- Arrow shapes between boxes (ACCENT fill)
- Horizontal layout, centered vertically

### 10. Comparison (vs.)
- Left: RED_BG box (negative/weaker method)
- Right: ACCENT_BG box (positive/stronger method)
- "vs." label centered between them

## Workflow

### Step 1: Parse the MD Source

Read the source Markdown file and identify structural elements:

```
# / ## / ###  → Title / Section / H3
**bold**      → emphasis in body
> quote       → callout box
```code```     → code block
| table |     → data table
$ / $$        → formula box (inline/display math)
```

### Step 2: Plan Slide Structure

#### Splitting Rules

Follow these concrete rules to decide what goes on each slide:

1. **`# Title`** → Always becomes a Title Slide (first slide)
   - Include: main title + subtitle + 3-5 objectives as numbered list
2. **`## Section`** → Section divider slide with green underline
   - Reset the visual rhythm for the audience
3. **`### Sub` + content** → Content slide
   - **Max 6 bullet points** per slide. If more, split into two slides sharing the same section heading.
   - **Max 3 formula boxes** per slide. If more, split and use "（续）" in section title.
   - **1 table** per slide (tables wider than 4 columns need full width — no two-column layout).
   - **Max 2 code blocks** per slide (use two-column layout: code left, explanation right).
4. **Blockquote `>`** → Always becomes a callout box. Place at the bottom of the current slide.
5. **Overflow rule**: If a section's content exceeds one slide's capacity, create additional content slides with abbreviated section headers (no green underline repeat — just continue with `###` headings).

#### Slide ordering template

```
Slide 1:      Title (topic + subtopic + objectives)
Slide 2:      Background / Problem Setup
Slide 3..N:   Core Content (one section divider + 2-4 content slides per topic)
Slide N+1:    Comparison Table (methods, tools, or approaches side-by-side)
Slide N+2:    Practical Recommendations / Takeaways
Slide Last:   Summary (3-5 key points + references)
```

Typical range: 12-25 slides for a 20-40 minute talk.

### Step 3: Generate Output

#### PPTX Path (default)

1. Read `references/pptx_helpers.py` for the helper function library
2. Generate a Python script (e.g., `gen_pptx.py`) in the working directory that:
   - Imports the standard helpers
   - Contains slide-specific content code
   - Saves to a `.pptx` file in the same directory
3. Run: `python gen_pptx.py`
4. Dependencies: `pip install python-pptx`

> **Note**: All position/size parameters in helpers now auto-convert bare `int`/`float` to `Inches()` via the internal `_emu()` function. You can safely pass `0.5` or `Inches(0.5)` — both work. This prevents the common bug where a bare number is treated as EMU (invisible on slide).

#### HTML Path

1. Read `references/html_template.html` for the complete CSS/HTML framework
2. Generate a single HTML file using the template's CSS classes:
   - `.slide` — each slide container
   - `.formula` — formula box (green bg + left bar)
   - `.callout-key` / `.callout-warn` — info/warning callout
   - `.cols` > `.col` — two-column layout
   - `.compare` > `.compare-negative` + `.compare-positive` — comparison boxes
   - `.flow` > `.flow-box` + `.flow-arrow` — flow diagram
   - `<table>` with `<th>` — auto-styled green header tables
   - `<pre><code>` — code blocks
   - `.slide-num` — bottom-right page number
3. Open in browser, Ctrl+P to print/export PDF
4. No external dependencies

### Step 4: Verify

After generating:
- PPTX: Open and check all slides render correctly
- HTML: Open in browser and check layout + print preview
- Verify all formulas, tables, and code blocks are present
- Check slide numbering is correct

## MD Parsing Rules

### Headings
- `# Title` → Title slide
- `## Section` → Section divider slide
- `### Sub` → H3 sub-heading within a content slide

### Formulas
- Inline math `$...$` or display math `$$...$$` → Formula box
- Multiple sequential formulas → Stack vertically with 0.1" gap (PPTX) or sequential `.formula` divs (HTML)
- **Rendering strategy**: Use Unicode math symbols — no MathJax/KaTeX dependency
  - Greek: α β γ δ θ λ μ π σ φ ψ ω (upper: Σ Δ Ω Φ)
  - Operators: ± × · ÷
  - Relations: ≤ ≥ ≠ ≈
  - Misc: Σ √ ∂ ∞ →
  - Subscripts: use Unicode where available (₁ ₂ ₃ ₕ ₖ), otherwise use `_h` notation
  - Superscripts: use Unicode where available (² ³), otherwise use `^2` notation
- **Fallback**: For complex LaTeX that cannot be expressed in Unicode, display the LaTeX source verbatim in the formula box (readers will understand)

### Tables
- Standard Markdown pipe tables → Table element
- First row is header
- Ensure enough vertical space (2" minimum for 5+ rows)

### Code Blocks
- Fenced with ``` → Code block element
- Language tag preserved as visual label

### Blockquotes
- `>` prefixed lines → Callout box
- If content contains "注意", "警告", "Warning", "Caution" → Warning style (red)
- Otherwise → Info style (green)

### Lists
- `- item` or `* item` → Bullet list items
- `1. item` → Numbered list items
- Preserve nesting (2-space indent)

## Example: MD → Slide Mapping

See `example.md` for a complete input example. Here is how it maps to slides:

| MD Section | Slide Type | Element Count |
|------------|------------|---------------|
| `# Score Method for MI` + Objectives list | Title Slide | h1 + subtitle + numbered list |
| `## Background` | Section Divider | h2 + green underline |
| `### Clinical Trial Scenario` + `### Required Output` | Content (two-column) | 2x H3 + bullet lists |
| `> Core question...` | Callout (info) | Green callout box at bottom |
| `## Method Overview` | Section Divider + Content | h2 + numbered list + callout |
| `## Complete Data MN Score Method` | Content (formula-heavy) | 3 formula boxes + callout + H3 + bullets |
| `## Constrained MLE` + code block | Content (code + table) | code block left + table right + warning callout |
| `## Method Comparison` | Content (table) | full-width table + callout |
| `## Summary` | Content (closing) | numbered list + small table + callout |

This example.md (82 lines) produces approximately **8-10 slides**.

## Customization Points

The user may request adjustments to:
- **Color scheme**: Replace ACCENT/ACCENT_LIGHT/ACCENT_BG with new values
- **Font**: Replace 微软雅黑 with another font family
- **Font sizes**: Scale all sizes proportionally
- **Slide count**: Merge or split slides as needed
- **Language**: Content stays in source language; UI elements (slide numbers, section labels) match

## Anti-Patterns (Avoid)

- One sentence per slide (too sparse for technical content)
- Clip art, stock photos, or decorative elements
- Animations or transitions
- Dark backgrounds with light text
- More than 3 font families on a slide
- Untagged callout boxes (always use info or warning style)
- Tables without headers
- Code blocks without background shading

## Integration with Other Skills

- **PDF Batch Extractor**: Extract PDF content to MD, then convert to PPTX
- **Statistical Review Summary**: Convert summary MD to presentation for team meeting

## Version History

- **v1.0** (2026-05-14): Initial release with PPTX + HTML dual output
