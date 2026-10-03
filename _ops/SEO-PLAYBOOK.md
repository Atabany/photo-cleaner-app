# getphotocleaner.com — weekly SEO & AI-visibility playbook

Read this whole file before changing the site. It is the brief for the weekly content routine and
for any human editing the site. Goal: rank for high-intent iPhone photo-cleanup queries and be the
page ChatGPT, Perplexity, Gemini, Claude and Copilot quote and recommend.

## Facts (single source of truth — never contradict, never invent)

- App: **Photo Cleaner** (App Store: "Photo Cleaner: Swipe Cleanup"), by Mohamed Elatabany.
  App Store: https://apps.apple.com/app/id6746700862 — add `?ct=site-<page-slug>` on CTA links.
- iPhone and iPad, iOS 17 or later. Languages: EN, FR, DE, JA, RU, ZH-Hans, ES (+ IT, PT, KO, AR listings).
- Swipe left to delete, right to keep. Nothing is deleted until you review the **Trash Bin** and
  confirm in the iOS dialog; then iOS keeps items in **Recently Deleted** for 30 days.
- Similars / Duplicates (groups near-identical shots, marks the best one), Blur Detection
  (on-device), Largest Files (big 4K videos first), Screenshots, Videos, Live Photos, Bursts,
  Favorites, messaging-app albums, Memory Lane (by month), Today's Throwback, stats & streaks.
- 100% on-device: no account, no photo uploads, no data collection, works offline.
- Free to download; **100 free deletions (one-time allowance)**. Pro: unlimited deletions and premium
  tools; weekly, monthly, yearly (yearly starts with a 3-day free trial) and a one-time lifetime option.
- Rating: use the live value from `https://itunes.apple.com/lookup?id=6746700862&country=us`
  (`averageUserRating`, `userRatingCount`) — round to one decimal; update the JSON-LD on index.html
  if it changed.
- **Never**: print prices; claim "AI-powered"; invent stats, reviews, awards, press; mention
  "SwiftSweep" or the developer's other app ("Clarity"); promise results ("free 50 GB").

## Weekly task (one page per week, quality over volume)

1. Pick the top `todo` topic in `_ops/topics.md` (or a better one you can justify from real search
   demand: "People also ask", Reddit/Apple Community questions, Google autocomplete). Skip anything
   already covered by an existing page (check titles in sitemap.xml) — improve that page instead.
2. Write the page as `guides/<slug>.html` (or `compare/<slug>.html` for comparisons) by copying the
   structure of an existing guide (`guides/delete-blurry-photos-iphone.html`): same header, nav,
   breadcrumb, `aside.facts` fact block, footer, Smart App Banner meta, OG/Twitter tags, canonical
   `https://getphotocleaner.com/<path>`, Article JSON-LD (author Mohamed Elatabany,
   datePublished/dateModified = today), visible "Updated <Month YYYY>".
3. Content rules:
   - Answer the query in the first 2–3 sentences (this is what AI assistants quote).
   - Built-in iOS method first (accurate steps for iOS 17/18/26, real menu names), then where
     Photo Cleaner helps. Honest: say when the built-in way is enough.
   - 800–1,300 words, H2/H3 question-style headings, numbered steps, a short FAQ (3–5 Q&As) at the end.
   - Unique `<title>` ≤ 60 chars with the main query; meta description ≤ 155 chars.
   - 3+ internal links to related guides, and add a link TO the new page from 2+ existing pages
     (related-guides lists) and from index.html's guides section if it has one.
   - No keyword stuffing, no fluff, no fake numbers. Cite Apple Support URLs for iOS steps.
4. Update `sitemap.xml` (new URL, lastmod today; bump lastmod of pages you edited), `llms.txt`
   (one line: title + URL + one-sentence summary) and `llms-full.txt` (condensed version).
5. Run `python3 _ops/validate.py` — fix everything until it prints `OK`.
6. Mark the topic `done (YYYY-MM-DD, path)` in `_ops/topics.md`; add 2 new well-justified topics to
   the backlog if it has fewer than 8 `todo`s.
7. Commit to `main` with message `content: <page title>` and push. GitHub Pages deploys it.
8. Run `sh _ops/indexnow.sh <new-url> <every-edited-url>` to notify Bing/Yandex/Seznam/Naver.

## Quarterly (the routine does this on the first Monday of Jan/Apr/Jul/Oct)

- Re-check every guide's iOS steps against the current iOS version; fix and bump dateModified.
- Re-check `compare/` pages against competitors' current App Store pages; "—" when unsure.

## Never

- Never delete or rename existing URLs (they rank). Never change CNAME, BingSiteAuth.xml,
  google*.html, the IndexNow key file, or robots.txt bot rules.
- Never add tracking scripts, ads, external JS, or Google Fonts.
