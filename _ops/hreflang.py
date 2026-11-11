#!/usr/bin/env python3
"""Write the hreflang block of every page that exists in more than one language.

    python3 _ops/hreflang.py           rewrite pages that are out of date
    python3 _ops/hreflang.py --check   change nothing; exit 1 and list them

English pages live at the root, translations at /<lang>/ with the same path. A page gets one
<link rel="alternate"> per language it exists in, plus x-default (English), between
<!-- hreflang --> and <!-- /hreflang --> right after its canonical link. Pages that exist only in
English get an empty block. Idempotent.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "https://getphotocleaner.com/"
LANGS = ("fr", "de", "es")
START, END = "<!-- hreflang -->", "<!-- /hreflang -->"


def url(rel):
    return BASE + re.sub(r"(^|/)index\.html$", r"\1", rel)


def base_rel(rel):
    lang, _, rest = rel.partition("/")
    return (lang, rest) if lang in LANGS else ("en", rel)


def block(rel):
    _, base = base_rel(rel)
    if base == "404.html":
        return ""
    have = [("en", base)] + [(l, f"{l}/{base}") for l in LANGS if (ROOT / l / base).exists()]
    if len(have) < 2:
        return ""
    lines = [f'<link rel="alternate" hreflang="{l}" href="{url(r)}">' for l, r in have]
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{url(base)}">')
    return "\n".join(lines) + "\n"


def sync(s, rel):
    if START not in s:
        m = re.search(r'<link rel="canonical"[^>]*>\n?', s)
        if not m:
            return s
        s = s[:m.end()] + f"{START}\n{END}\n" + s[m.end():]
    i, j = s.index(START) + len(START), s.index(END)
    return s[:i] + "\n" + block(rel) + s[j:]


def pages():
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith("_ops/") or re.match(r"google[0-9a-f]+\.html$", rel):
            continue
        yield p, rel


def main():
    check, stale = "--check" in sys.argv, []
    for p, rel in pages():
        s = p.read_text()
        n = sync(s, rel)
        if n != s:
            stale.append(rel)
            if not check:
                p.write_text(n)
    if check and stale:
        print("hreflang out of date (run python3 _ops/hreflang.py):\n  " + "\n  ".join(stale))
        sys.exit(1)
    print("hreflang OK" if check else f"hreflang synced: {len(stale)} page(s) updated")


if __name__ == "__main__":
    main()
