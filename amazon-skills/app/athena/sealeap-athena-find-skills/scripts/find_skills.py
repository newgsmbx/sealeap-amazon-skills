#!/usr/bin/env python3
"""Search local Skill entrypoints and their capability/legacy-name indexes."""
import argparse
import json
from pathlib import Path
import re
import sys

ALIASES = {
    "亚马逊": "amazon", "沃尔玛": "walmart", "虾皮": "shopee", "美客多": "mercado",
    "易贝": "ebay", "图片": "image", "图像": "image", "创意图": "image",
    "关键词": "关键词 keyword", "搜索词": "搜索词 keyword", "报表": "报表 report",
    "订单": "订单 order", "广告": "广告 ads", "专利": "专利 patent",
}
PLATFORMS = {"amazon", "walmart", "shopee", "temu", "tiktok", "ozon", "etsy", "shopify", "1688", "mercado", "ebay"}
REGION_ALIASES = {
    "us": ("美国区", "美国站", "美区", "美国", "us", "usa"),
    "eu": ("欧洲区", "欧洲站", "欧区", "欧洲", "欧盟", "eu"),
    "global": ("全球区", "全球", "global"),
}


def normalize(text):
    text = text.casefold()
    for source, target in ALIASES.items():
        text = text.replace(source, target)
    return text


def read_metadata(path):
    raw = path.read_text(encoding="utf-8-sig")
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|$)", raw, re.S)
    if not match:
        raise ValueError("missing YAML frontmatter")
    result = {}
    lines = match.group(1).splitlines()
    for index, line in enumerate(lines):
        field = re.match(r"^(name|description):\s*(.*)$", line)
        if not field:
            continue
        key, value = field.groups()
        if key in result:
            raise ValueError("duplicate metadata field")
        if value[:1] == '"':
            value = json.loads(value)
        elif value[:1] == "'":
            if not value.endswith("'"):
                raise ValueError("unterminated quoted metadata")
            value = value[1:-1].replace("''", "'")
        elif value in ("|", ">", "|-", ">-", ""):
            continued = []
            for following in lines[index + 1:]:
                if following and not following[0].isspace():
                    break
                continued.append(following.strip())
            value = " ".join(continued)
        elif value.startswith(("[", "{", "&", "*", "!")):
            raise ValueError("unsupported structured metadata")
        if not isinstance(value, str):
            raise ValueError("metadata must contain strings")
        result[key] = value.strip()
    if not result.get("name") or not result.get("description"):
        raise ValueError("missing name or description")
    heading = re.search(r"^#\s+(.+)$", raw[match.end():], re.M)
    result["title"] = heading.group(1).strip() if heading else result["name"]
    return result


def terms(query):
    chunks = re.findall(r"[a-z0-9]+|[\u3400-\u9fff]+", normalize(query))
    found = set()
    for chunk in chunks:
        if re.fullmatch(r"[\u3400-\u9fff]+", chunk) and len(chunk) > 2:
            found.update(chunk[i:i + 2] for i in range(len(chunk) - 1))
        else:
            found.add(chunk)
    return sorted(found - {"skill", "skills", "技能", "查找", "搜索", "帮我", "请"})


def platforms(text):
    text = normalize(text)
    return {p for p in PLATFORMS if re.search(r"(?<![a-z0-9])" + re.escape(p) + r"(?![a-z0-9])", text)}


def regions(text):
    text = text.casefold()
    found = set()
    for region, aliases in REGION_ALIASES.items():
        for alias in aliases:
            if re.fullmatch(r"[a-z]+", alias):
                match = re.search(r"(?<![a-z0-9])" + alias + r"(?![a-z0-9])", text)
            else:
                match = alias in text
            if match:
                found.add(region)
                break
    return found


def local_reference(package, value):
    if not isinstance(value, str) or not value:
        raise ValueError("missing capability reference")
    target = (package / value).resolve()
    if not target.is_relative_to(package.resolve()) or not target.is_file():
        raise ValueError("capability reference is missing or escapes the package")
    return str(target)


