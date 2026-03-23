from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _base_dir(base_dir: str | Path | None = None) -> Path:
    return Path(base_dir) if base_dir is not None else Path(__file__).resolve().parent


def _catalog_path(base_dir: str | Path | None = None) -> Path:
    return _base_dir(base_dir) / "catalog.json"


def load_catalog(base_dir: str | Path | None = None) -> dict[str, Any]:
    return json.loads(_catalog_path(base_dir).read_text(encoding="utf-8"))


def list_templates(base_dir: str | Path | None = None) -> list[dict[str, Any]]:
    return load_catalog(base_dir)["templates"]


def find_templates(
    keyword: str | None = None,
    category: str | None = None,
    has_python: bool | None = None,
    has_r: bool | None = None,
    base_dir: str | Path | None = None,
) -> list[dict[str, Any]]:
    items = list_templates(base_dir)
    if keyword:
        needle = keyword.lower()
        items = [
            item
            for item in items
            if needle in item["name"].lower()
            or needle in item["id"].lower()
            or needle in item["category"].lower()
            or needle in item["categoryTrailText"].lower()
        ]
    if category:
        items = [item for item in items if item["category"] == category]
    if has_python is not None:
        items = [item for item in items if bool(item["hasPython"]) is has_python]
    if has_r is not None:
        items = [item for item in items if bool(item["hasR"]) is has_r]
    return items


def get_template(template_id: str, base_dir: str | Path | None = None) -> dict[str, Any]:
    for item in list_templates(base_dir):
        if item["id"] == template_id:
            return item
    raise KeyError(f"Template not found: {template_id}")


def load_bundle(template_id: str, base_dir: str | Path | None = None) -> dict[str, Any]:
    root = _base_dir(base_dir)
    item = get_template(template_id, root)
    bundle: dict[str, Any] = dict(item)
    bundle["meta"] = json.loads((root / item["metaUrl"]).read_text(encoding="utf-8"))
    bundle["svg"] = (root / item["svgUrl"]).read_text(encoding="utf-8")
    bundle["data"] = {
        file_info["name"]: (root / file_info["url"]).read_text(encoding="utf-8")
        for file_info in item["dataFiles"]
    }
    if item.get("pythonUrl"):
        bundle["python_code"] = (root / item["pythonUrl"]).read_text(encoding="utf-8")
    if item.get("rUrl"):
        bundle["r_code"] = (root / item["rUrl"]).read_text(encoding="utf-8")
    return bundle


if __name__ == "__main__":
    catalog = load_catalog()
    print(f"Loaded {catalog['totalTemplates']} templates from {_catalog_path()}")
