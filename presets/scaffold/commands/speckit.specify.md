---
description: "创建功能规格说明（preset 覆盖）"
scripts:
  sh: scripts/bash/create-new-feature.sh "{ARGS}"
  ps: scripts/powershell/create-new-feature.ps1 "{ARGS}"
---

## 用户输入

```text
$ARGUMENTS
```

基于上面的功能描述：

1. **创建功能分支**：运行脚本。
   - Bash：`{SCRIPT} --json --short-name "<short-name>" "<description>"`
   - JSON 输出包含 `BRANCH_NAME` 和 `SPEC_FILE` 路径。
2. **读取规格模板**：查看需要填写的章节。
3. **写入规格说明**：将用户描述中的信息写入 `SPEC_FILE`，替换模板中的概览、需求和验收标准占位内容。
