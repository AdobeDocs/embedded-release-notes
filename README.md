# Embedded Release Notes

Published release-note content for Adobe Journey Optimizer, shown inside the
product by a web component. This repository holds the **generated files only**:
the release-note pages and the `toast.json` registry the component reads.

## How it works

1. The documentation team publishes a release-note page (`hub.html`) and updates
   `toast.json`.
2. The product passes a `surface` value (for example `loyalty`) to the component.
3. The component loads `toast.json`, finds the entry for that surface, and shows
   a card with two highlights. The card links to the full page, which opens in
   the product's release-note modal.

The component loads only `toast.json`. The page is loaded when the user opens
it. Updating the two files updates the product, with no new product release.

## Published files

Served with GitHub Pages from `main`:

| File | URL |
|---|---|
| Toast registry | https://adobedocs.github.io/embedded-release-notes/toast.json |
| Loyalty release notes | https://adobedocs.github.io/embedded-release-notes/generated/ajo/2026/10/loyalty/hub.html |

`toast.json` keeps one entry per surface. A new release for a surface replaces
its entry. Git history keeps the earlier ones. The contract with the component
is in [docs/toast-contract.md](docs/toast-contract.md).

## Repository layout

```text
toast.json                         Registry read by the component, keyed by surface
generated/<product>/<yyyy>/<mm>/<slug>/hub.html   Release-note pages
requests/<product>/<yyyy>/<mm>/<slug>.json        What each page covers (product, persona, period, sources)
schemas/                           JSON schemas for toast.json and requests
scripts/                           Validators and helpers
tests/                             Automated checks
docs/                              Component contract and workflow diagram
```

## External links

Pages are shown in an iframe. Sites such as Experience League refuse to be
framed, so every external link in a page must open in a new tab:
`target="_blank" rel="noopener noreferrer"`. In-page links (`#...`) are exempt.

```bash
python3 scripts/hub_links.py check   # fail if an external link is missing either attribute
python3 scripts/hub_links.py fix     # add the attributes
```

## Validate

These checks also run on every pull request.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/toast_registry.py validate
python3 scripts/release_files.py validate
python3 scripts/hub_links.py check
```

Names use lowercase ASCII `kebab-case`, years use four digits and months two.

## Registry commands

```bash
python3 scripts/toast_registry.py list
python3 scripts/toast_registry.py resolve --surface loyalty
python3 scripts/toast_registry.py upsert --entry /path/to/entry.json
```
