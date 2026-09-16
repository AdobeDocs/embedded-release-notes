---
name: toast-registry
description: "Create, replace, list, and validate in-product release-note cards in the central toast.json registry. Use when managing surface-based content, icons, release IDs, or links to generated hubs."
argument-hint: "create, replace, list, or validate a toast"
---

# Toast Registry

Manage toast data consumed by the web component. Toasts are JSON entries, not
standalone HTML files.

## Contract

The single registry is `toast.json`; its contract is
`schemas/toasts.schema.json`. The component selects an entry using its
`surface` attribute:

```html
<releasenote surface="ajo"></releasenote>
```

Only one entry may exist per surface. Adding a new release to an existing
surface replaces the previous entry; Git history preserves old values.

Each ID uses `<surface>-<release-year>-<release-month>-<slug>`. Content is
English-only and contains a title, exactly two items with icon configuration,
an action to the generated hub, and a dismissal label.

## Create or replace

1. Collect surface, release year/month/slug, release label, and the approved
   card copy and icon tokens/colors.
2. Verify every item against the release-note source. Never fabricate content.
3. Set `action.href` to `<output_directory>hub.html` from the source request and
   verify that file exists.
4. Write one temporary entry JSON outside the registry.
5. Run:

   ```bash
   python3 scripts/toast_registry.py upsert --entry <entry.json>
   ```

6. Run both validations:

   ```bash
   python3 scripts/toast_registry.py validate
   python3 scripts/release_files.py validate
   ```

7. Report which surface was added or replaced. Never edit `toast.json` with
   ad hoc string replacement.

## Other operations

```bash
python3 scripts/toast_registry.py list
python3 scripts/toast_registry.py resolve --surface ajo
python3 scripts/toast_registry.py validate
```

Use the release file manager when changing a release slug, because it
updates the request, output directory, toast ID, and source reference together.