# Personalization signals — deciding what goes in and who it's for

Covers Steps 1.1, 2.1, 2.2, 2.3, and 3 of `SKILL.md`'s workflow: Product →
Theme/Context → Refinement → Release scope → Persona. (Step 1 itself — which
deliverable(s) to build — is covered directly in `SKILL.md`, not here.)
Today there is no live personalization engine — "producing a variant" means
a human (or this skill) manually works through these and repeats the
relevant content steps.

## Steps 1 & 2.1 — detecting Product and Theme/Context

Try these in order, for both the product (Step 1) and the finer-grained
product area/theme (Step 2.1):

1. **Detect from context already available this turn** — an `ide_selection`
   block, a file path just read/edited, or a working directory sitting
   inside a known `~/Documents/GitHub/<slug>.en/` repo (`repo-map.md`).
   A path like `.../journey-optimizer.en/help/using/building-journeys/...`
   is a strong double signal: product = AJO, theme = Journeys. State what
   you detected and confirm it rather than silently assuming — this is a
   best-effort read of whatever signal happens to be present, not a
   guaranteed capability, so it can be wrong.
2. **An external source the user points at** — a wiki page, a JIRA
   issue/filter, a SharePoint link, or a screenshot. Fetch/read it (wiki and
   JIRA MCP tools are available; a screenshot can be read directly) and
   extract the product/theme from its actual content — don't guess from the
   link text alone.
