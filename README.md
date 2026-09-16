# Embedded Release Notes

Generate curated Adobe release-note hub pages and component-facing contextual
toast configurations from official documentation sources.

## Run from VS Code

1. Open this repository in VS Code.
2. In Copilot Chat, run `/generate-release-notes`.
3. Provide the requested product, deliverable, scope, persona, and output slug.
4. Review and approve the draft before the skill writes HTML.

The launcher creates a request manifest and invokes the
`custom-release-notes` skill. You can also invoke the skill directly:

```text
/custom-release-notes request=requests/ajo/2026/09/loyalty-admin.json
```

## Create a request from the terminal

```bash
python3 scripts/new_request.py \
	--products ajo \
	--surface ajo \
	--year 2026 \
	--month 9 \
	--slug loyalty-admin \
	--deliverables hub toast \
	--theme Loyalty \
	--persona Admin
```

This creates:

```text
requests/ajo/2026/09/loyalty-admin.json
generated/ajo/2026/09/loyalty-admin/
```

The workflow first generates the complete release note as `hub.html`, then
derives exactly two highlighted items into the central `toast.json`. The web
component renders the card from JSON; no standalone toast HTML is generated.

## Toast lookup

The component supplies the value of its `surface` attribute. The matching
entry contains the card title, two illustrated items, dismissal label, and
the action that opens the generated `hub.html`. Adding a newer release for
the same surface replaces the previous entry.

See [docs/toast-contract.md](docs/toast-contract.md) for the exact contract.

Manage the registry with:

```bash
python3 scripts/toast_registry.py list
python3 scripts/toast_registry.py resolve --surface ajo
python3 scripts/toast_registry.py validate
python3 scripts/toast_registry.py upsert --entry /path/to/toast-entry.json
```

Names use lowercase ASCII `kebab-case`. Years use four digits and months use
two digits. For a multi-product request, the product folder joins slugs in
the supplied order, such as `ajo-aep`.

## Repository layout

```text
.github/skills/custom-release-notes/  Skill, references, templates, utilities
.github/skills/toast-registry/        Toast JSON creation and replacement
.github/skills/release-file-manager/  File naming and reference integrity
.github/skills/release-publisher/     Branch, commit, push, and PR workflow
.github/prompts/                      VS Code launchers
requests/                             Versioned generation manifests
generated/                            Generated standalone hub HTML pages
toast.json                            Release-note cards keyed by UI surface
schemas/                              Request contract
scripts/                              Repository-level command-line tools
tests/                                Automated validation
```

## Validate

```bash
python3 -m unittest discover -s tests -v
python3 scripts/toast_registry.py validate
python3 scripts/release_files.py validate
```