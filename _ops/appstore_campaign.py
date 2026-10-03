#!/usr/bin/env python3
"""Rewrite every App Store link to Apple's campaign format so App Analytics attributes
website downloads per page:  https://apps.apple.com/app/apple-store/id<APP>?pt=<provider>&ct=<tag>&mt=8

The provider token (pt) belongs to the developer account (same for all of Mohamed Elatabany's
apps; generated in App Store Connect's campaign link tool). ct ≤ 40 chars, one tag per page.
Run after adding pages; idempotent.
"""
import html, pathlib, re
from urllib.parse import urlencode, urlsplit

ROOT = pathlib.Path(__file__).resolve().parents[1]
APP, PROVIDER = "6746700862", "127826363"


def tag_for(path: pathlib.Path) -> str:
    rel = path.relative_to(ROOT).with_suffix("").as_posix()
    if rel == "index": return "web-home"
    folder, _, slug = rel.rpartition("/")
    prefix = {"guides": "g", "compare": "c"}.get(folder, "p")
    return f"web-{prefix}-{slug}"[:40]


for p in ROOT.rglob("*.html"):
    if p.relative_to(ROOT).as_posix().startswith("_ops"): continue
    def fix(m):
        u = urlsplit(html.unescape(m.group(1)))
        if u.hostname != "apps.apple.com" or APP not in u.path: return m.group(0)
        q = urlencode({"pt": PROVIDER, "ct": tag_for(p), "mt": "8"})
        return 'href="' + html.escape(f"https://apps.apple.com/app/apple-store/id{APP}?{q}", quote=True) + '"'
    s = p.read_text(); n = re.sub(r'href="([^"]+)"', fix, s)
    if n != s: p.write_text(n)
print("ok")