3. **Ask directly** — a plain open question ("which product/product area is
   this for?"), never a multiple-choice picker. Product may have a short
   enough real list to make options reasonable (a handful of Adobe
   solutions); theme/product-area should stay free text since it's far more
   open-ended.

Multiple products in one request is valid — repeat detection per product,
see `repo-detection.md`'s multi-solution section.

## Step 2.2 — Refinement (include/exclude)

Ask, always as a plain open question — never multiple-choice, this is
unbounded: **"Any features to exclude, or focus on?"** Layer the answer on
top of the Step 2.1 scope:

- An **include** pulls something in past the default theme/area scope.
- An **exclude** drops something the default scope would otherwise include.
- Match against the real inventory's actual items/categories, not just an
  exact keyword — a theme can be a category, a sub-topic, or a
  channel/product area.
- **State the resulting filter explicitly** (what's in, what's out, why) as
  part of Step 5's confirmation recap — never apply refinements silently.

## Step 2.3 — Release scope

Ask which release this relates to — single-select, one answer, **no option
marked "(Recommended)"** since none of these is a universal default:

1. **Latest release** — the most recent completed release (`repo-detection.md`
   Step 3's "this month" bucket).
2. **Last 2 releases** — latest + the one before it, both in full
   (`repo-detection.md`'s "this month" + "last month" buckets).
3. **Latest updates** — not release-anchored; whatever changed on the
   `release-notes.md` page since a timeframe the user supplies. Requires a
   follow-up question for the actual timeframe — never assume one.
4. Other (the tool's automatic free-text slot) — a specific named release,
   version, or month, typed directly.

For the toast, this is literally the pool the two entries are drawn from —
it's the "Freshness" signal below made explicit and user-chosen instead of
defaulting silently to "since your last visit." For the hub page, the
three-bucket structure stays fixed (`content-model.md` §2) — this only
changes what anchors "this month" or, for "Latest updates since X", filters
items inside the fixed buckets to that date range.

## Step 3 — Persona

Ask as a single-select — one persona, not multiSelect — with **no option
marked "(Recommended)"**: there's no universal-default persona, so present
the choices neutrally and let the user pick freely.

Order the options: the personas relevant to context first, then
`Generic (all personas)` last, then the tool's automatic free-text "Other"
option (for a custom-typed user profile). The context-relevant set is
typically **`Marketer` / `Developer` / `Admin`**, adapted if the Step 2.1
theme/scope points at a more natural split. The user can also **skip this
step, which means Generic/all users** — don't block on it if they'd rather
move on without picking.

### Persona → category relevance, tone, and (hub-page only) disclosure treatment

Persona is the **single** personalization axis for both formats — there's no
separate "level of expertise" question anymore. For the toast, only the
first two columns matter (which entries get proposed, how they're worded —
a toast has no room for disclosure boxes or benefit-line callouts, see
`toast-spec.md`). For the hub page, all four columns apply, since that
format has `.tuned`/`.notincluded` disclosure boxes and `.why` benefit lines
that the toast structurally can't have.

| Persona | Typical category relevance (adapt to the real inventory) | Tone | Hub page: `.why` lines | Hub page: `.tuned`/`.notincluded` disclosure |
|---|---|---|---|---|
| **Admin** | Administration, channel configuration, access control/permissions, data governance, deprecations | Precise, original terminology, exact field names | No | No — an admin is assumed to know they're seeing a role-scoped view on purpose |
| **Marketer** | Content Management, Campaigns, Journeys, Orchestrated Campaigns, customer-facing Channels | Plain-ish, benefit-oriented | Yes | Yes |
| **Developer** | APIs / MCP tools, custom channels & integrations, Decisioning rules-as-code, Sources/Destinations, SDKs | Precise, keep exact function/field names | Light (not on every item) | Yes |
| **Generic (all personas)** | Everything in scope after Steps 1-2.2 | Neutral, no persona-specific rewrite | No | No — nothing was cut, so there's nothing to disclose |
| **Custom profile** | Whatever the typed profile implies — ask if unclear | Match the profile's stated technical depth | Judge from the profile (closer to Marketer if plain-language, closer to Admin/Developer if technical) | Judge from the profile — disclose if the profile implies a filtered/narrow view |

These are starting points, not a rigid list — always check against what the
real inventory (Steps 1-2.2's scope) actually contains. Admin hub variants
also get one extra footer link (to the Administration guide) — see
`content-model.md` §4 step 8.

## Further refinement signals (either deliverable, layer on top)

These come from the fuller Knowledge Agent signal model (§8 of the original
process spec) and none are wired to a live pipeline — only use them if the
user actually hands you this kind of input.

| Signal | What it captures | What it changes |
|---|---|---|
| **Usage** | Which capabilities this org/user already uses | Which items get featured/proposed first |
| **Permissions** | What the org/sandbox can actually access | Hide items gated behind licenses/entitlements the viewer doesn't have (flag with a "Licensed feature" callout when relevant — ask the user whether to omit or flag-as-upsell rather than silently dropping a real capability) |
| **Freshness** | What's new since the viewer's last visit | Now handled directly by Step 2.3's Release scope question rather than an implicit default — "New since your last visit" is just the toast's kicker copy when Latest release is picked |
| **Intent** | Recurring questions/topics asked to an AI assistant | Promote a specific item to a proposed entry if it solves something the user is known to be stuck on, even if Persona alone wouldn't have surfaced it |

## Observed persona archetypes (hub-page samples, for pattern-matching)

Useful for imitating an existing sample's actual copy voice — see
`samples-catalog.md` for file paths. These predate the Persona-only model
above; read them as "Persona = X, with this much filtering/depth" rather
than a separate axis:

- **Generic / no filter** — everything, standard tags, no rewrite. (`1-ajo-whats-new.html`, `1-aep-whats-new.html`)
- **Marketer (plain-language)** — one product area, plain language, "Why it helps," disclosure boxes. (`2-ajo-whats-new-oc-beginner.html`, `6-aep-whats-new-audiences-beginner.html`)
- **Marketer (cross-cutting)** — a cross-cutting slice (e.g. a capability + the channels it touches), still disclosed. (`3-ajo-whats-new-journeys-mobile.html`)
- **Admin** — config & channels lens, full jargon, no benefit lines, no disclosure boxes, extra Administration-guide link. (`4-ajo-whats-new-admin-channels-config.html`, `5-aep-whats-new-admin-access-governance.html`)
- **Marketer (feature-family deep-dive)** — one named capability across the whole page (e.g. Loyalty). (`7-ajo-whats-new-loyalty.html`)

For the toast deliverable, the equivalent reference sample is
`ajo-new-since-last-visit-concept.html` (see `toast-spec.md`).
