---
name: Generate Embedded Release Notes
description: "Launch the Custom Release Notes skill with structured product, scope, persona, and output variables."
argument-hint: "Generate a hub page, toast, or both"
agent: agent
---

Use the [Custom Release Notes skill](../skills/custom-release-notes/SKILL.md)
to prepare embedded release notes with these intake values:

- Products: `${input:products:ajo or a comma-separated list such as ajo,aep}`
- Deliverables: `${input:deliverables:hub,toast}`
- Theme or context: `${input:theme:product area or feature family}`
- Persona: `${input:persona:Generic, Marketer, Developer, Admin, or custom}`
- Release scope: `${input:releaseScope:latest-release, last-two-releases, latest-updates, or custom}`
- Release value or timeframe: `${input:releaseValue:optional date, month, or version}`
- Include: `${input:include:optional comma-separated features}`
- Exclude: `${input:exclude:optional comma-separated features}`
- Output year: `${input:year:four-digit year}`
- Output month: `${input:month:month number}`
- Output slug: `${input:slug:lowercase-kebab-case name}`
- UI surface: `${input:surface:component surface, defaults to the product for a single-product request}`

First create the request manifest with `scripts/new_request.py`, translating
comma-separated values into separate command arguments. Then follow the full
skill workflow. Do not repeat questions answered above. Generate and display
`hub.preview.html`, offer to revise its content, order, images, or presentation,
and repeat until the author has no more changes. Ask whether the page is ready
to render as final before creating `hub.html`. Only then derive exactly two
illustrated items into `toast.json`, with `action.href` pointing back to that
hub. Never create a standalone toast HTML file.