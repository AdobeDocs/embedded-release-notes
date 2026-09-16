# Content model — rules that must hold in every variant

Derived from the Custom Release Notes process spec (`0-wiki-creation-process.md`
in the source project). These rules govern *what* goes on the page; see
`design-system.md` for *how* it's built, and `personalization-signals.md` for
*who* a given variant is for.

## 1. Single-sourcing (non-negotiable)

Every entry on every page must trace back to the official release notes for
the solution (AJO, AEP, ...). There is no parallel writing pipeline. One
structured entry — feature name, category, status, date, description — gets
**reworded**, never **re-authored**, per surface/persona.

Before building any variant:
1. Confirm the current release's feature list, dates, and status tags against
   the official release notes.
2. Confirm the next release's items against the pre-release notes.
3. If a "full inventory" draft doesn't already exist for this month (every
   item, untrimmed, tagged by status, organized by category), build that
   first — it's the source every persona cut gets filtered from.

## 2. Three time buckets, always

Every variant — general or persona-specific — has exactly these three tabs,
in this order:

1. **Released this month** — the current release. A couple of *featured*
   items (full `.feature-row`/`.spot` treatment) plus a "More from
   {month}" grid (`.threeup`) for the rest — **but only when there's
   actually a meaningful tail to group that way.** When a persona/theme
   scope narrows this month down to just a handful of items (roughly 3 or
   fewer), promote **all** of them to the featured `.feature-row`/`.spot`
   tier and drop the "More from {month}" grid/heading entirely — a
   `.threeup` grid holding one real card plus the mandatory closing
   `.tcard.dark` link card reads as padding, not a real secondary tier, and
   implies a hierarchy between items that doesn't exist when there are this
   few of them. Every item earning equal visual weight is correct in that
   case, not evidence something was left out.
2. **Released last month** — the prior release, **in full, not trimmed**.
   This is what "single-sourcing, previous release included" means in
   practice — even a narrow persona variant keeps last month complete for
   its scope (see §4 on filtering — filter by category, not by trimming this
   bucket further).
3. **Coming soon** — pre-release notes for the next release window. Pull from
   **both** the dedicated pre-release file *and* any inline `+++ Coming soon`
   accordion blocks inside the current release-notes file's "this month"
   section — see `repo-detection.md` Step 3; don't rely on the pre-release
   file alone or a real item can get silently dropped. Dedupe if the same
   item appears in both. Must carry the "Subject to change until release"
   banner (`.soon-banner`), always. Item count scales with persona scope: 1
   item is fine for a narrow persona, up to the full pre-release list for
   general/admin variants.

Never drop a bucket. Never drop the "subject to change" caveat on bucket 3.

## 3. Status tags travel everywhere

`Live`, `Rolling out`, `Limited` / `Limited Availability`, `Private beta`.
These ride along with an item through every bucket and every persona cut.
Don't drop them — only adjust verbosity per audience (e.g. an admin variant
spells out "Limited Availability" in full; a beginner variant might just say
"Limited").

## 4. Producing a persona/solution variant — step by step

1. **Start from the full inventory**, not a blank page.
2. **Pick the audience.** See `personalization-signals.md` for how to map
   role/usage/permissions/freshness/intent signals to a persona. Observed
   personas so far: general/no-filter, feature-scope beginner (e.g.
   Orchestrated Campaigns only), workflow specialist (e.g. Journeys +
   mobile channels), admin/power user (config & channels lens), a
   feature-family deep-dive (e.g. Loyalty).
3. **Filter scope, not tone, first.** Drop entire *categories* irrelevant to
   the persona (e.g. drop Journeys/Decisioning entirely for a
   Campaigns-only beginner). Filter at the category level, not by hand-
   picking individual items, so the cut stays maintainable as new items
   ship next month.
4. **Disclose what was cut — required, not optional, for any filtered
   variant:**
   - An opening disclosure box (`.tuned`) inside the "this month" bucket,
     before any content: *"Why this page looks shorter than the official
     release notes: ..."* — explain in plain language what categories were
     dropped and why, note an escalation path ("ask your admin"), and point
     back to the "Full release notes" link.
   - A closing box (`.notincluded`) at the end of the bucket: *"Not shown on
     this page"* — name what this month's release also included that isn't
     shown here, and link to the full release notes.
   - General/full and admin/power-user variants do **not** get these boxes —
     they show everything in scope, so there's nothing to disclose.
5. **Reframe tone to match the persona's technical depth:**
   - **Beginner / specialist:** plain-language rewrite. Add a "Why it
     helps" benefit line (`.why`) under each item. Strip category-pill
     jargon where it doesn't help.
   - **Admin / power-user:** keep original terminology, exact field names,
     precise stats. Keep category and status tags prominent. No benefit
     callouts.
   - **General / full page:** standard category tags, no persona rewrite.
6. **Reuse content blocks across variants** where a feature applies to more
   than one persona — write the copy once per feature-per-tone-level (e.g.
   once for "beginner tone"), then reuse it verbatim across every beginner-
   tone variant that includes that category. Don't re-write it per persona.
7. **Keep bucket structure and footer identical across every variant** —
   only the *contents* differ, never the skeleton (§2, §8 below).
8. **Link out, don't duplicate:**
   - Every variant carries a "Full release notes →" link back to the
     official/complete notes.
   - Admin variants additionally link to the Administration guide.

## 5. Footer disclaimer (exact pattern, solution name swapped in)

```
Sourced from the official {SOLUTION_NAME} release notes. Availability dates
reflect phased rollout — check your environment.
```

Plus three links, always: Release notes ↗, Release cycle ↗, Product page ↗
(all pointing at the solution's real Experience League / product pages).

## 6. What NOT to do

- Don't invent feature details not present in the official/pre-release
  notes — reword, don't fabricate.
- Don't silently drop a status tag when rewording for tone.
- Don't skip the "subject to change until release" caveat on the Coming Soon
  bucket, regardless of how small that bucket is for a given persona.
- Don't source the Coming Soon bucket from the pre-release file alone — also
  check for inline `+++ Coming soon` accordions inside the current
  release-notes file's "this month" section (`repo-detection.md` Step 3);
  missing that second source under-counts real coming-soon items.
- Don't build a new variant's visual design from scratch — see
  `design-system.md` and reuse the existing component vocabulary so the
  whole hub reads as one system.
