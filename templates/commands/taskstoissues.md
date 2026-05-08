---
description: 基于现有设计产物，将 tasks.md 转换为按依赖排序、可执行的 GitHub Issue。
tools: ['github/github-mcp-server/issue_write']
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

## 用户输入

```text
$ARGUMENTS
```

如果用户输入非空，你**必须**先纳入考虑再继续。

## 执行前检查

**检查扩展钩子（任务转 Issue 之前）**：

- 检查项目根目录下是否存在 `.specify/extensions.yml`。
- 如果存在，读取 `hooks.before_taskstoissues` 下的条目。
- 如果 YAML 无法解析或无效，静默跳过钩子检查并正常继续。
- 过滤 `enabled` 明确为 `false` 的钩子；未声明 `enabled` 视为启用。
- 对其余钩子，不要解释或求值 `condition`。
  - 没有 `condition`，或其值为 null/空字符串时，视为可执行。
  - 若存在非空 `condition`，跳过该钩子，把条件判断交给 HookExecutor。
- 对每个可执行钩子，按 `optional` 输出：
  - **可选前置钩子**（`optional: true`）：
    ```text
    ## 扩展钩子

    **可选前置钩子**：{extension}
    命令：`/{command}`
    说明：{description}

    提示：{prompt}
    执行方式：`/{command}`
    ```
  - **强制前置钩子**（`optional: false`）：
    ```text
    ## 扩展钩子

    **自动前置钩子**：{extension}
    正在执行：`/{command}`
    EXECUTE_COMMAND: {command}

    等待该钩子命令完成后，再进入执行纲要。
    ```
- 如果未注册任何钩子，或 `.specify/extensions.yml` 不存在，则静默跳过。

## 执行纲要

1. 在仓库根目录运行 `{SCRIPT}`，解析 `FEATURE_DIR` 与 `AVAILABLE_DOCS`。所有路径必须使用绝对路径。
2. 从脚本输出中取得 `tasks.md` 路径。
3. 运行以下命令读取 Git 远端：

```bash
git config --get remote.origin.url
```

> [!CAUTION]
> 只有当远端是 GitHub 仓库 URL 时，才能继续创建 Issue。

4. 读取 `tasks.md`，按任务顺序和依赖关系为每个任务创建一个 GitHub Issue。Issue 必须创建在当前 Git 远端对应的仓库中。

> [!CAUTION]
> 绝不能在与当前 Git 远端不匹配的仓库里创建 Issue。

## 执行后检查

**检查扩展钩子（任务转 Issue 之后）**：

- 如果 `.specify/extensions.yml` 存在，读取 `hooks.after_taskstoissues`。
- YAML 无法解析时静默跳过。
- 过滤 `enabled: false`。
- 不要解释或求值 `condition`。
- 对每个可执行钩子，按 `optional` 输出：
  - **可选钩子**：
    ```text
    ## 扩展钩子

    **可选钩子**：{extension}
    命令：`/{command}`
    说明：{description}

    提示：{prompt}
    执行方式：`/{command}`
    ```
  - **强制钩子**：
    ```text
    ## 扩展钩子

    **自动钩子**：{extension}
    正在执行：`/{command}`
    EXECUTE_COMMAND: {command}
    ```
- 如果没有钩子或文件不存在，则静默跳过。
