from __future__ import annotations

import importlib.util
from pathlib import Path


def load_aggregator():
    script = Path(__file__).parents[2] / "evaluation" / "scripts" / "aggregate_results.py"
    spec = importlib.util.spec_from_file_location("aggregate_results", script)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_collect_runs_excludes_templates_and_non_ab_runs():
    aggregator = load_aggregator()
    rows = aggregator.collect_runs(Path(__file__).parents[2] / "evaluation")

    assert {row["run_id"] for row in rows} == {
        "sim-cli-dry-run-001-a-01",
        "sim-cli-dry-run-001-b-01",
    }


def test_aggregate_reports_b_improvement_for_simulated_case():
    aggregator = load_aggregator()
    evaluation_root = Path(__file__).parents[2] / "evaluation"
    summary = aggregator.aggregate(
        aggregator.collect_runs(evaluation_root),
        aggregator.collect_judges(evaluation_root),
    )

    assert summary["run_count"] == 2
    assert summary["case_count"] == 1
    assert summary["b_win_rate"] == 1.0
    assert summary["metrics"]["missing_path_count"]["relative_improvement"] == 1.0
    assert summary["metrics"]["gold_diff_alignment_score"]["B_mean"] == 5.0
