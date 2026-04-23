# Spec Asset Kit

基于 `spec-kit` fork 的中文增强版 SDD 工具链。

它保留 `spec-kit` 的核心工作流：

`constitution -> specify -> plan -> tasks -> implement`

同时补强三件事：

- 中文原生模板与提示词
- 面向 brownfield 项目的 `ai-assets` 项目理解层
- 让 `plan` 显式消费项目理解资产，减少“只会按模板写文档”的空转

## 项目定位

`Spec Asset Kit` 不是重写版 `spec-kit`，而是在上游框架上做最小侵入增强的 fork。

当前版本重点解决的问题：

- 在中文团队环境中，默认工作流、模板和产出仍然可读、可维护
- AI 在进入项目时，不只看到单个 feature 文档，还能看到持续积累的项目级 AI 资产
- 技术规划阶段能显式利用项目术语、结构、约定、历史线索，而不是每次从零猜

## 当前能力

### 1. 中文原生 SDD 主链

默认工作流为：

1. `constitution`
2. `specify`
3. `plan`
4. `tasks`
5. `implement`

核心命令模板、核心文档模板和工作流说明已经默认中文化。

### 2. 内置 `ai-assets` 扩展

初始化项目后会自动安装 bundled 扩展 `ai-assets`，提供：

- 命令：`speckit.ai-assets.extract`
- 兼容别名：`speckit.assets.extract`
- 强制 `before_plan` 钩子：规划前自动确保项目理解资产存在

默认生成的资产目录：

```text
ai-assets/
|- project-overview.md
|- glossary.md
|- architecture.md
|- repo-map.md
|- conventions.md
|- evolution-log.md
`- extraction-report.md
```

每类核心资产都要求明确区分：

- `Observed`
- `Inferred`
- `Open Questions`

### 3. `plan` 显式消费 `ai-assets`

规划阶段会优先读取：

- `ai-assets/glossary.md`
- `ai-assets/repo-map.md`
- `ai-assets/architecture.md`
- `ai-assets/conventions.md`

这样做的目标是：

- 稳定项目术语
- 校正目录结构和模块边界假设
- 把项目隐性规则带进技术规划

## 快速开始

### 安装

推荐使用 `uv`：

```bash
uv tool install specify-cli --from git+https://github.com/Ly1nxhw/spec-asset-kit.git
```

如果你当前就在仓库里做本地开发，也可以直接在源码目录运行：

```bash
python -m specify_cli --help
```

### 初始化项目

在新项目中：

```bash
specify init <PROJECT_NAME> --integration codex --script sh
```

在当前目录中：

```bash
specify init --here --integration codex --script sh
```

常见参数：

- `--integration <name>`：选择 AI agent 集成
- `--script sh|ps`：选择 Bash 或 PowerShell 脚本
- `--no-git`：跳过 git 初始化
- `--ignore-agent-tools`：跳过 agent CLI 检查

初始化完成后，项目里会出现：

- `.specify/`：工作流、模板、脚本、记忆与扩展
- `ai-assets/`：由 `ai-assets` 扩展维护的项目理解层
- 对应 agent 的命令或技能目录，例如 `.agents/skills/`

## 推荐工作流

### 1. 建立宪章

```text
/speckit.constitution
```

定义项目原则、质量门槛、测试要求与团队约束。

### 2. 写功能规格

```text
/speckit.specify
```

关注用户价值和业务目标，不要先写实现细节。

### 3. 生成项目理解资产

虽然 `plan` 前会自动触发，但在 brownfield 仓库中建议先手动跑一次：

```text
/speckit.ai-assets.extract
```

这会帮助 AI 先理解项目是什么，再做规划。

### 4. 生成技术规划

```text
/speckit.plan
```

此阶段会显式消费 `ai-assets`，避免术语漂移、目录假设错误和设计脱离现有结构。

### 5. 拆任务

```text
/speckit.tasks
```

把规划拆成可执行、带真实路径的任务。

### 6. 实施

```text
/speckit.implement
```

按照任务清单分阶段推进实现。

## `ai-assets` 的设计原则

`ai-assets` 是 AI 辅助理解层，不是正式事实源。

冲突时的优先级建议：

1. 源码与运行行为
2. 正式契约与 schema
3. 配置与构建定义
4. `constitution`
5. `ai-assets`
6. `spec / plan / tasks` 中的推断内容

因此：

- `ai-assets` 负责总结、提炼、解释
- 不负责替代源码、配置、契约和正式文档

## 文档入口

- 项目概览：[docs/index.md](./docs/index.md)
- 快速开始：[docs/quickstart.md](./docs/quickstart.md)
- 详细使用说明：[docs/user-manual.zh-CN.md](./docs/user-manual.zh-CN.md)
- 扩展参考：[docs/reference/extensions.md](./docs/reference/extensions.md)
- fork 改造蓝图：[enhance/fork-enhancement-blueprint.zh-CN.md](./enhance/fork-enhancement-blueprint.zh-CN.md)

## 适用场景

适合以下团队或项目：

- 主要使用中文协作的研发团队
- 希望把 Spec-Driven Development 落到真实项目中的团队
- 需要 AI 先理解项目，再规划和实施的 brownfield 仓库
- 希望通过可持续文档资产降低 AI 上下文漂移的团队

## 当前边界

当前版本已经完成：

- Phase 1：中文原生化
- Phase 2：`ai-assets.extract` 与 `plan` 联动

当前还没有做的事：

- `assets.reconcile`
- 完整 drift 检测
- 复杂多语言切换
- 更重型的静态分析或知识治理系统

## 开发与验证

本仓库当前重点回归覆盖了：

- bundled `ai-assets` 扩展安装
- `specify init` 自动安装 `ai-assets`
- 命令/模板覆盖解析
- `plan` 对 `ai-assets` 的显式消费
- 多类 agent 集成的初始化与命令注册

如果你在这个 fork 上继续迭代，建议优先保持：

- CLI 入口兼容
- 文件路径兼容
- workflow 主链稳定
- 文档与测试同步更新

## 许可证

继承上游仓库许可证，详见 [LICENSE](./LICENSE)。
