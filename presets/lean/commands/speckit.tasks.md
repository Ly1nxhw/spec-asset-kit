---
description: 创建实现所需任务并写入 tasks.md。
---

## 用户输入

```text
$ARGUMENTS
```

## 执行纲要

1. 读取 `.specify/feature.json`，取得功能目录路径。
2. **加载上下文**：`.specify/memory/constitution.md`、`<feature_directory>/spec.md` 和 `<feature_directory>/plan.md`。
3. 创建按依赖排序的实现任务，并保存到 `<feature_directory>/tasks.md`。
   - 每个任务使用清单格式：`- [ ] [TaskID] 包含文件路径的任务描述`。
   - 按阶段组织：初始化、基础能力、按优先级排列的用户故事、收尾打磨。
