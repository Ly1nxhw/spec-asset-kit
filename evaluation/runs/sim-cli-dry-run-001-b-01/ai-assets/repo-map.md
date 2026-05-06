# Repo Map

## Observed

- [high] `sample_cli.py`: only source file and CLI entrypoint. Source: fixture tree.
- [high] `tests/test_sample_cli.py`: pytest behavior tests. Source: fixture tree.

## Inferred

- [medium] A feature of this size should touch only `sample_cli.py` and `tests/test_sample_cli.py`.

## Open Questions

- [low] There is no `src/` directory in the fixture.
