# MD to PPTX/HTML Presentation

将结构化 Markdown 文档转换为专业演示文稿（HTML 或 PPTX）。专为技术/统计内容设计，支持公式、表格、代码块和提示框。

## 特点

- **双输出格式**: HTML（零依赖）或 PPTX（python-pptx）
- **技术内容优化**: 公式框、代码块、对比表格、警告提示框
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

1. 查看 `references/pptx_helpers.py` 获取所有 helper 函数
2. 基于模板创建你的 `gen_pptx.py`
3. 运行 `pip install python-pptx && python gen_pptx.py`

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

## 输出示例

参考 `Proposed_Score_Method_PPT.pptx` 的 24 页演示文稿，包含：
- 公式框（Cardano 公式、Z 统计量）
- 对比表格（四种 CI 方法）
- 代码块（R 和 SAS 代码片段）
- 警告提示框（边界场景、SAS missing 值陷阱）
- 流程图（MI → Score → Rubin → CI）
- 行业分析（FDA 监管现状、MOVER 竞争方法）

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
└── references/
    └── pptx_helpers.py         # PPTX helper 函数模板
```

## 版本历史

- **v1.1** (2026-05-18): 修复 `_emu()` 参数单位 bug — 所有 position/size 参数自动转为 Inches()
- **v1.0** (2026-05-14): 初始版本，支持 PPTX + HTML 双输出
