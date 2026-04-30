---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: PDF Batch Extractor
description: "Batch extract PDF files to markdown format using opendataloader_pdf"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: pdf
tags:
  - pdf
  - markdown
  - batch-processing
  - text-extraction
  - document-conversion
department: All

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
  - batch_pdf_extraction
  - markdown_conversion
  - document_structuring

# Language Support
languages:
  - en
  - zh
---

# PDF Batch Extractor

Batch extract multiple PDF files to markdown format using opendataloader_pdf library.

## Overview

This skill helps you:
- Batch convert multiple PDF files to markdown format
- Preserve document structure including tables and images
- Extract text from both native and scanned PDFs
- Organize extracted content in a structured directory
- Process large numbers of documents efficiently

## Prerequisites

### Required Python Package

The skill uses `opendataloader_pdf` for PDF extraction. The script will automatically install it if not present.

```bash
pip install opendataloader_pdf
```

### System Requirements

- Python 3.7+
- Java Runtime Environment (JRE) - required by opendataloader_pdf
- Sufficient disk space for output files

## How to Use

### Basic Usage

1. **Prepare your PDF files**: Place all PDF files in a single directory

2. **Create extraction script**: Use the provided Python script template

3. **Run the extraction**: Execute the script to batch convert PDFs

### Script Template

```python
import importlib.util
import subprocess
import sys
import os

# Check and install opendataloader_pdf
if importlib.util.find_spec("opendataloader_pdf") is None:
    print("opendataloader_pdf not installed, installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "opendataloader_pdf"])
    print("Installation complete!")

import opendataloader_pdf

# Define PDF files to process
pdf_files = [
    "document1.pdf",
    "document2.pdf",
    "document3.pdf"
]

# Create output directory
output_dir = "extracted_markdown"
os.makedirs(output_dir, exist_ok=True)

# Batch process all PDF files
print(f"Starting to process {len(pdf_files)} PDF files...")
for i, pdf_file in enumerate(pdf_files, 1):
    print(f"[{i}/{len(pdf_files)}] Processing: {pdf_file}")
    try:
        opendataloader_pdf.convert(
            input_path=[pdf_file],
            output_dir=output_dir,
            format="markdown"
        )
        print(f"  [Completed] {pdf_file}")
    except Exception as e:
        print(f"  [Failed] {pdf_file} - Error: {str(e)}")

print(f"\nProcessing complete! Markdown files saved to: {output_dir}")
```

### Using Glob Pattern for Multiple Files

```python
import glob

# Find all PDF files in current directory
pdf_files = glob.glob("*.pdf")

# Or find PDFs in subdirectories
pdf_files = glob.glob("**/*.pdf", recursive=True)
```

## Output Structure

### Directory Layout

```
extracted_markdown/
├── document1.md
├── document1_images/
│   ├── imageFile1.png
│   ├── imageFile2.png
│   └── ...
├── document2.md
├── document2_images/
│   └── ...
└── document3.md
```

### Markdown Output Format

The extracted markdown preserves:
- Document headings and structure
- Tables with proper formatting
- Lists (ordered and unordered)
- Images (saved separately and referenced)
- Text formatting (bold, italic, etc.)

## Example Output

```markdown
# Document Title

## Section 1

This is the content of section 1.

### Subsection 1.1

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |

## Section 2

- Item 1
- Item 2
- Item 3

![Image Description](document1_images/imageFile1.png)
```

## Advanced Usage

### Processing Files from Different Directories

```python
pdf_files = [
    "path/to/file1.pdf",
    "another/path/file2.pdf",
    "C:/absolute/path/file3.pdf"
]
```

### Custom Output Directory

```python
# Organize by date
from datetime import datetime
output_dir = f"extracted_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# Or by category
output_dir = "extracted_reports/clinical_trials"
```

### Error Handling and Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    file_handler=logging.FileHandler('extraction.log')
)

# Add to extraction loop
try:
    opendataloader_pdf.convert(...)
    logging.info(f"Successfully extracted: {pdf_file}")
except Exception as e:
    logging.error(f"Failed to extract {pdf_file}: {str(e)}")
```

## Command Line Usage

### Simple Batch Extraction Script

Save as `extract_pdfs.py`:

```python
#!/usr/bin/env python3
"""
PDF Batch Extractor - Convert multiple PDFs to markdown format
Usage: python extract_pdfs.py [directory_path]
"""

import importlib.util
import subprocess
import sys
import os
import glob

def install_package():
    """Install opendataloader_pdf if not present"""
    if importlib.util.find_spec("opendataloader_pdf") is None:
        print("Installing opendataloader_pdf...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "opendataloader_pdf"])
        print("Installation complete!")

def extract_pdfs(input_dir=".", output_dir="extracted_markdown"):
    """Extract all PDFs from input directory"""
    import opendataloader_pdf
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all PDF files
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return
    
    print(f"Found {len(pdf_files)} PDF files")
    
    # Process each file
    for i, pdf_file in enumerate(pdf_files, 1):
        filename = os.path.basename(pdf_file)
        print(f"[{i}/{len(pdf_files)}] Processing: {filename}")
        
        try:
            opendataloader_pdf.convert(
                input_path=[pdf_file],
                output_dir=output_dir,
                format="markdown"
            )
            print(f"  ✓ Completed")
        except Exception as e:
            print(f"  ✗ Failed: {str(e)}")
    
    print(f"\nDone! Files saved to: {output_dir}")

if __name__ == "__main__":
    install_package()
    
    # Get directory from command line argument or use current directory
    input_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    extract_pdfs(input_dir)
```

Run with:
```bash
python extract_pdfs.py
# Or specify a directory
python extract_pdfs.py /path/to/pdfs
```

## Best Practices

### 1. File Organization

- Group related PDFs in the same directory
- Use descriptive filenames
- Consider creating a backup before batch processing

### 2. Output Management

- Use timestamped output directories for multiple runs
- Review extracted markdown for accuracy
- Check that images are properly extracted

### 3. Error Handling

- Monitor the console output for failed extractions
- Check log files if available
- Retry failed files individually if needed

### 4. Performance

- Process files in batches for large collections
- Ensure sufficient disk space
- Close other applications to free up memory

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Java not found | Install JRE and ensure it's in PATH |
| Out of memory | Process files in smaller batches |
| Corrupted PDF | Skip or repair the file first |
| Permission error | Check file/directory permissions |
| Encoding issues | Ensure Python uses UTF-8 encoding |

### Error Messages

- **"opendataloader_pdf not installed"**: Run `pip install opendataloader_pdf`
- **"Java not found"**: Install Java Runtime Environment
- **"File not found"**: Check file path and permissions
- **"Unsupported format"**: File may be corrupted or password-protected

## Limitations

- Requires Java Runtime Environment
- Processing time depends on PDF size and complexity
- Some complex layouts may not convert perfectly
- Password-protected PDFs cannot be processed
- Very large PDFs may require significant memory

## Integration with Other Skills

This skill works well with:
- **PDF OCR Extraction**: For scanned documents requiring OCR
- **Document Analysis**: For analyzing extracted content
- **Data Processing**: For structuring extracted data

## Version History

- **v1.0** (2026-04-30): Initial release with batch processing capabilities
