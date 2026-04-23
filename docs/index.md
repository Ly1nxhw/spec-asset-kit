# Spec Asset Kit

基于 `spec-kit` fork 的中文增强版 Spec-Driven Development 工具链。

## 它的目标

这个 fork 关注三件事：

- 保留标准 SDD 主链：`constitution -> specify -> plan -> tasks -> implement`
- 默认提供中文原生模板、提示词和产出体验
- 通过 `ai-assets` 把“项目理解”显式纳入 AI 工作流

## 它解决的问题

在真实项目里，AI 常见的失败模式通常不是“不会写代码”，而是：

- 不了解项目结构
- 不理解项目术语
- 不知道团队隐性约定
- 在 brownfield 仓库里做出脱离现实的规划

`Spec Asset Kit` 的核心思路是：

- 用 SDD 文档稳定 feature 级上下文
- 用 `ai-assets` 稳定项目级上下文
- 让 `plan` 显式消费项目理解资产，而不是只依赖当前规格

## 快速入口

- [安装说明](installation.md)
- [快速开始](quickstart.md)
- [详细使用说明书](user-manual.zh-CN.md)
- [升级说明](upgrade.md)
- [本地开发](local-development.md)

## 核心能力

### 中文原生工作流

默认命令模板、核心文档模板和工作流步骤说明已中文化，适合中文团队直接协作。

### 内置 `ai-assets` 扩展

初始化项目后会自动安装 bundled `ai-assets` 扩展，提供：

- `speckit.ai-assets.extract`
- `speckit.assets.extract`
- `before_plan` 强制钩子
- `plan` 对 `ai-assets` 的显式消费

### 最小侵入增强

优先通过：

- 扩展机制
- 模板覆盖
- 工作流增强

来实现能力，而不是大规模重写核心 CLI。

## 推荐阅读顺序

如果你是第一次使用：

1. [quickstart.md](quickstart.md)
2. [user-manual.zh-CN.md](user-manual.zh-CN.md)
3. [reference/extensions.md](reference/extensions.md)

如果你是维护者或二次开发者：

1. [user-manual.zh-CN.md](user-manual.zh-CN.md)
2. [reference/extensions.md](reference/extensions.md)
3. [reference/workflows.md](reference/workflows.md)
4. [../enhance/fork-enhancement-blueprint.zh-CN.md](../enhance/fork-enhancement-blueprint.zh-CN.md)

## 支持与贡献

- 上游协作规范仍参考项目根目录下的 `CONTRIBUTING.md`
- 如需理解当前 fork 的产品方向，请优先阅读 `enhance/` 下的改造蓝图与实施计划
