#!/usr/bin/env python3
"""Validate the static site before publishing. Prints OK or a list of problems (exit 1).

Checks: internal links/assets resolve; JSON-LD parses; one <h1>; title ≤ 60 and meta description
≤ 155; canonical points at https://getphotocleaner.com/; every indexable page is in sitemap.xml
and llms.txt; images have alt/width/height; banned strings; free-tier wording; shared chrome
(header, footer, sticky bar, head assets) present and identical to _ops/chrome/<lang>.html.
"""
import json, pathlib, re, sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "_ops"))
import sync_chrome  # noqa: E402
import hreflang  # noqa: E402

LANGS = hreflang.LANGS
PAGE_LANG = lambda rel: rel.split('/')[0] if rel.split('/')[0] in LANGS else 'en'
BASE = "https://getphotocleaner.com/"
BANNED = [r"swift ?sweep", r"\bclarity\b", r"ai-powered", r"\$\d", r"\d ?€", r"€ ?\d", r"50 (free )?deletions", r"per week", r"every week"]
problems = []


class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.imgs = []; self.h1 = 0; self.title = ""; self.in_title = False
        self.desc = None; self.canon = None; self.ld = []; self.in_ld = False; self.buf = ""; self.noindex = False

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag in ("a", "link") and a.get("href"): self.links.append(a["href"])
        if tag in ("img", "script", "source", "video") and (a.get("src") or a.get("poster")):
            self.links.append(a.get("src") or a.get("poster"))
        if tag == "img": self.imgs.append(a)
        if tag == "h1": self.h1 += 1
        if tag == "title": self.in_title = True
        if tag == "meta" and a.get("name") == "description": self.desc = a.get("content", "")
        if tag == "meta" and a.get("name") == "robots" and "noindex" in a.get("content", ""): self.noindex = True
        if tag == "link" and a.get("rel") == "canonical": self.canon = a.get("href")
        if tag == "script" and a.get("type") == "application/ld+json": self.in_ld = True; self.buf = ""

    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
        if tag == "script" and self.in_ld: self.ld.append(self.buf); self.in_ld = False

    def handle_data(self, d):
        if self.in_title: self.title += d
        if self.in_ld: self.buf += d


sitemap = (ROOT / "sitemap.xml").read_text()
llms = (ROOT / "llms.txt").read_text()
for f in sorted(ROOT.rglob("*.html")):
    rel = f.relative_to(ROOT).as_posix()
    if rel.startswith("_ops/") or re.match(r"google[0-9a-f]+\.html", rel): continue
    html = f.read_text(); p = P(); p.feed(html)
    for href in p.links:
        if re.match(r"^(https?:|mailto:|tel:|#|data:)", href): continue
        target = (ROOT / href.split("#")[0].split("?")[0]) if href.startswith("/") else (f.parent / href.split("#")[0].split("?")[0])
        if href.startswith("/"): target = ROOT / href.lstrip("/").split("#")[0].split("?")[0]
        if target.is_dir(): target = target / "index.html"
        if not target.exists(): problems.append(f"{rel}: broken link {href}")
    for raw in p.ld:
        try: json.loads(raw)
        except Exception as e: problems.append(f"{rel}: JSON-LD invalid ({e})")
    try:
        if sync_chrome.sync(html, rel) != html:
            problems.append(f"{rel}: shared chrome missing or out of date (run python3 _ops/sync_chrome.py)")
    except SystemExit as e:
        problems.append(f"{rel}: {e}")
    if hreflang.sync(html, rel) != html:
        problems.append(f"{rel}: hreflang block missing or out of date (run python3 _ops/hreflang.py)")
    lang = PAGE_LANG(rel)
    m = re.search(r'<html[^>]*\blang="([^"]+)"', html)
    if not m or m.group(1).split("-")[0] != lang: problems.append(f"{rel}: <html lang> should be {lang}")
    if lang != "en" and not (ROOT / rel.split("/", 1)[1]).exists(): problems.append(f"{rel}: no English page at the same path")
    if lang != "en" and rel != "404.html":
        og = dict(re.findall(r'<meta property="(og:url|og:locale)" content="([^"]*)"', html))
        if og.get("og:url") != p.canon: problems.append(f"{rel}: og:url differs from the canonical")
        if og.get("og:locale") != {"fr": "fr_FR", "de": "de_DE", "es": "es_ES"}[lang]: problems.append(f"{rel}: og:locale should match {lang}")
        if f'"inLanguage": "{lang}"' not in html: problems.append(f"{rel}: JSON-LD has no inLanguage {lang}")
    if rel == "404.html" or p.noindex: continue
    if p.h1 != 1: problems.append(f"{rel}: {p.h1} <h1> elements")
    if not p.title or len(p.title.strip()) > 60: problems.append(f"{rel}: title length {len(p.title.strip())}")
    if not p.desc or len(p.desc) > 155: problems.append(f"{rel}: meta description length {len(p.desc or '')}")
    url = BASE + re.sub(r"(^|/)index\.html$", r"\1", rel)
    if p.canon != url: problems.append(f"{rel}: canonical {p.canon} != {url}")
    if url not in sitemap: problems.append(f"{rel}: missing from sitemap.xml")
    if lang == "en" and rel != "index.html" and url not in llms and rel not in llms: problems.append(f"{rel}: missing from llms.txt")
    for img in p.imgs:
        for k in ("alt", "width", "height"):
            if k not in img: problems.append(f"{rel}: <img {img.get('src')}> missing {k}")
    text = re.sub(r"<[^>]+>", " ", html).lower()
    for b in BANNED:
        if re.search(b, text): problems.append(f"{rel}: banned/outdated phrase /{b}/")

# Every guide and comparison must be linked from every page's footer, in the page's own language.
def content(prefix):
    return sorted(f.relative_to(ROOT).as_posix() for d in ("guides", "compare") for f in (ROOT / prefix / d).glob("*.html"))
for f in sorted(ROOT.rglob("*.html")):
    rel = f.relative_to(ROOT).as_posix()
    if rel.startswith("_ops/") or re.match(r"google[0-9a-f]+\.html", rel): continue
    lang = PAGE_LANG(rel)
    footer = f.read_text().split("<footer", 1)[-1]
    for c in content("" if lang == "en" else lang):
        if "/" + c + '"' not in footer.replace('href="', 'href="/'): problems.append(f"{rel}: footer does not link {c}")

for txt in ("llms.txt", "llms-full.txt", "robots.txt"):
    t = (ROOT / txt).read_text().lower()
    for b in BANNED:
        if re.search(b, t): problems.append(f"{txt}: banned/outdated phrase /{b}/")

if problems:
    print("\n".join(problems)); sys.exit(1)
print("OK")
