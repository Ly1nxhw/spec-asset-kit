# Plan: Add dry-run support

## Technical Context

- CLI entrypoint appears to need a command layer.
- Proposed path: `src/commands/dry_run.py`.
- Tests should cover argument parsing.

## Implementation Plan

1. Add a new dry-run command helper under `src/commands/dry_run.py`.
2. Add a `--dry-run` flag to the parser.
3. Print preview output when dry-run is set.
4. Keep the existing write path unchanged.

## Risks

- The repository may need a new `src/commands/` package for command handlers.
