from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
from typing import Any

FAMILY_HINTS = [
    "横向小提琴图",
    "横向箱线图",
    "横向柱状图",
    "环形柱状图",
    "小提琴图",
    "箱线图",
    "云雨图",
    "柱状图",
    "折线图",
    "热图",
    "散点图",
    "气泡图",
    "饼图",
    "桑基图",
    "网络图",
    "大头针图",
    "地图",
    "雷达图",
    "火山图",
    "甘特图",
    "流程图",
    "旭日图",
]


def resolve_chart_family(record: dict[str, Any]) -> str:
    def canonical_family(text: str) -> str:
        for family in FAMILY_HINTS:
            if family in text:
                return family
        return ""

    name = str(record.get("name", ""))
    category_trail = record.get("category_trail", []) or []
    source_family = str(record.get("chart_family", ""))
    leading = name.split("-")[0].strip()
    votes: dict[str, int] = defaultdict(int)

    for text, weight in (
        (source_family, 4),
        (" ".join(str(item) for item in category_trail), 3),
        (leading, 2),
        (name, 1),
    ):
        family = canonical_family(text)
        if family:
            votes[family] += weight

    if votes:
        return max(votes.items(), key=lambda item: (item[1], len(item[0])))[0]
    return source_family


def load_records(jsonl_path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with jsonl_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def make_text(record: dict[str, Any]) -> str:
    resolved_family = resolve_chart_family(record)
    source_family = record.get("chart_family", "")
    required_columns = "；".join(
        f"{column['column_name']}（{column['semantic']}）" for column in record.get("required_columns", [])
    ) or "无明确字段约束"
    data_patterns = "、".join(record.get("data_shape", {}).get("data_patterns", [])) or "模板特定"
    features = "、".join(record.get("visual_features", [])) or "标准模板样式"
    styles = "、".join(record.get("style_tags", [])) or "无"
    goals = "、".join(record.get("analysis_goal", [])) or "科研绘图"
    use_cases = "；".join(record.get("use_cases", [])) or "适合作为科研绘图模板"
    avoid_cases = "；".join(record.get("avoid_cases", [])) or "使用前需检查数据是否匹配"
    available_columns = "、".join(record.get("data_shape", {}).get("available_columns", [])) or "未提供示例列名"
    subtype = "、".join(record.get("subtype", [])) or "基础模板"

    return (
        f"模板ID：{record['id']}。\n"
        f"模板名称：{record['name']}。\n"
        f"图形家族：{resolved_family}。\n"
        f"来源图形家族：{source_family}。\n"
        f"子类型：{subtype}。\n"
        f"分析目标：{goals}。\n"
        f"视觉特征：{features}。\n"
        f"风格标签：{styles}。\n"
        f"复杂度：{record.get('complexity', 'unknown')}。\n"
        f"数据表数量：{record.get('data_shape', {}).get('table_count', 0)}。\n"
        f"数据模式：{data_patterns}。\n"
        f"必需字段：{required_columns}。\n"
        f"示例数据列：{available_columns}。\n"
        f"适用场景：{use_cases}。\n"
        f"不适用场景：{avoid_cases}。\n"
        f"推荐摘要：{record.get('selection_summary', '')}"
    )


def build_embedding_record(record: dict[str, Any]) -> dict[str, Any]:
    resolved_family = resolve_chart_family(record)
    filters = {
        "chart_family": resolved_family,
        "source_chart_family": record.get("chart_family"),
        "complexity": record.get("complexity"),
        "table_count": record.get("data_shape", {}).get("table_count"),
        "supports_grouping": record.get("data_shape", {}).get("supports_grouping"),
        "supports_matrix": record.get("data_shape", {}).get("supports_matrix"),
        "supports_hierarchy": record.get("data_shape", {}).get("supports_hierarchy"),
        "supports_geo": record.get("data_shape", {}).get("supports_geo"),
        "supports_multiple_series": record.get("data_shape", {}).get("supports_multiple_series"),
        "has_python": record.get("has_python"),
        "has_r": record.get("has_r"),
        "analysis_goal": record.get("analysis_goal", []),
        "visual_features": record.get("visual_features", []),
        "style_tags": record.get("style_tags", []),
    }

    return {
        "id": record["id"],
        "text": make_text(record),
        "metadata": {
            "name": record.get("name"),
            "chart_family": resolved_family,
            "source_chart_family": record.get("chart_family"),
            "subtype": record.get("subtype", []),
            "filters": filters,
            "paths": {
                "preview_path": record.get("preview_path"),
                "svg_path": record.get("svg_path"),
                "python_path": record.get("python_path"),
                "r_path": record.get("r_path"),
                "meta_path": record.get("meta_path"),
                "local_dir": record.get("local_dir"),
                "data_paths": record.get("data_paths", []),
            },
            "selection_summary": record.get("selection_summary", ""),
            "search_text": record.get("search_text", ""),
        },
    }


def discover_root_dir(provided: str | None) -> Path:
    if provided:
        candidate = Path(provided).resolve()
        if candidate.is_file():
            if candidate.name != "catalog_enriched.jsonl":
                raise SystemExit(f"Expected catalog_enriched.jsonl, got: {candidate}")
            return candidate.parent
        if (candidate / "catalog_enriched.jsonl").exists():
            return candidate
        raise SystemExit(f"catalog_enriched.jsonl not found under: {candidate}")

    script_dir = Path(__file__).resolve().parent
    bundled_dir = script_dir.parent / "assets" / "bioinforw_ngplot_dump"

    direct_candidates = [
        Path.cwd() / "bioinforw_ngplot_dump",
        Path.cwd(),
        bundled_dir,
    ]
    for candidate in direct_candidates:
        if (candidate / "catalog_enriched.jsonl").exists():
            return candidate.resolve()

    for found in Path.cwd().rglob("catalog_enriched.jsonl"):
        return found.resolve().parent

    raise SystemExit("Could not find catalog_enriched.jsonl. Pass the dump root path or the catalog file path.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build embedding_input.jsonl from catalog_enriched.jsonl.")
    parser.add_argument("root_dir", nargs="?", help="Dump root directory or direct catalog_enriched.jsonl path")
    args = parser.parse_args()

    root_dir = discover_root_dir(args.root_dir)
    input_path = root_dir / "catalog_enriched.jsonl"
    output_path = root_dir / "embedding_input.jsonl"

    records = load_records(input_path)
    with output_path.open("w", encoding="utf-8") as fh:
        for record in records:
            embedding_record = build_embedding_record(record)
            fh.write(json.dumps(embedding_record, ensure_ascii=False) + "\n")

    print(
        json.dumps(
            {
                "root_dir": str(root_dir),
                "input": str(input_path),
                "output": str(output_path),
                "total_records": len(records),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
