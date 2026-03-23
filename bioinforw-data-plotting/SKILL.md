---
name: bioinforw-data-plotting
description: Recommend and adapt scientific plotting templates from a local Bioinforw or NGplot catalog for research data visualization. Use when Codex needs to choose a chart type from `catalog_enriched.jsonl`, refresh `embedding_input.jsonl`, return top-k templates with Python/R code paths, map user columns to template-required columns, or turn a research plotting request into an executable plotting starting point.
---

# Bioinforw Data Plotting

## Overview

Prefer the local template catalog before inventing a chart from scratch. Start by matching the user's data and analysis goal to existing templates, then adapt the selected Python or R example code to the user's columns and file paths.

## Workflow

1. Discover the local catalog. Prefer `bioinforw_ngplot_dump/catalog_enriched.jsonl`. If the user workspace does not contain one, fall back to the bundled asset catalog under `assets/bioinforw_ngplot_dump/`.
2. Refresh `embedding_input.jsonl` when it is missing or stale. Use `scripts/build_embedding_input.py`. The script can auto-discover the dump root from the current workspace.
3. Convert the user request into a structured query when possible. Capture analysis goal, table count, variable roles, grouping, statistical annotation needs, must-have visual features, and families to avoid. Use `references/request-format.md`.
4. Rank templates with `scripts/recommend_bioinforw_templates.py`. Prefer JSON output for downstream use.
5. Return the best matches with:
   - template id and name
   - resolved `chart_family` and original `source_chart_family`
   - ranking reasons
   - `python_path`, `r_path`, `svg_path`, `preview_path`, and `data_paths`
6. If the user wants an actual figure, open the selected template's `python_example.py` or `R_example.R`, map the user's columns to `required_columns`, and modify that code in the current repo instead of rewriting everything.
7. If no template fits, state that clearly and explain the nearest matching families instead of forcing an unrelated chart.

## Query Construction

- Record the user's scientific question first: comparison, distribution, trend, correlation, composition, hierarchy, network, geography, or significance.
- Normalize variables into roles such as `group`, `category`, `measurement`, `time`, `source`, `target`, `geo`, or `p_value`.
- Prefer a structured JSON query when the user provides schema details. Fall back to raw text only when the request is underspecified.
- Penalize templates that conflict with hard constraints such as `不分组`, missing statistics, wrong table count, or banned families.

## Commands

Run from the user's workspace root when possible.

```powershell
python C:\Users\ciheb\.codex\skills\bioinforw-data-plotting\scripts\build_embedding_input.py
python C:\Users\ciheb\.codex\skills\bioinforw-data-plotting\scripts\recommend_bioinforw_templates.py --query-file .\bioinforw_ngplot_dump\recommend_query_example.json --top-k 8 --format json
```

Pass an explicit path when the catalog is not under the current working directory.

## Resources

- `scripts/build_embedding_input.py`: Regenerate `embedding_input.jsonl` from `catalog_enriched.jsonl`.
- `scripts/recommend_bioinforw_templates.py`: Score templates against natural-language or structured requests and return reusable code paths.
- `references/request-format.md`: Structured query fields, examples, and response expectations.
- `assets/bioinforw_ngplot_dump/`: Bundled `345`-template snapshot with `catalog_enriched.jsonl`, `embedding_input.jsonl`, local index page, preview images, rendered SVGs, example Python/R code, and example input data.
