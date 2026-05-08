"""Tests for the bundled ai-assets extension (extensions/ai-assets/)."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from tests.conftest import requires_bash

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
EXT_DIR = PROJECT_ROOT / "extensions" / "ai-assets"
EXT_BASH = EXT_DIR / "scripts" / "bash" / "extract-ai-assets.sh"
EXT_PS = EXT_DIR / "scripts" / "powershell" / "extract-ai-assets.ps1"
CHECK_BASH = EXT_DIR / "scripts" / "bash" / "check-ai-assets.sh"
CHECK_PS = EXT_DIR / "scripts" / "powershell" / "check-ai-assets.ps1"

HAS_PWSH = shutil.which("pwsh") is not None


def _build_repo_fixture(tmp_path: Path) -> Path:
    (tmp_path / ".github" / "workflows").mkdir(parents=True)
    (tmp_path / "docs").mkdir()
    (tmp_path / "scripts").mkdir()
    (tmp_path / "src").mkdir()
    (tmp_path / "templates").mkdir()

    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("# Agent Rules\n", encoding="utf-8")
    (tmp_path / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
    (tmp_path / "CONTRIBUTING.md").write_text("# Contributing\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    (tmp_path / "docs" / "architecture.md").write_text("# Architecture\n", encoding="utf-8")
    (tmp_path / "scripts" / "bootstrap.sh").write_text("#!/usr/bin/env bash\n", encoding="utf-8")
    (tmp_path / "src" / "main.py").write_text("print('hello')\n", encoding="utf-8")
    (tmp_path / ".github" / "workflows" / "ci.yml").write_text("name: ci\n", encoding="utf-8")
    (tmp_path / "templates" / "spec-template.md").write_text("# template\n", encoding="utf-8")
    return tmp_path


def _build_assets_fixture(tmp_path: Path) -> Path:
    repo = _build_repo_fixture(tmp_path)
    assets = repo / "ai-assets"
    assets.mkdir()
    core = """## Confirmed Knowledge

| Field | Value |
|---|---|
| Status | confirmed |
| Source | `README.md` |

## Candidate Signals

| Field | Value |
|---|---|
| Status | candidate |
| Source | `missing/path.md` |

## Implementation Anchors

- `src/main.py`

## Open Questions

