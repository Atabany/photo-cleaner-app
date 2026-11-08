"""Add a transparent author page and local-only calculator; preserve existing copy."""
from pathlib import Path
import html
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://getphotocleaner.com/'
DATE = '2026-10-18'

def page(path, title, description, content):
    prefix = '../' if '/' in path else ''
    source = (ROOT / 'guides/delete-blurry-photos-iphone.html').read_text()
    head = source.split('</head>')[0]
    if prefix:
        head += '<style>#storage-form fieldset {border:1px solid var(--border);border-radius:16px;padding:20px;min-width:0} #storage-form p {display:grid;grid-template-columns:1fr 1fr;gap:16px} #storage-form label {display:grid;gap:6px;min-width:0} #storage-form input {box-sizing:border-box;width:100%;min-width:0;padding:10px;font:inherit} #storage-form button {font:inherit;padding:10px 16px;cursor:pointer} #storage-result {display:block;margin:20px 0} @media(max-width:480px){#storage-form p{grid-template-columns:1fr}}</style>'
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', '', head, flags=re.S)
    head = re.sub(r'<title>.*?</title>', '<title>' + title + '</title>', head)
    for attr, key, value in [('name', 'description', description), ('property', 'og:title', title), ('property', 'og:description', description), ('property', 'og:url', BASE + path), ('name', 'twitter:title', title), ('name', 'twitter:description', description)]:
        head = re.sub(r'(<meta ' + attr + '="' + key + '" content=")[^"]*', lambda m: m[1] + html.escape(value, quote=True), head)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="' + BASE + path + '">', head)
    if not prefix:
        head = head.replace('../assets/', 'assets/')
    schemas = [{'@context': 'https://schema.org', '@type': 'AboutPage' if path == 'about.html' else 'WebPage', 'name': title, 'url': BASE + path, 'description': description, 'author': {'@type': 'Person', 'name': 'Mohamed Elatabany', 'url': BASE + 'about.html'}}, {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Photo Cleaner', 'item': BASE}, {'@type': 'ListItem', 'position': 2, 'name': title, 'item': BASE + path}]}]
    if path == 'about.html':
        schemas.append({'@context': 'https://schema.org', '@type': 'Person', '@id': BASE + 'about.html#author', 'name': 'Mohamed Elatabany', 'url': BASE + 'about.html', 'sameAs': ['https://github.com/Atabany', 'https://apps.apple.com/us/developer/mohamed-elatabany/id1814429185']})
    header = re.search(r'<header.*?</header>', source, re.S)[0]
    footer = re.search(r'<footer.*?</footer>', source, re.S)[0]
    if not prefix:
        header = header.replace('../', '')
        footer = footer.replace('../', '')
    campaign = 'web-tool-storage' if prefix else 'web-about'
    cta = f'<aside class="facts"><h2>Review your library with Photo Cleaner.</h2><p>Find repeated shots, blurry photos, screenshots and large videos. Review your choices before deletion.</p><a class="store-cta" href="https://apps.apple.com/app/apple-store/id6746700862?pt=127826363&amp;ct={campaign}&amp;mt=8"><img class="store-icon" src="{prefix}assets/apple-touch-icon.png" width="56" height="56" alt="Photo Cleaner app icon"><img class="store-badge" src="{prefix}assets/app-store-badge.svg" width="150" height="50" alt="Download on the App Store"></a></aside>'
    out = head + '<script type="application/ld+json">' + json.dumps(schemas, ensure_ascii=False) + '</script></head><body><a class="skip" href="#main">Skip to content</a>' + header + '<main id="main"><div class="wrap narrow"><article class="article"><h1>' + title + '</h1><p class="updated">By <a href="' + prefix + 'about.html">Mohamed Elatabany</a> · Updated 18 October 2026</p>' + content + '</article>' + cta + '</div></main>' + footer
    if prefix:
        out += '<script src="../assets/storage-calculator.js" defer></script>'
    out += '</body></html>\n'
    target = ROOT / path
    target.parent.mkdir(exist_ok=True)
    target.write_text(out)

page('about.html', 'About Photo Cleaner and Its Developer', 'Meet Mohamed Elatabany, developer of Photo Cleaner: Swipe Cleanup. Learn how the official site checks its guides and handles corrections.', '''
<p class="lead">I’m Mohamed Elatabany, the developer of Photo Cleaner: Swipe Cleanup. This is the app’s official website, with practical guides for reviewing an iPhone or iPad photo library.</p>
<h2>What the app is for</h2><p>Photo Cleaner helps you find photos and videos worth reviewing: duplicates and similar shots, blurry images, screenshots and large files. You decide what to keep. Marking an item for removal is followed by a review before confirmed deletion.</p>
<h2>How these guides are written</h2><p>I check app claims against its implementation and listing, and link Apple documentation for system behavior. Guides start with built-in options when they can solve the problem. Comparison pages are written by the maker of Photo Cleaner; they should be read with that relationship in mind.</p><p>Examples and calculator assumptions are illustrations, not measurements of your library. Neither the site nor the app can promise a particular amount of recovered storage.</p>
<h2>Photos, privacy and deletion</h2><p>Photo review happens on your device. Read the <a href="privacy.html">privacy policy</a> for the complete statement. With iCloud Photos, confirmed library deletion can synchronize to other devices; read the <a href="guides/iphone-storage-full-icloud-photos.html">iCloud storage guide</a> before choosing a cleanup strategy.</p>
<h2>Find a useful starting point</h2><ul><li><a href="tools/storage-calculator.html">Estimate the file sizes you want to review</a></li><li><a href="guides/delete-duplicate-photos-iphone.html">Try Apple’s duplicate-photo review first</a></li><li><a href="guides/find-large-videos-iphone.html">Look for large videos</a></li></ul>
<h2>Contact and corrections</h2><p>If a guide is unclear or a menu has changed, <a href="support.html">contact support</a>. Please include the page and your iOS version; personal photographs are usually unnecessary for a correction.</p><p><a href="https://github.com/Atabany">GitHub profile</a> · <a href="https://apps.apple.com/us/developer/mohamed-elatabany/id1814429185">Developer on the App Store</a></p>''')

page('tools/storage-calculator.html', 'iPhone Photo Storage Calculator', 'Estimate file sizes for photos, screenshots and videos using your own assumptions. Local-only calculator, reference examples and iCloud storage limits.', '''
<p class="lead">Estimate file bytes by multiplying an item count by its average size in MB, then divide by 1,000 for decimal GB. This calculator does not scan your library or measure recoverable iPhone storage.</p>
<form id="storage-form"><fieldset><legend>Enter non-overlapping groups</legend><p><label>Photos, excluding screenshots <input id="photo-count" type="number" min="0" max="1000000" step="1" value="100" required></label> <label>Average MB each <input id="photo-mb" type="number" min="0.001" max="1000000" step="any" value="3" required></label></p><p><label>Screenshots <input id="shot-count" type="number" min="0" max="1000000" step="1" value="100" required></label> <label>Average MB each <input id="shot-mb" type="number" min="0.001" max="1000000" step="any" value="1" required></label></p><p><label>Videos <input id="video-count" type="number" min="0" max="1000000" step="1" value="10" required></label> <label>Average MB each <input id="video-mb" type="number" min="0.001" max="1000000" step="any" value="200" required></label></p><button type="submit">Calculate file sizes</button></fieldset></form>
<output id="storage-result" for="photo-count photo-mb shot-count shot-mb video-count video-mb" aria-live="polite">Example: 2.4 GB of total file bytes. Videos contribute 2 GB.</output><p>Runs in your browser. No entries are sent or stored. The defaults are illustrative assumptions, not measured averages.</p><noscript><p>JavaScript is needed for interactive calculation. The formula and worked examples below are available without it.</p></noscript>
<h2>Worked examples without JavaScript</h2><div class="table-wrap"><table><caption>Decimal units: 1 GB = 1,000 MB. Each size is an assumption.</caption><thead><tr><th scope="col">Group</th><th scope="col">Count</th><th scope="col">Assumed MB each</th><th scope="col">Total</th></tr></thead><tbody><tr><th scope="row">Photos</th><td>100</td><td>3</td><td>300 MB = 0.3 GB</td></tr><tr><th scope="row">Screenshots</th><td>100</td><td>1</td><td>100 MB = 0.1 GB</td></tr><tr><th scope="row">Videos</th><td>10</td><td>200</td><td>2,000 MB = 2 GB</td></tr><tr><th scope="row">Combined</th><td>210</td><td>Mixed</td><td>2,400 MB = 2.4 GB</td></tr></tbody></table></div>
<h2>Use sizes from your own library</h2><p>Open an item’s information in Photos and sample a few unwanted examples. Video duration, format and resolution can change the size considerably. Enter photos and screenshots separately so the same file does not appear in two groups.</p>
<h2>Why this is not a free-space guarantee</h2><p>Optimize iPhone Storage can keep smaller local copies while originals remain in iCloud. Full file bytes can therefore differ from bytes stored on this phone. Apple’s Recently Deleted recovery stage also affects the deletion workflow. Check Settings → General → iPhone Storage for actual local usage.</p><p>Deleting through iCloud Photos synchronizes across devices using the same library. Keep a separate copy of irreplaceable media and review selections before confirming anything. This calculator cannot access, inspect or delete photos.</p>
<h2>Turn the estimate into a review</h2><p>Start with a small group contributing the largest total file size. Keep meaningful originals even if they are large. Try the <a href="../guides/find-large-videos-iphone.html">large-video guide</a>, <a href="../guides/delete-screenshots-iphone.html">screenshot cleanup</a> or <a href="../guides/delete-duplicate-photos-iphone.html">duplicate-photo guide</a>, then compare actual device storage.</p>
<h2>Sources and corrections</h2><p><a href="https://support.apple.com/en-us/105061">Apple: photo and video storage</a> · <a href="https://support.apple.com/en-us/104967">Apple: deleting photos</a> · <a href="../support.html">Suggest a correction</a>.</p>''')

(ROOT / 'assets/storage-calculator.js').write_text('''"use strict";
const form = document.getElementById("storage-form");
const output = document.getElementById("storage-result");
function updateStorage(event) {
  if (event) event.preventDefault();
  if (!form.reportValidity()) return;
  const groups = [["photo-count", "photo-mb", "Photos"], ["shot-count", "shot-mb", "Screenshots"], ["video-count", "video-mb", "Videos"]];
  const parts = groups.map(([count, size, label]) => ({label, mb: Number(document.getElementById(count).value) * Number(document.getElementById(size).value)}));
  if (parts.some(part => !Number.isFinite(part.mb) || part.mb < 0)) return;
  const total = parts.reduce((sum, part) => sum + part.mb, 0);
  const format = value => new Intl.NumberFormat(undefined, {maximumFractionDigits: 3}).format(value);
  output.textContent = `${format(total / 1000)} GB of total file bytes (${format(total)} MB). ${parts.map(part => `${part.label}: ${format(part.mb)} MB`).join("; ")}. This is not measured free phone storage.`;
}
if (form && output) form.addEventListener("submit", updateStorage);
''')

changed = {'about.html', 'tools/storage-calculator.html'}
for p in ROOT.rglob('*.html'):
    if '_ops' in p.parts or p.relative_to(ROOT).as_posix() in changed or p.name.startswith('google'):
        continue
    s = p.read_text()
    old = s
    prefix = '../' if p.parent != ROOT else ''
    s = s.replace('· By Mohamed Elatabany', '· By <a href="' + prefix + 'about.html">Mohamed Elatabany</a>')
    if '<li><a href="' + prefix + 'about.html">About the developer</a></li>' not in s:
        s = s.replace('<li><a href="' + prefix + 'support.html">Support</a></li>', '<li><a href="' + prefix + 'about.html">About the developer</a></li><li><a href="' + prefix + 'tools/storage-calculator.html">Storage calculator</a></li><li><a href="' + prefix + 'support.html">Support</a></li>')
    if s != old:
        p.write_text(s)
        changed.add(p.relative_to(ROOT).as_posix())
ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('', ns)
tree = ET.parse(ROOT / 'sitemap.xml')
known = {x.text for x in tree.getroot().iter('{' + ns + '}loc')}
for path in sorted(changed):
    if path == '404.html':
        continue
    url = BASE + ('' if path == 'index.html' else path)
    if url not in known:
        node = ET.SubElement(tree.getroot(), '{' + ns + '}url')
        ET.SubElement(node, '{' + ns + '}loc').text = url
        ET.SubElement(node, '{' + ns + '}lastmod').text = DATE
ET.indent(tree, space='  ')
tree.write(ROOT / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
for name in ['llms.txt', 'llms-full.txt']:
    p = ROOT / name
    text = p.read_text()
    if BASE + 'about.html' not in text:
        text += '\n## Author and local tool\n- [About the developer](' + BASE + 'about.html)\n- [Photo storage calculator](' + BASE + 'tools/storage-calculator.html): counts × assumed MB per item, divided by 1,000 for decimal GB. No scan or upload; estimates file bytes, not recoverable local storage.\n'
        p.write_text(text)
subprocess.run([sys.executable, str(ROOT / '_ops/appstore_campaign.py')], check=True)
subprocess.run([sys.executable, str(ROOT / '_ops/sync_chrome.py')], check=True)  # restore the shared chrome (2026-11)
print('Added author page, local calculator and internal discovery links.')
