import importlib.util
import subprocess
import sys
import os

# 检查是否安装了 opendataloader_pdf
if importlib.util.find_spec("opendataloader_pdf") is None:
    print("opendataloader_pdf not installed，installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "opendataloader_pdf"])
    print("安装完成！")

# 现在可以安全地导入 opendataloader_pdf
import opendataloader_pdf

# 定义要处理的PDF文件
pdf_files = [
    "Prot_000 (1).pdf",
    "SAP_001.pdf",
    "213793Orig1s000StatR.pdf"
]

# 创建输出目录
output_dir = "extracted_markdown"
os.makedirs(output_dir, exist_ok=True)

# 批量处理所有PDF文件
print(f"开始处理 {len(pdf_files)} 个PDF文件...")
for i, pdf_file in enumerate(pdf_files, 1):
    print(f"[{i}/{len(pdf_files)}] 处理: {pdf_file}")
    try:
        # 使用opendataloader_pdf转换
        opendataloader_pdf.convert(
            input_path=[pdf_file],
            output_dir=output_dir,
            format="markdown"
        )
        print(f"  [完成] {pdf_file}")
    except Exception as e:
        print(f"  [失败] {pdf_file} - 错误: {str(e)}")

print(f"\n处理完成！Markdown文件已保存到: {output_dir}")

# 列出生成的文件
if os.path.exists(output_dir):
    files = os.listdir(output_dir)
    if files:
        print("\n生成的Markdown文件:")
        for file in files:
            print(f"  - {file}")
    else:
        print("\n警告：没有生成任何Markdown文件。")
else:
    print(f"\n错误：输出目录 {output_dir} 不存在。")