# AI Assets 扩展

该 bundled 扩展用于在标准 Spec Kit 工作流旁维护轻量的 `ai-assets/` 项目理解层。

它提供：

- `speckit.ai-assets.extract` / `speckit.assets.extract`
- `speckit.ai-assets.refine` / `speckit.assets.refine`
- `speckit.ai-assets.check` / `speckit.assets.check`
- `speckit.ai-assets.reconcile` / `speckit.assets.reconcile`
- `before_plan` 钩子，让规划阶段先刷新项目理解资产

## 设计目标

- 从仓库事实中提取可追溯的业务线索
- 将弱推断默认标记为 `candidate`
- 把需要人工确认的问题汇总到 `open-questions.md`
- 通过 `refine` 消费人工回答并沉淀 `confirmed` 知识
- 通过 `check` 做只读漂移检查
- 通过 `reconcile` 在实现后对齐资产，但不静默改写已确认业务含义

## 默认资产

```text
ai-assets/
|- business-context.md
|- domain-glossary.md
|- business-rules.md
|- user-journeys.md
|- external-systems.md
|- decision-log.md
|- open-questions.md
`- extraction-report.md
```

核心资产必须区分：

- `已确认知识`
- `候选线索`
- `实现锚点`
- `待确认问题`

知识状态：

- `confirmed`：来自正式文档、契约、测试，或人的明确确认
- `candidate`：来自 repo 线索的推断，仍需要人工确认
- `deprecated`：旧术语、旧流程或不应继续驱动新需求的知识

重要规则：`ai-assets/` 是 AI 辅助理解层，不替代源码、配置、契约或正式项目文档的事实源地位。
