# Design system — visual language and component vocabulary

This covers the **full hub-page deliverable** (see `SKILL.md`'s note on the
two deliverable shapes) — for the **toast** deliverable, see
`references/toast-spec.md` instead; it's a much smaller component and
doesn't use most of what's below.

Every Custom Release Notes hub page is a **single standalone HTML file**: all
CSS inline in a `<style>` block, all images inline as base64 `data:` URIs, no
external JS libraries. It must open correctly from `file://` with no server
and no network dependency other than the Google Fonts CDN link (fonts are the
one allowed external reference — everything else is embedded).

Start from `templates/base-template.html` in this skill for every new page —
don't design new CSS from scratch. It contains the full token set and every
component below, with `{{PLACEHOLDER}}` text markers and `ASSET:filename.png`
image markers ready to fill in.

## Tokens

| Token | Value | Use |
|---|---|---|
| `--red` | `#FA0F00` | Primary brand accent (Adobe red) — CTAs, active tab underline, links |
| `--red-dark` | `#D80000` | Hover state for red elements |
| `--ink` | `#161616` | Primary text, dark backgrounds (ctaband) |
| `--gray` | `#5B5B60` | Secondary/body text |
| `--off` | `#FAF9F7` | Page background |
| `--white` | `#ffffff` | Card backgrounds |
| `--line` | `#ECEAE6` | Hairline borders |
| `--rose` / `--rose-ink` | `#FFE2EC` / `#8A1538` | Tag color 1 |
| `--lav` / `--lav-ink` | `#ECE7FF` / `#4B3B9E` | Tag color 2 |
| `--mint` / `--mint-ink` | `#E1F5EC` / `#146C43` | Tag color 3 |
| `--amber` / `--amber-ink` | `#FFF1DA` / `#8A5A00` | Callout/alert color — see below, not a rotation color |
| `--radius` | `24px` | Large card corner radius |
| `--wrap` | `1160px` (general) / `980–1080px` (narrower persona variants) | Max content width — narrower for filtered variants reads as more focused, not a hard rule |

Fonts (Google Fonts CDN, already wired in the template `<head>`):
- **Sora** (`.disp`) — all headings/display text, weights 400–800.
- **Source Sans 3** — body text (page default).
- **IBM Plex Mono** (`.mono`) — dates, availability stamps, small technical labels.

## Tag color rule

`tag-rose` / `tag-lav` / `tag-mint` are **rotated for visual variety within a
page** — they are *not* a fixed category→color mapping. The same category
(e.g. "Channels") can be rose in one file and lav in another. Just avoid
using the same color on two adjacent items in the same grid/section.

`tag-amber` is reserved differently: it flags something that needs a second
look — "Heads up", "Licensed feature", a governance/compliance category, or
similar callouts — not a fourth rotation color for ordinary items.

## Component inventory

All defined in `templates/base-template.html`; use the closest one, don't
invent a new pattern.

| Component (class) | Use for |
|---|---|
| `nav` + `.brand` + `.navlinks` | Sticky top nav, mirrors the tab bar buttons + a CTA link to the product page |
| `.hero` / `.hero-title` / `.hero-visual` | Page header: headline, one-liner, primary screenshot, optional `.mock-badge` caption |
| `.stats` | 4-cell factual stats strip under the hero (counts, throughput numbers) — shrink to 2 cells or omit for narrow personas where the numbers wouldn't be scoped to them |
| `.tabbar` / `.tabbtn` / `.tabpanel` | The three time-bucket tabs — see `content-model.md` §2. JS tab-switching is already wired in the template's `<script>` |
| `.feature-row` (+ `.rev` to mirror) | One big featured item: copy left/right, screenshot in a `.visual-card` — used in general/admin variants. When this month's in-scope item count is small (roughly ≤3, see `content-model.md` §2), use this for **every** item and skip `.threeup` entirely rather than padding out a near-empty grid |
| `.spot` (+ `.rev`) | Lighter-weight equivalent of `.feature-row`, used in beginner/specialist variants (smaller type, tighter spacing). Same low-item-count rule as `.feature-row` applies |
| `.threeup` / `.tcard` | Grid of secondary items ("More from this month"); always end the grid with a `.tcard.dark` card linking to the full release notes. Only use this when there's a real secondary tier — don't build one to hold just a single item (`content-model.md` §2) |
| `.band` / `.brow` | Category rollup of several smaller items grouped under one heading — used heavily in the "released last month" bucket |
| `.alertbar` | Deprecation / action-needed notices — amber, always includes a link to a migration guide when one exists |
| `.soon-banner` / `.soon-card` / `.soon-ribbon` | Coming-soon bucket: banner is the mandatory "subject to change" caveat; cards are dashed-border to visually read as "not final yet" |
| `.tuned` | Opening disclosure box for filtered variants — "why this page looks shorter" (see `content-model.md` §4 step 4) |
| `.notincluded` | Closing disclosure box for filtered variants — "not shown on this page" |
| `.why` | "Why it helps" benefit line — beginner/specialist only |
| `.ctaband` | Dark full-width closing CTA before the footer |
| `footer` | Single-sourcing disclaimer + the three standard links (`content-model.md` §5) |

