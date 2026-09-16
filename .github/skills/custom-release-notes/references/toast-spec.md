# Toast specification - component-facing JSON

The toast deliverable is one configuration entry in the repository's central
`toast.json` registry. The web component owns rendering. Never generate a
standalone toast HTML file.

## Selection

The component supplies one `surface` value. The registry permits exactly one
release-note card per surface. Publishing a new release for an occupied
surface replaces the old entry; Git history retains previous releases.

The stable entry ID is:

```text
<surface>-<release-year>-<release-month>-<slug>
```

Example: `ajo-2026-06-general`.

## Required content

- `title`: the card heading, such as `What's new for Loyalty`.
- `items`: exactly two entries derived from the generated hub.
- `items[].icon`: a component icon token plus foreground and background hex
   colors.
- `items[].title`: the bold item subtitle.
- `items[].description`: the concise supporting sentence.
- `action.label`: action label such as `See what's new`.
- `action.href`: repository-relative path to the request's generated
   `hub.html`.
- `dismiss.label`: dismissal label such as `Dismiss`.

Items can represent a feature, deprecation, confirmed video, or meaningful
documentation update. Every item must trace to an official source or explicit
author input. Never invent content to fill the item count.

## Draft and review

1. Generate and approve the complete hub before deriving the card.
2. Draft exactly two candidates from that hub and name each source.
3. Confirm surface, release, title, icon configuration, items, action label,
   and dismissal label with the author.
4. Obtain explicit approval before updating the registry.
5. Create a temporary entry JSON and run:

   ```bash
   python3 scripts/toast_registry.py upsert --entry <entry.json>
   ```

6. Validate:

   ```bash
   python3 scripts/toast_registry.py validate
   python3 scripts/release_files.py validate
   ```

## Checklist

- [ ] ID matches surface, release year/month, and slug.
- [ ] Surface lookup is explicit and unique.
- [ ] Exactly two sourced items with icons are present.
- [ ] `action.href` points to the existing hub from the source request.
- [ ] `source_request` points to an existing request manifest.
- [ ] Both validators pass.