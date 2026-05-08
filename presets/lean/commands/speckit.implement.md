---
description: 按 tasks.md 中的任务执行实现计划。
---

## 用户输入

```text
$ARGUMENTS
```

## 执行纲要

1. 读取 `.specify/feature.json`，取得功能目录路径。
2. **加载上下文**：`.specify/memory/constitution.md`、`<feature_directory>/spec.md`、`<feature_directory>/plan.md` 和 `<feature_directory>/tasks.md`。
3. **按顺序执行任务**：
   - 完成当前任务后再进入下一个任务。
   - 完成任务后，将 `<feature_directory>/tasks.md` 中对应项从 `- [ ]` 改为 `- [x]`。
   - 遇到失败时立即停止并报告问题。
4. **验证**：确认所有任务已完成，且实现结果符合规格说明。
