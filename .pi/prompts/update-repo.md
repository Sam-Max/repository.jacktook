---
description: Update repository submodules and regenerate the Kodi index
argument-hint: "[submodule_path]"
---

# Update repository

Read and follow `.opencode/skills/submodule-updater/SKILL.md` exactly for this request.

Execute the workflow; do not only describe it. Use `$ARGUMENTS` as the preferred submodule target or additional scope details. If no target is provided, update all top-level submodules.

Preserve unrelated local changes, never use `--recursive` for update commands, and do not create a commit unless the user explicitly requests one. Report the update scope, changed submodule paths, generated artifacts, staging status, blockers, and whether a commit was created.
