# Plan: Add dry-run support

## AI Assets 输入

- `ai-assets/repo-map.md`: CLI entrypoint is `sample_cli.py`; tests live in `tests/test_sample_cli.py`.
- `ai-assets/architecture.md`: behavior is currently concentrated in `build_parser`, `write_message`, and `main`.
- `ai-assets/conventions.md`: use argparse in the existing file and pytest for behavior tests.
- `ai-assets/glossary.md`: `dry-run` means preview without writing the output file.

## Technical Context

- Modify `sample_cli.py`; do not add a new command package.
- Preserve the existing write behavior when `--dry-run` is absent.
- Add a behavior test that proves the output file is not created.

## Implementation Plan

1. Add `--dry-run` to `build_parser`.
2. Extend `write_message` with a `dry_run` keyword-only flag.
3. In dry-run mode, print the preview and return before writing.
4. In normal mode, keep writing `message + "\n"` and keep the existing `wrote` output.
5. Add a pytest case in `tests/test_sample_cli.py` for no-file dry-run behavior.

## Risks

- Avoid changing file encoding or newline behavior for the existing path.
