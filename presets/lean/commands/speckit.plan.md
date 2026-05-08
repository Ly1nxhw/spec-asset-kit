---
description: 创建实现计划并写入 plan.md。
---

## 用户输入

```text
$ARGUMENTS
```

## 执行纲要

1. 读取 `.specify/feature.json`，取得功能目录路径。
2. **加载上下文**：`.specify/memory/constitution.md` 和 `<feature_directory>/spec.md`。
3. 创建实现计划并保存到 `<feature_directory>/plan.md`。
   - 写清技术上下文、技术栈、依赖和项目结构。
   - 记录设计决策、架构取舍和文件结构。
