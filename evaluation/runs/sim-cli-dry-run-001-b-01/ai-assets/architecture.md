# Architecture

## Observed

- [high] `build_parser()` owns argparse configuration. Source: `sample_cli.py`.
- [high] `write_message()` owns filesystem writes. Source: `sample_cli.py`.
- [high] `main()` parses arguments, calls `write_message()`, prints status, and returns an integer. Source: `sample_cli.py`.

## Inferred

- [medium] The right extension point for `--dry-run` is the existing parser plus write function, not a new command module.

## Open Questions

- [low] No separate logging or command dispatch layer exists in this fixture.
