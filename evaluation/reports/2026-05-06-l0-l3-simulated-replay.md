# AI Assets Evaluation Report

## Summary

- Date: 2026-05-06
- Evaluator: Codex
- Model: gpt-5.5
- Cases: 1 simulated historical replay case
- Groups: A baseline / B asset enhanced
- Case: `sim-cli-dry-run-001`

## Main Result

| Metric | A Baseline | B Asset | Delta |
|---|---:|---:|---:|
| L0 engineering regression | 60 passed, 1 skipped | 60 passed, 1 skipped | 0 |
| L1 asset file completeness | n/a | 100% | n/a |
| L1 section completeness | n/a | 100% | n/a |
| L1 grounded rate | n/a | 91% | n/a |
| Plan score | 62 | 94 | +52% |
| Missing path count | 1 | 0 | -100% |
| Hallucination count | 1 | 0 | -100% |
| Review blocker count | 1 | 0 | -100% |
| Task actionability | 3/5 | 5/5 | +2 |
| Expected file hit rate | 100% | 100% | 0 |
| Out-of-scope file count | 0 | 0 | 0 |
| Behavior match score | 2/5 | 5/5 | +3 |
| Gold diff alignment score | 2/5 | 5/5 | +3 |
| Gold acceptance tests | 1 failed, 1 passed | 2 passed | B passed |

## Historical Replay Result

| Case | A Acceptable | B Acceptable | A Score | B Score | Winner | Reason |
|---|---|---|---:|---:|---|---|
| `sim-cli-dry-run-001` | false | true | 51 | 100 | B | B matched no-write dry-run behavior and avoided hallucinated paths. |

## L0 Evidence

Command:

```bash
PYTHONPATH=src pytest tests/extensions/ai_assets/test_ai_assets_extension.py -v tests/integrations/test_integration_generic.py -v tests/integrations/test_integration_codex.py -v
```

Result: `60 passed, 1 skipped in 1.21s`.

## L1 Evidence

Assets evaluated from `evaluation/runs/sim-cli-dry-run-001-b-01/ai-assets/`:

- `project-overview.md`
- `glossary.md`
- `architecture.md`
- `repo-map.md`
- `conventions.md`
- `evolution-log.md`
- `extraction-report.md`

Result:

- `asset_file_completeness = 100%`
- `section_completeness = 100%`
- `grounded_rate = 91%`
- `unsupported_observed_count = 0`
- `wrong_fact_count = 0`

## L2 Evidence

A group output:

- `evaluation/runs/sim-cli-dry-run-001-a-01/plan.md`
- `evaluation/runs/sim-cli-dry-run-001-a-01/tasks.md`

B group output:

- `evaluation/runs/sim-cli-dry-run-001-b-01/plan.md`
- `evaluation/runs/sim-cli-dry-run-001-b-01/tasks.md`

L2 finding:

- A group hallucinated `src/commands/dry_run.py`.
- B group referenced `repo-map.md`, `architecture.md`, `conventions.md`, and `glossary.md`, then planned against the real files.

## L3 Evidence

Gold reference:

- `evaluation/cases/sim-cli-dry-run-001/gold.diff`
- `evaluation/cases/sim-cli-dry-run-001/gold-files.txt`

A group:

- Project tests: `2 passed`
- Gold acceptance tests: `1 failed, 1 passed`
- Blocker: `--dry-run` still creates the output file.

B group:

- Project tests: `2 passed`
- Gold acceptance tests: `2 passed`
- Blocker: none.

## Judge Notes

- A changed the correct files but missed the core side-effect requirement.
- B changed the same gold key files and matched the behavior checklist.
- This is a simulated replay, so it validates the evaluation mechanics and demonstrates the expected signal shape, but it is not yet evidence from a real team feature.

## Template Changes Suggested

- Keep the `AI Assets 输入` section strict: require concrete asset filenames and extracted facts.
- Add a planning reminder that parser-only tests are insufficient when the requirement is behavioral.

## Extractor Changes Suggested

- No extractor change is required from this single simulated case.

## Decision

- [x] Continue
- [ ] Roll back default enablement
- [ ] Ship with limitations
- [ ] Expand to real team A/B
