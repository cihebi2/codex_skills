from __future__ import annotations

import argparse
from collections import defaultdict
import json
import re
from pathlib import Path
from typing import Any


TOKEN_SPLIT_RE = re.compile(r"[\s,;:(){}\[\]<>，。；：、/|]+")

FAMILY_HINTS = [
    "柱状图",
    "横向柱状图",
    "环形柱状图",
    "折线图",
    "热图",
    "箱线图",
    "小提琴图",
    "云雨图",
    "散点图",
    "气泡图",
    "饼图",
    "桑基图",
    "网络图",
    "地图",
    "大头针图",
    "雷达图",
    "火山图",
    "甘特图",
    "流程图",
    "旭日图",
]

GOAL_HINTS = {
    "分布": "分布比较",
    "离散": "离散度展示",
    "趋势": "趋势分析",
    "时间变化": "时间变化",
    "相关": "变量关系",
    "关系": "变量关系",
    "占比": "组成分析",
    "构成": "组成分析",
    "整体": "部分与整体关系",
    "聚类": "聚类展示",
    "模式": "模式发现",
    "流向": "流向分析",
    "层级": "层级关系",
    "网络": "连接关系展示",
    "空间": "空间位置展示",
    "地理": "空间位置展示",
    "显著": "显著性展示",
    "p值": "显著性展示",
}

FEATURE_HINTS = [
    "误差线",
    "显著性星号",
    "显著性字母",
    "P 值标注",
    "渐变色",
    "矩阵排版",
    "截断轴",
    "双 Y 轴",
    "散点叠加",
    "平滑线",
    "拟合线",
    "置信区间",
    "聚类树",
    "环形布局",
    "极坐标",
    "嵌套分组",
    "多层结构",
    "三维表达",
]

SEMANTIC_HINTS = {
    "分组": "分组变量",
    "处理组": "分组变量",
    "组别": "分组变量",
    "类别": "类别名称",
    "名称": "类别名称",
    "数值": "主数值",
    "x轴": "X 轴数值",
    "y轴": "Y 轴数值",
    "z轴": "Z 轴数值",
    "经纬度": "经纬度坐标",
    "节点": "来源节点",
    "终点": "目标节点",
    "权重": "权重",
    "p值": "P 值",
}

DIST_FAMILIES = {"箱线图", "横向箱线图", "小提琴图", "横向小提琴图", "云雨图", "蜂群图", "山峦图", "极坐标箱线图"}
STATS_FAMILIES = {"柱状图", "横向柱状图", "箱线图", "横向箱线图", "小提琴图", "横向小提琴图", "云雨图", "折线图", "火山图"}
SORTED_FAMILY_HINTS = sorted(FAMILY_HINTS, key=len, reverse=True)


