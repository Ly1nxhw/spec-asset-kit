#!/usr/bin/env python3
"""Deterministic drift checks for the bundled ai-assets extension."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ASSET_FILES = [
    "business-context.md",
    "domain-glossary.md",
    "business-rules.md",
    "user-journeys.md",
    "external-systems.md",
    "decision-log.md",
    "open-questions.md",
    "extraction-report.md",
]

CORE_ASSET_FILES = ASSET_FILES[:6]
CORE_SECTIONS = [
    "## Confirmed Knowledge",
    "## Candidate Signals",
    "## Implementation Anchors",
    "## Open Questions",
]

PATH_RE = re.compile(r"`([^`\n]+)`")
STATUS_RE = re.compile(r"\b(confirmed|candidate|deprecated)\b", re.IGNORECASE)
TASK_PATH_RE = re.compile(r"\b(?:src|tests|test|docs|app|apps|packages|backend|frontend|scripts|templates|contracts|specs)/[A-Za-z0-9_./\-\[\]]+")


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def looks_like_path(value: str) -> bool:
    if value.startswith(("http://", "https://", "mailto:")):
        return False
    if "{{" in value or "}}" in value:
        return False
    if any(ch.isspace() for ch in value):
        return False
    return "/" in value or "\\" in value or Path(value).suffix != ""


def existing_path(root: Path, token: str) -> bool:
    candidate = (root / token.replace("\\", "/")).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return False
    return candidate.exists()


def line_number(content: str, needle: str) -> int:
    before = content.split(needle, 1)[0]
    return before.count("\n") + 1


def check_assets(root: Path, feature_dir: Path | None = None) -> dict[str, Any]:
    assets_dir = root / "ai-assets"
    result: dict[str, Any] = {
        "project_root": str(root),
        "assets_dir": str(assets_dir),
        "summary": {
            "status": "PASS",
            "missing_asset_count": 0,
            "missing_section_count": 0,
            "stale_anchor_count": 0,
            "confirmed_without_source_count": 0,
            "candidate_without_question_count": 0,
            "task_missing_path_count": 0,
            "plan_candidate_misuse_count": 0,
        },
        "assets": {},
        "findings": [],
        "metrics": {
            "confirmed": 0,
            "candidate": 0,
            "deprecated": 0,
        },
    }

    findings: list[dict[str, Any]] = result["findings"]

    for asset_name in ASSET_FILES:
        path = assets_dir / asset_name
        asset_info: dict[str, Any] = {
            "exists": path.is_file(),
            "missing_sections": [],
            "status_counts": {"confirmed": 0, "candidate": 0, "deprecated": 0},
        }
        result["assets"][asset_name] = asset_info

        if not path.is_file():
            result["summary"]["missing_asset_count"] += 1
            findings.append({
                "id": f"MISSING_ASSET:{asset_name}",
                "severity": "HIGH",
                "file": f"ai-assets/{asset_name}",
                "message": "Required asset file is missing.",
            })
            continue

        content = path.read_text(encoding="utf-8", errors="replace")
        if asset_name in CORE_ASSET_FILES:
            for section in CORE_SECTIONS:
                if section not in content:
                    asset_info["missing_sections"].append(section)
                    result["summary"]["missing_section_count"] += 1
                    findings.append({
                        "id": f"MISSING_SECTION:{asset_name}:{section}",
                        "severity": "MEDIUM",
                        "file": f"ai-assets/{asset_name}",
                        "message": f"Missing required section {section}.",
                    })

        for status in STATUS_RE.findall(content):
            normalized = status.lower()
            asset_info["status_counts"][normalized] += 1
            result["metrics"][normalized] += 1

        for token in PATH_RE.findall(content):
            if not looks_like_path(token):
                continue
            if token.startswith("ai-assets/"):
                continue
            if not existing_path(root, token):
                result["summary"]["stale_anchor_count"] += 1
                findings.append({
                    "id": f"STALE_ANCHOR:{asset_name}:{token}",
                    "severity": "MEDIUM",
                    "file": f"ai-assets/{asset_name}",
                    "line": line_number(content, f"`{token}`"),
                    "message": f"Referenced path does not exist: {token}",
                })

        for line_no, line in enumerate(content.splitlines(), start=1):
            lower = line.lower()
            if "confirmed" in lower and "source" not in lower and "user confirmed" not in lower and "`" not in line:
                result["summary"]["confirmed_without_source_count"] += 1
                findings.append({
                    "id": f"CONFIRMED_WITHOUT_SOURCE:{asset_name}:{line_no}",
                    "severity": "MEDIUM",
                    "file": f"ai-assets/{asset_name}",
                    "line": line_no,
                    "message": "Confirmed knowledge appears without a visible source or anchor.",
                })

    open_questions_text = ""
    open_questions = assets_dir / "open-questions.md"
    if open_questions.is_file():
        open_questions_text = open_questions.read_text(encoding="utf-8", errors="replace").lower()

    for asset_name, asset_info in result["assets"].items():
        if asset_name == "open-questions.md":
            continue
        if asset_info["status_counts"]["candidate"] and asset_name.replace(".md", "") not in open_questions_text:
            result["summary"]["candidate_without_question_count"] += 1
            findings.append({
                "id": f"CANDIDATE_WITHOUT_QUESTION:{asset_name}",
                "severity": "MEDIUM",
                "file": f"ai-assets/{asset_name}",
                "message": "Candidate knowledge exists, but open-questions.md does not reference this asset.",
            })

    feature = feature_dir or discover_feature_dir(root)
    if feature:
        check_feature_docs(root, feature, result)

    if any(f["severity"] == "HIGH" for f in findings):
        result["summary"]["status"] = "FAIL"
    elif findings:
        result["summary"]["status"] = "WARN"

    return result


def discover_feature_dir(root: Path) -> Path | None:
    feature_file = root / ".specify" / "feature.json"
    if feature_file.is_file():
        try:
            data = json.loads(feature_file.read_text(encoding="utf-8"))
            value = data.get("feature_directory") or data.get("FEATURE_DIR")
            if value:
                candidate = root / value
                if candidate.is_dir():
                    return candidate
        except (OSError, json.JSONDecodeError):
            pass
    return None


def check_feature_docs(root: Path, feature: Path, result: dict[str, Any]) -> None:
    findings: list[dict[str, Any]] = result["findings"]
    plan = feature / "plan.md"
    tasks = feature / "tasks.md"

    if plan.is_file():
        content = plan.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(content.splitlines(), start=1):
            lower = line.lower()
            if "candidate" in lower and not any(marker in lower for marker in ("risk", "open question", "needs confirmation", "refine")):
                result["summary"]["plan_candidate_misuse_count"] += 1
                findings.append({
                    "id": f"PLAN_CANDIDATE_MISUSE:{line_no}",
                    "severity": "MEDIUM",
                    "file": rel(plan, root),
                    "line": line_no,
                    "message": "Plan references candidate knowledge without treating it as risk or confirmation work.",
                })

    if tasks.is_file():
        content = tasks.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(content.splitlines(), start=1):
            for token in TASK_PATH_RE.findall(line):
                cleaned = token.strip(".,);:")
                if "[" in cleaned or "]" in cleaned:
                    continue
                if not existing_path(root, cleaned):
                    result["summary"]["task_missing_path_count"] += 1
                    findings.append({
                        "id": f"TASK_MISSING_PATH:{line_no}:{cleaned}",
                        "severity": "MEDIUM",
                        "file": rel(tasks, root),
                        "line": line_no,
                        "message": f"Task references a path that does not exist yet: {cleaned}",
                    })


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--feature-dir")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    feature_dir = Path(args.feature_dir).resolve() if args.feature_dir else None
    payload = check_assets(root, feature_dir)
    json.dump(payload, fp=__import__("sys").stdout, indent=2, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
