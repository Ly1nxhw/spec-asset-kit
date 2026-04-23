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


class TestAIAssetsManifest:
    def test_manifest_validates(self):
        from specify_cli.extensions import ExtensionManifest

        manifest = ExtensionManifest(EXT_DIR / "extension.yml")
        assert manifest.id == "ai-assets"
        assert manifest.version == "1.0.0"

    def test_manifest_declares_command_alias_and_hook(self):
        from specify_cli.extensions import ExtensionManifest

        manifest = ExtensionManifest(EXT_DIR / "extension.yml")
        assert manifest.commands[0]["name"] == "speckit.ai-assets.extract"
        assert "speckit.assets.extract" in manifest.commands[0]["aliases"]
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


class TestAIAssetsInstall:
    def test_install_from_directory(self, tmp_path: Path):
        from specify_cli.extensions import ExtensionManager

        (tmp_path / ".specify").mkdir()
        manager = ExtensionManager(tmp_path)
        manifest = manager.install_from_directory(EXT_DIR, "0.5.0", register_commands=False)

        assert manifest.id == "ai-assets"
        assert manager.registry.is_installed("ai-assets")
        assert (tmp_path / ".specify" / "extensions" / "ai-assets" / "scripts" / "scan_repo.py").is_file()
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
