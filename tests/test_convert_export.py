"""Unit tests for src.convert.export — HTML, XML, JSON exporters."""
from __future__ import annotations

import json
from xml.etree import ElementTree as ET

import pytest

from src.convert.export import _split_frontmatter, to_html, to_json, to_xml

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_MD_WITH_FM = """\
---
title: "Test RFP"
issuer: Acme Corp
deadline: null
---

# Introduction

Some content here.
"""

SAMPLE_MD_BARE = """\
# Introduction

Some content here.
"""


# ---------------------------------------------------------------------------
# _split_frontmatter
# ---------------------------------------------------------------------------

class TestSplitFrontmatter:
    def test_with_frontmatter(self):
        meta, body = _split_frontmatter(SAMPLE_MD_WITH_FM)
        assert meta["title"] == "Test RFP"
        assert meta["issuer"] == "Acme Corp"
        assert meta["deadline"] is None
        assert body.startswith("# Introduction")

    def test_without_frontmatter(self):
        meta, body = _split_frontmatter(SAMPLE_MD_BARE)
        assert meta == {}
        assert "# Introduction" in body


# ---------------------------------------------------------------------------
# HTML export
# ---------------------------------------------------------------------------

class TestToHtml:
    def test_basic_structure(self):
        html = to_html(SAMPLE_MD_WITH_FM)
        assert "<!DOCTYPE html>" in html
        assert "<title>Test RFP</title>" in html
        assert '<meta name="issuer" content="Acme Corp">' in html
        assert "<h1>Introduction</h1>" in html

    def test_bare_markdown(self):
        html = to_html(SAMPLE_MD_BARE)
        assert "<title>Converted Document</title>" in html
        assert "<h1>Introduction</h1>" in html

    def test_custom_title(self):
        html = to_html(SAMPLE_MD_WITH_FM, title="Custom Title")
        assert "<title>Custom Title</title>" in html


# ---------------------------------------------------------------------------
# XML export
# ---------------------------------------------------------------------------

class TestToXml:
    def test_well_formed(self):
        xml_str = to_xml(SAMPLE_MD_WITH_FM)
        root = ET.fromstring(xml_str)
        assert root.tag == "document"

    def test_metadata_elements(self):
        xml_str = to_xml(SAMPLE_MD_WITH_FM)
        root = ET.fromstring(xml_str)
        meta_el = root.find("metadata")
        assert meta_el is not None
        assert meta_el.find("title").text == "Test RFP"
        assert meta_el.find("issuer").text == "Acme Corp"
        # null fields produce self-closing tags with no text
        assert meta_el.find("deadline").text is None

    def test_content_cdata(self):
        xml_str = to_xml(SAMPLE_MD_WITH_FM)
        assert "<![CDATA[" in xml_str
        assert "# Introduction" in xml_str


# ---------------------------------------------------------------------------
# JSON export
# ---------------------------------------------------------------------------

class TestToJson:
    def test_valid_json(self):
        result = json.loads(to_json(SAMPLE_MD_WITH_FM))
        assert "metadata" in result
        assert "content" in result

    def test_metadata_fields(self):
        result = json.loads(to_json(SAMPLE_MD_WITH_FM))
        assert result["metadata"]["title"] == "Test RFP"
        assert result["metadata"]["issuer"] == "Acme Corp"
        assert result["metadata"]["deadline"] is None

    def test_content_body(self):
        result = json.loads(to_json(SAMPLE_MD_WITH_FM))
        assert "# Introduction" in result["content"]

    def test_bare_markdown(self):
        result = json.loads(to_json(SAMPLE_MD_BARE))
        assert result["metadata"] == {}
        assert "# Introduction" in result["content"]
