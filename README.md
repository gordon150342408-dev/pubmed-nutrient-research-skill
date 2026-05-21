# PubMed 营养素文献搜索与证据提取 Skill

[![Skill](https://img.shields.io/badge/WorkBuddy-Skill-green)](https://www.codebuddy.cn)
[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> 🔬 WorkBuddy Skill：搜索 PubMed 数据库，提取营养素功效结论、Oxford CEBM 证据等级、GRADE 质量评分，支持多种营养素输入方式。

---

## ✨ 功能特性

### 📊 证据评级系统

| 证据等级 | 研究类型 | GRADE 质量 |
|---------|---------|-----------|
| Level 1 | 荟萃分析 / 系统综述 | 🟢 High |
| Level 2 | RCT / 临床试验 | 🟢 High |
| Level 3 | 队列研究 | 🔵 Moderate |
| Level 4 | 病例对照 / 横断面 | 🟡 Low |
| Level 5 | 叙述性综述 / 其他 | 🔴 Very Low |

### 🤖 双模式提取

- **规则引擎模式**（默认，无需 API Key）：基于关键词匹配，零成本
- **AI 模型模式**（需 API Key）：LLM 精准提取，中文结论输出

### 📥 多格式营养素输入

- ✏️ 手动输入（每行一个，格式：英文名|中文名）
- 📊 Excel / CSV 上传
- 📄 PDF 解析（pdfplumber）
- 🖼️ 图片 OCR 识别（easyocr）

### 📤 导出功能

- Excel 报告（含证据等级、GRADE 评分、中文结论）
- Word 文档报告

---

## 🚀 安装

### 方式一：拖入安装

将本 Skill 文件夹直接拖入 CodeBuddy / WorkBuddy 窗口。

### 方式二：手动放置

```bash
# 用户级（全局可用）
cp -r pubmed-nutrient-research ~/.workbuddy/skills/

# 项目级（仅当前项目）
cp -r pubmed-nutrient-research .workbuddy/skills/
```

### 方式三：技能市场

在 WorkBuddy 左侧「技能市场」搜索 `pubmed-nutrient-research` 一键安装。

---

## 📖 使用方法

### 自动触发

直接在对话中描述需求，AI 自动匹配：

> 帮我搜索维生素D的文献证据

### 手动调用

```
使用 pubmed-nutrient-research 技能搜索 Vitamin D
```

### @ 调用

```
@pubmed-nutrient-research 搜索锌和镁的营养功效
```

### 命令行直接搜索

```bash
cd /path/to/pubmed-nutrient-research
python scripts/cli_search.py "Vitamin D|维生素D" "Zinc|锌" --max-papers 30
```

---

## 📁 Skill 结构

```
pubmed-nutrient-research/
├── SKILL.md                    # 核心配置（触发条件 + 工作流程）
├── README.md                   # 本文件
├── scripts/
│   └── cli_search.py           # 命令行快捷搜索脚本
└── references/
    └── architecture.md         # 项目架构参考
```

### 关联项目

本 Skill 驱动的 Streamlit 应用位于：
`/Users/gordon/WorkBuddy/20260411204142/pubmed-nutrient-research/`

---

## 🔧 依赖

运行 Streamlit Web 应用需安装以下依赖：

```bash
pip install -r /path/to/pubmed-nutrient-research/requirements.txt
```

核心依赖：streamlit, biopython, openai, openpyxl, python-docx, pdfplumber, easyocr, pandas

---

## ⚠️ 注意事项

1. 首次使用 easyocr OCR 功能时会自动下载模型（约 100MB）
2. PubMed API 有速率限制（无 Key: 3 req/s，有 Key: 10 req/s）
3. 建议每次搜索不超过 10 种营养素
4. 规则引擎模式零成本，AI 模式需 API Key

---

## 📄 License

MIT License
