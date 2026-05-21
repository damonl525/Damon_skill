# MD to PPTX/HTML Presentation

将结构化 Markdown 文档转换为专业演示文稿（HTML 或 PPTX）。专为技术/统计内容设计，支持公式、表格、代码块和提示框。

## 特点

- **双输出格式**: HTML（零依赖）或 PPTX（python-pptx）
- **自动布局**: `Layout` 类自动追踪 Y 游标，无需手动指定坐标
- **技术内容优化**: 公式框、代码块、对比表格、警告提示框、流程图
- **统一视觉风格**: 微软雅黑 + 绿色主题 (#2D6A4F)
- **信息密度**: 每页包含充足的公式、表格和文字，适合方法论讲解

## 快速使用

### 在 Claude Code 中

```
# 在你的 MD 文件所在目录，直接说：
"用 md-to-pptx skill 把这个 MD 转成 PPT"
```

Claude 会：
1. 读取你的 MD 文件
2. 解析结构（标题、公式、表格、代码块、引用）
3. 生成 `gen_pptx.py` 脚本
4. 运行脚本生成 `.pptx` 文件

### 手动使用

```python
from references.pptx_helpers import *

prs, layout = create_presentation()
total = 3

s = add_slide(prs, layout)
lm = Layout(s)
lm.title("Presentation Title")
lm.subtitle("Subtitle text here")
lm.bullets(["Objective 1", "Objective 2", "Objective 3"])
lm.slide_num(1, total)

prs.save("output.pptx")
```

运行: `pip install python-pptx && python gen_pptx.py`

## Layout 自动布局（推荐）

`Layout(slide)` 类追踪 Y 游标，自动估算每个元素的高度并定位：

```python
lm = Layout(s)
lm.title("Title")              # 大标题
lm.section("1. Background")    # 章节标题 + 绿色下划线
lm.h3("1.1 Sub-heading")       # H3 子标题
lm.bullets(["a", "b", "c"])    # 项目列表（自动估算高度）
lm.formula("Z = d / sqrt(V)")  # 公式框
lm.code("x <- rnorm(100)")     # 代码块
lm.callout("Note", "Details")  # 提示框（info 或 warning）
lm.table(headers, rows)        # 数据表
lm.comparison("Bad", [...], "Good", [...])  # 红绿对比
lm.flow(["Step 1", "Step 2", "Step 3"])     # 流程图
lm.slide_num(1, total)         # 页码（不移动游标）
```

### 双栏组合方法

| 方法 | 布局 |
|------|------|
| `two_col_bullets(lt, li, rt, ri)` | 左右两栏：标题 + 列表 |
| `two_col_table_code(th, tr, code)` | 左栏表格 + 右栏代码 |
| `two_col_bullets_table(bt, bi, th, tr)` | 左栏列表 + 右栏表格 |

## 支持的 Markdown 元素

| MD 语法 | PPT 元素 | 说明 |
|----------|----------|------|
| `# Title` | 标题页 | 大标题 + 副标题 |
| `## Section` | 章节分隔页 | 绿色下划线 |
| `### Sub` | 子标题 | H3 级别 |
| `$...$` / `$$...$$` | 公式框 | 绿色背景 + Consolas |
| `> quote` | 提示框 | 绿色(info)或红色(warning) |
| `` ```code``` `` | 代码块 | 灰色背景 + Consolas |
| `\| table \|` | 数据表 | 绿色表头 + 斑马纹 |
| `- item` / `1. item` | 列表 | 项目符号 / 编号 |

## 视觉风格

```
主字体:    微软雅黑
代码字体:  Consolas
主色调:    #2D6A4F (深绿)
辅助色:    #40916C (中绿)
背景色:    #D8F3DC (浅绿)
警告色:    #D00000 (红)
```

## 依赖

### PPTX 输出
```bash
pip install python-pptx
```

### HTML 输出
无外部依赖，直接在浏览器中打开 HTML 文件。

## 文件结构

```
md-to-pptx/
├── SKILL.md                    # 技能主文件（Claude 读取）
├── README.md                   # 本文件
├── example.md                  # 示例 MD 输入
└── references/
    ├── pptx_helpers.py         # PPTX helper 函数 + Layout 类
    └── html_template.html      # HTML 模板
```

## 版本历史

- **v1.2** (2026-05-21): Layout 自动布局类、add_h3()、双栏组合方法、_emu int 启发式修复
- **v1.1** (2026-05-18): 修复 `_emu()` 参数单位 bug
- **v1.0** (2026-05-14): 初始版本，支持 PPTX + HTML 双输出
