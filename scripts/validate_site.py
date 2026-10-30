#!/usr/bin/env python3
"""Validate static Fresh Ride HTML, clean URLs, schema, and sitemap."""

import json
import os
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = []
        self.in_title = False
        self.h1 = 0
        self.description = None
        self.canonical = None
        self.refs = []
        self.jsonld = []
        self.in_jsonld = False
        self.json_buffer = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.h1 += 1
        if tag == "meta" and attrs.get("name") == "description":
            self.description = attrs.get("content")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")
        if tag in {"a", "img", "script", "link"}:
            key = "href" if tag in {"a", "link"} else "src"
            if attrs.get(key):
                self.refs.append((tag, attrs[key]))
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_jsonld = True
            self.json_buffer = []

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "script" and self.in_jsonld:
            self.in_jsonld = False
            self.jsonld.append("".join(self.json_buffer))

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)
        if self.in_jsonld:
            self.json_buffer.append(data)


def resolve_clean_url(root, ref):
    parsed = urlparse(ref)
    if parsed.scheme or parsed.netloc or ref.startswith(("#", "tel:", "mailto:")):
        return None
    path = parsed.path
    if not path or path == "/":
        return root / "index.html"
    candidate = root / path.lstrip("/")
    if candidate.is_file():
        return candidate
    html_candidate = Path(str(candidate) + ".html")
    if html_candidate.is_file():
        return html_candidate
    index_candidate = candidate / "index.html"
    if index_candidate.is_file():
        return index_candidate
    return candidate


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    pages = sorted(page for page in root.rglob("*.html") if not any(part in {".git", "node_modules", ".vercel"} for part in page.parts))
    pages = list(dict.fromkeys(page for page in pages if page.is_file()))
    errors = []
    titles = {}
    canonicals = {}

    for page in pages:
        source = page.read_text(encoding="utf-8")
        parser = PageParser()
        parser.feed(source)
        rel = page.relative_to(root)
        title = "".join(parser.title).strip()
        if parser.h1 != 1:
            errors.append(f"{rel}: expected one H1, found {parser.h1}")
        if not title:
            errors.append(f"{rel}: missing title")
        elif title in titles:
            errors.append(f"{rel}: duplicate title also used by {titles[title]}")
        else:
            titles[title] = rel
        if not parser.description or len(parser.description) < 70:
            errors.append(f"{rel}: missing or thin meta description")
        if not parser.canonical:
            errors.append(f"{rel}: missing canonical")
        elif parser.canonical in canonicals:
            errors.append(f"{rel}: duplicate canonical also used by {canonicals[parser.canonical]}")
        else:
            canonicals[parser.canonical] = rel
        if "fonts.googleapis.com" in source or "fonts.gstatic.com" in source:
            errors.append(f"{rel}: external Google Fonts dependency remains")
        if not parser.jsonld:
            errors.append(f"{rel}: missing JSON-LD")
        for index, block in enumerate(parser.jsonld, start=1):
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"{rel}: invalid JSON-LD block {index}: {exc}")
        for tag, ref in parser.refs:
            target = resolve_clean_url(root, ref)
            if target is not None and not target.exists():
                errors.append(f"{rel}: missing {tag} target {ref}")

    sitemap_path = root / "sitemap.xml"
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls = [node.text for node in ET.parse(sitemap_path).findall("s:url/s:loc", namespace)]
    sitemap_paths = {urlparse(url).path or "/" for url in sitemap_urls}
    canonical_paths = {urlparse(url).path or "/" for url in canonicals}
    if sitemap_paths != canonical_paths:
        errors.append(f"sitemap/canonical mismatch: sitemap={sorted(sitemap_paths)} canonical={sorted(canonical_paths)}")

    for required in ("robots.txt", "llms.txt", "sitemap.xml", "fonts.css", "content-pages.css"):
        if not (root / required).is_file():
            errors.append(f"missing required file: {required}")

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"VALIDATION OK — {len(pages)} pages, {len(canonicals)} canonicals, {len(sitemap_urls)} sitemap URLs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
