#!/usr/bin/env python3
"""Copy the shared page chrome (head assets, header, sticky download bar, footer) onto every page
from one template, so the HTML files never drift apart.

    python3 _ops/sync_chrome.py           rewrite every page that is out of date
    python3 _ops/sync_chrome.py --check   change nothing; exit 1 and list pages that are out of date

Template: _ops/chrome/<lang>.html, chosen by the page's <html lang="..."> (falls back to en.html).
In the template a block sits between <!-- block:NAME --> and <!-- /block:NAME -->; on a page the same
block sits between <!-- chrome:NAME --> and <!-- /chrome:NAME -->. Blocks: head, header, footer.
Placeholders in the template:
  {root}  path from the page to the site root: "" for top-level pages, "../" one folder down.
          404.html is served at any depth; its <base href="/"> makes "" correct there too.
  {ct}    the page's App Store campaign tag, from tag_for() in appstore_campaign.py (one tag per page).
Links in the chrome that point at the page itself get aria-current="page".

A page without markers (for example one copied from an old version) is migrated: the legacy skip link
and <header class="site-header">, the <footer class="site-footer"> plus its main.js tag, and the
theme-color, icon and stylesheet tags in <head> are replaced by marked blocks. Idempotent.
"""
import pathlib
import posixpath
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_ops"))
from appstore_campaign import tag_for  # noqa: E402

TEMPLATES = ROOT / "_ops" / "chrome"
BLOCKS = ("head", "header", "footer")
VIEWPORT = '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'


def pages():
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith("_ops/") or re.match(r"google[0-9a-f]+\.html$", rel):
            continue
        yield p, rel


def load_template(lang):
    path = TEMPLATES / f"{lang}.html"
    if not path.exists():
        path = TEMPLATES / "en.html"
    text = path.read_text()
    blocks = {}
    for name in BLOCKS:
        m = re.search(rf"<!-- block:{name} -->\n(.*?)<!-- /block:{name} -->", text, re.S)
        if not m:
            sys.exit(f"{path.name}: missing block:{name}")
        blocks[name] = m.group(1)
    return blocks


def mark_current(html, rel):
    """Add aria-current="page" to chrome links that resolve to this page (not to #fragments)."""
    here = posixpath.dirname(rel)

    def fix(m):
        href = m.group(1)
        if "#" in href or "://" in href or "aria-current" in m.group(0):
            return m.group(0)
        target = posixpath.normpath(posixpath.join(here, href))
        return m.group(0) + ' aria-current="page"' if target == rel else m.group(0)

    return re.sub(r'<a (?:class="[^"]*" )?href="([^"]+)"', fix, html)


def render(block, rel):
    root = "../" * rel.count("/")
    out = block.replace("{root}", root).replace("{ct}", tag_for(ROOT / rel))
    return mark_current(out, rel)


def migrate(s, name, rel):
    """Wrap legacy (unmarked) chrome in markers so the normal replacement can run."""
    start, end = f"<!-- chrome:{name} -->", f"<!-- /chrome:{name} -->"
    if name == "head":
        head_end = s.find("</head>")
        head = s[:head_end]
        legacy = (r'<meta name="theme-color"[^>]*>\n?', r'<link rel="icon"[^>]*>\n?',
                  r'<link rel="apple-touch-icon"[^>]*>\n?')
        sheet = re.search(r'<link rel="stylesheet" href="[^"]*style\.css[^"]*">\n?', head)
        anchor = sheet.start() if sheet else head_end
        before, after = head[:anchor], head[anchor:]
        for pat in legacy:
            before, after = re.sub(pat, "", before), re.sub(pat, "", after)
        after = re.sub(r'<link rel="stylesheet" href="[^"]*style\.css[^"]*">\n?', "", after, count=1)
        return before + f"{start}\n{end}\n" + after + s[head_end:]
    if name == "header":
        pat = r'(?:<a class="skip" href="#main">Skip to content</a>\s*)?<header class="site-header">.*?</header>\n?'
    else:
        pat = (r'(?:<div class="sticky-cta">.*?</div>\s*)?<footer class="site-footer">.*?</footer>'
               r'(?:\s*<script src="[^"]*main\.js[^"]*" defer></script>)?\n?')
    m = re.search(pat, s, re.S)
    if not m:
        sys.exit(f"{rel}: no chrome:{name} markers and no legacy {name} to migrate")
    return s[:m.start()] + f"{start}\n{end}\n" + s[m.end():]


def sync(s, rel):
    lang = (re.search(r'<html[^>]*\blang="([^"]+)"', s) or [None, "en"])[1].split("-")[0]
    blocks = load_template(lang)
    s = re.sub(r'<meta name="viewport" content="[^"]*">', VIEWPORT, s, count=1)
    for name in BLOCKS:
        start, end = f"<!-- chrome:{name} -->", f"<!-- /chrome:{name} -->"
        if start not in s:
            s = migrate(s, name, rel)
        i, j = s.index(start) + len(start), s.index(end)
        s = s[:i] + "\n" + render(blocks[name], rel) + s[j:]
    return s


def main():
    check = "--check" in sys.argv
    stale = []
    for p, rel in pages():
        s = p.read_text()
        n = sync(s, rel)
        if n != s:
            stale.append(rel)
            if not check:
                p.write_text(n)
    if check:
        if stale:
            print("chrome out of date (run python3 _ops/sync_chrome.py):\n  " + "\n  ".join(stale))
            sys.exit(1)
        print("chrome OK")
    else:
        print(f"chrome synced: {len(stale)} page(s) updated")


if __name__ == "__main__":
    main()
