# Sample catalog — existing hand-built variants

Location: a local folder of hand-built mockups — ask the user for the path
if it isn't already known on this machine (images live in an `assets-RN/`
subfolder alongside the HTML files, including an `assets-RN/Loyalty/`
subfolder for loyalty-specific screenshots). **Reference-only folder** — read
from it, never write generated output here; skip this catalog entirely if
the folder isn't present rather than guessing a path. This skill's own
generated HTML is saved to the user's Downloads folder (`~/Downloads/`)
instead, per `SKILL.md` Step 5.

These are the original hand-authored mockups this skill was distilled from.
When asked to produce a variant close to one of these, **open the real file
and imitate its actual copywriting voice and section choices** — this
catalog is a map, not a substitute for reading the source. Files are large
(hundreds of KB to several MB, mostly embedded base64 images); read them in
chunks or grep for structure rather than loading the whole file.

| File | Solution | Persona | Notes |
|---|---|---|---|
| `1-ajo-whats-new.html` | AJO | General / no filter | The reference "full variant" — this is what `templates/base-template.html` was distilled from. Wrap 1160px. |
| `2-ajo-whats-new-oc-beginner.html` | AJO | Beginner — Orchestrated Campaigns only | Drops Journeys/Decisioning entirely. Uses `.tuned`/`.notincluded`/`.spot`/`.why`. Wrap 980px. |
| `3-ajo-whats-new-journeys-mobile.html` | AJO | Specialist — Journeys + mobile channels | Cross-cutting scope (a capability + the channels touching it), not a single product area. |
| `4-ajo-whats-new-admin-channels-config.html` | AJO | Admin — channels & configuration | Full jargon, no `.why` lines, extra Administration-guide footer link. Wrap 1160px. |
| `7-ajo-whats-new-loyalty.html` | AJO | Feature-family deep-dive — Loyalty | Uses `assets-RN/Loyalty/` screenshots specifically. |
| `8-ajo-whats-new-orchestrated-campaigns.html` | AJO | Feature-family deep-dive — Orchestrated Campaigns | 4-tab variant (includes a `jun26` bucket) — shows the tab pattern extends past 3 when there's a reason to keep an extra month. |
| `1-aep-whats-new.html` | AEP | General / no filter | AEP equivalent of file 1 — same component vocabulary, different category set (Destinations, Sandboxes, Segmentation, Sources, Access Control). |
| `5-aep-whats-new-admin-access-governance.html` | AEP | Admin — access control & data governance | AEP admin equivalent of file 4. |
| `6-aep-whats-new-audiences-beginner.html` | AEP | Beginner — Audiences | AEP beginner equivalent of file 2; note it runs 3 tabs including a `jun26` bucket. |
| `ajo-whats-new-hub-full-august.html` | AJO | Raw inventory (not a persona page) | The "everything, untrimmed, tagged by status" pattern every persona cut should be filtered from. Copy this pattern first when a new month's inventory doesn't exist yet. |

## The toast deliverable's reference sample

`ajo-new-since-last-visit-concept.html` ("Exploration 2 · corner toast, in
the AI-tooltip's slot") is the real source for the **toast** deliverable —
see `toast-spec.md` and the central `toast.json` registry, both distilled from
it. Unlike the hub samples above, this one uses its own blue/neutral palette
(`--blue:#577CF8`), kept deliberately distinct from the hub's Adobe-red
system (confirmed with the user, not an oversight).

## Not part of the reusable pattern

The following files in the same folder are earlier-stage exploration
artifacts (four-surface debate, entry-point iteration, pitch decks) — useful
for background on *why* the hub/toast exist, not templates to copy:
`in-product-release-initiative.html`, `release-awareness*.html`,
`hub-entry-points-v2.html`, `exploration*-in-product-hub*.html`,
`explainer-for-content-authors.html`, `ajo-whats-new-OLD.html`, and the
`.pptx` files. See `0-wiki-creation-process.md` in that folder for the full
history if asked.
