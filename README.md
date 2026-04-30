# Damon_skill

个人技能集合，包含各种实用的工具和自动化脚本。

## 技能列表

| 技能名称 | 描述 | 用途 |
|----------|------|------|
| [PDF Batch Extractor](./pdf-batch-extractor/) | 批量提取PDF文件为Markdown格式 | 文档处理、内容提取 |

## 使用方法

### 克隆仓库

```bash
git clone https://github.com/damonl525/Damon_skill.git
```

### 使用特定技能

进入对应的技能目录，查看其README.md文件了解具体使用方法。

```bash
cd Damon_skill/pdf-batch-extractor
# 查看使用说明
cat README.md
```

## 技能结构

每个技能都包含在一个独立的文件夹中，通常包括：

- `SKILL.md` - 技能的主要描述文件
- `README.md` - 使用说明文档
- `*.py` / `*.sh` - 可执行脚本
- `examples/` - 示例文件（如果有）

## 添加新技能

1. 在仓库根目录创建新的文件夹
2. 将技能文件放入该文件夹
3. 更新根目录的README.md，添加新技能到列表
4. 提交并推送更改

```bash
git add .
git commit -m "Add new skill: [技能名称]"
git push
```

## 许可证

MIT License
