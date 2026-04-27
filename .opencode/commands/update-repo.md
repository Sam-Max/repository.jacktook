---
description: Update repository submodules and regenerate the Kodi index
---

Load the `submodule-updater` skill and execute its workflow for this repository.

If the user passes arguments, treat them as the preferred submodule target or extra scope details: `$ARGUMENTS`.

Follow the skill exactly, preserve unrelated local changes, and do not create a commit unless the user explicitly asks for one.
