# Embedded Release Notes

Generate curated Adobe release-note hub pages and contextual toasts from
official documentation sources.

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

Names use lowercase ASCII `kebab-case`. Years use four digits and months use
two digits. For a multi-product request, the product folder joins slugs in
the supplied order, such as `ajo-aep`.

## Repository layout

```text
.github/skills/custom-release-notes/  Skill, references, templates, utilities
.github/prompts/                      VS Code launchers
requests/                             Versioned generation manifests
generated/                            Generated standalone HTML pages
schemas/                              Request contract
scripts/                              Repository-level command-line tools
tests/                                Automated validation
```

## Validate

```bash
python3 -m unittest discover -s tests -v
```