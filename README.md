# PDF Batch Extractor Skill

## 简介

这是一个用于批量提取PDF文件内容为Markdown格式的技能。它使用`opendataloader_pdf`库，能够高效地处理多个PDF文件，并保留文档的结构、表格和图片。

## 主要功能

- ✅ 批量处理多个PDF文件
- ✅ 转换为Markdown格式
- ✅ 保留文档结构（标题、段落、列表）
- ✅ 提取表格并保持格式
- ✅ 提取图片并单独保存
- ✅ 支持中英文文档
- ✅ 自动生成输出目录

## 快速开始

### 1. 安装依赖

```bash
pip install opendataloader_pdf
```

### 2. 准备PDF文件

将所有要处理的PDF文件放在一个目录中。

### 3. 运行提取脚本

```bash
python extract_pdfs_example.py
```

或者使用自定义脚本：

```python
import opendataloader_pdf
import os

# 定义PDF文件列表
pdf_files = ["file1.pdf", "file2.pdf", "file3.pdf"]

# 创建输出目录
output_dir = "extracted_markdown"
os.makedirs(output_dir, exist_ok=True)

# 批量处理
for pdf_file in pdf_files:
    opendataloader_pdf.convert(
        input_path=[pdf_file],
        output_dir=output_dir,
        format="markdown"
    )
```

## 输出结构

```
extracted_markdown/
├── document1.md                    # 提取的Markdown文件
├── document1_images/               # 提取的图片目录
│   ├── imageFile1.png
│   └── imageFile2.png
├── document2.md
└── document2_images/
    └── ...
```

## 使用场景

### 1. 临床试验文档整理

```python
# 提取多个临床试验相关PDF
pdf_files = [
    "protocol.pdf",
    "statistical_analysis_plan.pdf",
    "clinical_study_report.pdf"
]
```

### 2. 学术文献批量处理

```python
# 使用glob模式获取所有PDF
import glob
pdf_files = glob.glob("papers/*.pdf")
```

### 3. 报告归档

```python
# 按日期组织输出
from datetime import datetime
output_dir = f"reports_{datetime.now().strftime('%Y%m%d')}"
```

## 高级功能

### 错误处理

```python
for pdf_file in pdf_files:
    try:
        opendataloader_pdf.convert(...)
        print(f"成功: {pdf_file}")
    except Exception as e:
        print(f"失败: {pdf_file} - {str(e)}")
```

### 日志记录

```python
import logging

logging.basicConfig(filename='extraction.log', level=logging.INFO)
logging.info(f"开始处理: {pdf_file}")
```

## 注意事项

1. **Java环境**: 需要安装Java Runtime Environment (JRE)
2. **文件大小**: 大文件可能需要更多处理时间和内存
3. **文件格式**: 支持原生PDF和扫描PDF（扫描PDF可能需要OCR）
4. **编码问题**: 确保Python使用UTF-8编码

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| Java未找到 | 安装JRE并确保在PATH中 |
| 内存不足 | 分批处理文件 |
| 文件损坏 | 跳过或修复文件 |
| 权限错误 | 检查文件/目录权限 |

## 相关技能

- **PDF OCR Extraction**: 用于扫描文档的OCR提取
- **Document Analysis**: 用于分析提取的内容
- **Data Processing**: 用于结构化提取的数据

## 更新日志

### v1.0 (2026-04-30)
- 初始发布
- 支持批量PDF提取
- 支持Markdown格式输出
- 支持图片提取

## 许可证

MIT License