## Images — always inline, never linked, and always attempted

Every screenshot in a finished page is embedded as a base64 `data:image/...`
URI. Never leave a page pointing at a relative/absolute file path for an
image — it must open standalone, from anywhere, without the assets folder
present.

Fill every image slot the template offers (`.hero-visual`, `.visual-card`,
`.tcard` shotwrap, `.band` thumb) if a plausible image exists — don't default
to a text-only layout just because the exact item lacks a bespoke asset.
Full priority order and confirmed paths per solution are in
`repo-detection.md` step 4 and `repo-map.md`'s asset-folder table —
summarized here:

**Source priority per image slot:**
1. **Real per-feature production asset already in the docs repo** (e.g.
   AJO's `help/using/rn/assets/do-not-localize/`, AEP's
   `help/release-notes/<year>/assets/<month>/`) — the actual product UI,
   often filenamed after the feature.
2. **A thematic match in that same repo's curated custom-release-notes
   folder** (e.g. AJO's `help/using/rn/assets/do-not-localize/custom/`,
   which recurses into topic subfolders like `Loyalty/`). Match by keyword
   between the item/theme and the filename — it's full of descriptively-
   named assets (e.g. `contextual-push-notification-message.png`,
   `access-control-team-permissions.png`, `multi-channel-campaign-orchestration.png`).
   List the folder and pick the closest keyword match rather than guessing a
   filename blind. A theme the user explicitly included/excluded
   (`personalization-signals.md`) is a strong hint for which keywords to
   search for.
3. **Text-only**, only if neither source has a plausible match — never
   invent a placeholder that looks like real product UI.

**Mechanics:**
1. While drafting, write `<img src="ASSET:some-descriptive-name.png" alt="...">`
   using the real filename you found in step 1 or 2 above.
2. Once the draft is content-complete, run:
   ```
   python3 <this-skill>/scripts/embed_images.py <draft.html> <assets_folder>
   ```
   pointing `<assets_folder>` at whichever source(s) you drew from (run it
   twice — once per folder — if you mixed docs-repo screenshots and
   `assets-RN/` in the same draft). This resolves every `ASSET:` marker to
   the real inline base64 data URI in place, and fails loudly with
   fuzzy-match suggestions if a filename doesn't match anything, rather than
   silently leaving a broken image.
3. Re-open the output file and confirm no `ASSET:` markers remain (the
   script's exit code is non-zero if any are left unresolved — treat that as
   a blocking error, not a warning to ignore).

This two-step flow (draft with markers → batch-resolve) exists because
hand-pasting multi-KB base64 strings into a draft is slow and error-prone;
let the script do it exactly once, mechanically.

The nav-bar Adobe mark / favicon can reuse
`templates/adobe-favicon-base64.txt` (one small red monogram icon) rather
than sourcing a new one per page — drop its contents into
`{{FAVICON_BASE64}}` in the template.

## Validation checklist before calling a page done

- [ ] Opens correctly as a standalone `file://` HTML with no `ASSET:` markers
      or external image paths remaining.
- [ ] All three time-bucket tabs present, nav buttons and tab-bar buttons in
      sync, tab-switching JS works.
- [ ] Status tags (`Live`/`Rolling out`/`Limited`/`Private beta`) preserved
      on every item that had one in the source inventory.
- [ ] If filtered: `.tuned` box present before content, `.notincluded` box
      present after, both name what was cut.
- [ ] If general/admin: no `.tuned`/`.notincluded`/`.why` boxes present.
- [ ] Footer disclaimer wording matches the pattern in `content-model.md` §5,
      solution name correctly substituted, all three links point at real
      solution-specific URLs.
- [ ] "Coming soon" bucket carries the "subject to change" banner.
- [ ] If "this month" (in scope) has only a few items (roughly ≤3), every one
      of them got `.feature-row`/`.spot` treatment — no "More from {month}"
      `.threeup` grid holding just one or two real cards.
