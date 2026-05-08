---
description: 只读检查 ai-assets 是否存在漂移、过期锚点或规划误用。
scripts:
  sh: .specify/extensions/ai-assets/scripts/bash/check-ai-assets.sh --json
  ps: .specify/extensions/ai-assets/scripts/powershell/check-ai-assets.ps1 -Json
---

## 用户输入

```text
$ARGUMENTS
```

如果用户输入非空，将其作为本次检查的关注点。此命令必须严格只读：不要创建、编辑、删除、暂存、提交或重写任何文件。

## 执行纲要

1. 在仓库根目录运行 `{SCRIPT}`，解析返回的 JSON。
2. 根据 `summary.status` 输出总体状态：
   - `PASS`：没有发现漂移问题。
   - `WARN`：存在可处理问题，但必需资产文件仍然完整。
   - `FAIL`：缺少必需资产，或存在阻断可靠规划的高严重度问题。
3. 输出紧凑 Markdown 报告，包含：
   - 摘要
   - 指标
   - 按严重度分组的问题
   - 建议的下一步动作
4. 如果结果是 `WARN` 或 `FAIL`，只有在问题适合通过资产更新解决时才建议运行 `/speckit.ai-assets.reconcile`。如果问题来自源码、规格或任务本身，应先修复事实源。

## 检查范围

脚本 JSON 可能包含以下类别：

- 缺失的资产文件
- 缺失的必需资产章节
- 过期的实现锚点路径
- 缺少可见来源或锚点的 `confirmed` 条目
- 未同步到 `open-questions.md` 的 `candidate` 条目
- plan 中疑似把 `candidate` 当成事实使用的位置
- tasks 中不存在的路径

## 输出规则

- 报告必须简洁、可行动。
- 如 JSON 提供文件路径和行号，必须引用。
- 不要把 `ai-assets/` 当成事实源。源码、契约、配置、正式文档、宪章和当前 feature 产物优先。
- 不要把 `candidate` 升级为 `confirmed`。
- 不要通过本命令修改资产来掩盖漂移。

## 完成标准

- 脚本成功运行。
- 报告包含状态、指标和发现的问题。
- 最后的下一步建议明确：无需动作、运行 reconcile、先 refine 候选知识，或先修复事实源。
