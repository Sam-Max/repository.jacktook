---
name: submodule-updater
description: Update Jacktook repository submodules and regenerate the Kodi repository index.
---

# Submodule Updater Skill

This skill provides a standardized workflow for updating Jacktook submodules (like `plugin.video.jacktook`) and synchronizing the Kodi repository.

## 📋 Workflow

### 1. Update the Submodule
Navigate to the submodule directory and fetch the latest changes.
```bash
git submodule update --remote <submodule_path>
```
*Note: If local changes cause conflicts, you may need to enter the submodule and run `git reset --hard origin/main`.*

### 2. Verify Version and Changelog
Ensure the repository's metadata files match the updated submodule version.
- Check `packages/jacktook_version`
- Check `packages/jacktook_changelog`

### 3. Regenerate Repository Index
Run the repository generator script to update `addons.xml`, MD5 hashes, and create new ZIP packages.
```bash
python3 _repo_generator.py
```

### 4. Stage Changes
Stage the updated submodule pointer, the generated ZIPs, and the updated index files.
```bash
git add repo/<submodule_name> repo/zips/ packages/jacktook_changelog packages/jacktook_version
```

## ⚠️ Important Considerations
- **No Path Changes**: Always use absolute paths or paths relative to the repository root.
- **Clean Slate**: Ensure the submodule is on the correct branch (usually `main`) before regenerating the index.
- **Manual Commits**: Review the staged changes before committing, as per the user's preference for manual commits.
