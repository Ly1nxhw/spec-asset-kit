---
description: 创建规格说明并写入 spec.md。
---

## 用户输入

```text
$ARGUMENTS
```

## 执行纲要

1. **询问用户**功能目录路径，例如 `specs/my-feature`。在用户提供之前不要继续。
2. 创建目录并写入 `.specify/feature.json`：
   ```json
   { "feature_directory": "<feature_directory>" }
   ```
3. 基于用户输入创建规格说明，并保存到 `<feature_directory>/spec.md`。
   - 包含概览、功能需求、用户场景和成功标准。
   - 每条需求都必须可测试。
   - 对未明确说明的细节做合理默认，并记录假设。
