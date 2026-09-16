---
name: custom-release-notes
description: Generate and visually review a standalone HTML release-note hub, then derive a component-facing JSON card for an Adobe UI surface. Collect product, scope, persona, and surface; source only official release notes; iterate on an HTML preview; require final approval; publish the hub; then update the central toast registry. Use for personalized release notes and in-product what's-new cards.
argument-hint: "request=requests/<product>/<year>/<month>/<slug>.json or product=ajo surface=ajo theme=loyalty persona=admin"
---

# Custom Release Notes

## Prerequisite

The `embedded-release-notes` repository must be cloned and opened as a VS Code
workspace folder. Stop and explain this prerequisite if the repository root,
this skill, `../../../scripts/new_request.py`, or `templates/base-template.html` cannot
be resolved. Do not attempt to reproduce the workflow from memory outside the
repository.

## Invocation variables

When invoked with `request=<path>`, read that JSON manifest first and treat its
values as answers already supplied to the intake. Confirm inferred or missing
values, but do not ask the user to repeat populated fields. The request format
is defined by `schemas/request.schema.json` at the repository root.

When invoked with inline `key=value` arguments, accept `product` or `products`,
`deliverables`, `theme`, `persona`, `release_scope`, `release_value`, `include`,
`exclude`, `year`, `month`, `slug`, and `surface`. Create the
corresponding request with
the repository's `../../../scripts/new_request.py` before sourcing content.

Produces **Custom Release Notes for in-product display**, sourced entirely
from a solution's real, official release notes (never fabricated) and
filtered for a specific audience/context. **The workflow below is the
one intake process for generating these deliverables, full stop — it is not a
toast-only path.** It governs both output formats:

- **Release-note card configuration** — one entry in the central `toast.json`
   registry, consumed and rendered by `<releasenote surface="...">`. It
   contains exactly two curated entries with icons and an action to the hub
   (see `references/toast-spec.md` and the sibling
   `../toast-registry/SKILL.md`).
- **Hub page** — the larger standalone "what's new" page with three time
  buckets (this month / last month / coming soon — see
  `references/content-model.md` and `references/design-system.md`).

Format determines whether the hub template, toast registry, or both are
updated at Step 6. The
earlier steps are otherwise identical. Step 1 asks directly which
combination is wanted (hub, toast, both, or a toast built from an existing
hub) rather than assuming.

This skill packages a process originally worked out by hand across ~10 hub
mockups plus a toast concept mockup for Adobe Journey Optimizer and AEP.
Read the reference files below before generating anything non-trivial; they
contain the actual rules, not just a summary.

## Before you start

1. **Read `references/repo-detection.md`** (and `references/repo-map.md`) —
   how to find each solution's real release-notes source, and its
   in-product-display asset folders, in a local docs repo.
2. **Read `references/personalization-signals.md`** — how Product → Theme/
   Context → Refinement → Release scope → Persona narrow down what goes in,
   for either format.
3. **Read `references/toast-spec.md` and `references/content-model.md` +
   `references/design-system.md`** — the toast and hub-page shapes
   respectively. Read whichever matches the format in play (both, if
   unsure yet which format the user wants).
4. Skim **`references/samples-catalog.md`** for existing examples to imitate
   the actual copy voice of, rather than just following this skill's
   abstractions.

## Workflow

In order — each step narrows the next, **for every output format and Step 1
branch**. Never skip the rendered-preview loop: the author reviews an actual
HTML page before the canonical hub or toast registry is finalized.

### Step 0 — Proactively propose the deliverable

Before asking anything, lead with the proposal itself rather than a question.
Detect the product from context already available this turn: an
`ide_selection`, a recently-opened/edited file path, or a working directory
that falls inside a known `~/Documents/GitHub/<slug>.en/` repo
(`repo-map.md`). If a clear signal exists, open with something like "I can
put together Custom Release Notes for **{detected product}** based on the
file you have open — want me to build these?" rather than silently starting
Step 1's intake or waiting to be asked. If no such signal exists, skip the
proactive framing and go straight into Step 1's question.

### Step 1 — What do you want to do?

Ask as a single-select, **no option marked "(Recommended)"** — which of
these fits depends entirely on where the user is in their process, not on
any universal default:

1. **Build custom release notes for in-product display, plus its contextual
   toast** — both deliverables together: the hub page and a companion toast
   that highlights its top entries.
2. **Draft the custom release notes only, for now** — just the hub page. A
   toast can be generated from it later via option 3.
3. **Generate a contextual toast only, from custom release notes already
   created** — skips fresh sourcing; pulls the toast's entries from an
   existing hub page instead (see "Toast-from-an-existing-hub" below).
