# Tasks

The tasks to actually run for elmo are invocations of `compare-locales`.
There can be multiple invocations per task, mainly optimizing for VCS
interactions.

Each task needs the following metadata:

- a list of repositories, with revisions and expected local path
- a command line, referencing the `l10n.toml` files and locales
- a tree identifier to hook back into elmo.

Once compare-locales is run, there's going to be an artifact of its JSON
output.

The task should be created with TC metadata to signal its completion on
a pulse queue. There's going to be a small bot watching the pulse queue.
