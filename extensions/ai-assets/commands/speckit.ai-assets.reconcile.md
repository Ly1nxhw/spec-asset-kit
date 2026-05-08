---
description: 实现后对齐 ai-assets，且不静默改写已确认业务含义。
scripts:
  sh: .specify/extensions/ai-assets/scripts/bash/check-ai-assets.sh --json
  ps: .specify/extensions/ai-assets/scripts/powershell/check-ai-assets.ps1 -Json
---

## 用户输入

```text
$ARGUMENTS
```

将非空用户输入作为本次对齐的人工确认或修正说明。如果用户明确确认或否定某条业务知识，按 `/speckit.ai-assets.refine` 的安全规则处理。

## 执行纲要

1. 在仓库根目录运行 `{SCRIPT}`，解析返回的 JSON。
2. 如存在当前 feature 目录，读取：
   - `spec.md`
   - `plan.md`
   - `tasks.md`
3. 检查实现变更：
   - 如果当前目录是 Git 仓库，运行 `git status --short` 和 `git diff --name-only`。
   - 变更文件列表只能作为对齐证据；不要暂存或提交。
4. 只允许更新 `ai-assets/` 下的文件：
   - 创建或刷新 `ai-assets/reconcile-report.md`。
   - 将未解决冲突、过期锚点和待确认业务问题追加到 `ai-assets/open-questions.md`。
   - 只有在正确替代路径非常明确时，才修正明显过期的实现锚点。
5. 不要编辑源码、`.specify/`、`specs/`、模板或任何非资产文件。

## 安全规则

- 不得静默改写 `confirmed` 的业务含义。
- 没有用户明确确认、正式文档、契约或测试依据时，不得把 `candidate` 升级为 `confirmed`。
- 如果代码行为与 `ai-assets` 冲突，记录冲突并提出确认问题，不要直接覆盖任一方。
- 如果路径锚点已过期但无法确定替代路径，写入 `open-questions.md`。
- 如果本次实现改变了业务规则、术语、用户旅程、外部系统或历史决策，先在 `reconcile-report.md` 中记录建议更新；不确定内容保持 `candidate`。

## 报告格式

写入 `ai-assets/reconcile-report.md`：

```markdown
# AI Assets 对齐报告

## 摘要

## 已检查输入

## 已应用更新

## 冲突与待确认问题

## 建议下一步
```

向 `open-questions.md` 追加问题时使用：

```markdown
| ID | 问题 | 为什么重要 | 证据 | 影响资产 |
|---|---|---|---|---|
```

使用下一个可用的 `AQ###` 编号，并保留已有问题。

## 完成标准

- `ai-assets/reconcile-report.md` 存在。
- 所有未解决漂移都已记录到 `open-questions.md`。
- 除非用户或正式事实源明确确认，否则没有改写 `confirmed` 业务含义。
- 最终回复总结更新了哪些文件，以及还剩哪些风险。
