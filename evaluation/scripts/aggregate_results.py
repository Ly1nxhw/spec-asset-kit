#!/usr/bin/env python3
"""Aggregate ai-assets evaluation run records into quantitative summaries."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

import yaml


POSITIVE_METRICS = {
    "path_exists_rate",
    "expected_file_hit_rate",
    "changed_file_precision",
    "behavior_match_score",
    "test_overlap_rate",
    "gold_diff_alignment_score",
    "asset_file_completeness",
    "section_completeness",
    "grounded_rate",
    "useful_asset_score",
}

NEGATIVE_METRICS = {
    "missing_path_count",
    "unknown_dependency_count",
    "wrong_test_framework_count",
    "out_of_scope_file_count",
    "review_blocker_count",
    "manual_fix_minutes",
    "unsupported_observed_count",
    "wrong_fact_count",
}

GROUPS = ("A", "B")


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def numeric(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int | float):
        return float(value)
    return None


def collect_runs(evaluation_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for run_file in sorted((evaluation_root / "runs").glob("*/run.yml")):
        if run_file.parent.name.startswith("_"):
            continue
        run = load_yaml(run_file)
        group = str(run.get("group", ""))
        if group not in GROUPS:
            continue

        outputs = run.get("outputs") or {}
        if not isinstance(outputs, dict):
            outputs = {}
        if not (outputs.get("plan") or outputs.get("tasks")):
            continue

        metrics_file = run_file.parent / "metrics.yml"
        metrics = load_yaml(metrics_file) if metrics_file.exists() else (run.get("metrics") or {})
        if not isinstance(metrics, dict):
            metrics = {}

        review = run.get("review") or {}
        if not isinstance(review, dict):
            review = {}

        row: dict[str, Any] = {
            "run_id": run.get("run_id") or run_file.parent.name,
            "case_id": run.get("case_id"),
            "group": group,
            "model": run.get("model"),
            "agent": run.get("agent"),
            "run_file": str(run_file),
            "metrics_file": str(metrics_file) if metrics_file.exists() else "",
            "review_blocker_count": metrics.get(
                "review_blocker_count", review.get("blocker_count")
            ),
        }
        row.update(metrics)
        rows.append(row)
    return rows


def collect_judges(evaluation_root: Path) -> dict[str, dict[str, Any]]:
    judges: dict[str, dict[str, Any]] = {}
    for judge_file in sorted((evaluation_root / "runs").glob("*/judge-summary.yml")):
        judge = load_yaml(judge_file)
        case_id = judge.get("case_id")
        if case_id:
            judges[str(case_id)] = judge
    return judges


def metric_average(rows: list[dict[str, Any]], metric: str) -> float | None:
    values = [value for row in rows if (value := numeric(row.get(metric))) is not None]
    return mean(values) if values else None


def relative_delta(group_a: float | None, group_b: float | None, higher_is_better: bool) -> float | None:
    if group_a is None or group_b is None:
        return None
    if group_a == 0:
        return None if group_b == 0 else 1.0
    if higher_is_better:
        return (group_b - group_a) / abs(group_a)
    return (group_a - group_b) / abs(group_a)


def aggregate(rows: list[dict[str, Any]], judges: dict[str, dict[str, Any]]) -> dict[str, Any]:
    by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_group[str(row["group"])].append(row)
        by_case[str(row["case_id"])].append(row)

    metrics = sorted((POSITIVE_METRICS | NEGATIVE_METRICS) & set().union(*(row.keys() for row in rows)))
    metric_summary = {}
    for metric in metrics:
        higher_is_better = metric in POSITIVE_METRICS
        a_avg = metric_average(by_group.get("A", []), metric)
        b_avg = metric_average(by_group.get("B", []), metric)
        metric_summary[metric] = {
            "direction": "higher_is_better" if higher_is_better else "lower_is_better",
            "A_mean": a_avg,
            "B_mean": b_avg,
            "relative_improvement": relative_delta(a_avg, b_avg, higher_is_better),
        }

    case_summaries: dict[str, Any] = {}
    b_wins = 0
    judged_cases = 0
    for case_id, case_rows in sorted(by_case.items()):
        groups = {row["group"]: row for row in case_rows if row["group"] in GROUPS}
        judge = judges.get(case_id, {})
        winner = judge.get("winner")
        if winner in GROUPS:
            judged_cases += 1
            if winner == "B":
                b_wins += 1
        case_summaries[case_id] = {
            "groups_present": sorted(groups.keys()),
            "winner": winner,
            "judge_summary": judge.get("summary"),
        }

    return {
        "run_count": len(rows),
        "case_count": len(by_case),
        "group_counts": {group: len(group_rows) for group, group_rows in sorted(by_group.items())},
        "judged_case_count": judged_cases,
        "b_win_rate": (b_wins / judged_cases) if judged_cases else None,
        "metrics": metric_summary,
        "cases": case_summaries,
    }


def write_csv(rows: list[dict[str, Any]], output_path: Path) -> None:
    fieldnames = sorted(set().union(*(row.keys() for row in rows))) if rows else []
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def format_percent(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.1f}%"


def write_report(summary: dict[str, Any], output_path: Path) -> None:
    lines = [
        "# Quantitative Evaluation Summary",
        "",
        f"- Runs: {summary['run_count']}",
        f"- Cases: {summary['case_count']}",
        f"- Judged cases: {summary['judged_case_count']}",
        f"- B win rate: {format_percent(summary['b_win_rate'])}",
        "",
        "## Metric Summary",
        "",
        "| Metric | Direction | A mean | B mean | Relative improvement |",
        "|---|---|---:|---:|---:|",
    ]
    for metric, item in summary["metrics"].items():
        a_mean = "n/a" if item["A_mean"] is None else f"{item['A_mean']:.3g}"
        b_mean = "n/a" if item["B_mean"] is None else f"{item['B_mean']:.3g}"
        lines.append(
            f"| `{metric}` | {item['direction']} | {a_mean} | {b_mean} | {format_percent(item['relative_improvement'])} |"
        )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--evaluation-root",
        type=Path,
        default=Path("evaluation"),
        help="Directory containing cases/, runs/, and reports/.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory. Defaults to <evaluation-root>/metrics.",
    )
    args = parser.parse_args()

    evaluation_root = args.evaluation_root
    out_dir = args.out_dir or (evaluation_root / "metrics")
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = collect_runs(evaluation_root)
    judges = collect_judges(evaluation_root)
    summary = aggregate(rows, judges)

    write_csv(rows, out_dir / "results.csv")
    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_report(summary, out_dir / "quantitative-summary.md")
    print(f"Wrote {len(rows)} run rows to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
