"""
Export stage — convert markdown-with-frontmatter to HTML, XML, and JSON.

Each exporter takes the full markdown string (with optional YAML frontmatter)
and returns the exported string in the target format.
"""
from __future__ import annotations

import json
import re
from xml.sax.saxutils import escape as xml_escape

import markdown


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\n(.+?)\n---\n*", re.DOTALL)


def _split_frontmatter(md_text: str) -> tuple[dict[str, str | None], str]:
    """Split YAML frontmatter from the markdown body.

    Returns (metadata_dict, body).  If there is no frontmatter the metadata
    dict is empty and body is the full text.
    """
    m = _FRONTMATTER_RE.match(md_text)
    if not m:
        return {}, md_text

    body = md_text[m.end():]
    meta: dict[str, str | None] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if value == "null":
            meta[key.strip()] = None
        else:
            # Strip surrounding quotes added by metadata_to_yaml_frontmatter
            if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
                value = value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
            meta[key.strip()] = value
    return meta, body


# ---------------------------------------------------------------------------
# HTML export
# ---------------------------------------------------------------------------

def to_html(md_text: str, title: str | None = None) -> str:
    """Convert markdown (with optional frontmatter) to a standalone HTML page."""
    meta, body = _split_frontmatter(md_text)
    page_title = title or meta.get("title") or "Converted Document"

    html_body = markdown.markdown(body, extensions=["tables", "fenced_code"])

    meta_tags = ""
    for key, value in meta.items():
        if value is not None:
            meta_tags += f'    <meta name="{xml_escape(key)}" content="{xml_escape(value)}">\n'

    return (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "    <meta charset=\"utf-8\">\n"
        f"    <title>{xml_escape(page_title)}</title>\n"
        f"{meta_tags}"
        "</head>\n"
        "<body>\n"
        f"{html_body}\n"
        "</body>\n"
        "</html>\n"
    )


# ---------------------------------------------------------------------------
# XML export
# ---------------------------------------------------------------------------

def to_xml(md_text: str) -> str:
    """Convert markdown (with optional frontmatter) to a simple XML envelope."""
    meta, body = _split_frontmatter(md_text)

    meta_elements = ""
    for key, value in meta.items():
        if value is None:
            meta_elements += f"    <{key} />\n"
        else:
            meta_elements += f"    <{key}>{xml_escape(value)}</{key}>\n"

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<document>\n"
        "  <metadata>\n"
        f"{meta_elements}"
        "  </metadata>\n"
        "  <content><![CDATA[\n"
        f"{body}"
        "\n  ]]></content>\n"
        "</document>\n"
    )


# ---------------------------------------------------------------------------
# JSON export
# ---------------------------------------------------------------------------

def to_json(md_text: str) -> str:
    """Convert markdown (with optional frontmatter) to a JSON document."""
    meta, body = _split_frontmatter(md_text)

    doc = {
        "metadata": meta,
        "content": body,
    }
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
