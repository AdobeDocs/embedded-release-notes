---
name: release-file-manager
description: "Create, list, rename, and validate embedded release-note requests, generated folders, and cross-file references. Use when organizing files or changing a release slug without breaking toast IDs and links."
argument-hint: "create, list, rename, or validate release files"
---

# Release File Manager

Keep request manifests, generated folders, and toast references synchronized.

## Create

Use `scripts/new_request.py`; do not create the hierarchy manually:

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

## List and validate

```bash
python3 scripts/release_files.py list
python3 scripts/release_files.py validate
python3 scripts/toast_registry.py validate
```

Validation must pass before generation or publication.

## Rename

Never rename a request or generated directory directly. Run:

```bash
python3 scripts/release_files.py rename \
  --request requests/<product>/<year>/<month>/<slug>.json \
  --new-slug <new-slug>
```

This updates the request filename, `slug`, `output_directory`, generated
directory, matching toast ID, release slug, and `source_request`. Review the
result with `git status --short` and rerun both validators.