def load_capabilities(package, metadata):
    index = package / "references" / "capabilities.json"
    if not index.exists():
        return [{**metadata, "guide_path": "SKILL.md"}]
    payload = json.loads(index.read_text(encoding="utf-8"))
    records = payload.get("capabilities") if isinstance(payload, dict) else None
    if not isinstance(records, list) or not records:
        raise ValueError("invalid capability index")
    names = set()
    for record in records:
        if not isinstance(record, dict) or not all(isinstance(record.get(k), str) and record[k] for k in ("name", "title", "description")):
            raise ValueError("invalid capability metadata")
        if record["name"] in names:
            raise ValueError("duplicate capability name")
        names.add(record["name"])
        local_reference(package, record.get("guide_path"))
    return records


def capability_result(package, record, score):
    result = {k: record[k] for k in ("name", "title", "description", "mode", "route") if k in record}
    result["score"] = score
    for field in ("guide_path", "playbook_path", "tool_routing_path"):
        if field in record:
            result[field] = local_reference(package, record[field])
    return result


def search(root, query, limit):
    root = Path(root).resolve()
    tokens = terms(query)
    normalized_query = normalize(query)
    requested_platforms = platforms(query)
    requested_regions = regions(query)
    context_tokens = requested_platforms | set().union(*(set(terms(a)) for r in requested_regions for a in REGION_ALIASES[r]))
    action_tokens = set(tokens) - context_tokens
    exact = query.strip().removeprefix("$")
    exact_name = bool(re.fullmatch(r"sealeap-athena-[a-z0-9-]+", exact))
    matches, warnings = [], []
    for path in sorted(root.glob("*/SKILL.md")):
        package = path.parent
        try:
            if not path.resolve().is_relative_to(root):
                raise ValueError("package escapes search root")
            metadata = read_metadata(path)
            records = load_capabilities(package, metadata)
            parent_exact = exact_name and exact == metadata["name"]
            hits = []
            for record in records:
                record_exact = exact_name and exact == record["name"]
                if exact_name and not (parent_exact or record_exact):
                    continue
                text = " ".join(record.get(k, "") for k in ("name", "title", "description"))
                candidate_platforms = platforms(record["name"] + " " + record["title"])
                candidate_regions = regions(record["name"] + " " + record["title"])
                if not exact_name:
                    if requested_platforms and candidate_platforms and not requested_platforms.intersection(candidate_platforms):
                        continue
                    if requested_regions and candidate_regions and not requested_regions.intersection(candidate_regions):
                        continue
                title, name, description = (normalize(record.get(k, "")) for k in ("title", "name", "description"))
                parent_text = normalize(metadata["name"] + " " + metadata["title"])
                if not exact_name and action_tokens and not any(t in title or t in name or t in description or t in parent_text for t in action_tokens):
                    continue
                score = sum(8 * (t in title) + 4 * (t in name) + (t in description) for t in tokens)
                score += sum(2 * (t in parent_text) for t in tokens)
                if requested_platforms.intersection(candidate_platforms):
                    score += 12
                if requested_regions.intersection(candidate_regions):
                    score += 12
                compact_query = "".join(normalized_query.split())
                if compact_query and compact_query in "".join(title.split()):
                    score += 80
                if record_exact:
                    score = 20000
                elif parent_exact:
                    score = 10000
                if score:
                    hits.append(capability_result(package, record, score))
            if not hits:
                continue
            hits.sort(key=lambda item: (-item["score"], item["name"]))
            matches.append({**metadata, "path": str(package.resolve()), "score": hits[0]["score"],
                            "matched_capability_count": len(hits), "matched_capabilities": hits[:5]})
        except (OSError, UnicodeError, ValueError, TypeError, KeyError) as error:
            warnings.append({"path": str(path), "error": str(error)})
    matches.sort(key=lambda item: (-item["score"], item["name"]))
    return {"query": query, "root": str(root), "total_matches": len(matches), "results": matches[:limit], "warnings": warnings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    if not 1 <= args.limit <= 50:
        parser.error("--limit must be between 1 and 50")
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        parser.error("--root must be an existing Skill parent directory")
    print(json.dumps(search(root, args.query, args.limit), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
