---
name: MD to PPTX/HTML
description: "Convert structured Markdown documents to professional HTML or PPTX presentations with formulas, tables, code blocks, and callout boxes"
version: "1.1"
author: damonl525
license: MIT
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
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o
capabilities:
  - md-to-pptx
  - md-to-html
  - formula-rendering
  - table-generation
  - code-block-rendering
  - callout-boxes
languages:
  - en
  - zh
---

# MD to PPTX/HTML Presentation

Convert structured Markdown into professional presentations. Optimized for technical/statistical content.

Style: clean, information-dense, green accent theme, left accent bar, no animations.

---

## PPTX API Reference

**MANDATORY:** Start every script with:
```python
from references.pptx_helpers import *
```

### Auto-Layout API (Recommended)

Use `Layout(slide)` to add elements sequentially — **no coordinates needed**.
Tracks Y cursor, auto-estimates height from content. Chain methods fluently.

```python
s = add_slide(prs, layout)
lm = Layout(s)
lm.title("Title Text")          # No (left, top, w, h) needed
lm.bullets(["item 1", "item 2"]) # Height auto-calculated
lm.formula("E = mc²")
lm.callout("Note", "Details")
lm.slide_num(1, total)
```

#### Layout Methods

| Method | Description |
|--------|-------------|
| `title(text)` | Large green title |
| `subtitle(text)` | Gray subtitle |
| `section(text)` | Section heading + green underline |
| `h3(text)` | Bold sub-heading |
| `bullets(items)` | Bullet list (auto-height) |
| `formula(text)` | Formula box (green bg + left bar) |
| `code(text)` | Code block (gray bg) |
| `callout(title, body, warn=False)` | Info/warning callout |
| `table(headers, rows)` | Table with green header |
| `comparison(l_title, l_items, r_title, r_items)` | Red vs green comparison |
| `flow(items)` | Flow diagram (auto-positioned) |
| `two_col_bullets(lt, li, rt, ri)` | Two-column bullets |
| `two_col_table_code(th, tr, code)` | Table left, code right |
| `two_col_bullets_table(bt, bi, th, tr)` | Bullets left, table right |
| `slide_num(num, total)` | Page number (no cursor advance) |
| `gap(inches)` | Explicit vertical gap |
| `remaining` | Remaining usable height (property) |

### Low-level Functions (Advanced)

```python
# Setup
create_presentation()          -> (prs, blank_layout)

# Slide
add_slide(prs, layout)         -> slide

# Text
add_title(slide, text, top=0.4)
add_subtitle(slide, text, top=1.1)
add_section(slide, text, top=0.25)    # Green underline bar
add_h3(slide, text, top=0.3)          # Bold sub-heading
add_slide_num(slide, num, total)

# Content
add_formula(slide, text, left, top, width, height)
add_code(slide, text, left, top, width, height)
add_callout(slide, title, body, left, top, width, height, warn=False)
add_table(slide, headers, rows, left, top, width, height)
add_bullet_list(slide, items, left, top, width, height, sz=17, bold=False)

# Composite
add_flow_boxes(slide, items, top, box_height=0.9)
add_comparison(slide, left_title, left_items, right_title, right_items,
               left_pos=0.5, right_pos=6.8, top=4.9, width=5.8, height=2.0,
               left_warn=True)

# Low-level
add_bg(slide, left, top, w, h, fill, border_color=None)
add_tb(slide, left, top, width, height) -> textbox
set_text(tf, text, sz=SZ_BODY, bold=False, color=BLACK, align=LEFT)
add_para(tf, text, sz=SZ_BODY, bold=False, color=BLACK, align=LEFT, sb=Pt(5))
```

### Constants

