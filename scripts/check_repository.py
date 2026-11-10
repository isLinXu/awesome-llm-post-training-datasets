#!/usr/bin/env python3
"""检查 GitHub 仓库文档链接、必需文件和本地路径卫生。"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import parse_qs, unquote

ROOT = Path(__file__).resolve().parents[1]
CITATION_RE = re.compile(r'\[([^\]]+)\]\(kimi-cite://web\?([^\)\s]+)\s+"citation"\)')
LINK_RE = re.compile(r'!?\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
REQUIRED = [
    "README.md",
    "CONTRIBUTING.md",
    "datasets-list.yaml",
    "datasets-list.md",
    "datasets-multimodal.yaml",
    "datasets-catalog.md",
    "multimodal-post-training-datasets-zh.md",
    "build_datasets_list.py",
    "build_multimodal_datasets.py",
    "dataset_markdown_links.py",
    "research/build_multimodal_report.py",
    "research/plot_multimodal_coverage.py",
    "research/multimodal-asset-coverage.png",
    "commercial-default-manifest.yaml",
    "research-isolated-manifest.yaml",
    "training-recipes.md",
    "config/dataset-taxonomy.yaml",
    ".github/workflows/validate.yml",
    ".github/workflows/update-datasets-catalog.yml",
]


def markdown_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*.md") if ".git" not in path.parts and ".venv" not in path.parts)


def convert_session_citations() -> int:
    """把早期会话专用引用转换为 GitHub 可用的普通 HTTPS 链接。"""
    count = 0
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")

        def replace(match: re.Match[str]) -> str:
            nonlocal count
            params = parse_qs(match.group(2))
            urls = params.get("url")
            if not urls or not urls[0].startswith("https://"):
                raise ValueError(f"无法转换引用：{path}: {match.group(0)}")
            count += 1
            return f"[{match.group(1)}]({urls[0]})"

        converted = CITATION_RE.sub(replace, text)
        if converted != text:
            path.write_text(converted, encoding="utf-8")
    return count


def check() -> tuple[list[str], int, int]:
    errors: list[str] = []
    local_links = 0
    files = markdown_files()
    sys.path.insert(0, str(ROOT))
    from dataset_markdown_links import link_dataset_table_entries, load_assets, validate_primary_catalog
    assets = load_assets()
    for required in REQUIRED:
        if not (ROOT / required).is_file():
            errors.append(f"缺少必需文件：{required}")
    for path in files:
        relative = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        if "kimi-cite://" in text:
            errors.append(f"{relative}: 仍包含会话专用 kimi-cite 链接")
        if "/Users/" in text or "file://" in text:
            errors.append(f"{relative}: 包含本机绝对路径或 file:// 链接")
        # research/cards 是上游数据卡归档，其中的相对链接指向原仓库，而非本仓库。
        if relative.parts[:2] == ("research", "cards"):
            continue
        linked = link_dataset_table_entries(text, assets)
        if linked != text:
            errors.append(f"{relative}: 表格仍有未链接的 canonical 数据集名称或 ID")
        if any(re.search(r"\[[^\]]+\]\(", match.group(0)) for match in re.finditer(r"`[^`\n]+`", text)):
            errors.append(f"{relative}: 代码字段中嵌入了 Markdown 链接")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip("<>")
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            if "://" in target:
                errors.append(f"{relative}: 非标准本地链接 {target}")
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            local_links += 1
            if target.startswith("/"):
                errors.append(f"{relative}: 本地链接不能使用绝对路径 {target}")
                continue
            resolved = (path.parent / target).resolve()
            if ROOT != resolved and ROOT not in resolved.parents:
                errors.append(f"{relative}: 本地链接越出仓库 {target}")
            elif not resolved.exists():
                errors.append(f"{relative}: 本地链接目标不存在 {target}")
    for catalog_name in ("datasets-list.md", "datasets-catalog.md"):
        catalog_path = ROOT / catalog_name
        if catalog_path.is_file():
            catalog_text = catalog_path.read_text(encoding="utf-8")
            errors.extend(f"{catalog_name}: {error}" for error in validate_primary_catalog(catalog_text, assets))
    return errors, len(files), local_links


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fix-citations", action="store_true", help="将早期会话引用一次性转换为普通 HTTPS 链接")
    args = parser.parse_args()
    if args.fix_citations:
        print(f"已转换 {convert_session_citations()} 个会话引用链接。")
    errors, files, links = check()
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"仓库检查失败：{len(errors)} 项错误。", file=sys.stderr)
        return 1
    print(f"仓库检查通过：{files} 个 Markdown 文件，{links} 个本地链接，无会话引用或本机路径。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
