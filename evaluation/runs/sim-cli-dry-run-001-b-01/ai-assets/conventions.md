# Conventions

## Observed

- [high] CLI options are declared with `argparse.ArgumentParser`. Source: `sample_cli.py`.
- [high] Tests call `main([...])` directly and use pytest `tmp_path`. Source: `tests/test_sample_cli.py`.
- [high] File reads and writes use UTF-8. Source: `sample_cli.py`, `tests/test_sample_cli.py`.

## Inferred

- [medium] New behavior should be validated through direct `main([...])` behavior tests.

## Open Questions

- [low] No formatting or linting configuration is present in the fixture.
