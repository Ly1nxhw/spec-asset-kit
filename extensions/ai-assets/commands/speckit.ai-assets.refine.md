---
description: 基于人工回答，将 ai-assets 中的候选业务知识沉淀为已确认知识。
---

## 用户输入

```text
$ARGUMENTS
```

用户输入应包含对 `ai-assets/open-questions.md` 中问题的回答、业务补充说明，或要求废弃/修正的术语和规则。若用户输入为空，先读取 `open-questions.md` 并列出最需要人工回答的 3-5 个问题，不要擅自改写资产。

## 执行纲要

1. 读取 `ai-assets/` 下的业务资产：
   - `business-context.md`
   - `domain-glossary.md`
   - `business-rules.md`
   - `user-journeys.md`
   - `external-systems.md`
   - `decision-log.md`
   - `open-questions.md`
   - `extraction-report.md`

2. 解析用户回答：
   - 将明确确认的内容标记为 `confirmed`
   - 将明确否定或过时的内容标记为 `deprecated`
   - 将仍不完整的内容保留为 `candidate`
   - 不要把含糊回答升级为 confirmed

3. 更新对应资产：
   - 把已确认内容移动或合并到 `## 已确认知识`
   - 把仍需验证的内容保留在 `## 候选线索`
   - 在 `## 实现锚点` 中保留相关源码、测试、契约或文档路径
   - 在 `## 待确认问题` 中删除已回答问题，保留未回答问题

4. 更新 `open-questions.md`：
   - 已回答的问题移入 `## 已回答待整理` 或从待确认列表移除
   - 新发现的问题追加新 ID
   - 每个问题都保留“为什么重要”“线索来源”“影响资产”

5. 更新 `extraction-report.md`：
   - 记录本次 refine 的输入来源
   - 记录升级为 confirmed 的条目
   - 记录标记为 deprecated 的条目
   - 记录仍需人工确认的问题数量

## 写作规则

- 人的明确回答优先于 repo 推断。
- 正式业务文档、契约、测试优先于代码命名推断。
- 如果人工回答与代码行为冲突，不要静默覆盖；记录冲突并提出后续修正建议。
- 保留来源路径和确认来源，例如“用户在本次 refine 中确认”。
- 不要使用 `[high]`、`[medium]`、`[low]`；使用 `confirmed`、`candidate`、`deprecated`。

## 完成标准

- 已确认知识被写入正确资产，不再停留在 `open-questions.md`
- 未确认内容仍保留为 candidate
- 所有修改都能追溯到用户回答、正式文档、契约、测试或 repo 线索
- 输出本次 refine 摘要：确认了什么、废弃了什么、还需要问什么