```
Colors:    ACCENT, ACCENT_LIGHT, ACCENT_BG, WHITE, BLACK, GRAY,
           RED, RED_BG, CODE_BG, BORDER, DARK_GREEN, DARK_RED

Alignment: LEFT, CENTER, RIGHT

Sizes:     SZ_TITLE(38), SZ_SECTION(32), SZ_SUBTITLE(22), SZ_H3(20),
           SZ_BODY(17), SZ_BODY_SM(16), SZ_LIST(17), SZ_FORMULA(16),
           SZ_CODE(13), SZ_CALLOUT_TITLE(16), SZ_CALLOUT_BODY(15),
           SZ_TABLE_HDR(15), SZ_TABLE_CELL(14), SZ_SLIDE_NUM(11)

Layout:    CONTENT_LEFT(0.5"), CONTENT_WIDTH(12.3"),
           COL_L_LEFT(0.5"), COL_R_LEFT(6.8"), COL_W(5.8")
```

### Rules

1. ALWAYS start with `from references.pptx_helpers import *`
2. ALWAYS use `Layout(s)` after `add_slide()` — let it handle positioning
3. NEVER specify coordinates manually unless using low-level functions for two-column
4. NEVER redefine any function listed above (no `def _emu`, `def create_presentation`, etc.)
5. NEVER use raw python-pptx API (no `.add_textbox`, `.add_shape`, `.add_table` on slide)
6. NEVER copy helper code inline — just import and call
7. Only the functions listed above exist — do NOT invent new ones

### Common Mistakes (MUST AVOID)

**Use Layout — do NOT manually position elements:**

    ❌  add_title(s, "Title", 0.4)
        add_bullet_list(s, ["a", "b"], 0.5, 1.3, 12.3, 1.5)  # manual coordinates
    ✅  lm = Layout(s)
        lm.title("Title")
        lm.bullets(["a", "b"])                                 # auto-positioned

**add_slide vs add_title — DIFFERENT functions:**

    ❌  s = add_slide(s, "Title Text", 0.4)               # WRONG
    ✅  s = add_slide(prs, layout)                        # create slide first
        lm = Layout(s)
        lm.title("Title Text")                            # Layout handles position

**NEVER use raw python-pptx API on slide objects:**

    ❌  s.add_textbox(...)  /  s.shapes.add_shape(...)
    ✅  Use Layout methods or helper functions

**NEVER redefine helper functions:**

    ❌  def _emu(v): ...  /  def add_title(...): ...
    ✅  from references.pptx_helpers import *

### Complete Example

