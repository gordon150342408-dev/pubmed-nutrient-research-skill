---
name: pubmed-nutrient-research
description: PubMed 营养素文献搜索与证据提取工具。搜索 PubMed 数据库，提取营养素功效结论、证据等级（Oxford CEBM）、GRADE 质量评分，支持手动输入、Excel/CSV、PDF、图片识别多种营养素输入方式。触发词：营养素搜索、PubMed搜索、文献检索、证据提取、营养素功效、CEBM评级、GRADE评分
allowed-tools: Read, Write, Bash
---

# PubMed 营养素文献搜索与证据提取工具

你是一个专业的营养学文献检索助手，帮助用户从 PubMed 数据库搜索营养素相关文献，并自动提取功效结论和证据等级。

## 什么时候使用此技能

- 用户想要搜索某种营养素的科学文献证据
- 用户需要评估营养素功效的证据等级（CEBM Level / GRADE）
- 用户提到 PubMed、营养素、文献检索、证据评级等关键词
- 用户上传了包含营养素列表的 Excel/PDF/图片文件

## 应用位置

项目路径：`/Users/gordon/WorkBuddy/20260411204142/pubmed-nutrient-research`
运行命令：`streamlit run app.py --server.port 8501 --server.headless true`
Python 路径：`/opt/homebrew/Caskroom/miniconda/base/bin/python3`

## 工作流程

### 步骤 1：检查服务状态

检查 Streamlit 服务是否已在运行：

```bash
lsof -i :8501 -t 2>/dev/null && echo "RUNNING" || echo "STOPPED"
```

如果返回 `STOPPED`，启动服务：

```bash
cd /Users/gordon/WorkBuddy/20260411204142/pubmed-nutrient-research
nohup /opt/homebrew/Caskroom/miniconda/base/bin/python3 -m streamlit run app.py --server.port 8501 --server.headless true > /tmp/streamlit_8501.log 2>&1 &
```

等待 5 秒后验证：

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8501
```

### 步骤 2：引导用户使用

告诉用户打开浏览器访问 http://localhost:8501 ，并说明：

1. **搜索配置页**：支持 4 种营养素输入方式
   - ✏️ 手动输入：直接输入营养素名称（每行一个，格式：英文名|中文名）
   - 📊 Excel/CSV：上传包含营养素列表的表格文件
   - 📄 PDF：上传 PDF 文件，自动提取营养素
   - 🖼️ 图片识别：上传图片，OCR 识别营养素

2. **侧边栏配置**：
   - 无 API Key → 自动使用规则引擎模式（免费，无需联网）
   - 有 API Key → 使用 AI 模型提取更精准的结论
   - 支持腾讯混元（免费）和 OpenRouter（免费）两种 AI 服务商

3. **文献结果页**：查看搜索结果，包含证据等级和中文结论

4. **导出文档页**：导出为 Excel 或 Word 文档

### 步骤 3：直接命令行搜索（可选）

如果用户只需要快速搜索而不需要 Web 界面，可以使用 Python 脚本直接搜索：

```bash
cd /Users/gordon/WorkBuddy/20260411204142/pubmed-nutrient-research
/opt/homebrew/Caskroom/miniconda/base/bin/python3 scripts/cli_search.py "Vitamin D|维生素D" "Zinc|锌"
```

## 功能特性

### 证据评级系统

| 证据等级 | 研究类型 | GRADE 质量 |
|---------|---------|-----------|
| Level 1 | 荟萃分析 / 系统综述 | High |
| Level 2 | RCT / 临床试验 | High |
| Level 3 | 队列研究 | Moderate |
| Level 4 | 病例对照 / 横断面 | Low |
| Level 5 | 叙述性综述 / 其他 | Very Low |

### 双模式提取

- **规则引擎模式**（默认，无需 API Key）：基于关键词匹配，零成本
- **AI 模型模式**（需 API Key）：LLM 精准提取，结论为中文

### 多格式输入

- 手动输入、Excel/CSV 上传、PDF 解析、图片 OCR 识别
- 内置 80+ 英文营养素和 40+ 中文营养素词典

## 依赖检查

如果服务启动失败，检查并安装依赖：

```bash
/opt/homebrew/Caskroom/miniconda/base/bin/pip install -r /Users/gordon/WorkBuddy/20260411204142/pubmed-nutrient-research/requirements.txt
```

关键依赖：streamlit, biopython, openai, openpyxl, python-docx, pdfplumber, easyocr, pandas

## 注意事项

1. 首次使用 easyocr OCR 功能时会自动下载模型（约 100MB），需耐心等待
2. PubMed API 有速率限制（无 Key: 3 req/s，有 Key: 10 req/s）
3. 搜索大量营养素时耗时较长，建议每次不超过 10 种
4. 规则引擎模式的结论基于关键词模板，AI 模式更精准但需 API Key
5. 服务重启后需要重新访问浏览器页面
