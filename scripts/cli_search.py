#!/usr/bin/env python3
"""
cli_search.py - 命令行快捷搜索脚本
用法: python cli_search.py "Vitamin D|维生素D" "Zinc|锌" [--max-papers 30] [--min-year 2010]
"""

from __future__ import annotations

import argparse
import json
import sys
import os

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.data_models import Nutrient, SearchResult
from src.pubmed_client import PubMedClient
from src.search_strategies import SearchConfig, search_nutrient
from src.ai_extractor import create_extractor
from src.rule_extractor import classify_publication


def parse_nutrients(args: list[str]) -> list[Nutrient]:
    """解析命令行营养素参数，格式: '英文名|中文名' 或 '英文名'"""
    nutrients = []
    for arg in args:
        parts = arg.split("|")
        name = parts[0].strip()
        name_cn = parts[1].strip() if len(parts) > 1 else ""
        nutrients.append(Nutrient(name=name, name_cn=name_cn))
    return nutrients


def main():
    parser = argparse.ArgumentParser(description="PubMed 营养素文献搜索")
    parser.add_argument("nutrients", nargs="+", help='营养素列表，格式: "Vitamin D|维生素D"')
    parser.add_argument("--max-papers", type=int, default=30, help="每营养素最大文献数 (默认30)")
    parser.add_argument("--min-year", type=int, default=2010, help="最早发表年份 (默认2010)")
    parser.add_argument("--api-key", type=str, default="", help="AI API Key (留空用规则引擎)")
    parser.add_argument("--output", type=str, default="", help="输出 JSON 文件路径 (留空则打印)")
    args = parser.parse_args()

    nutrients = parse_nutrients(args.nutrients)
    print(f"🔍 搜索 {len(nutrients)} 种营养素: {', '.join(n.name for n in nutrients)}")

    client = PubMedClient(min_year=args.min_year)
    search_cfg = SearchConfig(total_max=args.max_papers)
    extractor = create_extractor(
        api_key=args.api_key or None,
        enabled=True,
    )

    all_results = []
    for i, nutrient in enumerate(nutrients, 1):
        print(f"\n🌿 [{i}/{len(nutrients)}] 搜索: {nutrient.name}")
        try:
            result = search_nutrient(nutrient, client, search_cfg)
            if result.publications:
                print(f"   获取 {len(result.publications)} 篇文献，开始提取结论...")
                extractor.extract_batch(result.publications)
            all_results.append(result)
            print(f"   ✅ 完成: {result.paper_count} 篇")
        except Exception as e:
            print(f"   ❌ 失败: {e}")
            all_results.append(SearchResult(nutrient=nutrient, publications=[], errors=[str(e)]))

    # 输出结果
    output_data = []
    for r in all_results:
        nutrient_info = {
            "nutrient": r.nutrient.name,
            "nutrient_cn": r.nutrient.name_cn,
            "paper_count": r.paper_count,
            "publications": [],
            "errors": r.errors,
        }
        for pub in r.publications:
            pub_info = {
                "pmid": pub.pmid,
                "title": pub.title,
                "year": pub.year,
                "journal": pub.journal,
                "study_type": pub.study_type.value if pub.study_type else "",
                "evidence_level": pub.evidence_level,
                "evidence_grade": pub.evidence_grade,
                "evidence_description": pub.evidence_description,
                "ai_conclusion": pub.ai_conclusion,
                "ai_effects": pub.ai_effects,
            }
            nutrient_info["publications"].append(pub_info)
        output_data.append(nutrient_info)

    result_json = json.dumps(output_data, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result_json)
        print(f"\n📄 结果已保存到: {args.output}")
    else:
        print(f"\n{'='*60}")
        print(result_json)

    # 统计
    total_papers = sum(r["paper_count"] for r in output_data)
    print(f"\n✅ 搜索完成！共 {len(nutrients)} 种营养素，{total_papers} 篇文献")


if __name__ == "__main__":
    main()