4. Something else (the tool's automatic free-text option) — clarify what's
   wanted, then use judgment on which of the steps below actually apply.

This choice decides both the format(s) to build and which steps below are in
play:
- **Options 1 & 2** run the full workflow below (Steps 1.1 through 6) — for
   option 1, Step 6 finalizes the hub and updates `toast.json`; for option 2, only
  `base-template.html`.
- **Option 3** skips Steps 2.1-2.3 (theme, refinement, and release scope were
  already decided when the hub was built) — see "Toast-from-an-existing-hub"
  below — then rejoins the normal flow at Step 3.
- **Option 4** — no fixed path; scope it with the user first.

If the user wants a toast but there is no existing hub page to source it from,
use option 1: generate and keep the hub first, then derive the JSON card. A
toast entry must never reference an internal draft or a missing hub.

### Step 1.1 — Product

Ask this as its own confirm-or-change question — never lock in Step 0's
detected product silently, since the open file is a guess, not a
declaration:

- If Step 0 detected a product, lead with it as the suggested pick: a
  single-select with that product first, the other solution(s) from
  `repo-map.md`'s Confirmed table next, and the tool's automatic free-text
  "Other" option last for anything not listed. **No option marked
  "(Recommended)"** — even for the detected guess, present it neutrally so
  correcting it is frictionless, not a case of overriding a suggested
  default.
- If Step 0 found no signal, ask the same shape without a pre-selected
  guess: "which product is this for?" with the Confirmed-table solutions as
  suggested options and "Other" for anything else.

Multiple products are valid (a combined request) — see `repo-detection.md`'s
multi-solution section. For Step 1 option 3, the product may already be
implied by whichever existing hub page gets picked in the next section —
state the inferred product and confirm rather than re-asking redundantly.

### Toast-from-an-existing-hub (Step 1 option 3 only)

Replaces Steps 2.1-2.3 when the user picked option 3:

1. Ask which existing custom release notes to base the toast on, if not
   already clear — a previously generated hub page (this skill's own past
   output in `~/Downloads/`, or one of the hand-built mockups in
   `samples-catalog.md`).
   Confirm the specific file before reading it; don't guess between
   candidates.
2. Read that file's current "this month"/featured content, and whichever
   persona and release scope it was built for. State what you found (persona,
   release scope, entry list) and confirm it rather than silently treating it
   as authoritative — the user may want the toast to diverge (a different
   persona, a narrower scope) even though it's sourced from the same hub.
   Treat a divergence request as an explicit override into Step 2.3/Step 3,
   not a reason to skip them for real.
3. Rejoin the normal flow at Step 3 (persona — confirm it matches the hub, or
   take the override), then Step 4, drafting the two highest-impact toast
   entries from that hub's content per `toast-spec.md`.
4. Confirm the UI surface, then Step 6 updates `toast.json` after final review.

### Step 2.1 — Theme / Context

Try, in order:
1. Detect the product area from the same open-file/working-directory
   signals as Step 1 (e.g. a file under `building-journeys/` suggests
   "Journeys"), and suggest it back to the user for confirmation.
2. If the user offers a wiki page, JIRA issue/filter, SharePoint link, or a
   screenshot, use it to extract the theme/context (Confluence/JIRA MCP
   tools, or read the screenshot directly if it's an image).
3. Otherwise ask the user to enter the product area directly, as a plain
   open question — not a multiple-choice picker (themes/areas are too
   open-ended for a fixed list).

### Step 2.2 — Refinement

Ask: "Any features to exclude, or focus on?" — again a plain open question,
free text, no suggested options. This layers on top of the Step 2.1 scope:
an include narrows further in, an exclude narrows further out.

### Step 2.3 — Release scope

Ask which release this relates to, as a single-select (one answer, not
multiSelect — this is a scope choice, not a checklist) with **no option
marked "(Recommended)"**:

1. **Latest release** — the most recent completed release per the docs
   repo's release notes (`repo-detection.md` Step 3's "this month" bucket).
2. **Last 2 releases** — the latest release plus the one before it, both in
   full (`repo-detection.md`'s "this month" + "last month" buckets).
3. **Latest updates** — not tied to a release at all; based on whatever
   changed on the `release-notes.md` page itself since a timeframe the user
   specifies. Picking this needs a follow-up question for the actual
   timeframe (e.g. "latest updates since Sept 1st" or "latest updates since
   the last release notes were published") — never guess a window.
4. Other (the tool's automatic free-text option) — the user names a specific
   release directly (a past release, a version number, a specific month).

What this changes per format:
- **Toast**: this is the pool the two entries get drawn from — it makes
  concrete the "Freshness" signal in `personalization-signals.md` (previously
  a default "since your last visit" framing; now user-chosen).
- **Hub page**: the three-bucket structure (`content-model.md` §2) stays
  fixed regardless of this answer — it only changes what anchors "this
  month" (e.g. a specific named release builds a retrospective hub as if
  that release were current) or, for "Latest updates since X", filters items
  inside the buckets to those on/after that date.

### Step 3 — Persona

Ask as a single-select (one persona, not multiSelect) with **no option
marked "(Recommended)"** — there's no default persona, so present the
choices neutrally. Order the options: the personas relevant to context first
(typically `Marketer` / `Developer` / `Admin`, adapted if the theme/scope
points at a different natural split), then `Generic (all personas)` last,
before the tool's automatic free-text "Other" option (for a custom user
profile). **The user can skip this step — skipping means Generic (applies to
all users)**, so don't block waiting for an answer here if they'd rather
move on. This is the single personalization axis for **both formats** — see
`personalization-signals.md` for how Persona maps to category relevance,
tone, and (for hub pages only) whether disclosure boxes/benefit-lines are
used. There's no separate "level of expertise" question — Persona alone
drives it now, for toast and hub page alike.

### Step 4 — Build and display the HTML preview

Using the scope from Steps 1-3, select and draft candidate entries — same
gate regardless of format:
- **Toast**: exactly two entries, chosen for the highest impact/importance to the
  selected persona within the Step 2.3 release scope — not just the first
  items found in source order. Content isn't limited to shipped features —
  a deprecation notice, a new how-to video, or a documentation update are
  all valid entry types (`toast-spec.md`). Pull real content only; if a
  desired type (e.g. "there's a new video") isn't in the docs repo, ask the
  user for it rather than inventing a link.
- **Hub page**: the full bucketed content per `content-model.md`, drafted
  the same way — proposed, not silently finalized.

For options 1 and 2, copy `templates/base-template.html`, fill it with the
selected content, resolve its images, and write a working preview to:

```text
generated/<product-scope>/<YYYY>/<MM>/<slug>/hub.preview.html
```

Open the preview in a browser when browser tools are available. Otherwise,
provide its exact path so the author can open it. This is a review artifact:
do not set the request status to `generated`, create the canonical `hub.html`,
or update `toast.json` yet.

For option 3, open the existing approved hub instead of creating a new preview.
If the author asks to change that hub, create `hub.preview.html` beside it and
review the copy; never overwrite the existing canonical hub during review.

### Step 5 — Review the rendered page and revise

After displaying the rendered preview, ask a concrete review question:

> Here is the rendered release note. Would you like to change any content,
> ordering, images, or presentation?

Apply requested changes directly to `hub.preview.html`, refresh or reopen it,
and ask again. Continue until the author says there are no more changes. Do
not derive the two card items during this loop; they must come from the final
approved HTML.

### Step 6 — Confirm and render final

Recap the product, source repository, scope, persona, deliverables, output
path, and titles visible in the reviewed preview. Ask:

> Are we ready to render this as final?

Wait for explicit approval. Once approved:
1. Promote the reviewed preview to
   `generated/<product-scope>/<YYYY>/<MM>/<slug>/hub.html`. Do not overwrite
   an existing canonical hub without explicit approval. Remove the temporary
   `hub.preview.html` after the canonical file is safely written.
2. Derive exactly two highlighted items automatically from the approved
   canonical hub. Build the toast entry matching
   `schemas/toasts.schema.json`, with ID
   `<surface>-<release-year>-<release-month>-<slug>`, then use
   `scripts/toast_registry.py upsert --entry <entry.json>`. Include the card
   title, exactly two items with icon configuration, and set `action.href` to
   the request's `<output_directory>/hub.html`. Never generate a toast HTML
   file.
3. Validate with `scripts/toast_registry.py validate`,
   `scripts/release_files.py validate`, and the relevant content checklist.
4. Set the request status to `generated` and report both the canonical hub
   path and toast ID.

## Common requests this skill should handle directly

- "Make an in-product toast for [product] about [topic]" → if an existing
   hub page is meant as the source, Step 1 option 3. Otherwise, run option 1's
   full sourcing pipeline: generate the hub first, then derive its JSON card.
- "Make a version of the AJO what's-new page for [role/feature/team]" → the
  same full workflow above, Step 1 option 2 (hub only) — every step still
  applies here, this is not a shortcut path.
- "Turn this what's-new page into a toast" / "make a toast version of
  [existing hub file]" → Step 1 option 3, the "Toast-from-an-existing-hub"
  path.
- "Add [product]'s release notes to this hub/toast using the same pattern"
  → same workflow, new solution, same component vocabulary, new
  category/theme set (categories are solution-specific — don't force one
  solution's categories onto another's content).
