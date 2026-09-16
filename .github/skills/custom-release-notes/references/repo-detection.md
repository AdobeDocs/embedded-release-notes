# Repo detection — finding the source of truth before asking the user for content

The official release notes for each Adobe solution live in a local docs repo
under `~/Documents/GitHub/<slug>.en/` (Experience League docs-repo
convention). Read this file *before* asking the user to paste release-notes
content — for known solutions, the real source is already on disk.

## Step 1 — resolve solution → repo

1. Check `references/repo-map.md` first. If the solution is in the
   **Confirmed** table, use those exact paths — skip straight to Step 2.
2. If it's in the **Unconfirmed** table, treat those paths as a strong lead,
   but verify by reading the file (check it's actually the full-product
   release notes, not a sub-feature) before relying on it.
3. If the solution isn't listed at all: search `~/Documents/GitHub/` for a
   directory matching the solution name (case-insensitive, try the obvious
   slug — e.g. "Customer Journey Analytics" → `analytics-platform`,
   "Journey Optimizer" → `journey-optimizer` — and also try the product's
   common abbreviation). List candidates and confirm with the user if more
   than one plausible match exists, or if nothing matches (ask where the
   repo lives, or fall back to asking for pasted content).
4. Once confirmed, **append a row to `repo-map.md`** with the verified paths
   so the next request for this solution skips detection entirely.

## Step 2 — locate the release-notes files within the repo

Layout is not standardized across repos — don't assume one convention.
Search for candidates in this order and pick the one that is clearly the
whole-product notes (not a sub-feature/extension/debugger page):

1. `help/using/rn/release-notes.md`, `help/**/rn/release-notes.md`,
   `help/**/release-notes.md` (prefer the shallowest match; a match nested
   under `tags/extensions/*` or a similarly narrow-sounding path is a
   sub-feature, not the product).
2. `help/release-notes/latest/latest.md` or similarly named "latest/current"
   file.
3. A pre-release counterpart: `e-release-notes.md`, `pre-release-notes.md`,
   or similar "pre-release"/"early" naming.
4. Yearly/monthly archive files (`release-notes-<year>.md`, or
   `<year>/<month>-<year>.md`) for "last month" if it's not already inside
   the "current" file as a second section.

If more than one candidate looks plausible, open the top of each (frontmatter
+ first heading) and confirm which is the real whole-product page before
reading further — a wrong guess here silently pulls the wrong content.

## Step 3 — extract the three buckets

- **This month**: whichever section/file is confirmed (by frontmatter date
  or heading text, not filename alone — see the caveat in `repo-map.md`) to
  be the most recent completed release.
- **Last month**: the next-most-recent section/file. For repos where the
  "current" file holds multiple months as H2 sections (AJO-style), this is
  simply the second H2. For repos with one file per month (AEP-style), it's
  the previous month's file.
- **Coming soon**: check **both** of these sources, not just one — either can
  hold real items the other doesn't:
  1. The dedicated pre-release/early-release file (e.g. AJO's
     `e-release-notes.md`). Check it actually has content — these files are
     sometimes left as commented-out templates between releases. If empty,
     say so rather than inventing "coming soon" items.
  2. Inline `+++ Coming soon` accordion blocks embedded *inside* the main
     "this month" section of the current release-notes file itself (seen in
     AJO's `release-notes.md`, e.g. nested under a category like
     `### Campaigns`, closed by a bare `+++` line). These are easy to miss
     since they're mixed in with shipped-item tables in the same section
     rather than living in a separate file — grep the "this month" section
     for `+++ Coming soon` before concluding the pre-release file is the
     only source.
  If the same item appears in both places, treat it as one entry (dedupe by
  feature name), not two.

## Step 4 — images (three-tier priority)

Check sources in this order — see `repo-map.md`'s asset-folder columns for
confirmed paths per solution:

1. **Real per-feature production asset**, in the docs repo's main
   `assets/do-not-localize/` folder (co-located with the release-notes
   files, e.g. AJO's `help/using/rn/assets/do-not-localize/`, or AEP's
   `help/release-notes/<year>/assets/<month>/`). These are the actual GIFs/
   screenshots already used in the official docs, often filenamed after the
   feature itself (e.g. `execution-metadata.gif`, `journey-simulation.gif`,
   `rule-ai.gif`, `waves.gif`) — if one plausibly matches an item in scope,
   this is the best possible image: the real product UI, already produced.
2. **Curated custom-release-notes asset library**, in that same repo's
   `assets/do-not-localize/custom/` subfolder (confirmed for AJO — see
   `repo-map.md`). Purpose-built for this skill: generic, topically-named
   images for when no feature-specific production asset exists yet. Search
   recursively (it has topic subfolders, e.g. `Loyalty/`) and match by
   keyword against the item or an explicit theme from Step 2.1/2.2.
   Supersedes the older standalone `assets-RN/` folder outside the repo —
   prefer this in-repo copy when both exist for the same solution.
3. **Text-only**, only if neither source has a plausible match — never
   invent a placeholder that looks like real product UI.

The toast deliverable (`toast-spec.md`) has no image slots by default, so
this mostly applies to the hub-page deliverable — but check it any time a
variant does want a thumbnail.

## Multi-solution requests

If asked for a page spanning more than one solution (e.g. "AJO + AEP
combined hub"), repeat Steps 1–4 independently per solution, then:
- Merge into shared time-bucket tabs (one "this month" tab covering both
  solutions' items, grouped/labeled by solution), OR keep the buckets
  solution-specific if the user asked for solutions to stay visually
  separate — ask if unclear which they want.
- The footer disclaimer must name every solution actually sourced from
  (`content-model.md` §5's single-solution wording needs pluralizing:
  "Sourced from the official {Solution A} and {Solution B} release notes.").
- AJO's own release notes note that AJO is built on AEP and inherits its
  capabilities — for an AJO variant, it's reasonable to link out to AEP's
  notes without duplicating AEP content, unless the user explicitly asked
  for a merged/combined inventory.