```python
from references.pptx_helpers import *

prs, layout = create_presentation()
total = 8

# ── Slide 1: Title ──
s = add_slide(prs, layout)
lm = Layout(s)
lm.title("Score Method for Missing Data")
lm.subtitle("Rubin's Rules & Variance Estimation")
lm.bullets([
    "Objective 1: Derive score test statistic",
    "Objective 2: Compare with Wald-Rubin method",
    "Objective 3: Simulation study under MAR"
])
lm.slide_num(1, total)

# ── Slide 2: Section divider ──
s = add_slide(prs, layout)
Layout(s).section("1. Background").slide_num(2, total)

# ── Slide 3: Two-column bullets + table ──
s = add_slide(prs, layout)
lm = Layout(s)
lm.h3("1.1 Clinical Trial Scenario")
lm.two_col_bullets_table(
    "Key Design",
    ["Phase III randomized trial", "Primary endpoint: PFS", "n = 350 per arm"],
    ["Factor", "Value"],
    [["Design", "1:1 randomization"], ["Population", "HER2-negative"], ["Follow-up", "24 months"]]
)
lm.callout("Note", "Key assumption: MAR holds for missing data mechanism.")
lm.slide_num(3, total)

# ── Slide 4: Formulas ──
s = add_slide(prs, layout)
lm = Layout(s)
lm.h3("1.2 Score Statistic")
lm.formula("D = d - delta_0")
lm.formula("Z = D / sqrt(V_total)")
lm.callout("Key", "V_total = V_W + (1 + 1/m) * V_B (Rubin's variance)")
lm.slide_num(4, total)

# ── Slide 5: Code + Table ──
s = add_slide(prs, layout)
lm = Layout(s)
lm.h3("1.3 Implementation")
lm.two_col_table_code(
    ["Method", "Variance", "CI Type"],
    [["Wald-Rubin", "Rubin", "Wald"],
     ["Score", "Rubin", "Score inversion"]],
    "score_test <- function(d, V) {\n  Z <- d / sqrt(V)\n  2 * pnorm(-abs(Z))\n}"
)
lm.slide_num(5, total)

# ── Slide 6: Comparison ──
s = add_slide(prs, layout)
lm = Layout(s)
lm.h3("1.4 Method Comparison")
lm.comparison(
    "Wald-Rubin", ["Symmetric CI", "May undercover", "Simple to compute"],
    "Score Test", ["Asymmetric CI", "Better coverage", "Requires score derivation"]
)
lm.slide_num(6, total)

# ── Slide 7: Flow diagram ──
s = add_slide(prs, layout)
lm = Layout(s)
lm.h3("1.5 Analysis Workflow")
lm.flow(["Collect Data", "Apply MI (m=20)", "Pool Estimates", "Score Test"])
lm.slide_num(7, total)

# ── Slide 8: Summary ──
s = add_slide(prs, layout)
lm = Layout(s)
lm.section("Summary")
lm.bullets([
    "Score method provides better small-sample coverage",
    "Rubin's variance decomposition is the foundation",
    "Simulation confirms robustness under MAR",
    "Recommended for regulatory submissions"
])
lm.slide_num(8, total)

prs.save("output.pptx")
```

---

## HTML Path

Generate a single HTML file using these CSS classes from `references/html_template.html`:

- `.slide` — each slide container
- `.formula` — formula box (green bg + left bar)
- `.callout-key` / `.callout-warn` — info/warning callout
- `.cols` > `.col` — two-column layout
- `.compare` > `.compare-negative` + `.compare-positive` — comparison boxes
- `.flow` > `.flow-box` + `.flow-arrow` — flow diagram
- `<table>` with `<th>` — auto-styled green header tables
- `<pre><code>` — code blocks
- `.slide-num` — bottom-right page number

No external dependencies. Open in browser, Ctrl+P to print/export PDF.

---

## MD Parsing Rules

### Headings
- `# Title` → Title slide
- `## Section` → Section divider slide
- `### Sub` → H3 sub-heading within a content slide

### Formulas
- `$...$` or `$$...$$` → Formula box
- Rendering: Use Unicode math symbols (α β γ ± × ≤ ≥ ≠ Σ √ ∞ → ² ³ ₁ ₂)
- Fallback: For complex LaTeX, display source verbatim

### Tables
- Markdown pipe tables → `add_table()`
- First row is header

### Code Blocks
- Fenced ``` → `add_code()`

### Blockquotes
- `>` → `add_callout()`
- Contains "注意"/"警告"/"Warning" → `warn=True`

### Lists
- `- item` / `* item` → `add_bullet_list()`
- `1. item` → numbered list

---

## Slide Splitting Rules

1. `# Title` → Title slide (first slide, include 3-5 objectives)
2. `## Section` → Section divider with green underline
3. `### Sub + content` → Content slide
   - Max 6 bullet points per slide (split if more)
   - Max 3 formula boxes per slide (split if more)
   - 1 table per slide
   - Max 2 code blocks per slide
4. `>` blockquote → Callout at bottom of current slide
5. Overflow → Continue with `###` headings, add "（续）" to title

Slide ordering: Title → Background → Core Content (section + 2-4 slides each) → Comparison → Takeaways → Summary

Typical range: 12-25 slides for 20-40 minute talk.

---

## Anti-Patterns

- One sentence per slide
- Decorative elements (clip art, stock photos)
- Animations or transitions
- Dark backgrounds
- More than 3 font families
- Untagged callouts or headerless tables
