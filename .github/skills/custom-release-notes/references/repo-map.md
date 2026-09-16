# Repo map — solution → local docs repo → release-notes file paths

Living lookup table. All repos live under `~/Documents/GitHub/` and follow
Adobe's Experience League docs-repo naming convention: `<slug>.en`. These are
local clones of `github.com/Adobe-Enterprise-Docs/<slug>.en` — if a solution's
repo isn't cloned locally on this machine, that's the canonical remote to
clone from (or browse read-only via the GitHub MCP tools) before falling
back to asking the user for pasted content.

**When you confirm a new solution → repo mapping with the user (see
`repo-detection.md`), append a row here** so future sessions skip straight to
it instead of re-searching. Keep entries factual (verified paths), not
guesses — if you only *think* a path is right, don't add it until read and
confirmed.

## Confirmed

| Solution | Repo | "This month" file | "Last month" / archive | "Coming soon" file | Real screenshots in-repo? |
|---|---|---|---|---|---|
| Adobe Journey Optimizer (AJO) | `journey-optimizer.en` | `help/using/rn/release-notes.md` — first two `## <Month> '<YY>` H2 sections (first = current, second = prior; older content already moved to the yearly archive) | `help/using/rn/release-notes-<year>.md` (e.g. `release-notes-2026.md`) for anything older than the two H2s in the live file | **Two sources, check both** (see `repo-detection.md` Step 3): `help/using/rn/e-release-notes.md` (often mostly empty/commented-out between releases — check for actual content before assuming it's populated) **and** any inline `+++ Coming soon` ... `+++` accordion block nested inside a category under the current "this month" H2 of `release-notes.md` itself — dedupe if an item shows up in both | See the asset-folder table below |
| Adobe Experience Platform (AEP) | `experience-platform.en` | `help/release-notes/latest/latest.md` | `help/release-notes/<year>/<month>-<year>.md` (e.g. `2026/july-2026.md`) — confirm the actual prior month by filename, not by assumption | `help/release-notes/pre-release-notes.md` | See the asset-folder table below |

**Caveat for both:** file *names*/section headers can lag the actual
calendar — always check the frontmatter `title`/`last-update` (AEP) or the
H2 heading text (AJO) to confirm which month a file really covers before
treating it as "this month." Don't assume from the filename alone.

## In-product-display asset folders (per `repo-detection.md` step 4)

| Solution | Repo | Real per-feature production assets | Curated custom-release-notes assets |
|---|---|---|---|
| AJO | `journey-optimizer.en` | `help/using/rn/assets/do-not-localize/` — hundreds of real feature GIFs/PNGs used in the official docs, largely filenamed after the feature (e.g. `execution-metadata.gif`, `journey-simulation.gif`, `rule-ai.gif`, `waves.gif`, `custom-channel.gif`, `pdf-attachments.gif`). Check here first for an exact/near-exact feature-name match. | `help/using/rn/assets/do-not-localize/custom/` — confirmed present (includes a `Loyalty/` subfolder); canonical remote: `github.com/Adobe-Enterprise-Docs/journey-optimizer.en/tree/main/help/using/rn/assets/do-not-localize/custom`. Prefer this in-repo copy over any older standalone mockups-folder asset library. |
| AEP | `experience-platform.en` | `help/release-notes/<year>/assets/<month>/*.png`/`.gif` — real screenshots already keyed to that month's items. | Not yet confirmed — search for a sibling `do-not-localize/custom/`-style folder near the release-notes files, or ask the user, before assuming one exists. |

Update this table (and mark it Confirmed) as soon as you verify an asset
folder for a new solution — don't assume AJO's exact relative path
(`rn/assets/do-not-localize/custom/`) generalizes to other repos' layouts.

**Sibling-solution URLs** (found in AEP's `pre-release-notes.md` intro — useful
for footer/cross-link URLs on combined or AEP-adjacent pages):
- AJO: `https://experienceleague.adobe.com/en/docs/journey-optimizer/using/whats-new/release-notes`
- AJO B2B: `https://experienceleague.adobe.com/en/docs/journey-optimizer-b2b/user/release-notes`
- Customer Journey Analytics (CJA): `https://experienceleague.adobe.com/en/docs/analytics-platform/using/releases/latest`
- Federated Audience Composition: `https://experienceleague.adobe.com/en/docs/federated-audience-composition/using/release-notes`
- Real-Time CDP Collaboration: `https://experienceleague.adobe.com/en/docs/real-time-cdp-collaboration/using/latest`

## Repos that exist locally but aren't confirmed yet

Seen under `~/Documents/GitHub/` as of the last scan — release-notes-style
files exist in most of these, but the exact "this month / last month / coming
soon" mapping hasn't been verified against a real request yet. Verify before
relying on them, then move the row up to Confirmed:

| Repo | A release-notes-shaped file spotted at... |
|---|---|
| `target.en` | `help/main/r-release-notes/release-notes.md` |
| `campaign.en` (Campaign v8) | `help/v8/start/release-notes.md`, `help/v8/start/whats-new.md` |
| `campaign-standard.en` | `help/rn/using/release-notes.md` |
| `campaign-web.en` | `help/v8/rn/release-notes.md`, `help/v8/rn/whats-new.md` |
| `cx-enterprise-ai.en` | `help/coworker/campaigns/release-notes.md` (looks scoped to one Coworker feature, not the whole product — verify before treating as the full inventory) |
| `analytics-platform.en` (likely CJA) | not found by filename search — CJA release notes may be documented elsewhere or under a different name; ask the user or search again before assuming it doesn't exist |
| `campaign-classic.en`, `control-panel.en`, `journey-optimizer-learn.en`, `cx-enterprise-agentic-tools.en`, `experience-cloud.en`, `experience-cloud-ai.en`, `OLD-journey-optimizer.en` | no release-notes-shaped file found in a shallow search — either doesn't exist, needs a deeper search, or isn't the right repo for that solution (`OLD-journey-optimizer.en` in particular looks superseded by `journey-optimizer.en` — don't use it) |

Note: `experience-platform.en` also contains many narrower `release-notes.md`
files for sub-features (`help/debugger/`, `help/privacy-service/`,
`help/tags/extensions/client/*/`, etc.) — these are **not** the main AEP
release notes. Don't match on filename alone; prefer the path in the
Confirmed table above.
