---
name: submodule-updater
description: "Trigger: update repository, update submodule, refresh addons. Update one or all Jacktook submodules and regenerate repository artifacts."
license: Apache-2.0
metadata:
  author: sammax
  version: "1.0"
---

## Activation Contract

Load when the user requests a repository or submodule update. Support an explicitly named submodule and an all-submodule update.

## Hard Rules

- Run commands from the repository root using root-relative paths.
- Never reset, checkout, stash, or otherwise discard local submodule changes. If they block the update, report the conflict and stop.
- Preserve unrelated working-tree and staging changes. Do not commit unless the user explicitly requests it.

## Decision Gates

| Request | Update command |
| --- | --- |
| No submodule target | `git submodule update --remote --recursive` |
| Specific `<submodule_path>` | `git submodule update --remote <submodule_path>` |

## Execution Steps

1. Inspect `git status --short` and `git submodule status --recursive` before updating.
2. Run the command selected above. Verify the changed submodule pointers afterward.
3. Check `packages/jacktook_version` and append, never replace, the appropriate changelog entry in `packages/jacktook_changelog` for each updated add-on.
4. Run `python3 _repo_generator.py` to refresh repository indexes, hashes, and ZIP packages.
5. Stage only the updated submodule pointer or pointers, generated artifacts, and relevant metadata. For an all-submodule update, use every changed submodule path rather than one hard-coded path. Review staged changes; leave committing to the user.

## Output Contract

Return the update scope, changed submodule paths, generated artifacts, staging status, and any local-change blocker. State that no commit was created.

## References

- `_repo_generator.py` — generates repository indexes and ZIP packages.
- `packages/jacktook_version` — repository version metadata.
- `packages/jacktook_changelog` — append-only changelog metadata.
