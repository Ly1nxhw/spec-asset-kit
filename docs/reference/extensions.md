# 扩展参考

扩展用于给 Spec Kit 增加新的命令、模板覆盖、质量门禁和外部工具集成。

## 内置扩展：`ai-assets`

本 fork 在 `specify init` 时默认安装 bundled `ai-assets` 扩展。

它提供：

- `speckit.ai-assets.extract`
- 别名：`speckit.assets.extract`
- `speckit.ai-assets.refine`
- 别名：`speckit.assets.refine`
- `speckit.ai-assets.check`
- 别名：`speckit.assets.check`
- `speckit.ai-assets.reconcile`
- 别名：`speckit.assets.reconcile`
- 强制 `before_plan` 钩子
- `plan` 与 `plan-template` 模板覆盖

职责边界：

- `extract` 从仓库证据生成候选业务知识和待确认问题。
- `refine` 消费人的明确回答，把候选知识沉淀为 `confirmed`。
- `check` 严格只读，用于检查资产缺失、章节缺失、过期锚点、缺来源确认项、候选项未进入待确认队列、plan 误用 candidate、tasks 引用不存在路径等问题。
- `reconcile` 只更新 `ai-assets/`，用于实现后对齐资产、生成 `reconcile-report.md`、追加待确认问题，并保留人工确认边界。

重要规则：

- `ai-assets/` 是 AI 辅助理解层，不是事实源。
- 业务知识是主要内容，技术事实只作为实现锚点。
- `confirmed` 可以指导规划；`candidate` 只能作为风险、待确认项或 refine 输入。
- 不得用资产内容替代源码、配置、契约或正式文档。

## 常用命令

```bash
specify extension search [query]
specify extension add <name>
specify extension list
specify extension info <name>
specify extension update [<name>]
specify extension remove <name>
specify extension enable <name>
specify extension disable <name>
```

## 配置

扩展可以在 `.specify/extensions/<ext>/` 下提供项目配置、本地配置和配置模板。配置优先级通常是：

1. 扩展默认值
2. 项目配置
3. 本地配置
4. 环境变量

安装第三方扩展前，应先检查源码、命令、脚本和 hook 行为。