- Needs confirmation.
"""
    for name in [
        "business-context.md",
        "domain-glossary.md",
        "business-rules.md",
        "user-journeys.md",
        "external-systems.md",
        "decision-log.md",
    ]:
        (assets / name).write_text(core, encoding="utf-8")
    (assets / "open-questions.md").write_text(
        "## Needs Human Confirmation\n\n| ID | Question | Why It Matters | Evidence | Affected Assets |\n"
        "|---|---|---|---|---|\n| AQ001 | Confirm candidate? | Planning risk | `README.md` | `business-context.md` |\n",
        encoding="utf-8",
    )
    (assets / "extraction-report.md").write_text("# Extraction Report\n", encoding="utf-8")
    return repo


def _run_bash(repo_root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(EXT_BASH), "--json"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )


def _run_pwsh(repo_root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["pwsh", "-NoProfile", "-File", str(EXT_PS), "-Json"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )


def _run_check_bash(repo_root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(CHECK_BASH), "--json"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )


def _run_check_pwsh(repo_root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["pwsh", "-NoProfile", "-File", str(CHECK_PS), "-Json"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )


class TestAIAssetsManifest:
    def test_manifest_validates(self):
        from specify_cli.extensions import ExtensionManifest

        manifest = ExtensionManifest(EXT_DIR / "extension.yml")
        assert manifest.id == "ai-assets"
        assert manifest.version == "1.0.0"

    def test_manifest_declares_command_alias_and_hook(self):
        from specify_cli.extensions import ExtensionManifest

        manifest = ExtensionManifest(EXT_DIR / "extension.yml")
        commands = {command["name"]: command for command in manifest.commands}

        assert "speckit.ai-assets.extract" in commands
        assert "speckit.assets.extract" in commands["speckit.ai-assets.extract"]["aliases"]
        assert "speckit.ai-assets.refine" in commands
        assert "speckit.assets.refine" in commands["speckit.ai-assets.refine"]["aliases"]
        assert "speckit.ai-assets.check" in commands
        assert "speckit.assets.check" in commands["speckit.ai-assets.check"]["aliases"]
        assert "speckit.ai-assets.reconcile" in commands
        assert "speckit.assets.reconcile" in commands["speckit.ai-assets.reconcile"]["aliases"]
        assert manifest.hooks["before_plan"]["command"] == "speckit.ai-assets.extract"
        assert manifest.hooks["before_plan"]["optional"] is False

    def test_manifest_files_exist(self):
        from specify_cli.extensions import ExtensionManifest

        manifest = ExtensionManifest(EXT_DIR / "extension.yml")
        for command in manifest.commands:
            assert (EXT_DIR / command["file"]).is_file()

        assert (EXT_DIR / "templates" / "commands" / "plan.md").is_file()
        assert (EXT_DIR / "templates" / "plan-template.md").is_file()
        assert (EXT_DIR / "scripts" / "scan_repo.py").is_file()
        assert (EXT_DIR / "scripts" / "check_ai_assets.py").is_file()

    def test_extract_command_targets_business_assets(self):
        command = (EXT_DIR / "commands" / "speckit.ai-assets.extract.md").read_text(encoding="utf-8")

        assert "business-context.md" in command
        assert "domain-glossary.md" in command
        assert "business-rules.md" in command
        assert "user-journeys.md" in command
        assert "open-questions.md" in command
        assert "confirmed" in command
        assert "candidate" in command
        assert "deprecated" in command
        assert "已确认知识" in command
        assert "候选线索" in command
        assert "技术栈、目录结构、模块边界、运行命令只在“实现锚点”中简要列出" in command
        assert "不再使用 `[high]`、`[medium]`、`[low]` 平铺列表" in command

    def test_refine_command_promotes_human_confirmed_knowledge(self):
        command = (EXT_DIR / "commands" / "speckit.ai-assets.refine.md").read_text(encoding="utf-8")

        assert "open-questions.md" in command
        assert "将明确确认的内容标记为 `confirmed`" in command
        assert "将明确否定或过时的内容标记为 `deprecated`" in command
        assert "将仍不完整的内容保留为 `candidate`" in command
        assert "人的明确回答优先于 repo 推断" in command

    def test_check_command_is_read_only(self):
        command = (EXT_DIR / "commands" / "speckit.ai-assets.check.md").read_text(encoding="utf-8")

        assert "严格只读" in command
        assert "过期的实现锚点路径" in command
        assert "不要把 `candidate` 升级为 `confirmed`" in command

    def test_reconcile_command_limits_write_scope(self):
        command = (EXT_DIR / "commands" / "speckit.ai-assets.reconcile.md").read_text(encoding="utf-8")

        assert "只允许更新 `ai-assets/`" in command
        assert "reconcile-report.md" in command
        assert "不得静默改写 `confirmed`" in command


class TestAIAssetsInstall:
    def test_install_from_directory(self, tmp_path: Path):
        from specify_cli.extensions import ExtensionManager

        (tmp_path / ".specify").mkdir()
        manager = ExtensionManager(tmp_path)
        manifest = manager.install_from_directory(EXT_DIR, "0.5.0", register_commands=False)

        assert manifest.id == "ai-assets"
        assert manager.registry.is_installed("ai-assets")
        assert (tmp_path / ".specify" / "extensions" / "ai-assets" / "scripts" / "scan_repo.py").is_file()
        assert (tmp_path / ".specify" / "extensions" / "ai-assets" / "scripts" / "check_ai_assets.py").is_file()
        assert (tmp_path / ".specify" / "extensions" / "ai-assets" / "templates" / "commands" / "plan.md").is_file()

    def test_install_registers_before_plan_hook(self, tmp_path: Path):
        from specify_cli.extensions import ExtensionManager

        (tmp_path / ".specify").mkdir()
        manager = ExtensionManager(tmp_path)
        manager.install_from_directory(EXT_DIR, "0.5.0", register_commands=False)

        hook_config = yaml.safe_load((tmp_path / ".specify" / "extensions.yml").read_text(encoding="utf-8"))
        before_plan = hook_config["hooks"]["before_plan"]
        assert before_plan[0]["extension"] == "ai-assets"
        assert before_plan[0]["command"] == "speckit.ai-assets.extract"
        assert before_plan[0]["optional"] is False

    def test_bundled_extension_locator(self):
        from specify_cli import _locate_bundled_extension

        path = _locate_bundled_extension("ai-assets")
        assert path is not None
        assert (path / "extension.yml").is_file()

    def test_resolver_prefers_ai_assets_overrides(self, tmp_path: Path):
        from specify_cli.extensions import ExtensionManager
        from specify_cli.presets import PresetResolver

        (tmp_path / ".specify").mkdir()
        manager = ExtensionManager(tmp_path)
        manager.install_from_directory(EXT_DIR, "0.5.0", register_commands=False)

        resolver = PresetResolver(tmp_path)
        assert resolver.resolve("plan", "command") == (
            tmp_path / ".specify" / "extensions" / "ai-assets" / "templates" / "commands" / "plan.md"
        )
        assert resolver.resolve("plan-template", "template") == (
            tmp_path / ".specify" / "extensions" / "ai-assets" / "templates" / "plan-template.md"
        )


@requires_bash
class TestAIAssetsScannerBash:
    def test_scanner_outputs_expected_json(self, tmp_path: Path):
        repo = _build_repo_fixture(tmp_path)
        result = _run_bash(repo)

        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)

        assert payload["project_root"] == str(repo.resolve())
        assert "docs" in payload["top_level"]["directories"]
        assert "README.md" in payload["sources"]["readme"]
        assert "AGENTS.md" in payload["sources"]["agents"]
        assert "pyproject.toml" in payload["config_files"]
        assert "src/main.py" in payload["entrypoints"]
        assert "scripts/bootstrap.sh" in payload["scripts"]
        assert ".github/workflows/ci.yml" in payload["workflows"]
        assert "templates/spec-template.md" in payload["templates"]


@requires_bash
class TestAIAssetsCheckBash:
    def test_checker_reports_stale_anchors(self, tmp_path: Path):
        repo = _build_assets_fixture(tmp_path)
        result = _run_check_bash(repo)

        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)

        assert payload["summary"]["status"] == "WARN"
        assert payload["summary"]["stale_anchor_count"] >= 1
        assert any(f["id"].startswith("STALE_ANCHOR") for f in payload["findings"])


@pytest.mark.skipif(not HAS_PWSH, reason="pwsh not available")
class TestAIAssetsScannerPowerShell:
    def test_scanner_matches_bash_contract(self, tmp_path: Path):
        repo = _build_repo_fixture(tmp_path)
        bash_result = _run_bash(repo)
        pwsh_result = _run_pwsh(repo)

        assert bash_result.returncode == 0, bash_result.stderr
        assert pwsh_result.returncode == 0, pwsh_result.stderr

        bash_payload = json.loads(bash_result.stdout)
        pwsh_payload = json.loads(pwsh_result.stdout)
        assert pwsh_payload == bash_payload

    def test_check_wrapper_matches_bash_contract(self, tmp_path: Path):
        repo = _build_assets_fixture(tmp_path)
        bash_result = _run_check_bash(repo)
        pwsh_result = _run_check_pwsh(repo)

        assert bash_result.returncode == 0, bash_result.stderr
        assert pwsh_result.returncode == 0, pwsh_result.stderr

        bash_payload = json.loads(bash_result.stdout)
        pwsh_payload = json.loads(pwsh_result.stdout)
        assert pwsh_payload == bash_payload
