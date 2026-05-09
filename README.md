<div align="center">
    <img src="./media/logo_large.webp" alt="Spec Asset Kit Logo" width="180" height="180"/>
    <h1>Spec Asset Kit</h1>
    <h3><em>面向中文团队的 Spec-Driven Development 工具包。</em></h3>
</div>

<p align="center">
    <strong>基于 GitHub Spec Kit 的增强 fork，保留上游能力，同时加入中文化工作流、ai-assets 业务知识层、评测资产与细粒度 Git checkpoint 策略。</strong>
</p>

<p align="center">
    <a href="https://github.com/Ly1nxhw/spec-asset-kit/releases/latest"><img src="https://img.shields.io/github/v/release/Ly1nxhw/spec-asset-kit" alt="Latest Release"/></a>
    <a href="https://github.com/Ly1nxhw/spec-asset-kit/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Ly1nxhw/spec-asset-kit" alt="License"/></a>
    <a href="https://github.com/github/spec-kit"><img src="https://img.shields.io/badge/upstream-github%2Fspec--kit-blue" alt="Upstream"/></a>
</p>

---

## 这个 fork 解决什么问题

Spec Kit 的核心价值是把“先写规格，再规划，再拆任务，再实现”的 Spec-Driven Development 流程变成可执行工具链。Spec Asset Kit 在此基础上更偏向中文 AI-first 团队的实际协作：

- 中文原生体验：核心命令、模板、技能描述和用户可见提示优先使用中文表达。
- 业务知识沉淀：通过 `ai-assets` 将业务规则、术语、用户旅程、外部系统、决策记录和待确认问题结构化保存。
- 防止规格漂移：提供 ai-assets extract、check、refine、reconcile 工作流，帮助实现后回看业务知识是否失真。
- 可评测实现质量：内置 evaluation 目录，用模拟 replay、gold diff 和 reviewer rubric 记录 AI 实现质量。
- 更安全的 Git 节奏：强调按任务组 checkpoint，避免把整轮实现压成一个巨大提交。
- 保持上游兼容：同步 `github/spec-kit` 的官方 CLI、extensions、presets、integrations、workflow 和 catalog 更新。

## 快速安装

推荐使用 `uv` 从 GitHub 安装指定 release：

```bash
uv tool install specify-cli --from git+https://github.com/Ly1nxhw/spec-asset-kit.git@v0.8.8
```

安装最新 `main` 分支：

```bash
uv tool install specify-cli --force --from git+https://github.com/Ly1nxhw/spec-asset-kit.git
```

也可以用 `pipx`：

```bash
pipx install git+https://github.com/Ly1nxhw/spec-asset-kit.git@v0.8.8
```

验证安装：

```bash
specify version
specify check
```

## 初始化项目

创建新项目：

```bash
specify init my-project --integration codex --ai-skills
```

在已有项目中初始化：

```bash
specify init --here --integration codex --ai-skills
```

如果你希望安装更轻量的 preset：

```bash
specify init my-project --integration codex --preset lean
```

## 推荐工作流

在项目中按以下顺序推进：

```text
/speckit.constitution  -> 建立项目宪章和治理规则
/speckit.ai-assets.extract -> 从仓库中抽取候选业务知识
/speckit.specify      -> 编写或更新功能规格
/speckit.clarify      -> 澄清规格中定义不足的部分
/speckit.plan         -> 生成技术设计和实施计划
/speckit.tasks        -> 生成可执行任务清单
/speckit.implement    -> 按任务顺序实现并做 checkpoint
/speckit.ai-assets.reconcile -> 实现后回看业务知识和代码是否对齐
```

常用只读检查：

```text
/speckit.ai-assets.check
/speckit.analyze
```

## ai-assets 是什么

`ai-assets/` 是给 AI agent 和维护者共同使用的业务知识层。它不会替代规格，而是补齐规格背后的“业务语义记忆”。

默认资产包括：

- `business-context.md`：业务背景和目标。
- `domain-glossary.md`：领域术语。
- `business-rules.md`：业务规则。
- `user-journeys.md`：用户旅程。
- `external-systems.md`：外部系统。
- `decision-log.md`：历史决策。
- `open-questions.md`：待确认问题。
- `extraction-report.md`：抽取报告。

建议规则：

- `confirmed` 才能作为规划和实现依据。
- `candidate` 只能作为待确认线索，不要当成事实。
- `deprecated` 不应继续驱动新实现。

## 和上游 Spec Kit 的关系

本项目是 `github/spec-kit` 的增强 fork。同步原则是：

- 上游功能、修复、集成、catalog 和发布维护默认保留。
- 当前 fork 的中文化、ai-assets、evaluation、git checkpoint 增强必须保留。
- 若上游覆盖用户可见文案，需要重新检查中文表达。
- 若上游更改模板、命令占位符或 workflow，需要优先保持上游兼容。

上游仓库：

```text
https://github.com/github/spec-kit
```

当前 fork：

```text
https://github.com/Ly1nxhw/spec-asset-kit
```

## 本地开发

安装为 editable：

```bash
python -m pip install -e .
```

运行全量测试：

```bash
PYTHONUTF8=1 python -m pytest
```

Windows PowerShell：

```powershell
$env:PYTHONUTF8 = "1"
python -m pytest
```

`PYTHONUTF8=1` 很重要，因为本 fork 包含中文模板和技能文件；在 Windows 默认 GBK 环境下，部分测试会因为读取 UTF-8 文件失败。

## Release

当前 release 通过 Git tag 触发：

```bash
git tag -a v0.8.9 -m "Release v0.8.9"
git push origin v0.8.9
```

GitHub Actions 会在 tag push 后构建 wheel，并创建 GitHub Release。发布前必须先通过全量测试。

## 致谢

感谢上游 [github/spec-kit](https://github.com/github/spec-kit) 提供 Spec-Driven Development 的核心工具链。本 fork 在保持上游兼容的前提下，面向中文团队和 AI-first 工程实践做增强。

## License

本项目沿用上游开源许可证，详见 [LICENSE](./LICENSE)。
