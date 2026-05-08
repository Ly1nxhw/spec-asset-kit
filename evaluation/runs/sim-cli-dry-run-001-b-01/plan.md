# Plan: Add dry-run support

## AI Assets 输入

- `ai-assets/business-context.md`: the CLI is a small file-writing workflow where users need a safe preview path.
- `ai-assets/domain-glossary.md`: `dry-run` means previewing the write without creating the output file.
- `ai-assets/business-rules.md`: normal mode must keep writing the message, while dry-run mode must not create or modify the target file.
- `ai-assets/user-journeys.md`: the dry-run journey should parse the same inputs, print preview feedback, and stop before filesystem writes.

## Technical Context

- Modify `sample_cli.py`; do not add a new command package. This path is an implementation anchor, not an architecture decision.
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
