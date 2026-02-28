"""Extract template layout metadata from Next.js TSX files into a static JSON registry.

Run once: python scripts/extract_templates.py
Output: assets/template_registry.json
"""

import os
import re
import json
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent / "nextjs" / "app" / "presentation-templates"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "assets" / "template_registry.json"

ZOD_TYPE_MAP = {
    "z.string()": "string",
    "z.number()": "number",
    "z.boolean()": "boolean",
    "z.array(": "array",
    "z.enum(": "string",
    "z.union(": "string",
}


def parse_zod_schema(content: str, schema_var_name: str) -> dict:
    """Parse a Zod schema definition from TSX source into a JSON schema approximation."""
    pattern = rf"(?:const|let)\s+{re.escape(schema_var_name)}\s*=\s*z\.object\(\{{(.*?)\}}\)"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return {}

    block = match.group(1)
    props = {}
    field_pattern = r"(\w+)\s*:\s*(.+?)(?:,\s*\n|\n)"
    for fm in re.finditer(field_pattern, block):
        field_name = fm.group(1)
        field_def = fm.group(2).strip().rstrip(",")

        field_type = "string"
        description = ""
        for ztype, jtype in ZOD_TYPE_MAP.items():
            if ztype in field_def:
                field_type = jtype
                break
        if "ImageSchema" in field_def or "image" in field_name.lower():
            field_type = "image"

        desc_match = re.search(r"description:\s*['\"](.+?)['\"]", field_def)
        if desc_match:
            description = desc_match.group(1)

        props[field_name] = {"type": field_type}
        if description:
            props[field_name]["description"] = description

    return {"type": "object", "properties": props}


def extract_layout_from_file(filepath: Path) -> dict | None:
    """Extract layoutId, layoutName, layoutDescription, Schema from a TSX file."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None

    layout_id_match = re.search(r"(?:export\s+)?const\s+layoutId\s*=\s*['\"](.+?)['\"]", content)
    layout_name_match = re.search(r"(?:export\s+)?const\s+layoutName\s*=\s*['\"](.+?)['\"]", content)
    layout_desc_match = re.search(r"(?:export\s+)?const\s+layoutDescription\s*=\s*['\"](.+?)['\"]", content)

    if not layout_id_match:
        return None

    layout_id = layout_id_match.group(1)
    layout_name = layout_name_match.group(1) if layout_name_match else layout_id
    layout_desc = layout_desc_match.group(1) if layout_desc_match else ""

    schema_var_match = re.search(r"export\s+const\s+Schema\s*=\s*(\w+)", content)
    json_schema = {}
    if schema_var_match:
        json_schema = parse_zod_schema(content, schema_var_match.group(1))

    return {
        "id": layout_id,
        "name": layout_name,
        "description": layout_desc,
        "json_schema": json_schema,
    }


def main():
    if not TEMPLATES_DIR.exists():
        print(f"Templates directory not found: {TEMPLATES_DIR}")
        return

    registry = {}

    for group_dir in sorted(TEMPLATES_DIR.iterdir()):
        if not group_dir.is_dir() or group_dir.name.startswith("."):
            continue

        group_name = group_dir.name
        settings_file = group_dir / "settings.json"
        settings = {"description": "", "ordered": False, "default": False}
        if settings_file.exists():
            try:
                settings = json.loads(settings_file.read_text())
            except Exception:
                pass

        layouts = []
        for tsx_file in sorted(group_dir.glob("*.tsx")):
            if tsx_file.name == "index.tsx" or tsx_file.name.startswith("Example"):
                continue
            layout_data = extract_layout_from_file(tsx_file)
            if layout_data:
                layouts.append(layout_data)

        if layouts:
            registry[group_name] = {
                "name": group_name,
                "description": settings.get("description", ""),
                "ordered": settings.get("ordered", False),
                "default": settings.get("default", False),
                "slides": layouts,
            }
            print(f"  {group_name}: {len(layouts)} layouts extracted")

    os.makedirs(OUTPUT_PATH.parent, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

    total = sum(len(g["slides"]) for g in registry.values())
    print(f"\nTotal: {len(registry)} groups, {total} layouts → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
