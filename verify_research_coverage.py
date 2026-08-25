#!/usr/bin/env python3
"""驗證台股研究名冊、研究檔、Index 與 Obsidian entity 是否一致。只讀，不自動修改。"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "meta" / "research_universe.json"
INDEX = ROOT / "INDEX.md"
RESEARCH = ROOT / "research"
ENTITIES = Path.home() / "obsidian-wiki" / "entities"
REQUIRED = ("last_verified", "confidence", "sources_as_of")


def frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    parts = text.split("---", 2)
    return parts[1] if len(parts) >= 3 else ""


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    if not MANIFEST.exists():
        print(f"ERROR missing manifest: {MANIFEST}")
        return 2
    universe = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = universe.get("stocks", [])
    codes = [str(x["code"]) for x in entries]
    if len(codes) != len(set(codes)):
        errors.append("manifest contains duplicate codes")
    index_text = INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""
    index_codes = set(re.findall(r"^\| (\d{4}) \|", index_text, re.M))
    manifest_codes = set(codes)
    for code in sorted(manifest_codes - index_codes):
        errors.append(f"manifest missing from INDEX: {code}")
    for code in sorted(index_codes - manifest_codes):
        warnings.append(f"INDEX not in manifest: {code}")
    for item in entries:
        code, name = str(item["code"]), item["name"]
        research_path = ROOT / item.get("research_path", f"research/{code}_{name}.md")
        entity_path = Path.home() / "obsidian-wiki" / item.get("entity_path", f"entities/{code}_{name}.md")
        if not research_path.exists():
            errors.append(f"missing research: {code} {research_path}")
            continue
        if not entity_path.exists():
            errors.append(f"missing entity: {code} {entity_path}")
        text = research_path.read_text(encoding="utf-8", errors="replace")
        fm = frontmatter(text)
        for key in REQUIRED:
            if f"{key}:" not in fm:
                errors.append(f"missing frontmatter {key}: {research_path.name}")
        m = re.search(r"research_maturity:\s*[\"']?(\d+)", fm)
        if m and int(m.group(1)) < int(item.get("required_maturity", 75)):
            warnings.append(f"low maturity {m.group(1)}: {research_path.name}")
        if "_wrong" in research_path.name:
            errors.append(f"wrong-name file requires isolation review: {research_path.name}")
        if "未確認" not in text:
            warnings.append(f"no explicit uncertainty marker: {research_path.name}")
    print(f"manifest_stocks={len(entries)} index_stocks={len(index_codes)}")
    print(f"errors={len(errors)} warnings={len(warnings)}")
    for line in errors:
        print("ERROR", line)
    for line in warnings:
        print("WARN", line)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
