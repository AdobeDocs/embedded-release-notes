# Toast spec — the in-product popup deliverable

The primary Custom Release Notes deliverable: a small popup shown in-product
(a corner toast), surfacing 2-3 curated entries rather than a full page.
Grounded in an original concept mockup ("Exploration 2 · corner toast, in
the AI-tooltip's slot" — see `samples-catalog.md` if a local copy is
available) — reuse that mockup's actual visual style (blue/neutral, not the
hub's Adobe-red system — this was a deliberate choice, confirmed with the
user, to keep the toast distinct from the hub rather than unify the two).

## What the generated file contains

**Standalone toast card only** — no product screenshot behind it. The
original mockup shows the toast absolutely-positioned over a screenshot of
the product; this skill generates just the card itself (the reusable
in-product component), not a recreated screenshot mockup. Start from
`templates/toast-template.html`.

## Structure (all required, in this order)

1. **Kicker** — a small uppercase label with a colored dot, e.g. `SINCE AUG
   12` or `NEW THIS WEEK` — a freshness marker, not a category tag.
2. **Title** — one short line, e.g. "New since your last visit." Adjust to
   context (e.g. a single-topic toast might title itself after that topic).
3. **Close button** — a dismiss affordance (×), always present.
4. **Items — exactly 2 or 3**, each: a small leading dot, a bold one-line
   headline, and one short supporting sentence. No images, no tags, no
   dates on individual items — the toast is a teaser, not a report. Keep
   each headline+sentence pair short enough to fit a ~30%-viewport-width
   card without wrapping awkwardly (match the mockup's real line lengths as
   a length guide, e.g. "Catch email issues before you send" /
   "Content check in the Email Designer is now generally available.").
5. **Footer** — a "See everything that shipped →" (or equivalent) link back
   to the full official release notes, plus a primary dismiss button
   ("Got it").

## What counts as a valid entry

Not limited to shipped features. Valid entry types, per Step 4 of
`SKILL.md`'s workflow:
- A newly shipped feature or improvement (from the release notes).
- A deprecation / action-needed notice (from the release notes' alert-style
  items).
- A new how-to video (only if one is confirmed to exist — ask the user
  rather than inventing a link if the docs repo doesn't reference one).
- A documentation update (a meaningfully rewritten/expanded doc page, not
  every minor edit — ask if unsure whether something rises to this level).

All entries must trace back to real content — the docs repo's release
notes, a wiki/JIRA source the user pointed at, or something the user
explicitly told you exists. Never fabricate an entry to fill the 2-3 slot
count; if fewer than 2 good candidates exist in scope, say so rather than
padding with a marginal item.

## The draft → review loop (Step 4 of SKILL.md)

1. Propose 2-3 candidate entries with drafted headline + supporting
   sentence for each, and say explicitly which content type each is
   (feature / deprecation / video / doc update).
2. Ask the author to confirm the scope, swap an entry, or add specific
   additional scope. This is a real review gate — don't proceed past it on
   an ambiguous or missing reply.
3. Only after that, move to Step 5's final validation recap before
   generating the HTML.

## Assets

The toast card itself doesn't have image slots (see Structure above) — but
if a future variant needs one (e.g. a thumbnail), follow the same
asset-priority order as the hub deliverable: real per-feature asset in the
docs repo's `assets/do-not-localize/` folder first, then the curated
`assets/do-not-localize/custom/` folder, then text-only. See
`repo-detection.md` step 4.

## Validation checklist before presenting the toast

- [ ] Exactly 2 or 3 items, each traceable to a real source.
- [ ] Kicker + title + close button + footer (link + primary button) all
      present.
- [ ] No images, tags, or per-item dates inside the card.
- [ ] Author explicitly reviewed and approved the drafted entries (Step 4)
      and the final recap (Step 5) before the HTML was generated.
- [ ] Footer link points at the real full release notes for the product(s)
      in scope.
- [ ] File is self-contained (no external asset references) if any images
      were ever added to a variant.
