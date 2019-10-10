# Scheduler


When to compare which locales for which project.

We don't want to regenerate all l10n metadata for each push to each
repository, so there's scheduling involved when creating a task graph.

This is relatively easy for monorepos, but for multi-repo projects, that's
a tad trickier.

All scheduling is done by configuration files in the main project repository.

The scheduling takes these steps, broadly:

1. Identify which repositories hold configuration files for the triggering repo.
2. Identify the current revisions for each repository.
3. Load the configurations for each repository, and annotate them with
   elmo build metadata, a tree name.
4. Match the changed files against the configs, keeping track of found locales
   and trees.

To evaluate the files, we'll need to map the file paths in the repositories
into a local file system. We don't necessarily need the full repositories to
be checked out locally, though.

## Virtual file system

The taskgraph generation works on a virtual file structure. For hgmo, the
file paths are rooted in `/hgmo/`, and then continue with the repository
name and then the local paths.

```
/hgmo/
    mozilla-central/
        browser/locales/l10n.toml
    l10n-central/
        af/browser/browser/browser.ftl
        de/browser/browser/browser.ftl
    releases/
        mozilla-beta/
            browser/locales/l10n.toml
```
