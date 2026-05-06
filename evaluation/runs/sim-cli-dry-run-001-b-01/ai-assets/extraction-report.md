# Extraction Report

## Sources Scanned

- `sample_cli.py`
- `tests/test_sample_cli.py`
- `evaluation/cases/sim-cli-dry-run-001/input.md`

## Main Conclusions

- The fixture has one CLI entrypoint and one pytest file.
- `--dry-run` should be implemented in `sample_cli.py`.
- The most important behavioral check is that dry-run does not create the output file.

## Gaps

- The fixture intentionally has no package metadata, CI config, or changelog.

## Planning Guidance

- `speckit.plan` should consume `glossary.md`, `repo-map.md`, `architecture.md`, and `conventions.md` before planning.
