---
description: "覆盖 myext 扩展的 myextcmd 命令"
---

<!-- speckit.myext.myextcmd 的 preset 覆盖示例 -->

你正在执行 `myext` 扩展中 `myextcmd` 命令的定制版本。

执行该命令时：

1. 从 `$ARGUMENTS` 读取用户输入。
2. 遵循标准 `myextcmd` 工作流。
3. 额外应用此 preset 的定制要求：
   - 继续之前先执行合规检查。
   - 在输出中包含审计追踪条目。

> 自定义提示：请将上面的说明替换为你自己的 preset 逻辑。
> 此文件会覆盖 `myext` 扩展提供的命令。
> 安装该 preset 后，所有 agent 都会使用这个版本，而不是扩展原始版本。
