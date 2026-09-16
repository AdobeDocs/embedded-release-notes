---
name: release-publisher
description: "Validate, branch, commit, push, and open a pull request for embedded release-note changes. Use when asked to auto-commit, publish, push, or create a PR for generated hubs and toast registry updates."
argument-hint: "publish request=requests/<product>/<year>/<month>/<slug>.json"
---

# Release Publisher

Publish one release-note change set through a reviewable Git branch and pull
request. Never commit directly to `main` and never include unrelated changes.

## Workflow

1. Read the request manifest and derive a branch named
   `release/<product>-<year>-<month>-<slug>`.
2. Inspect `git status --short`, the diff, and untracked files. Identify the
   exact request, generated hub, and `toast.json` changes belonging to the
   release. Stop if unrelated changes cannot be separated safely.
3. Run:

   ```bash
   python3 scripts/toast_registry.py validate
   python3 scripts/release_files.py validate
   python3 -m unittest discover -s tests -v
   git diff --check
   ```

4. Present the branch, exact files, proposed commit message, and PR title to
   the user. Obtain explicit confirmation before any branch, commit, or push.
5. Create the branch, stage only the approved paths, commit, and push with
   upstream tracking.
6. Open a PR with `gh pr create`, summarizing the release ID, UI surface,
   source request, generated hub, and validations.
7. If `gh auth status` fails, do not request credentials in chat. Leave the
   pushed branch intact and provide the GitHub compare URL so the user can open
   the PR in their authenticated browser.

Never merge the PR, force-push, amend an existing commit, or bypass branch
protection unless the user explicitly requests it.