# PubMed 营养素研究工具 - 项目架构参考

## 项目文件结构

```
pubmed-nutrient-research/
├── app.py                      # Streamlit 主入口
├── config.py                   # 全局配置
├── requirements.txt            # Python 依赖
├── nutrients.csv               # 营养素词典
├── src/
│   ├── data_models.py          # 数据模型（Nutrient, Publication, SearchResult, StudyType）
│   ├── pubmed_client.py        # PubMed/NCBI Entrez API 客户端
│   ├── search_strategies.py    # 搜索策略（search_nutrient, search_nutrients_batch）
│   ├── ai_extractor.py         # AI 结论提取器 + RuleExtractorAdapter 适配器
│   ├── rule_extractor.py       # 规则引擎提取器（无需 API Key 的备选方案）
│   └── document_generator.py   # Excel/Word 文档生成器
├── components/
│   ├── input_panel.py          # 营养素输入面板（4种输入方式）
│   ├── results_table.py        # 搜索结果展示（含证据等级、GRADE评分）
│   └── export_panel.py         # 导出面板
└── utils/
    └── document_parser.py      # PDF/图片解析，营养素文本提取
```

## 核心数据流

1. 用户输入营养素 → Nutrient 对象列表
2. PubMedClient 调用 NCBI Entrez API 搜索 → Publication 列表
3. AI/规则提取器处理 Publication → 填充 evidence_level/grade/description/ai_conclusion
4. 展示结果 / 导出文档

## 关键数据模型

```python
class StudyType(str, Enum):
    META_ANALYSIS = "Meta-Analysis"
    SYSTEMATIC_REVIEW = "Systematic Review"
    RCT = "RCT"
    CLINICAL_TRIAL = "Clinical Trial"
    COHORT = "Cohort Study"
    CASE_CONTROL = "Case-Control Study"
    CROSS_SECTIONAL = "Cross-Sectional Study"
    REVIEW = "Review"
    OTHER = "Other"
```

## 双模式提取逻辑

- **AI 模式**（有 API Key）：`AIExtractor` → LLM 提取 → JSON 解析 → 填充字段
- **规则模式**（无 API Key）：`RuleExtractorAdapter` → `classify_publication()` → 关键词匹配 → CEBM/GRADE 映射

两种模式接口一致：`extract_one(publication)` / `extract_batch(publications)`

## 运行环境

- Python 3.9+
- Streamlit 1.32
- 关键依赖：biopython, openai, openpyxl, pdfplumber, easyocr, pandas
