# getphotocleaner.com — weekly SEO & AI-visibility playbook

Read this whole file before changing the site. It is the brief for the weekly content routine and
for any human editing the site. Goal: rank for high-intent iPhone photo-cleanup queries and be the
page ChatGPT, Perplexity, Gemini, Claude and Copilot quote and recommend.

## Facts (single source of truth — never contradict, never invent)

- App: **Photo Cleaner** (App Store: "Photo Cleaner: Swipe Cleanup"), by Mohamed Elatabany.
  App Store links: always Apple's campaign format `https://apps.apple.com/app/apple-store/id6746700862?pt=127826363&ct=<tag>&mt=8`
  — run `python3 _ops/appstore_campaign.py` after adding a page (sets one tag per page; App Analytics
  → Sources → Web/Campaigns attributes downloads, after Apple's privacy thresholds).
- iPhone and iPad, iOS 17 or later. Languages: EN, FR, DE, JA, RU, ZH-Hans, ES (+ IT, PT, KO, AR listings).
- Swipe left to delete, right to keep. Nothing is deleted until you review the **Trash Bin** and
  confirm in the iOS dialog; then iOS keeps items in **Recently Deleted** for 30 days.
- Similars / Duplicates (groups near-identical shots, marks the best one), Blur Detection
  (on-device), Largest Files (big 4K videos first), Screenshots, Videos, Live Photos, Bursts,
  Favorites, messaging-app albums, Memory Lane (by month), Today's Throwback, stats & streaks.
- 100% on-device: no account, no photo uploads, no data collection, works offline.
- Free to download; **100 free deletions (one-time allowance)**. Pro: unlimited deletions and premium
  tools; weekly, monthly, yearly (no free trial) and a one-time lifetime option.
- Rating: use the live value from `https://itunes.apple.com/lookup?id=6746700862&country=us`
  (`averageUserRating`, `userRatingCount`) — round to one decimal. Every run, if either changed, update
  ALL of: the JSON-LD aggregateRating on index.html, the hero line ("4.6 on the App Store · rated by
  N users"), the reviews intro ("Rated 4.6★ by N App Store users"), every fact block ("4.6★ on the App
  Store, from N ratings"), and llms.txt / llms-full.txt. Never round the count up.
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

## Growth batch — 18 October 2026

Prepared `about.html` and `tools/storage-calculator.html`; run `_ops/build_growth_tools.py` then `_ops/validate.py`. New pages and author/tool links use valid per-page campaigns. The deployment was based on the current public main branch and retains the existing Recently Deleted guide. Private app source has pre-existing edits; do not overwrite this checkout wholesale from that older source site.

The existing large-video guide was also refined for observed Search Console queries about sorting iPhone videos by file size. Its URL is preserved; title, direct answer and modification date reflect this review. Query observations are small-sample evidence, not search-volume estimates.

## 2026-11-04 — mass delete guide

Owner asked for one new guide. Added `guides/mass-delete-photos-iphone.html` from the `todo` backlog: how to select and delete many photos at once. The closest pages cover one category (screenshots), a daily swipe habit (camera roll) or the follow-up step (Recently Deleted); none answers the general selection question. Choosing it is editorial judgment: no Search Console query or search volume was read for this run.

Contents: Select plus drag steps per iOS version, a table of which grid to delete from, iCloud and Shared Library checks, getting the storage back, when drag-select is the wrong tool, exact app steps and a free-limit worked example (100 allowance, 40 used, 250 in the Trash Bin: Select All selects 60, 190 stay). Article, BreadcrumbList and FAQPage JSON-LD match the visible text. Campaign tag `web-g-mass-delete` is set through `TAG_OVERRIDES` in `appstore_campaign.py` because the default would be 31 characters.

Sources checked 4 November against the iOS 27, 26, 18 and 17 editions: Apple's iPhone guide (delete or hide photos, media types), Photos for Mac (delete, album versus Smart Album) and iCloud.com (shared libraries). Only the iOS 17 edition mentions dragging for Delete (iOS 18 mentions it for Hide), and no edition documents Select All for the Library, so the page says that rather than asserting either way for every screen. Command-A on Mac is standard behavior, not from those pages. App labels checked in `TrashBinScreen.swift`, Home views and `Localizable.strings` at build 58 (2.2.0). Live lookup: 2.2.0, 4.6 from 35 US ratings, unchanged.

Linked from the home guide cards and home footer, and from the camera roll, screenshots and Recently Deleted guides. The other pages' footer lists were left alone. The table uses inline `min-width:0` and `white-space:normal` on this page because the shared table CSS hides two of three columns at 390 px; other tables keep the shared rule.

Verified: validator OK, desktop 1280 and true 390 px read, no horizontal overflow. Commit `a286b7a` deployed through pages-build-deployment; changed pages return 200 and the checked files match the commit byte for byte. IndexNow HTTP 200 for 5 URLs (received, not proof of indexing).

Known issues, not changed: `guides/recently-deleted-photos-iphone.html` has a footer link labelled "Delete blurry photos on iPhone" that points to itself. Open owner decision: the site shows 4.6 from 35 US ratings (lookup rule above), while the app repo recorded a rule on 2026-10-22 to show the App Store Connect global value (4.7 from 118 as of 2026-10-04). This run did not choose between them.

Source flow: this repo was ahead of `site/` in the app repo, so the guide was written here and `site/` was then mirrored from it. Edit here or in `site/`, then copy across in the same run.