def load_records(jsonl_path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with jsonl_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def resolve_chart_family(record: dict[str, Any]) -> str:
    def canonical_family(text: str) -> str:
        for family in SORTED_FAMILY_HINTS:
            if family in text:
                return family
        return ""

    name = str(record.get("name", ""))
    category_trail = record.get("category_trail", []) or []
    votes: dict[str, int] = defaultdict(int)
    source_family = str(record.get("chart_family", ""))
    leading = name.split("-")[0].strip()

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


def normalize_text(text: str) -> str:
    return str(text or "").lower().replace("p 值", "p值")


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def tokenize_text(text: str) -> list[str]:
    parts = [part.strip().lower() for part in TOKEN_SPLIT_RE.split(text) if part.strip()]
    return unique([part for part in parts if len(part) >= 2])


def read_request(args: argparse.Namespace) -> dict[str, Any]:
    if args.query_file:
      raw = Path(args.query_file).read_text(encoding="utf-8")
    elif args.query:
      raw = args.query
    else:
      raise SystemExit("Provide --query or --query-file.")

    raw = raw.strip()
    if raw.startswith("{"):
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            parsed["_raw_query_text"] = raw
            return parsed
    return {"goal": raw, "_raw_query_text": raw}


def build_query_text(request: dict[str, Any]) -> str:
    parts: list[str] = []
    if "goal" in request and request["goal"]:
        parts.append(str(request["goal"]))

    data_schema = request.get("data_schema") or {}
    if isinstance(data_schema, dict):
        if "description" in data_schema and data_schema["description"]:
            parts.append(str(data_schema["description"]))
        if "n_tables" in data_schema:
            parts.append(f"{data_schema['n_tables']} tables")
        for variable in data_schema.get("variables", []) or []:
            if isinstance(variable, dict):
                parts.extend(
                    str(variable.get(key, ""))
                    for key in ("name", "type", "role", "description")
                    if variable.get(key)
                )
        for key in ("has_grouping", "has_matrix", "has_geo", "has_hierarchy", "has_replicates"):
            if data_schema.get(key):
                parts.append(key)

    preferences = request.get("preferences") or {}
    if isinstance(preferences, dict):
        for key, value in preferences.items():
            if isinstance(value, list):
                parts.extend(str(item) for item in value if item)
            elif value:
                parts.append(str(value))

    for key in ("must_have_features", "avoid_families", "notes"):
        value = request.get(key)
        if isinstance(value, list):
            parts.extend(str(item) for item in value if item)
        elif value:
            parts.append(str(value))

    if request.get("_raw_query_text"):
        parts.append(str(request["_raw_query_text"]))

    return " ".join(parts).strip()


def extract_query_signals(request: dict[str, Any]) -> dict[str, Any]:
    query_text = build_query_text(request)
    norm = normalize_text(query_text)

    family_terms = [family for family in FAMILY_HINTS if family in query_text]

    goal_terms = []
    for needle, goal in GOAL_HINTS.items():
        if needle in query_text:
            goal_terms.append(goal)

    feature_terms = []
    for feature in FEATURE_HINTS:
        if normalize_text(feature) in norm or feature.replace(" ", "") in query_text:
            feature_terms.append(feature)

    semantic_terms = []
    for needle, semantic in SEMANTIC_HINTS.items():
        if needle in query_text:
            semantic_terms.append(semantic)

    keyword_terms = tokenize_text(query_text)
    keyword_terms.extend(family_terms)
    keyword_terms.extend(goal_terms)
    keyword_terms.extend(feature_terms)
    keyword_terms.extend(semantic_terms)
    keyword_terms = unique(keyword_terms)

    data_schema = request.get("data_schema") if isinstance(request.get("data_schema"), dict) else {}
    preferences = request.get("preferences") if isinstance(request.get("preferences"), dict) else {}

    wanted_table_count = data_schema.get("n_tables")
    flags = {
        "needs_grouping": bool(data_schema.get("has_grouping") or any(term in query_text for term in ["分组", "处理组", "组间", "多组"])),
        "needs_matrix": bool(data_schema.get("has_matrix") or any(term in query_text for term in ["热图", "矩阵", "聚类"])),
        "needs_geo": bool(data_schema.get("has_geo") or any(term in query_text for term in ["地图", "经纬度", "地理", "空间"])),
        "needs_hierarchy": bool(data_schema.get("has_hierarchy") or any(term in query_text for term in ["层级", "树", "流程", "网络", "桑基"])),
        "needs_stats": bool(preferences.get("need_stats") or any(term in query_text for term in ["显著", "p值", "误差线", "置信区间", "统计"])),
        "needs_distribution": any(term in query_text for term in ["分布", "密度", "中位数", "四分位", "离散"]),
        "needs_correlation": any(term in query_text for term in ["相关", "关系", "关联"]),
    }

    variable_types = [str(item.get("type", "")).lower() for item in data_schema.get("variables", []) if isinstance(item, dict)]
    structured_features = request.get("must_have_features") or []
    avoid_families = request.get("avoid_families") or []
    style_terms = preferences.get("style") or []

    return {
        "query_text": query_text,
        "family_terms": unique(family_terms),
        "goal_terms": unique(goal_terms),
        "feature_terms": unique(feature_terms),
        "semantic_terms": unique(semantic_terms),
        "keyword_terms": keyword_terms,
        "wanted_table_count": wanted_table_count,
        "variable_types": variable_types,
        "structured_features": [str(item) for item in structured_features],
        "avoid_families": [str(item) for item in avoid_families],
        "style_terms": [str(item) for item in style_terms],
        "flags": flags,
    }


def stats_friendly(record: dict[str, Any]) -> bool:
    features = set(record.get("visual_features", []))
    family = resolve_chart_family(record)
    return (
        family in STATS_FAMILIES
        or "误差线" in features
        or "显著性星号" in features
        or "显著性字母" in features
        or "P 值标注" in features
        or "置信区间" in features
    )


def record_blob(record: dict[str, Any]) -> str:
    return " ".join(
        [
            record.get("name", ""),
            record.get("chart_family", ""),
            resolve_chart_family(record),
            " ".join(record.get("category_trail", [])),
            " ".join(record.get("analysis_goal", [])),
            " ".join(record.get("visual_features", [])),
            " ".join(record.get("style_tags", [])),
            " ".join(record.get("use_cases", [])),
            record.get("search_text", ""),
        ]
    )


def score_record(record: dict[str, Any], signals: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    blob = record_blob(record)
    blob_norm = normalize_text(blob)
    family = resolve_chart_family(record)
    data_shape = record.get("data_shape", {})
    subtype_text = " ".join(record.get("subtype", []))
    name_text = record.get("name", "")

    for family_term in signals["family_terms"]:
        if family_term == family:
            score += 24
            reasons.append(f"图型家族直接匹配：{family_term}")
        elif family_term in record.get("name", ""):
            score += 12
            reasons.append(f"模板名称包含目标图型：{family_term}")

    for goal_term in signals["goal_terms"]:
        if goal_term in record.get("analysis_goal", []):
            score += 14
            reasons.append(f"分析目标匹配：{goal_term}")

    for feature in signals["feature_terms"]:
        if feature in record.get("visual_features", []):
            score += 10
            reasons.append(f"视觉特征匹配：{feature}")
        elif normalize_text(feature) in blob_norm:
            score += 4

    for semantic in signals["semantic_terms"]:
        if any(column.get("semantic") == semantic for column in record.get("required_columns", [])):
            score += 8
            reasons.append(f"字段语义匹配：{semantic}")

    for keyword in signals["keyword_terms"]:
        keyword_norm = normalize_text(keyword)
        if len(keyword_norm) < 2:
            continue
        if keyword in record.get("name", ""):
            score += 8
        elif keyword == family:
            score += 8
        elif keyword_norm in blob_norm:
            score += 3

    wanted_table_count = signals["wanted_table_count"]
    if isinstance(wanted_table_count, int):
        table_count = int(data_shape.get("table_count", 0))
        if table_count == wanted_table_count:
            score += 8
            reasons.append(f"数据表数量匹配：{table_count}")
        else:
            score -= abs(table_count - wanted_table_count) * 1.5

    if signals["flags"]["needs_grouping"]:
        if data_shape.get("supports_grouping"):
            score += 10
            reasons.append("支持分组比较")
        else:
            score -= 15
        if "不分组" in name_text or "不分组" in subtype_text:
            score -= 18
        if "分组" in name_text or "分组" in subtype_text:
            score += 4

    if signals["flags"]["needs_matrix"]:
        if data_shape.get("supports_matrix"):
            score += 10
            reasons.append("支持矩阵/热图型数据")
        else:
            score -= 6

    if signals["flags"]["needs_geo"]:
        if data_shape.get("supports_geo"):
            score += 10
            reasons.append("支持空间/地理数据")
        else:
            score -= 6

    if signals["flags"]["needs_hierarchy"]:
        if data_shape.get("supports_hierarchy") or any(pattern == "edge_list_or_flow" for pattern in data_shape.get("data_patterns", [])):
            score += 10
            reasons.append("支持层级/流向/连接结构")
        else:
            score -= 6

    if signals["flags"]["needs_stats"]:
        if stats_friendly(record):
            score += 8
            reasons.append("适合统计标注或误差展示")
        else:
            score -= 2

    if signals["flags"]["needs_distribution"]:
        if family in DIST_FAMILIES or "分布比较" in record.get("analysis_goal", []):
            score += 10
            reasons.append("适合分布差异展示")
        else:
            score -= 3

    if signals["flags"]["needs_correlation"]:
        if "变量关系" in record.get("analysis_goal", []) or family in {"散点图", "气泡图", "网络图"}:
            score += 8
            reasons.append("适合关系/相关性分析")

    numeric_need = sum(1 for item in signals["variable_types"] if "num" in item or "float" in item or "int" in item)
    categorical_need = sum(1 for item in signals["variable_types"] if "cat" in item or "group" in item or "factor" in item or "text" in item)
    numeric_have = sum(1 for column in record.get("required_columns", []) if column.get("data_type") == "numeric")
    categorical_have = sum(1 for column in record.get("required_columns", []) if column.get("data_type") == "categorical")

    if numeric_need:
        score += min(numeric_need, numeric_have) * 2
    if categorical_need:
        score += min(categorical_need, categorical_have) * 2

    for feature in signals["structured_features"]:
        if normalize_text(feature) in blob_norm:
            score += 8
            reasons.append(f"满足指定特征：{feature}")
        else:
            score -= 3

    for style in signals["style_terms"]:
        if normalize_text(style) in blob_norm:
            score += 4

    for family_name in signals["avoid_families"]:
        if family_name == family:
            score -= 30
            reasons.append(f"命中避开图型：{family_name}")

    if record.get("has_python"):
        score += 1.5
    if record.get("has_r"):
        score += 1.0

    reasons = unique(reasons)
    return score, reasons


def recommend(records: list[dict[str, Any]], request: dict[str, Any], top_k: int) -> list[dict[str, Any]]:
    signals = extract_query_signals(request)
    scored = []
    for record in records:
        family = resolve_chart_family(record)
        score, reasons = score_record(record, signals)
        scored.append(
            {
                "id": record["id"],
                "name": record["name"],
                "chart_family": family,
                "source_chart_family": record["chart_family"],
                "score": round(score, 2),
                "reasons": reasons[:6],
                "selection_summary": record.get("selection_summary", ""),
                "paths": {
                    "python_path": record.get("python_path"),
                    "r_path": record.get("r_path"),
                    "svg_path": record.get("svg_path"),
                    "preview_path": record.get("preview_path"),
                    "meta_path": record.get("meta_path"),
                    "data_paths": record.get("data_paths", []),
                },
                "analysis_goal": record.get("analysis_goal", []),
                "visual_features": record.get("visual_features", []),
                "required_columns": record.get("required_columns", []),
                "complexity": record.get("complexity"),
            }
        )

    scored.sort(key=lambda item: (-item["score"], item["chart_family"], item["name"], item["id"]))
    return scored[:top_k]


def render_markdown(results: list[dict[str, Any]], request: dict[str, Any]) -> str:
    lines = []
    goal = request.get("goal") or request.get("_raw_query_text") or "未命名需求"
    lines.append(f"# 模板推荐结果")
    lines.append("")
    lines.append(f"需求：{goal}")
    lines.append("")
    for index, item in enumerate(results, start=1):
        lines.append(f"## {index}. {item['name']} [{item['id']}]")
        lines.append(f"- 图型：{item['chart_family']}")
        lines.append(f"- 评分：{item['score']}")
        lines.append(f"- 推荐理由：{'；'.join(item['reasons']) if item['reasons'] else '基于整体语义与数据结构匹配'}")
        lines.append(f"- 摘要：{item['selection_summary']}")
        lines.append(f"- Python：{item['paths']['python_path'] or '无'}")
        lines.append(f"- R：{item['paths']['r_path'] or '无'}")
        lines.append(f"- SVG：{item['paths']['svg_path'] or '无'}")
        lines.append(f"- Meta：{item['paths']['meta_path'] or '无'}")
        data_paths = item["paths"]["data_paths"]
        lines.append(f"- 数据：{', '.join(data_paths) if data_paths else '无'}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recommend NGplot templates for a research plotting request.")
    parser.add_argument("--catalog", help="Path to catalog_enriched.jsonl; if omitted, auto-discover under the current workspace")
    parser.add_argument("--query", help="Natural-language request or a JSON string")
    parser.add_argument("--query-file", help="Path to a text or JSON request file")
    parser.add_argument("--top-k", type=int, default=5, help="Number of templates to return")
    parser.add_argument("--format", choices=("json", "markdown"), default="json", help="Output format")
    parser.add_argument("--save", help="Optional output file path")
    return parser.parse_args()


def discover_catalog_path(provided: str | None) -> Path:
    if provided:
        candidate = Path(provided).resolve()
        if candidate.is_file():
            return candidate
        raise SystemExit(f"Catalog file not found: {candidate}")

    script_dir = Path(__file__).resolve().parent
    bundled_catalog = script_dir.parent / "assets" / "bioinforw_ngplot_dump" / "catalog_enriched.jsonl"

    direct_candidates = [
        Path.cwd() / "bioinforw_ngplot_dump" / "catalog_enriched.jsonl",
        Path.cwd() / "catalog_enriched.jsonl",
        bundled_catalog,
    ]
    for candidate in direct_candidates:
        if candidate.exists():
            return candidate.resolve()

    for found in Path.cwd().rglob("catalog_enriched.jsonl"):
        return found.resolve()

    raise SystemExit("Could not find catalog_enriched.jsonl. Pass --catalog explicitly.")


def main() -> None:
    args = parse_args()
    request = read_request(args)
    records = load_records(discover_catalog_path(args.catalog))
    results = recommend(records, request, max(1, args.top_k))

    payload: str
    if args.format == "markdown":
        payload = render_markdown(results, request)
    else:
        payload = json.dumps(
            {
                "request": request,
                "top_k": len(results),
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )

    if args.save:
        Path(args.save).write_text(payload, encoding="utf-8")

    print(payload)


if __name__ == "__main__":
    main()
