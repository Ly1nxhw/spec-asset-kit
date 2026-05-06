# AI Assets Evaluation Report

## Summary

- Date: 2026-05-06
- Evaluator: Codex
- Model: gpt-5.5
- Cases: 0 real historical replay cases
- Groups: L0 completed

## Main Result

| Metric | A Baseline | B Asset | Delta |
|---|---:|---:|---:|
| L0 engineering regression | 60 passed, 1 skipped | 60 passed, 1 skipped | 0 |
| Plan score | n/a | n/a | n/a |
| Missing path count | n/a | n/a | n/a |
| Hallucination count | n/a | n/a | n/a |
| Review blocker count | n/a | n/a | n/a |
| Task actionability | n/a | n/a | n/a |
| Expected file hit rate | n/a | n/a | n/a |
| Out-of-scope file count | n/a | n/a | n/a |
| Behavior match score | n/a | n/a | n/a |
| Gold diff alignment score | n/a | n/a | n/a |

## Historical Replay Result

| Case | A Acceptable | B Acceptable | A Score | B Score | Winner | Reason |
|---|---|---|---:|---:|---|---|
| none | n/a | n/a | n/a | n/a | n/a | No real case manifests are present yet. |

## Findings

- `extensions/ai-assets` regression coverage is green in the local checkout.
- `extensions/ai-assets/scripts/scan_repo.py .` completed and returned repository source inventory.
- `evaluation.zh-CN.md` defines the full L1-L4 process, but real case data still needs to be created.

## Failure Cases

- No generated root `ai-assets/` directory is present yet, so L1 asset quality scoring cannot start.
- No historical replay case has been prepared, so L2-L3 cannot start yet.

## Judge Notes

- The run is only a starter checkpoint. It does not yet exercise the A/B replay flow.

## Template Changes Suggested

- None.

## Extractor Changes Suggested

- None yet.

## Decision

- [ ] Continue
- [ ] Roll back default enablement
- [ ] Ship with limitations
- [ ] Expand to real team A/B
